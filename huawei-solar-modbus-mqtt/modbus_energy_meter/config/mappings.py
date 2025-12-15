# modbus_energy_meter/config/mappings.py
from typing import Dict

REGISTER_MAPPING: Dict[str, str] = {
    'active_power': 'power_active',
    'input_power': 'power_input',
    'day_active_power_peak': 'power_active_peak_day',
    'reactive_power': 'power_reactive',

    'daily_yield_energy': 'energy_yield_day',
    'accumulated_yield_energy': 'energy_yield_accumulated',
    'grid_exported_energy': 'energy_grid_exported',
    'grid_accumulated_energy': 'energy_grid_accumulated',

    'pv_01_voltage': 'voltage_PV1',
    'pv_01_current': 'current_PV1',
    'pv_02_voltage': 'voltage_PV2',
    'pv_02_current': 'current_PV2',
    'pv_03_voltage': 'voltage_PV3',
    'pv_03_current': 'current_PV3',
    'pv_04_voltage': 'voltage_PV4',
    'pv_04_current': 'current_PV4',

    'grid_A_voltage': 'voltage_grid_A',
    'grid_B_voltage': 'voltage_grid_B',
    'grid_C_voltage': 'voltage_grid_C',
    'line_voltage_A_B': 'voltage_line_AB',
    'line_voltage_B_C': 'voltage_line_BC',
    'line_voltage_C_A': 'voltage_line_CA',
    'grid_frequency': 'frequency_grid',

    'power_meter_active_power': 'meter_power_active',
    'power_meter_reactive_power': 'meter_reactive_power',
    'meter_status': 'meter_status',

    'active_grid_A_power': 'power_meter_A',
    'active_grid_B_power': 'power_meter_B',
    'active_grid_C_power': 'power_meter_C',

    'active_grid_A_B_voltage': 'voltage_meter_line_AB',
    'active_grid_B_C_voltage': 'voltage_meter_line_BC',
    'active_grid_C_A_voltage': 'voltage_meter_line_CA',

    'active_grid_A_current': 'current_meter_A',
    'active_grid_B_current': 'current_meter_B',
    'active_grid_C_current': 'current_meter_C',

    'active_grid_frequency': 'frequency_meter',
    'active_grid_power_factor': 'power_factor_meter',

    'storage_state_of_capacity': 'battery_soc',
    'storage_charge_discharge_power': 'battery_power',
    'storage_bus_voltage': 'battery_bus_voltage',
    'storage_bus_current': 'battery_bus_current',
    'storage_current_day_charge_capacity': 'battery_charge_day',
    'storage_current_day_discharge_capacity': 'battery_discharge_day',
    'storage_total_charge': 'battery_charge_total',
    'storage_total_discharge': 'battery_discharge_total',
    'storage_running_status': 'battery_status',

    'device_status': 'inverter_status',
    'state_1': 'inverter_state_1',
    'state_2': 'inverter_state_2',
    'startup_time': 'startup_time',

    'internal_temperature': 'inverter_temperature',
    'efficiency': 'inverter_efficiency',
    'insulation_resistance': 'inverter_insulation_resistance',
    'power_factor': 'power_factor',

    'model_name': 'model_name',
    'serial_number': 'serial_number',
    'rated_power': 'rated_power',
}

CRITICAL_DEFAULTS: Dict[str, int] = {
    'power_active': 0,
    'power_input': 0,
    'meter_power_active': 0,
    'battery_power': 0,
    'battery_soc': 0,
}
