# modbus_energy_meter/config/registers.py
"""Register configuration for Huawei Solar inverter."""

ESSENTIAL_REGISTERS = [
    # Power & Energy (11)
    "active_power",
    "input_power",
    "active_power_meter",
    "storage_charge_discharge_power",
    "storage_state_of_capacity",
    "daily_yield_energy",
    "accumulated_yield_energy",
    "grid_exported_energy",
    "grid_accumulated_energy",
    "storage_charge_capacity_today",
    "storage_discharge_capacity_today",

    # PV Strings 1-4 (8)
    "pv_01_voltage", "pv_01_current",
    "pv_02_voltage", "pv_02_current",
    "pv_03_voltage", "pv_03_current",
    "pv_04_voltage", "pv_04_current",

    # Battery (4)
    "storage_total_charge",
    "storage_total_discharge",
    "storage_bus_voltage",
    "storage_bus_current",

    # Grid 3-Phase (9)
    "grid_A_voltage",
    "grid_B_voltage",
    "grid_C_voltage",
    "line_voltage_A_B",
    "line_voltage_B_C",
    "line_voltage_C_A",
    "grid_frequency",
    "meter_status",
    "reactive_power_meter",

    # Inverter Performance (6)
    "internal_temperature",
    "day_active_power_peak",
    "power_factor",
    "efficiency",
    "reactive_power",
    "insulation_resistance",

    # Status & State (3)
    "device_status",
    "state_1",
    "state_2",

    # Device Information (4)
    "model_name",
    "serial_number",
    "rated_power",
    "startup_time",

    # Extended (2)
    "storage_running_status",
    "alarm_1",
]
