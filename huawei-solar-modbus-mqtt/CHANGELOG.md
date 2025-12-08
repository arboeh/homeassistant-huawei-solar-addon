# Changelog

## [Unreleased]

### Added

- [ ] Neue Features hier dokumentieren

### Fixed

- [ ] Bugfixes hier dokumentieren

### Changed

- [ ] Änderungen hier dokumentieren

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
- DecodeError-
