# Huawei Solar Modbus to MQTT

Dieses Add-on liest Daten deines Huawei SUN2000 Wechselrichters per Modbus TCP aus und veröffentlicht sie über MQTT inklusive Home Assistant MQTT Discovery. Dadurch tauchen die meisten Entitäten automatisch im MQTT-Integration-Panel von Home Assistant auf.

## Funktionen

- Modbus TCP Verbindung zum Huawei SUN2000 Inverter
- Veröffentlichung der Messwerte auf einem MQTT-Topic als JSON
- Automatische Erstellung von Home Assistant Entitäten via MQTT Discovery
- Unterstützung für:
  - PV-Leistungen (PV1/PV2, optional PV3/PV4)
  - Netzleistung (Import/Export)
  - Batterie (SOC, Lade-/Entladeleistung, Tages- und Gesamtenergie)
  - 3-phasige Netzspannungen
  - Tages- und Gesamtenergieertrag
  - Inverter-Temperatur und Wirkungsgrad
- Online-/Offline-Status mit:
  - Binary Sensor „Huawei Solar Status"
  - Heartbeat/Timeout-Überwachung
  - MQTT Last Will (LWT) beim Broker
- Konfigurierbares Logging mit verschiedenen Log-Levels
- Performance-Monitoring und automatische Warnungen

## Voraussetzungen

- Huawei SUN2000 Wechselrichter mit aktivierter Modbus TCP Schnittstelle
- Home Assistant mit konfigurierter MQTT-Integration
- MQTT Broker (z.B. Mosquitto), idealerweise über Home Assistant Supervisor bereitgestellt

## Konfiguration

Beispielkonfiguration im Add-on-UI:

    modbus_host: "192.168.1.100"
    modbus_port: 502
    modbus_device_id: 1
    mqtt_topic: "huawei-solar"
    log_level: "INFO"
    debug: false
    status_timeout: 180
    poll_interval: 60

### Optionen

- **modbus_host**  
  IP-Adresse deines Huawei Wechselrichters.

- **modbus_port**  
  Modbus TCP Port (Standard: 502).

- **modbus_device_id**  
  Modbus Slave ID des Inverters. In vielen Installationen ist dies `1`, in manchen `16` oder `0`.

- **mqtt_topic**  
  Basis-Topic, unter dem die Daten veröffentlicht werden (z.B. `huawei-solar`).

- **log_level**  
  Logging-Detailgrad (Standard: `INFO`):

  - `DEBUG`: Sehr detailliert - zeigt Performance-Metriken, einzelne Register-Reads, Zeitmessungen für jeden Schritt
  - `INFO`: Normal - zeigt wichtige Ereignisse und aktuelle Datenpunkte (Solar/Grid/Battery Power)
  - `WARNING`: Nur Warnungen und Fehler
  - `ERROR`: Nur Fehler

- **debug**  
  Legacy-Option: `true` setzt Log-Level automatisch auf DEBUG (Standard: `false`).

- **status_timeout**  
  Zeit in Sekunden, nach der der Status auf `offline` gesetzt wird, wenn keine erfolgreiche Abfrage mehr erfolgt ist (z.B. 180 Sekunden).

- **poll_interval**  
  Abfrageintervall in Sekunden zwischen zwei Modbus-Reads (z.B. 60 Sekunden).

## MQTT Topics

- **Messdaten (JSON):**  
  `huawei-solar` (oder dein konfiguriertes Topic)

- **Status (online/offline):**  
  `huawei-solar/status`  
  Wird genutzt für:
  - Binary Sensor „Huawei Solar Status"
  - `availability_topic` aller Sensoren

## Entitäten in Home Assistant

Nach dem Start des Add-ons werden automatisch MQTT Discovery Konfigurationen publiziert. Du findest die Entitäten dann unter:

- Einstellungen → Geräte & Dienste → MQTT → Geräte → „Huawei Solar Inverter"

Typische Entitäten:

- **Leistung:**
  - `sensor.solar_power`
  - `sensor.grid_power`
  - `sensor.battery_power`
  - `sensor.pv1_power`, `sensor.pv2_power`
- **Energie:**
  - `sensor.solar_daily_yield`
  - `sensor.solar_total_yield`
  - `sensor.grid_energy_exported`
  - `sensor.grid_energy_imported`
  - `sensor.battery_charge_today`
  - `sensor.battery_discharge_today`
- **Batterie:**
  - `sensor.battery_soc`
- **Netz:**
  - `sensor.grid_voltage_phase_a/b/c`
  - `sensor.grid_frequency`
- **Status:**
  - `binary_sensor.huawei_solar_status` (online/offline)
  - `sensor.inverter_status` (Textstatus)

Zusätzliche „diagnostic" Entitäten (z.B. detaillierte Ströme, Spannungen, Bus-Werte) sind standardmäßig deaktiviert und können bei Bedarf in Home Assistant manuell aktiviert werden.

## Logging & Fehleranalyse

### Log-Levels

Das Add-on bietet verschiedene Log-Levels:

**INFO (Standard)** - Übersichtlich für den normalen Betrieb:

    2025-12-08T08:37:00+0100 - huawei.main - INFO - Logging initialized with level: INFO
    2025-12-08T08:37:00+0100 - huawei.main - INFO - Huawei Solar Modbus to MQTT starting
    2025-12-08T08:37:01+0100 - huawei.main - INFO - AsyncHuaweiSolar created successfully (Slave ID: 1)
    2025-12-08T08:37:02+0100 - huawei.main - INFO - Data published - Solar: 4500W | Grid: -200W | Battery: 800W (85%)

**DEBUG** - Detailliert mit Performance-Metriken:

    2025-12-08T08:37:02+0100 - huawei.main - DEBUG - Starting cycle #1
    2025-12-08T08:37:02+0100 - huawei.main - DEBUG - Starting data acquisition cycle
    2025-12-08T08:37:03+0100 - huawei.main - DEBUG - Modbus read completed in 1.842s (87 successful, 5 failed)
    2025-12-08T08:37:03+0100 - huawei.transform - DEBUG - Transformation complete: 73 values extracted in 0.003s
    2025-12-08T08:37:03+0100 - huawei.mqtt - DEBUG - MQTT publish completed in 0.124s
    2025-12-08T08:37:03+0100 - huawei.main - DEBUG - Cycle complete in 1.969s (Modbus: 1.842s, Transform: 0.003s, MQTT: 0.124s)
    2025-12-08T08:37:03+0100 - huawei.main - DEBUG - Heartbeat: Last successful read 0.0s ago (timeout: 180s)

### Performance-Warnungen

Bei langsamen Zyklen erscheinen automatisch Warnungen:

    2025-12-08T08:37:02+0100 - huawei.main - WARNING - Cycle took 52.1s - close to poll_interval (60s). Consider increasing poll_interval.

### Add-on Logs ansehen

- Einstellungen → Add-ons → Huawei Solar Modbus to MQTT → „Log"

### Typische Fehler

- **Modbus-Verbindungsfehler:**

  - IP/Port prüfen
  - Modbus TCP im Inverter aktivieren
  - Slave ID testen (0, 1, 16, 100)
  - Bei `log_level: DEBUG` werden fehlgeschlagene Register-Reads angezeigt

- **MQTT-Verbindungsfehler:**

  - MQTT Broker in Home Assistant prüfen
  - Zugangsdaten kontrollieren
  - Im DEBUG-Modus werden MQTT-Verbindungsdetails geloggt

- **Performance-Probleme:**
  - Achte auf WARNING-Meldungen im Log
  - Erhöhe `poll_interval`, wenn Zyklen zu lange dauern
  - Bei DEBUG siehst du genaue Zeitmessungen für jeden Schritt

## Tipps

- **Erste Inbetriebnahme:** Setze `log_level: DEBUG`, um alle Details zu sehen
- **Normalbetrieb:** Nutze `log_level: INFO` für übersichtliche Logs
- **Performance optimieren:** Achte auf die Cycle-Time im DEBUG-Log und passe `poll_interval` an
- **Fehlersuche:** DEBUG-Level zeigt genau, welche Register gelesen werden und wo Probleme auftreten
- **Mehrere Inverter:** Das Add-on ist aktuell auf einen Inverter ausgelegt, kann aber später erweitert werden
