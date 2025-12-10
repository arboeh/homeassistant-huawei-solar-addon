#!/usr/bin/with-contenv bashio

bashio::log.info "🚀 Starting Huawei Solar Modbus → MQTT Add-on..."

# Modbus Configuration
export HUAWEI_MODBUS_HOST=$(bashio::config 'modbus_host')
export HUAWEI_MODBUS_PORT=$(bashio::config 'modbus_port')
export HUAWEI_MODBUS_DEVICE_ID=$(bashio::config 'slave_id')

# MQTT Topic & Intervals
export HUAWEI_MODBUS_MQTT_TOPIC=$(bashio::config 'mqtt_topic')
export HUAWEI_STATUS_TIMEOUT=$(bashio::config 'status_timeout')
export HUAWEI_POLL_INTERVAL=$(bashio::config 'poll_interval')

# Log Level Configuration
export HUAWEI_LOG_LEVEL=$(bashio::config 'log_level')
bashio::log.info "Log level: ${HUAWEI_LOG_LEVEL}"

# MQTT Broker (Custom or HA Service)
if bashio::config.has_value 'mqtt_host' && [ -n "$(bashio::config 'mqtt_host')" ]; then
    export HUAWEI_MODBUS_MQTT_BROKER=$(bashio::config 'mqtt_host')
    bashio::log.info "Using custom MQTT broker: ${HUAWEI_MODBUS_MQTT_BROKER}"
else
    export HUAWEI_MODBUS_MQTT_BROKER=$(bashio::services mqtt "host")
    bashio::log.info "Using HA MQTT service: ${HUAWEI_MODBUS_MQTT_BROKER}"
fi

# MQTT Port
if bashio::config.has_value 'mqtt_port' && [ -n "$(bashio::config 'mqtt_port')" ]; then
    export HUAWEI_MODBUS_MQTT_PORT=$(bashio::config 'mqtt_port')
else
    export HUAWEI_MODBUS_MQTT_PORT=$(bashio::services mqtt "port")
fi

# MQTT User
if bashio::config.has_value 'mqtt_user' && [ -n "$(bashio::config 'mqtt_user')" ]; then
    export HUAWEI_MODBUS_MQTT_USER=$(bashio::config 'mqtt_user')
else
    export HUAWEI_MODBUS_MQTT_USER=$(bashio::services mqtt "username")
fi

# MQTT Password
if bashio::config.has_value 'mqtt_password' && [ -n "$(bashio::config 'mqtt_password')" ]; then
    export HUAWEI_MODBUS_MQTT_PASSWORD=$(bashio::config 'mqtt_password')
else
    export HUAWEI_MODBUS_MQTT_PASSWORD=$(bashio::services mqtt "password")
fi

# Debug Mode (Legacy Compatibility)
if bashio::config.true 'debug'; then
    export HUAWEI_MODBUS_DEBUG="yes"
    export HUAWEI_LOG_LEVEL="DEBUG"
    bashio::log.level "debug"
    bashio::log.debug "Debug mode enabled (legacy flag)"
else
    export HUAWEI_MODBUS_DEBUG="no"
fi

# Connection Summary
bashio::log.info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
bashio::log.info "📡 Inverter: ${HUAWEI_MODBUS_HOST}:${HUAWEI_MODBUS_PORT} (Slave ID: ${HUAWEI_MODBUS_DEVICE_ID})"
bashio::log.info "📨 MQTT: ${HUAWEI_MODBUS_MQTT_BROKER}:${HUAWEI_MODBUS_MQTT_PORT}"
bashio::log.info "📢 Topic: ${HUAWEI_MODBUS_MQTT_TOPIC}"
bashio::log.info "⏱️  Poll Interval: ${HUAWEI_POLL_INTERVAL}s | Timeout: ${HUAWEI_STATUS_TIMEOUT}s"
bashio::log.info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Start Python application
bashio::log.info "Starting Python application..."
cd /app
exec python3 -u -m modbus_energy_meter.main
