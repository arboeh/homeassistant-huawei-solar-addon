# Home Assistant Add-on: Huawei Solar Modbus to MQTT

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

Query Huawei Solar Inverter Sun2000 via Modbus TCP and publish to MQTT with automatic Home Assistant discovery.

## About

This add-on connects to your Huawei Solar inverter via Modbus TCP and publishes all relevant data to MQTT. All entities are automatically discovered in Home Assistant.

**Based on the original idea by [mjaschen/huawei-solar-modbus-to-mqtt](https://github.com/mjaschen/huawei-solar-modbus-to-mqtt)** – extended and adapted for Home Assistant Add-on architecture with MQTT Auto-Discovery integration.

### Features

- 🔌 Direct Modbus TCP connection to Huawei inverter
- 📡 Automatic MQTT discovery for Home Assistant
- 🔋 Battery monitoring (SOC, charge/discharge power)
- ☀️ PV string monitoring (voltage, current, power)
- 📊 Grid monitoring (import/export, voltage, frequency)
- 🌡️ Temperature monitoring
- 📈 Energy statistics (daily yield, total yield)
- 🔄 Automatic reconnection on errors
- 📝 Configurable via Home Assistant UI

## Installation

1. Add this repository to your Home Assistant instance:

   [![Add Repository][repository-badge]][repository-url]

2. Click on "Huawei Solar Modbus to MQTT" in the add-on store
3. Click "Install"
4. Configure the add-on (see Configuration section)
5. Start the add-on
6. Check the logs for any errors
7. Entities will appear automatically in Home Assistant

## Configuration

    modbus_host: "192.168.1.100"
    modbus_port: 502
    modbus_device_id: 1
    mqtt_topic: "huawei-solar"
    debug: false
    status_timeout: 180
    poll_interval: 60

### Option: `modbus_host`

The IP address of your Huawei Solar inverter.

### Option: `modbus_port`

Modbus TCP port (default: 502).

### Option: `modbus_device_id`

Modbus Slave ID of your inverter (typically 1, sometimes 16 or 0).

### Option: `mqtt_topic`

MQTT topic prefix for publishing data (default: "huawei-solar").

### Option: `debug`

Enable debug logging (default: false).
### Option: `status_timeout`

Time in seconds after which the status is set to offline if no successful query occurred (default: 180).

### Option: `poll_interval`

Query interval in seconds between two Modbus reads (default: 60).

## MQTT Configuration

The add-on automatically uses the MQTT broker configured in Home Assistant. No additional MQTT configuration needed!
## Support

- [Home Assistant Community Forum][forum]

## Credits

This project is based on the original work by [Marcus Jaschen (mjaschen)](https://github.com/mjaschen) in his repository [huawei-solar-modbus-to-mqtt](https://github.com/mjaschen/huawei-solar-modbus-to-mqtt).

## License

MIT License

Copyright (c) 2025 arboeh

Based on work by Marcus Jaschen (mjaschen), Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[repository-badge]: https://img.shields.io/badge/Add%20to%20Home%20Assistant-Repository-blue
[repository-url]: https://github.com/arboeh/homeassistant-huawei-solar-addon
[forum]: https://community.home-assistant.io