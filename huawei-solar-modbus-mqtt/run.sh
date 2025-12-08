#!/usr/bin/env bashio
set -e

bashio::log.info "Starting Huawei Solar Modbus to MQTT Add On..."

# Read config from Home Assistant
export HUAWEI_MODBUS_HOST=$(bashio::config modbus_host)
export HUAWEI_MODBUS_PORT=$(bashio::config modbus_port)
export HUAWEI_MODBUS_DEVICE_ID=$(bashio::config modbus_device_id)
export HUAWEI_MODBUS_MQTT_TOPIC=$(bashio::config mqtt_topic)
export HUAWEI_STATUS_TIMEOUT=$(bashio::config status_timeout)
export HUAWEI_POLL_INTERVAL=$(bashio::config poll_interval)

# ✅ LOG LEVEL - UPPERCASE für Python logging
export HUAWEI_LOG_LEVEL=$(bashio::config log_level | tr '[:lower:]' '[:upper:]')

# Legacy debug flag
if bashio::config.true debug; then
    export HUAWEI_MODBUS_DEBUG="yes"
    export HUAWEI_LOG_LEVEL="DEBUG"
fi

# MQTT Config
if bashio::config.has_value mqtt_host; then
    export HUAWEI_MODBUS_MQTT_BROKER=$(bashio::config mqtt_host)
    bashio::log.info "Using custom MQTT broker: ${HUAWEI_MODBUS_MQTT_BROKER}"
else
    export HUAWEI_MODBUS_MQTT_BROKER=$(bashio::services mqtt host)
    bashio::log.info "Using HA MQTT broker: ${HUAWEI_MODBUS_MQTT_BROKER}"
fi

export HUAWEI_MODBUS_MQTT_PORT=$(bashio::config mqtt_port || bashio::services mqtt port)
export HUAWEI_MODBUS_MQTT_USER=$(bashio::config mqtt_user || bashio::services mqtt username)
export HUAWEI_MODBUS_MQTT_PASSWORD=$(bashio::config mqtt_password || bashio::services mqtt password)

# Final bashio logs
bashio::log.info "Log level: ${HUAWEI_LOG_LEVEL}"
bashio::log.info "Inverter: ${HUAWEI_MODBUS_HOST}:${HUAWEI_MODBUS_PORT} (ID: ${HUAWEI_MODBUS_DEVICE_ID})"
bashio::log.info "MQTT: ${HUAWEI_MODBUS_MQTT_TOPIC}"
bashio::log.info "Starting Python..."

# 🚀 Start Python - Logs werden jetzt sichtbar!
exec python3 -u /app/huawei2mqtt.py 2>&1
