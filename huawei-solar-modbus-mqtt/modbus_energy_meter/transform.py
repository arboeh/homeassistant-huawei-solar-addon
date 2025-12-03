def transform_result(data):
    return {
        'energy_yield_accumulated': get_value(data.get('accumulated_yield_energy')),
        'power_active_grid_A': get_value(data.get('active_grid_A_power')),
        'power_active_grid_B': get_value(data.get('active_grid_B_power')),
        'power_active_grid_C': get_value(data.get('active_grid_C_power')),
        'current_active_grid_A': get_value(data.get('active_grid_A_current')),
        'current_active_grid_B': get_value(data.get('active_grid_B_current')),
        'current_active_grid_C': get_value(data.get('active_grid_C_current')),
        'freq_active_grid': get_value(data.get('active_grid_frequency')),
        'power_factor_active_grid': get_value(data.get('active_grid_power_factor')),
        'power_active': get_value(data.get('active_power')),
        'enery_yield_day': get_value(data.get('daily_yield_energy')),
        'power_active_peak_day': get_value(data.get('day_active_power_peak')),
        'efficiency': get_value(data.get('efficiency')),
        'voltage_grid_A': get_value(data.get('grid_A_voltage')),
        'voltage_grid_B': get_value(data.get('grid_B_voltage')),
        'voltage_grid_C': get_value(data.get('grid_C_voltage')),
        'energy_grid_accumulated': get_value(data.get('grid_accumulated_energy')),
        'energy_grid_exported': get_value(data.get('grid_exported_energy')),
        'frequency_grid': get_value(data.get('grid_frequency')),
        'power_input': get_value(data.get('input_power')),
        'temperature_internal': get_value(data.get('internal_temperature')),
        'power_factor_meter': get_value(data.get('power_factor')),
        'power_active_meter': get_value(data.get('power_meter_active_power')),
        'power_reactive_meter': get_value(data.get('power_meter_reactive_power')),
        'voltage_PV1': get_value(data.get('pv_01_voltage')),
        'voltage_PV2': get_value(data.get('pv_02_voltage')),
        'current_PV1': get_value(data.get('pv_01_current')),
        'current_PV2': get_value(data.get('pv_02_current')),
        'power_PV1': calculate_power(get_value(data.get('pv_01_voltage')), get_value(data.get('pv_01_current'))),
        'power_PV2': calculate_power(get_value(data.get('pv_02_voltage')), get_value(data.get('pv_02_current'))),
        'power_battery': get_value(data.get('storage_charge_discharge_power')),
        'energy_battery_charge_day': get_value(data.get('storage_current_day_charge_capacity')),
        'energy_battery_discharge_day': get_value(data.get('storage_current_day_discharge_capacity')),
        'soc_battery': get_value(data.get('storage_state_of_capacity')),
        'energy_battery_charge_total': get_value(data.get('storage_total_charge')),
        'energy_battery_discharge_total': get_value(data.get('storage_total_discharge'))
    }


def calculate_power(voltage, current):
    if voltage is None or current is None:
        return None
    return voltage * current


def get_value(record):
    if record is None:
        return None
    return record.value
