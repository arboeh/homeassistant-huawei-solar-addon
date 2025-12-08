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

# Logger für dieses Modul
logger = logging.getLogger("huawei.main")

LAST_SUCCESS = 0  # Unix-Timestamp des letzten erfolgreichen Reads


def init():
    load_dotenv()

    # Log-Level aus Umgebungsvariable lesen
    log_level_str = os.environ.get("HUAWEI_LOG_LEVEL", "INFO").upper()

    # String in Logging-Konstante umwandeln
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR
    }

    loglevel = log_level_map.get(log_level_str, logging.INFO)

    # Debug-Flag für Abwärtskompatibilität beibehalten
    if os.environ.get("HUAWEI_MODBUS_DEBUG") == "yes":
        loglevel = logging.DEBUG

    # Root Logger konfigurieren
    root_logger = logging.getLogger()
    root_logger.setLevel(loglevel)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    root_logger.addHandler(handler)

    # Alte Handler entfernen (vermeidet Duplikate)
    for h in root_logger.handlers[:]:
        root_logger.removeHandler(h)
    root_logger.addHandler(handler)

    # Pymodbus-Logging konfigurieren
    pymodbus_logger = logging.getLogger("pymodbus")
    if loglevel == logging.DEBUG:
        # Bei DEBUG: Zeige alle pymodbus-Logs
        pymodbus_logger.setLevel(logging.DEBUG)
        logger.debug("Pymodbus debug logging enabled")
    else:
        # Sonst: Nur Warnungen und Fehler
        pymodbus_logger.setLevel(logging.WARNING)

    # Huawei-Solar Library (nutzt auch logging)
    huawei_solar_logger = logging.getLogger("huawei_solar")
    huawei_solar_logger.setLevel(loglevel)

    # Initialisierungs-Log
    logger.info(
        f"Logging initialized with level: {logging.getLevelName(loglevel)}")
    logger.debug(
        f"Environment: HUAWEI_LOG_LEVEL={log_level_str}, "
        f"HUAWEI_MODBUS_DEBUG={os.environ.get('HUAWEI_MODBUS_DEBUG', 'no')}"
    )
    logger.debug(
        f"Pymodbus log level: {logging.getLevelName(pymodbus_logger.level)}")


def heartbeat(topic: str):
    """
    Überwacht, ob seit zu langer Zeit kein erfolgreicher Read war,
    und setzt dann den Status auf offline.
    """
    global LAST_SUCCESS

    timeout = int(os.environ.get("HUAWEI_STATUS_TIMEOUT", "180"))

    if LAST_SUCCESS == 0:
        logger.debug("Heartbeat: No successful read yet, skipping check")
        return

    diff = time.time() - LAST_SUCCESS

    if diff > timeout:
        publish_status("offline", topic)
        logger.warning(
            f"No successful data for {timeout}s (actual: {diff:.1f}s) -> status=offline"
        )
    else:
        logger.debug(
            f"Heartbeat: Last successful read {diff:.1f}s ago (timeout: {timeout}s)"
        )


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
        from huawei_solar.registers import REGISTERS

        # Modbus-Read mit Zeitmessung
        modbus_start = time.time()

        data = {}
        successful_reads = 0
        failed_reads = 0

        for register_name in REGISTERS:
            try:
                value = await client.get(register_name)
                data[register_name] = value
                successful_reads += 1
                logger.debug(f"Read {register_name}: {value}")
            except Exception as e:
                failed_reads += 1
                logger.debug(f"Failed to read register {register_name}: {e}")
                continue

        modbus_duration = time.time() - modbus_start

        logger.debug(
            f"Modbus read completed in {modbus_duration:.3f}s "
            f"({successful_reads} successful, {failed_reads} failed)"
        )

    except DecodeError as e:
        logger.warning(
            f"DecodeError during data read after {time.time() - cycle_start:.3f}s: {e}"
        )
        raise
    except Exception as e:
        logger.error(f"Failed to read registers: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        raise

    if not data:
        logger.warning("No data received from inverter")
        return

    # Transformation mit Zeitmessung
    transform_start = time.time()
    mqtt_data = transform_result(data)
    transform_duration = time.time() - transform_start

    logger.debug(f"Data transformation completed in {transform_duration:.3f}s")

    # MQTT Publish mit Zeitmessung
    mqtt_start = time.time()
    mqtt_publish_data(mqtt_data, topic)
    publish_status("online", topic)
    mqtt_duration = time.time() - mqtt_start

    logger.debug(f"MQTT publish completed in {mqtt_duration:.3f}s")

    LAST_SUCCESS = time.time()

    # Gesamt-Zyklus-Zeit
    cycle_duration = time.time() - cycle_start

    # Strukturierte Info-Meldung mit wichtigen Werten
    logger.info(
        f"Data published - Solar: {mqtt_data.get('power_active', 0)}W | "
        f"Grid: {mqtt_data.get('meter_power_active', 0)}W | "
        f"Battery: {mqtt_data.get('battery_power', 0)}W ({mqtt_data.get('battery_soc', 0)}%)"
    )

    # Detaillierte Zyklus-Informationen nur bei DEBUG
    logger.debug(
        f"Cycle complete in {cycle_duration:.3f}s "
        f"(Modbus: {modbus_duration:.3f}s, Transform: {transform_duration:.3f}s, "
        f"MQTT: {mqtt_duration:.3f}s)"
    )

    # Performance-Warnung bei langsamen Zyklen
    poll_interval = int(os.environ.get("HUAWEI_POLL_INTERVAL", "60"))
    if cycle_duration > poll_interval * 0.8:
        logger.warning(
            f"Cycle took {cycle_duration:.1f}s - close to poll_interval ({poll_interval}s). "
            "Consider increasing poll_interval."
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
