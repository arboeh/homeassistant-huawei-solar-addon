# transform.py
import logging
import time

# Logger für dieses Modul
logger = logging.getLogger("huawei.transform")

def get_value(register_value):
    """Safely extract value from register object"""
    if register_value is None:
        return None

    try:
        # Wenn es ein RegisterValue-Objekt ist
        if hasattr(register_value, 'value'):
            value = register_value.value

            # Spezialbehandlung für Enum-Werte (z.B. DeviceStatus.STANDBY)
            if hasattr(value, 'name'):
                logger.debug(
                    f"Extracted enum value: {value.name} from {type(value).__name__}")
                return value.name

            # Spezialbehandlung für Datetime-Werte (z.B. startup_time)
            if hasattr(value, 'isoformat'):
                iso_string = value.isoformat()
                logger.debug(f"Extracted datetime value: {iso_string}")
                return iso_string

            logger.debug(
                f"Extracted value from RegisterValue: {value} (type: {type(value).__name__})")
            return value

        # Wenn es direkt ein Wert ist
        logger.debug(
            f"Direct value: {register_value} (type: {type(register_value).__name__})")
        return register_value

    except Exception as e:
        logger.warning(
            f"Error extracting value from register (type: {type(register_value).__name__}): {e}")
        return None


def transform_result(data):
    """Transform all available Huawei Solar inverter data"""

    logger.debug(f"Starting transformation of {len(data)} data keys")

    transform_start = time.time()

    result = {
        # === POWER (Hauptdaten) ===
        'power_active': get_value(data.get('active_power')),
        'power_input': get_value(data.get('input_power')),
        'power_active_peak_day': get_value(data.get('day_active_power_peak')),
        'power_reactive': get_value(data.get('reactive_power')),

        # === ENERGY ===
        'energy_yield_day': get_value(data.get('daily_yield_energy')),
        'energy_yield_accumulated': get_value(data.get('accumulated_yield_energy')),

        # === PV STRINGS ===
        'power_PV1': get_value(data.get('pv_01_power')),
        'voltage_PV1': get_value(data.get('pv_01_voltage')),
        'current_PV1': get_value(data.get('pv_01_current')),

        # Optional: PV2/PV3/PV4
        'power_PV2': get_value(data.get('pv_02_power')),
        'voltage_PV2': get_value(data.get('pv_02_voltage')),
        'current_PV2': get_value(data.get('pv_02_current')),

        'power_PV3': get_value(data.get('pv_03_power')),
        'voltage_PV3': get_value(data.get('pv_03_voltage')),
        'current_PV3': get_value(data.get('pv_03_current')),

        'power_PV4': get_value(data.get('pv_04_power')),
        'voltage_PV4': get_value(data.get('pv_04_voltage')),
        'current_PV4': get_value(data.get('pv_04_current')),

        # === GRID (3-Phase) ===
        'voltage_grid_A': get_value(data.get('grid_A_voltage')),
        'current_grid_A': get_value(data.get('grid_A_current')),
        'power_grid_A': get_value(data.get('phase_A_active_power')),

        'voltage_grid_B': get_value(data.get('grid_B_voltage')),
        'current_grid_B': get_value(data.get('grid_B_current')),
        'power_grid_B': get_value(data.get('phase_B_active_power')),

        'voltage_grid_C': get_value(data.get('grid_C_voltage')),
        'current_grid_C': get_value(data.get('grid_C_current')),
        'power_grid_C': get_value(data.get('phase_C_active_power')),

        'frequency_grid': get_value(data.get('grid_frequency')),

        # Line-to-Line Voltages
        'voltage_line_AB': get_value(data.get('line_voltage_A_B')),
        'voltage_line_BC': get_value(data.get('line_voltage_B_C')),
        'voltage_line_CA': get_value(data.get('line_voltage_C_A')),

        # === POWER METER ===
        'meter_power_active': get_value(data.get('active_grid_power_peak')),
        'meter_power_reactive': get_value(data.get('grid_accumulated_reactive_power')),

        'meter_voltage_A': get_value(data.get('grid_A_voltage')),
        'meter_voltage_B': get_value(data.get('grid_B_voltage')),
        'meter_voltage_C': get_value(data.get('grid_C_voltage')),

        'meter_current_A': get_value(data.get('grid_A_current')),
        'meter_current_B': get_value(data.get('grid_B_current')),
        'meter_current_C': get_value(data.get('grid_C_current')),

        'energy_grid_exported': get_value(data.get('grid_exported_energy')),
        'energy_grid_accumulated': get_value(data.get('grid_accumulated_energy')),
        'energy_grid_accumulated_reactive': get_value(data.get('grid_accumulated_reactive_power')),

        # === BATTERY ===
        'battery_soc': get_value(data.get('storage_state_of_capacity')),
        'battery_power': get_value(data.get('storage_charge_discharge_power')),
        'battery_bus_voltage': get_value(data.get('storage_bus_voltage')),
        'battery_bus_current': get_value(data.get('storage_bus_current')),

        'battery_charge_day': get_value(data.get('storage_day_charge')),
        'battery_discharge_day': get_value(data.get('storage_day_discharge')),
        'battery_charge_total': get_value(data.get('storage_total_charge')),
        'battery_discharge_total': get_value(data.get('storage_total_discharge')),

        # === STATUS ===
        'inverter_status': str(get_value(data.get('device_status'))),
        'inverter_state_1': str(get_value(data.get('state_1'))),
        'inverter_state_2': str(get_value(data.get('state_2'))),
        'inverter_state_3': str(get_value(data.get('state_3'))),
        'inverter_startup_time': str(get_value(data.get('startup_time'))),

        'battery_status': str(get_value(data.get('storage_status'))),
        'meter_status': str(get_value(data.get('meter_status'))),

        # === INVERTER METRICS ===
        'inverter_temperature': get_value(data.get('internal_temperature')),
        'inverter_efficiency': get_value(data.get('efficiency')),
        'inverter_insulation_resistance': get_value(data.get('insulation_resistance')),

        'power_factor': get_value(data.get('power_factor')),
    }

    # === NULL-WERTE-BEHANDLUNG FÜR KRITISCHE KEYS (v1.0.5) ===
    # Diese Werte sind essentiell für EVCC und andere Integrationen
    # und dürfen NIEMALS null/None sein
    critical_keys = {
        'power_active': 0,        # Solar-Leistung
        'power_input': 0,         # PV-Eingangsleistung
        'meter_power_active': 0,  # Netzleistung (Grid)
        'battery_power': 0,       # Batterieleistung
        'battery_soc': 0          # Batterie-Ladezustand
    }

    # Setze kritische Werte auf Default (0), falls sie fehlen oder None sind
    for key, default_value in critical_keys.items():
        if key not in result or result[key] is None:
            logger.warning(
                f"Critical key '{key}' is missing or None, setting to {default_value}")
            result[key] = default_value

    # Entferne restliche None-Werte für sauberere MQTT-Daten
    original_count = len(result)
    result = {k: v for k, v in result.items() if v is not None}
    removed_count = original_count - len(result)

    if removed_count > 0:
        logger.debug(f"Removed {removed_count} None values from result")

    # Konvertiere verbleibende komplexe Objekte zu Strings
    converted_count = 0
    for key, value in result.items():
        if not isinstance(value, (int, float, str, bool, type(None))):
            logger.debug(
                f"Converting {key} value to string: {type(value).__name__} -> str")
            result[key] = str(value)
            converted_count += 1

    if converted_count > 0:
        logger.debug(f"Converted {converted_count} complex values to strings")

    transform_duration = time.time() - transform_start

    logger.debug(
        f"Transformation complete: {len(result)} values extracted in {transform_duration:.3f}s")

    # Bei DEBUG: Zeige Statistiken über die transformierten Daten
    if logger.isEnabledFor(logging.DEBUG):
        power_values = [k for k in result.keys() if 'power' in k.lower()]
        energy_values = [k for k in result.keys() if 'energy' in k.lower()]
        voltage_values = [k for k in result.keys() if 'voltage' in k.lower()]

        logger.debug(
            f"Data categories - Power: {len(power_values)}, "
            f"Energy: {len(energy_values)}, Voltage: {len(voltage_values)}"
        )

        # Zeige kritische Werte für schnelle Diagnose
        logger.debug(
            f"Critical values - "
            f"Solar: {result.get('power_active', 'N/A')}W, "
            f"Grid: {result.get('meter_power_active', 'N/A')}W, "
            f"Battery: {result.get('battery_power', 'N/A')}W ({result.get('battery_soc', 'N/A')}%)"
        )

        # Zeige fehlende erwartete Werte
        expected_keys = ['active_power',
                         'storage_state_of_capacity', 'grid_A_voltage']
        missing_keys = [k for k in expected_keys if k not in data]
        if missing_keys:
            logger.warning(f"Expected keys not found in data: {missing_keys}")

    return result
