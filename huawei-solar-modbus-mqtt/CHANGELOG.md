# Changelog

## [1.3.2] - 2025-12-15
**Bugfixes:** Register-Namen korrigiert für Battery Daily Charge/Discharge
- `storage_charge_capacity_today` → `storage_current_day_charge_capacity`
- `storage_discharge_capacity_today` → `storage_current_day_discharge_capacity`
- `alarm_1` Register entfernt (nicht bei allen Inverter-Modellen verfügbar, verursachte Template-Fehler)
- Behebt "Template variable warning: 'dict object' has no attribute" Fehler in Home Assistant

**Dependencies:** Alle Core-Abhängigkeiten auf neueste stabile Versionen aktualisiert
- `huawei-solar`: 2.3.0 → **2.5.0**
- `paho-mqtt`: 1.6.1 → **2.1.0** (MQTT 5.0 Support)
- `pymodbus`: 3.8.6 → **3.11.4**
- `pytz`: 2024.2 → **2025.2**

---

## [1.3.1] - 2025-12-10
- Register-Set auf **58 Essential Registers** erweitert; alle Namen strikt an `huawei-solar-lib` angepasst (inkl. Grid-/Meter-Register und Groß-/Kleinschreibung)
- Vollständige 3‑Phasen‑Smart‑Meter-Unterstützung: Phasenleistung, -strom, Leiterspannungen, Frequenz und Leistungsfaktor werden jetzt als eigene MQTT-Werte publiziert
- MQTT‑Discovery-Sensoren mit den neuen Keys synchronisiert und `unit_of_measurement` konsequent verwendet, konform zur Home‑Assistant‑MQTT‑Spezifikation
- PV‑Power‑Sensoren entfernt; es werden nur noch PV‑Spannung/-Strom übertragen, sodass die Leistung bei Bedarf in Home Assistant per Template berechnet werden kann
- Add-on‑Option `modbus_device_id` in `slave_id` umbenannt, um Konflikte mit Home‑Assistant‑Device‑IDs zu vermeiden

---

## [1.3.0] - 2025-12-09
**Config:** Config nach config/ ausgelagert (registers.py, mappings.py, sensors_mqtt.py) mit 47 Essential Registers und 58 Sensoren  
**Register:** Fünf neue Register (u. a. Smart‑Meter‑Power, Battery‑Today, Meter‑Status, Grid‑Reactive‑Power) und 13 zusätzliche Entities für Batterie‑Bus und Netzdetails

---

## [1.2.1] - 2025-12-09
**Bugfix:** Persistente MQTT-Verbindung, Status-Flackern behoben  
**Entities** bleiben dauerhaft "available", keine Connection-Timeouts mehr

---

## [1.2.0] - 2025-12-09
**Extended Registers:** +8 neue Register (34 → 42)  
**Device Info:** Model, Serial, Rated Power, Efficiency, Alarms  
**Entities:** 38 → 46
