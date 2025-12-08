# huawei2mqtt.py
import asyncio
import logging
import os
import sys
import time
import traceback

from huawei_solar import AsyncHuaweiSolar
from huawei_solar.exceptions import DecodeError, ReadException
from dotenv import load_dotenv
from modbus_energy_meter.mqtt import (
    publish_data as mqtt_publish_data,
    publish_status,
    publish_discovery_configs,
)
from modbus_energy_meter.transform import transform_result

ESSENTIAL_REGISTERS = [
    "active_power",              # → power_active
    "input_power",               # → power_input  
    "active_grid_power_peak",    # → meter_power_active (HV-Meter)
    "storage_charge_discharge_power",  # → battery_power
    "storage_state_of_capacity", # → battery_soc
    "daily_yield_energy",        # → energy_yield_day
    "accumulated_yield_energy",  # → energy_yield_accumulated
    "grid_exported_energy",      # → energy_grid_exported
    "grid_accumulated_energy",   # → energy_grid_accumulated
    "storage_day_charge",        # → battery_charge_day
    "storage_day_discharge",     # → battery_discharge_day
    "pv_01_power",               # → power_PV1
    "pv_01_voltage",             # → voltage_PV1
    "pv_01_current",             # → current_PV1
    "internal_temperature",      # → inverter_temperature
    "efficiency",                # → inverter_efficiency
    "grid_A_voltage",            # → voltage_grid_A
    "grid_B_voltage",            # → voltage_grid_B
    "grid_C_voltage",            # → voltage_grid_C
    "grid_frequency",            # → frequency_grid
    "day_active_power_peak",     # → power_active_peak_day
]

# Logger für dieses Modul
logger = logging.getLogger("huawei.main")

LAST_SUCCESS = 0  # Unix-Timestamp des letzten erfolgreichen Reads


def init():
    load_dotenv()
    # ... (REST DER init() FUNKTION UNVERÄNDERT) ...
    log_level_str = os.environ.get("HUAWEI_LOG_LEVEL", "INFO").upper()
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR
    }
    loglevel = log_level_map.get(log_level_str, logging.INFO)
    if os.environ.get("HUAWEI_MODBUS_DEBUG") == "yes":
        loglevel = logging.DEBUG

    root_logger = logging.getLogger()
    root_logger.setLevel(loglevel)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    root_logger.addHandler(handler)
    for h in root_logger.handlers[:]:
        root_logger.removeHandler(h)
    root_logger.addHandler(handler)

    pymodbus_logger = logging.getLogger("pymodbus")
    if loglevel == logging.DEBUG:
        pymodbus_logger.setLevel(logging.DEBUG)
        logger.debug("Pymodbus debug logging enabled")
    else:
        pymodbus_logger.setLevel(logging.WARNING)

    huawei_solar_logger = logging.getLogger("huawei_solar")
    huawei_solar_logger.setLevel(loglevel)

    logger.info(f"Logging initialized with level: {logging.getLevelName(loglevel)}")
    logger.debug(f"Environment: HUAWEI_LOG_LEVEL={log_level_str}, HUAWEI_MODBUS_DEBUG={os.environ.get('HUAWEI_MODBUS_DEBUG', 'no')}")
    logger.debug(f"Pymodbus log level: {logging.getLevelName(pymodbus_logger.level)}")

def heartbeat(topic: str):
    global LAST_SUCCESS
    timeout = int(os.environ.get("HUAWEI_STATUS_TIMEOUT", "180"))
    if LAST_SUCCESS == 0:
        logger.debug("Heartbeat: No successful read yet, skipping check")
        return
    diff = time.time() - LAST_SUCCESS
    if diff > timeout:
        publish_status("offline", topic)
        logger.warning(f"No successful data for {timeout}s (actual: {diff:.1f}s) -> status=offline")
    else:
        logger.debug(f"Heartbeat: Last successful read {diff:.1f}s ago (timeout: {timeout}s)")


async def read_registers_filtered(client: AsyncHuaweiSolar):
    """Lese nur ESSENTIAL_REGISTERS sequentiell für maximale Performance"""
    all_data = {}
    logger.debug(f"Reading {len(ESSENTIAL_REGISTERS)} essential registers")
    
    read_start = time.time()
    successful = 0
    
    for name in ESSENTIAL_REGISTERS:
        try:
            result = await client.get(name)
            all_data[name] = result
            successful += 1
        except Exception as e:
            logger.debug("Failed %s: %s", name, type(e).__name__)
    
    duration = time.time() - read_start
    logger.info("Essential registers read in %.1fs (%d/%d successful)", 
                duration, successful, len(ESSENTIAL_REGISTERS))
    
    return all_data


async def main_once(client: AsyncHuaweiSolar):
    """
    Ein einzelner Read-Publish-Zyklus.
    Setzt Status nur bei Erfolg auf online.
    """
    global LAST_SUCCESS

    topic = os.environ.get("HUAWEI_MODBUS_MQTT_TOPIC")
    if not topic:
        raise RuntimeError("HUAWEI_MODBUS_MQTT_TOPIC not set")

    # Zeitmessung für den gesamten Zyklus
    cycle_start = time.time()

    logger.debug("Starting data acquisition cycle")

    try:
        modbus_start = time.time()
        data = await read_registers_filtered(client)
        modbus_duration = time.time() - modbus_start

        successful_reads = len(data)
        logger.info(
            "Essential Modbus read completed in %.1fs (%d/%d successful)", 
            modbus_duration, successful_reads, len(ESSENTIAL_REGISTERS)
        )

    except DecodeError as e:
        logger.warning(f"DecodeError during data read after {time.time() - cycle_start:.3f}s: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to read registers: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        raise

    if not data:
        logger.warning("No data received from inverter")
        return

    transform_start = time.time()
    mqtt_data = transform_result(data)
    transform_duration = time.time() - transform_start
    logger.debug(f"Data transformation completed in {transform_duration:.3f}s")

    mqtt_start = time.time()
    mqtt_publish_data(mqtt_data, topic)
    publish_status("online", topic)
    mqtt_duration = time.time() - mqtt_start
    logger.debug(f"MQTT publish completed in {mqtt_duration:.3f}s")

    LAST_SUCCESS = time.time()
    cycle_duration = time.time() - cycle_start

    logger.info(
        "Data published - Solar: %dW | Grid: %dW | Battery: %dW (%.1f%%)",
        mqtt_data.get('power_active', 0),
        mqtt_data.get('meter_power_active', 0),
        mqtt_data.get('battery_power', 0),
        mqtt_data.get('battery_soc', 0)
    )

    logger.debug(
        "Cycle complete in %.3fs (Modbus: %.3fs, Transform: %.3fs, MQTT: %.3fs)",
        cycle_duration, modbus_duration, transform_duration, mqtt_duration
    )

    poll_interval = int(os.environ.get("HUAWEI_POLL_INTERVAL", "60"))
    if cycle_duration > poll_interval * 0.8:
        logger.warning(
            "Cycle took %.1fs - close to poll_interval (%ds). Consider increasing.",
            cycle_duration, poll_interval
        )


async def main():
    init()

    topic = os.environ.get("HUAWEI_MODBUS_MQTT_TOPIC")
    if not topic:
        logger.error("HUAWEI_MODBUS_MQTT_TOPIC not set – exiting")
        sys.exit(1)

    modbus_host = os.environ.get("HUAWEI_MODBUS_HOST")
    modbus_port = int(os.environ.get("HUAWEI_MODBUS_PORT", "502"))
    slave_id = int(os.environ.get("HUAWEI_MODBUS_DEVICE_ID", "1"))

    logger.info("Huawei Solar Modbus to MQTT starting")
    logger.debug(
        f"Configuration: Host={modbus_host}:{modbus_port}, Slave ID={slave_id}, Topic={topic}"
    )

    publish_status("offline", topic)

    # Discovery nur einmal
    try:
        logger.debug("Publishing MQTT Discovery configs...")
        publish_discovery_configs(topic)
        logger.info("MQTT Discovery configs published")
    except Exception as e:
        logger.error(f"Failed to publish MQTT Discovery configs: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")

    wait = int(os.environ.get("HUAWEI_POLL_INTERVAL", "60"))
    logger.info(f"Poll interval set to {wait}s")

    # Client einmalig im selben Event Loop erstellen
    try:
        logger.debug(
            f"Creating AsyncHuaweiSolar connection to {modbus_host}:{modbus_port}..."
        )
        client = await AsyncHuaweiSolar.create(modbus_host, modbus_port, slave_id)
        logger.info(
            f"AsyncHuaweiSolar created successfully (Slave ID: {slave_id})")
    except Exception as e:
        logger.error(f"Failed to create AsyncHuaweiSolar: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        publish_status("offline", topic)
        return

    try:
        cycle_count = 0
        while True:
            cycle_count += 1
            logger.debug(f"Starting cycle #{cycle_count}")

            try:
                await main_once(client)

            except DecodeError as e:
                logger.error(
                    f"DecodeError in cycle #{cycle_count}: {e} - skipping this cycle"
                )
                logger.debug(f"Traceback:\n{traceback.format_exc()}")
                publish_status("offline", topic)
                await asyncio.sleep(10)

            except ReadException as e:
                logger.error(
                    f"ReadException in cycle #{cycle_count}: {e} - connection issue"
                )
                logger.debug(f"Traceback:\n{traceback.format_exc()}")
                publish_status("offline", topic)
                logger.info(
                    "Waiting 30s before retry due to connection issue...")
                await asyncio.sleep(30)

            except Exception as e:
                logger.error(
                    f"Read/publish failed in cycle #{cycle_count} ({type(e).__name__}): {e}"
                )
                logger.debug(f"Traceback:\n{traceback.format_exc()}")
                publish_status("offline", topic)
                await asyncio.sleep(10)

            heartbeat(topic)

            logger.debug(f"Cycle #{cycle_count} complete, sleeping {wait}s...")
            await asyncio.sleep(wait)

    except asyncio.CancelledError:
        logger.info("Shutting down gracefully...")
        publish_status("offline", topic)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        publish_status("offline", topic)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user, exiting...")
