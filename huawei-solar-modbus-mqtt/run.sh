#!/usr/bin/env bashio
set -e

bashio::log.info "Starting Huawei Solar Modbus to MQTT Add On..."

# === KONFIGURATION MIT FALLBACKS ===
get_config_or_default() {
    local key="$1"
    local default="$2"
    bashio::config "${key}" 2>/dev/null | bashio::to_json || echo "${default}"
}

# Basis-Konfiguration (mit Fallbacks)
export HUAWEI_MODBUS_HOST=$(get_config_or_default "modbus_host" "192.168.1.100")
export HUAWEI_MODBUS_PORT=$(get_config_or_default "modbus_port" "502")
export HUAWEI_MODBUS_DEVICE_ID=$(get_config_or_default "modbus_device_id" "1")
export HUAWEI_MODBUS_MQTT_TOPIC=$(get_config_or_default "mqtt_topic" "huawei-solar")
export HUAWEI_STATUS_TIMEOUT=$(get_config_or_default "status_timeout" "180")
export HUAWEI_POLL_INTERVAL=$(get_config_or_default "poll_interval" "60")

# Log-Level (mit Fallback)
export HUAWEI_LOG_LEVEL=$(get_config_or_default "log_level" "INFO" | tr '[:lower:]' '[:upper:]')

# Legacy debug flag
if bashio::config.true "debug" 2>/dev/null; then
    export HUAWEI_MODBUS_DEBUG="yes"
    export HUAWEI_LOG_LEVEL="DEBUG"
fi

# === MQTT KONFIGURATION ===
MQTT_HOST=$(get_config_or_default "mqtt_host" "")
MQTT_PORT=$(get_config_or_default "mqtt_port" "")
MQTT_USER=$(get_config_or_default "mqtt_user" "")
MQTT_PASSWORD=$(get_config_or_default "mqtt_password" "")

if [ -n "$MQTT_HOST" ]; then
    export HUAWEI_MODBUS_MQTT_BROKER="$MQTT_HOST"
    export HUAWEI_MODBUS_MQTT_PORT="${MQTT_PORT:-1883}"
    export HUAWEI_MODBUS_MQTT_USER="$MQTT_USER"
    export HUAWEI_MODBUS_MQTT_PASSWORD="$MQTT_PASSWORD"
    bashio::log.info "Using custom MQTT: ${MQTT_HOST}:${MQTT_PORT}"
else
    # Fallback auf HA MQTT (ohne bashio::services - da auch das fehlschlägt)
    export HUAWEI_MODBUS_MQTT_BROKER="core-mosquitto"
    export HUAWEI_MODBUS_MQTT_PORT="1883"
    export HUAWEI_MODBUS_MQTT_USER=""
    export HUAWEI_MODBUS_MQTT_PASSWORD=""
    bashio::log.info "Using default HA MQTT broker: core-mosquitto:1883"
fi

# === KONFIGURATION LOGGEN ===
bashio::log.info "=== CONFIGURATION ==="
bashio::log.info "Log level: ${HUAWEI_LOG_LEVEL}"
bashio::log.info "Inverter: ${HUAWEI_MODBUS_HOST}:${HUAWEI_MODBUS_PORT} (ID: ${HUAWEI_MODBUS_DEVICE_ID})"
bashio::log.info "MQTT Topic: ${HUAWEI_MODBUS_MQTT_TOPIC}"
bashio::log.info "MQTT Broker: ${HUAWEI_MODBUS_MQTT_BROKER}:${HUAWEI_MODBUS_MQTT_PORT}"
bashio::log.info "Poll: ${HUAWEI_POLL_INTERVAL}s | Timeout: ${HUAWEI_STATUS_TIMEOUT}s"
bashio::log.info "====================="

# === PRÜFUNG KRITISCHER WERTE ===
if [ -z "$HUAWEI_MODBUS_MQTT_TOPIC" ] || [ -z "$HUAWEI_MODBUS_HOST" ]; then
    bashio::log.fatal "CRITICAL: Missing required config! MQTT_TOPIC='${HUAWEI_MODBUS_MQTT_TOPIC}' HOST='${HUAWEI_MODBUS_HOST}'"
    exit 1
fi

bashio::log.info "All config values valid - Starting Python..."

# 🚀 PYTHON START - Jetzt definitiv funktioniert!
exec python3 -u /app/huawei2mqtt.py 2>&1
