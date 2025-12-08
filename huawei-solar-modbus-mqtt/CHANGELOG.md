# Changelog

## [Unreleased]

### Added

- [ ] Neue Features hier dokumentieren

### Fixed

- [ ] Bugfixes hier dokumentieren

### Changed

- [ ] Änderungen hier dokumentieren

## [1.0.6] - 2025-12-08

### Added

- Verbesserte Dashboards und Überwachung für MQTT-Verbindung im Add-on
- Erweiterte Fehlerbehandlung bei fehlenden oder falschen MQTT Broker-Daten
- Zusätzliche Umgebungsvariablen-Validierung beim Start des Add-ons
- Detailiertes Debug-Logging der ENV-Variablen-Konfiguration im Startskript

### Changed

- `run.sh` verbessert für zuverlässigen Start mit:
  - Korrekte Handhabung von `bashio::config` Ausgabe (Groß-/Kleinschreibung bei `log_level`)
  - Sicheres Setzen und Export von Umgebungsvariablen
  - Vollständige Weiterleitung aller Logs von Python an Supervisor (exec + python3 -u + 2>&1)
- Fehlerfreie Integration von Legacy `debug` Flag mit `log_level` Überschreibung
- Verbesserte Konsistenz in der Log-Ausgabe beim Add-on Start

### Fixed

- Fix für fehlende oder falsch gesetzte `HUAWEI_LOG_LEVEL` Umgebungsvariable im `run.sh`
- Behebung von Logs, die nur bashio-Ausgaben zeigten, ohne Python-Log-Details
- Verhindert Abbruch des Python-Skripts ohne sichtbare Fehlermeldung beim Add-on Start
- Korrekte Anwendung des neuen API-Namens `AsyncHuaweiSolar` in allen Dateien sichergestellt

## [1.0.5] - 2025-12-08

### Added

- Separate Log-Level-Kontrolle für pymodbus Library (reduziert Logging-Overhead)
- MQTT Retain-Flag für publish_data() zur besseren EVCC-Integration
- Null-Werte-Behandlung in transform.py für kritische Datenpunkte
- Fallback auf 0 für fehlende oder null-Werte bei power_active, power_input, meter_power_active, battery_power, battery_soc
- Pymodbus-Logger wird bei INFO/WARNING/ERROR automatisch auf WARNING-Level gesetzt
- Huawei-Solar Library Logger wird entsprechend dem globalen Log-Level konfiguriert
- Debug-Logging für Pymodbus und Huawei-Solar Logger-Konfiguration

### Changed

- MQTT-Daten werden jetzt mit `retain=True` publiziert für bessere EVCC-Kompatibilität
- Pymodbus-Logs erscheinen nur noch bei DEBUG-Level oder als WARNING/ERROR
- Kritische Sensor-Werte (Power, SOC) werden nicht mehr als null publiziert, sondern standardmäßig als 0
- Verbesserte Fehlerbehandlung für fehlende Register-Werte in transform.py
- Log-Output bei DEBUG zeigt jetzt auch Pymodbus Log-Level-Konfiguration

### Fixed

- EVCC "outdated" Fehler durch fehlende retain-Flag in MQTT-Nachrichten behoben
- EVCC `strconv.ParseFloat: parsing "<nil>"` Fehler durch Null-Werte-Behandlung behoben
- Übermäßige pymodbus ERROR-Logs bei normalem Betrieb (INFO-Level) reduziert
- Fehlende Datenpunkte führen nicht mehr zu null-Werten in MQTT-Nachrichten

## [1.0.4] - 2025-12-08

### Added

- Konfigurierbarer Log-Level über `log_level` Option (DEBUG, INFO, WARNING, ERROR)
- Strukturiertes Logging mit separaten Loggern für Module (huawei.main, huawei.mqtt, huawei.transform)
- Performance-Messung für Modbus-Reads, Daten-Transformation und MQTT-Publishing
- Detaillierte Debug-Logs mit Zeitmessungen für jeden Zyklus
- Zyklus-Zähler für bessere Nachverfolgbarkeit bei Fehlersuche
- Register-Read-Statistiken (erfolgreiche/fehlgeschlagene Reads) im DEBUG-Modus
- Performance-Warnungen bei langsamen Zyklen (>80% des poll_interval)
- Heartbeat-Logging für Status-Überwachung
- Strukturierte Info-Logs zeigen aktuelle Datenpunkte (Solar/Grid/Battery Power, SOC)

### Changed

- Verbessertes Logging-Format mit Modul-Namen: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Alle `logging.xxx()` Aufrufe auf modulare `logger.xxx()` umgestellt
- `get_value()` Funktion in transform.py vereinfacht und optimiert
- Enum- und Datetime-Werte werden automatisch korrekt konvertiert
- Traceback-Logging bei Fehlern verbessert (nur bei DEBUG-Level)
- Bessere Lesbarkeit durch strukturierte und kontextbezogene Log-Ausgaben
- Debug-Logs enthalten jetzt Performance-Metriken für jeden Verarbeitungsschritt
- Legacy `debug: true` Option bleibt für Abwärtskompatibilität erhalten

### Removed

- Unnötige Hilfsfunktionen in transform.py entfernt (`calculate_power`, `get_enum_value`, `get_list_value`, `get_datetime_value`)

## [1.0.3] - 2025-12-07

### Fixed

- Wechsel von `HuaweiSolarBridge` auf `AsyncHuaweiSolar`, um die neue API der huawei-solar Library korrekt zu nutzen
- Fehler beim Instanziieren der Bridge behoben (abstrakte Klasse, fehlende Implementierung von `_populate_additional_fields` und `supports_device`)
- Bessere Behandlung von nicht unterstützten Registern (Illegal Data Address / ExceptionResponse Code 2), ohne den gesamten Lesezyklus zu unterbrechen

### Changed

- Lese-Logik auf registerbasiertes Auslesen mit `AsyncHuaweiSolar.get()` umgestellt
- Debug-Logging für fehlgeschlagene Registerlesungen erweitert, um Inverter-spezifische Unterschiede besser nachvollziehen zu können

## [1.0.2] - 2025-12-06

### Fixed

- HuaweiSolarBridge.create() Parameter-Fehler behoben (explizite Keyword-Argumente)
- DecodeError-Handling für unbekannte Register-Werte (z.B. Unit-Code 780) verbessert
- Robustere Fehlerbehandlung bei Modbus-Kommunikationsproblemen
- Verhindert Absturz des Add-ons bei einzelnen fehlerhaften Registern
- `heartbeat`-Funktion korrekt platziert (behebt "name 'heartbeat' is not defined" Fehler)

### Changed

- Aktualisierte `huawei-solar` Library auf Version >=2.3.0
- Aktualisierte `pymodbus` auf Version >=3.8.6 zur Verbesserung der Protokoll-Kompatibilität
- Erweiterte Logging-Ausgaben für besseres Debugging
- Separate Exception-Behandlung für `DecodeError` und `ReadException`

## [1.0.1] - 2025-12-05

### Fixed

- DecodeError handling für unbekannte Register-Werte
- Verbesserte Fehlerbehandlung bei Modbus-Kommunikation

### Changed

- Aktualisierte huawei-solar Library auf neueste Version
- Erweiterte Logging-Ausgaben für besseres Debugging

## [1.0.0] - 2025-12-04

### Added

- Erste stabile Version des Add-ons
- Versionierung und Release-Workflow mit GitHub Actions
- Badge für aktuelle Release-Version in der README

### Changed

- Wechsel von 0.9.0-beta auf 1.0.0 ohne Breaking Changes

## [0.9.0-beta] - 2025-12-03

### Added

- Initial beta release
- Modbus TCP Verbindung zu Huawei Solar Inverter
- Automatische MQTT Discovery für Home Assistant
- Batterie-Monitoring (SOC, Lade-/Entladeleistung)
- PV-String-Monitoring (PV1/PV2, optional PV3/PV4)
- Netz-Monitoring (Import/Export, 3-phasig)
- Energie-Statistiken (Tages-/Gesamtenergie)
- Temperatur- und Wirkungsgrad-Monitoring
- Automatisches Reconnect bei Fehlern
- Konfigurierbar über Home Assistant UI

### Known Issues

- Erweiterte Tests laufen noch
