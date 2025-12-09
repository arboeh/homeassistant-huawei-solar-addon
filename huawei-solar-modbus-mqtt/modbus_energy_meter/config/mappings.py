# modbus_energy_meter/config/mappings.py
from typing import Dict

# Register → MQTT key mapping
REGISTER_MAPPING: Dict[str, str] = {
    # Power
    'active_power': 'power_active',
    'input_power': 'power_input',
    'day_active_power_peak': 'power_active_peak_day',
    'reactive_power': 'power_reactive',

    # Energy
    'daily_yield_energy': 'energy_yield_day',
    'accumulated_yield_energy': 'energy_yield_accumulated',
    'grid_exported_energy': 'energy_grid_exported',
    'grid_accumulated_energy': 'energy_grid_accumulated',
    'grid_accumulated_reactive_power': 'energy_grid_accumulated_reactive',

    # PV Strings
    'pv_01_power': 'power_PV1',
    'pv_01_voltage': 'voltage_PV1',
    'pv_01_current': 'current_PV1',
    'pv_02_power': 'power_PV2',
    'pv_02_voltage': 'voltage_PV2',
    'pv_02_current': 'current_PV2',
    'pv_03_power': 'power_PV3',
    'pv_03_voltage': 'voltage_PV3',
    'pv_03_current': 'current_PV3',
    'pv_04_power': 'power_PV4',
    'pv_04_voltage': 'voltage_PV4',
    'pv_04_current': 'current_PV4',

    # Grid (3-phase)
    'grid_A_voltage': 'voltage_grid_A',
    'grid_A_current': 'current_grid_A',
    'phase_A_active_power': 'power_grid_A',
    'grid_B_voltage': 'voltage_grid_B',
    'grid_B_current': 'current_grid_B',
    'phase_B_active_power': 'power_grid_B',
    'grid_C_voltage': 'voltage_grid_C',
    'grid_C_current': 'current_grid_C',
    'phase_C_active_power': 'power_grid_C',
    'grid_frequency': 'frequency_grid',
    'line_voltage_A_B': 'voltage_line_AB',
    'line_voltage_B_C': 'voltage_line_BC',
    'line_voltage_C_A': 'voltage_line_CA',

    # Power Meter
    'active_power_meter': 'meter_power_active',
    'meter_status': 'meter_status',
    'reactive_power_meter': 'meter_reactive_power',

    # Battery
    'storage_state_of_capacity': 'battery_soc',
    'storage_charge_discharge_power': 'battery_power',
    'storage_bus_voltage': 'battery_bus_voltage',
    'storage_bus_current': 'battery_bus_current',
    'storage_charge_capacity_today': 'battery_charge_day',
    'storage_discharge_capacity_today': 'battery_discharge_day',
    'storage_total_charge': 'battery_charge_total',
    'storage_total_discharge': 'battery_discharge_total',

    # Status
    'device_status': 'inverter_status',
    'state_1': 'inverter_state_1',
    'state_2': 'inverter_state_2',
    'state_3': 'inverter_state_3',
    'startup_time': 'inverter_startup_time',
    'storage_running_status': 'battery_status',

    # Inverter metrics
    'internal_temperature': 'inverter_temperature',
    'efficiency': 'inverter_efficiency',
    'insulation_resistance': 'inverter_insulation_resistance',
    'power_factor': 'power_factor',

    # Device Info
    'model_name': 'model_name',
    'serial_number': 'serial_number',
    'rated_power': 'rated_power',
    'alarm_1': 'alarm_1',
}

# Critical keys that must never be None (EVCC, integrations)
CRITICAL_DEFAULTS: Dict[str, int] = {
    'power_active': 0,
    'power_input': 0,
    'meter_power_active': 0,
    'battery_power': 0,
    'battery_soc': 0,
}
