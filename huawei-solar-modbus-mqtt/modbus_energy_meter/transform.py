def transform_result(data):
    """Transform all available Huawei Solar inverter data"""
    return {
        # === POWER (Hauptdaten) ===
        'power_active': get_value(data.get('active_power')),
        'power_input': get_value(data.get('input_power')),
        'power_active_peak_day': get_value(data.get('day_active_power_peak')),
        'power_reactive': get_value(data.get('reactive_power')),

        # === ENERGY (Hauptdaten) ===
        'energy_yield_accumulated': get_value(data.get('accumulated_yield_energy')),
        'energy_yield_day': get_value(data.get('daily_yield_energy')),
        'energy_grid_accumulated': get_value(data.get('grid_accumulated_energy')),
        'energy_grid_exported': get_value(data.get('grid_exported_energy')),
        'energy_grid_accumulated_reactive': get_value(data.get('grid_accumulated_reactive_power')),

        # === GRID - VOLTAGE (3-Phase) ===
        'voltage_grid_A': get_value(data.get('grid_A_voltage')),
        'voltage_grid_B': get_value(data.get('grid_B_voltage')),
        'voltage_grid_C': get_value(data.get('grid_C_voltage')),

        # === GRID - CURRENT (3-Phase) ===
        'current_grid_A': get_value(data.get('active_grid_A_current')),
        'current_grid_B': get_value(data.get('active_grid_B_current')),
        'current_grid_C': get_value(data.get('active_grid_C_current')),

        # === GRID - POWER (3-Phase) ===
        'power_grid_A': get_value(data.get('active_grid_A_power')),
        'power_grid_B': get_value(data.get('active_grid_B_power')),
        'power_grid_C': get_value(data.get('active_grid_C_power')),

        # === GRID - LINE VOLTAGE (L-L) ===
        'voltage_line_AB': get_value(data.get('active_grid_A_B_voltage')),
        'voltage_line_BC': get_value(data.get('active_grid_B_C_voltage')),
        'voltage_line_CA': get_value(data.get('active_grid_C_A_voltage')),

        # === GRID - FREQUENCY & POWER FACTOR ===
        'frequency_grid': get_value(data.get('grid_frequency')),
        'frequency_grid_active': get_value(data.get('active_grid_frequency')),
        'power_factor': get_value(data.get('power_factor')),
        'power_factor_active_grid': get_value(data.get('active_grid_power_factor')),

        # === PV STRINGS - VOLTAGE ===
        'voltage_PV1': get_value(data.get('pv_01_voltage')),
        'voltage_PV2': get_value(data.get('pv_02_voltage')),
        'voltage_PV3': get_value(data.get('pv_03_voltage')),
        'voltage_PV4': get_value(data.get('pv_04_voltage')),

        # === PV STRINGS - CURRENT ===
        'current_PV1': get_value(data.get('pv_01_current')),
        'current_PV2': get_value(data.get('pv_02_current')),
        'current_PV3': get_value(data.get('pv_03_current')),
        'current_PV4': get_value(data.get('pv_04_current')),

        # === PV STRINGS - POWER (calculated) ===
        'power_PV1': calculate_power(get_value(data.get('pv_01_voltage')), get_value(data.get('pv_01_current'))),
        'power_PV2': calculate_power(get_value(data.get('pv_02_voltage')), get_value(data.get('pv_02_current'))),
        'power_PV3': calculate_power(get_value(data.get('pv_03_voltage')), get_value(data.get('pv_03_current'))),
        'power_PV4': calculate_power(get_value(data.get('pv_04_voltage')), get_value(data.get('pv_04_current'))),

        # === BATTERY - MAIN ===
        'battery_power': get_value(data.get('storage_charge_discharge_power')),
        'battery_soc': get_value(data.get('storage_state_of_capacity')),
        'battery_charge_day': get_value(data.get('storage_current_day_charge_capacity')),
        'battery_discharge_day': get_value(data.get('storage_current_day_discharge_capacity')),
        'battery_charge_total': get_value(data.get('storage_total_charge')),
        'battery_discharge_total': get_value(data.get('storage_total_discharge')),

        # === BATTERY - TECHNICAL ===
        'battery_bus_voltage': get_value(data.get('storage_bus_voltage')),
        'battery_bus_current': get_value(data.get('storage_bus_current')),
        'battery_status': get_enum_value(data.get('storage_running_status')),

        # === POWER METER ===
        'meter_power_active': get_value(data.get('power_meter_active_power')),
        'meter_power_reactive': get_value(data.get('power_meter_reactive_power')),
        'meter_voltage_A': get_value(data.get('phase_A_voltage')),
        'meter_voltage_B': get_value(data.get('phase_B_voltage')),
        'meter_voltage_C': get_value(data.get('phase_C_voltage')),
        'meter_current_A': get_value(data.get('phase_A_current')),
        'meter_current_B': get_value(data.get('phase_B_current')),
        'meter_current_C': get_value(data.get('phase_C_current')),
        'meter_status': get_enum_value(data.get('meter_status')),
        'meter_type': get_enum_value(data.get('meter_type')),

        # === INVERTER STATUS ===
        'inverter_status': get_enum_value(data.get('device_status')),
        'inverter_state_1': get_list_value(data.get('state_1')),
        'inverter_state_2': get_list_value(data.get('state_2')),
        'inverter_state_3': get_list_value(data.get('state_3')),
        'inverter_alarm_1': get_list_value(data.get('alarm_1')),
        'inverter_alarm_2': get_list_value(data.get('alarm_2')),
        'inverter_alarm_3': get_list_value(data.get('alarm_3')),
        'inverter_fault_code': get_value(data.get('fault_code')),

        # === INVERTER TECHNICAL ===
        'inverter_temperature': get_value(data.get('internal_temperature')),
        'inverter_efficiency': get_value(data.get('efficiency')),
        'inverter_insulation_resistance': get_value(data.get('insulation_resistance')),
        'inverter_startup_time': get_datetime_value(data.get('startup_time')),
        'inverter_shutdown_time': get_datetime_value(data.get('shutdown_time')),

        # === LEGACY COMPATIBILITY (alte Namen) ===
        'power_active_meter': get_value(data.get('power_meter_active_power')),
        'soc_battery': get_value(data.get('storage_state_of_capacity')),
        'temperature_internal': get_value(data.get('internal_temperature')),
        'efficiency': get_value(data.get('efficiency')),
        # Typo for compatibility
        'enery_yield_day': get_value(data.get('daily_yield_energy')),
        'current_active_grid_A': get_value(data.get('active_grid_A_current')),
        'current_active_grid_B': get_value(data.get('active_grid_B_current')),
        'current_active_grid_C': get_value(data.get('active_grid_C_current')),
        'freq_active_grid': get_value(data.get('active_grid_frequency')),
        'power_factor_meter': get_value(data.get('power_factor')),
        'power_battery': get_value(data.get('storage_charge_discharge_power')),
        'energy_battery_charge_day': get_value(data.get('storage_current_day_charge_capacity')),
        'energy_battery_discharge_day': get_value(data.get('storage_current_day_discharge_capacity')),
        'energy_battery_charge_total': get_value(data.get('storage_total_charge')),
        'energy_battery_discharge_total': get_value(data.get('storage_total_discharge')),
    }


def calculate_power(voltage, current):
    """Calculate power from voltage and current"""
    if voltage is None or current is None:
        return None
    return round(voltage * current, 2)


def get_value(record):
    """Extract value from Result object"""
    if record is None:
        return None
    return record.value


def get_enum_value(record):
    """Extract enum value as string"""
    if record is None:
        return None
    value = record.value
    if hasattr(value, 'name'):
        return value.name
    return str(value)


def get_list_value(record):
    """Extract list value as comma-separated string"""
    if record is None:
        return None
    value = record.value
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def get_datetime_value(record):
    """Extract datetime value as ISO string"""
    if record is None:
        return None
    value = record.value
    if value is None:
        return None
    if hasattr(value, 'isoformat'):
        return value.isoformat()
    return str(value)
