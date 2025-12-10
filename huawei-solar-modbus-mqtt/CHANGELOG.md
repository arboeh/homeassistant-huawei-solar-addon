# Changelog

## [1.3.1] - 2025-12-10
- Register-Set auf **58 Essential Registers** erweitert; alle Namen strikt an `huawei-solar-lib` angepasst (inkl. Grid-/Meter-Register und Groß-/Kleinschreibung). [file:60]  
- Vollständige 3‑Phasen‑Smart‑Meter-Unterstützung: Phasenleistung, -strom, Leiterspannungen, Frequenz und Leistungsfaktor werden jetzt als eigene MQTT-Werte publiziert. [file:60]  
- MQTT‑Discovery-Sensoren mit den neuen Keys synchronisiert und `unit_of_measurement` konsequent verwendet, konform zur Home‑Assistant‑MQTT‑Spezifikation. [web:64]  
- PV‑Power‑Sensoren entfernt; es werden nur noch PV‑Spannung/-Strom übertragen, sodass die Leistung bei Bedarf in Home Assistant per Template berechnet werden kann. [file:60]  
- Add-on‑Option `modbus_device_id` in `slave_id` umbenannt, um Konflikte mit Home‑Assistant‑Device‑IDs zu vermeiden.  

---

## [1.3.0] - 2025-12-09
**Config:** Config nach config/ ausgelagert (registers.py, mappings.py, sensors_mqtt.py) mit 47 Essential Registers und 58 Sensoren.​  
**Register:** Fünf neue Register (u. a. Smart‑Meter‑Power, Battery‑Today, Meter‑Status, Grid‑Reactive‑Power) und 13 zusätzliche Entities für Batterie‑Bus und Netzdetails.​

---

## [1.2.1] - 2025-12-09
**Bugfix:** Persistente MQTT-Verbindung, Status-Flackern behoben  
**Entities** bleiben dauerhaft "available", keine Connection-Timeouts mehr

---

## [1.2.0] - 2025-12-09
**Extended Registers:** +8 neue Register (34 → 42)  
**Device Info:** Model, Serial, Rated Power, Efficiency, Alarms  
**Entities:** 38 → 46

---

## [1.1.2] - 2025-12-08
**Code Quality:** Refactoring, Dependencies reduziert (7 → 5 Pakete)  
**Dockerfile:** Dynamische Python-Version, Health Check

---

## [1.1.1] - 2025-12-08
**Performance:** Nur Essential Registers (21), <3s Cycle-Time  
**Optimierung:** 94% weniger Register-Reads

---

## [1.1.0] - 2025-12-08
**Major Performance:** Parallele Modbus-Reads (240s → 30s, 8x schneller)  
**Batch-Processing:** 20 Register parallel pro Batch

---

## [1.0.7] - 2025-12-08
**Bugfixes:** `UnboundLocalError` in mqtt.py, bashio-Kompatibilität

---

## [1.0.6] - 2025-12-08
**Logging:** ENV-Variablen-Debug, Performance-Metriken

---

## [1.0.5] - 2025-12-08
**MQTT:** `retain=True` für Integrationen, Null-Werte-Fallback

---

## [1.0.4] - 2025-12-08
**Logging:** Konfigurierbarer `log_level`, Performance-Messung

---

## [1.0.3] - 2025-12-07
**Migration:** `HuaweiSolarBridge` → `AsyncHuaweiSolar`

---

## [1.0.2] - 2025-12-06
**Bugfixes:** Modbus DecodeError, robustere Exception-Behandlung

---

## [1.0.1] - 2025-12-05
**Bugfixes:** DecodeError für unbekannte Register

---

## [1.0.0] - 2025-12-04
**Erste stabile Version** - GitHub Actions, Version-Badge

---

## [0.9.0-beta] - 2025-12-03
**Initial Beta Release**  
Modbus TCP → MQTT Discovery, Batterie/PV/Netz-Monitoring
