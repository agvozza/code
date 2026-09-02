# Toyota RAV4 XA50 (2019–2025) — Fuse Tables

Compiled reference for **VIN 2T3A1RFV8MC233488** — 2021 RAV4 XLE Premium, A25A-FKS gasoline, AWD.

> ## ⚠ Position numbers are UNVERIFIED
>
> Published sources disagree on numbering, and **the owner's manual contains no fuse table at all** —
> Toyota moved the chart entirely to the physical box lid for this generation. The manual says only:
> *"The amperage rating can be found on the fuse box lid."* (OM p.617)
>
> **The fuse NAME is the identifier. The box lid is the only authoritative position map.**
> Photograph it on arrival.

---

## Box locations (from the owner's manual, pp. 616–617)

| Box | Location | Access |
|---|---|---|
| **Instrument panel J/B (IJB)** | Left side instrument panel | Remove the lid |
| **Engine compartment — Type A** | Engine bay (if equipped) | Push claws A and B to release lock, lift cover |
| **Engine compartment — Type B** | Engine bay | Push claws A and B to release lock, lift cover |

The IJB grid is **36 positions in two columns of 18** (1–18 left, 19–36 right, numbered top to bottom)
— confirmed against the published layout drawing in `fuse-box-diagrams/IJB-instrument-panel-diagram.png`.

No luggage-compartment junction block on this vehicle — that box is Hybrid/Prime only.

---

## Instrument Panel J/B — full table

Positions per fuse-box.info. **StartMyCar disagrees** on several (noted in the Conflict column).

| Pos | Amps | Name | Circuit | Conflict |
|---:|---:|---|---|---|
| 1 | 7.5A | FOG RR | Rear fog lights | |
| 2 | 7.5A | **OBD** | On-board diagnostics — **DLC3 pin 16 (+B)** | listed as #3 elsewhere |
| 3 | 10A | DOME | Dome / interior lighting | |
| 4 | 7.5A | TRUNK OPN | Power trunk lid opener | |
| 6 | 10A | ECU-DCC NO.2 | ECU | |
| 7 | 5A | ECU-DCC NO.1 | ECU | |
| 8 | 15A | RADIO | Radio / audio | |
| 9 | 20A | DOOR R/R | Rear right door | |
| 10 | 7.5A | S-HORN | Horn / anti-theft | |
| 11 | 10A | STRG LOCK | Steering lock | |
| 12 | 7.5A | DCM | Data communication module (telematics) | |
| 13 | 5A | **ECU-ACC** | ACC rail | |
| 14 | 7.5A | **ECU-IG1 NO.3** | ECU — camera candidate | |
| 15 | 5A | EPS-IG1 | Electric power steering | |
| 16 | 10A | **A/BAG-IG2** | **Airbag control module IG2 feed** | listed as #31 elsewhere |
| 17 | 5A | **METER-IG2** | Combination meter | |
| 18 | 5A | **ECU-IG2 NO.3** | ECU | |
| 19 | 10A | **ECU-B NO.2** | Constant +B | listed as #2 elsewhere |
| 20 | 5A | **ECU-B NO.1** | Constant +B | listed as #4 elsewhere |
| 21 | 15A | D/L | Power door lock | |
| 22 | 7.5A | STOP | Stop lights | |
| 23 | 7.5A | **AM2** | Starter system | |
| 24 | 10A | HAZ | Hazard lights | |
| 25 | 5A | PANEL | Instrument panel lights | listed as #14 elsewhere |
| 26 | 10A | TAIL | Tail lights | |
| 27 | 20A | DOOR F/L | Front left door lock | |
| 28 | 20A | DOOR F/R | Front right door | |
| 29 | 15A | P/OUTLET NO.1 | Cigar lighter / power outlet | |
| 30 | 5A | SFT LOCK-ACC | Shift lock control | |
| 31 | 20A | WASHER | Windshield washer | |
| 33 | 10A | **ECU-IG1 NO.4** | ECU — camera candidate | |
| 34 | 5A | BKUP LP | Backup lights | |
| 35 | 7.5A | **ECU-IG1 NO.2** | ECU — camera candidate | |
| 36 | 5A | **ECU-IG1 NO.1** | ECU — camera candidate | |

Positions 5 and 32 are not populated in the published table.

---

## Engine Room J/B No.1 — relevant entries only

A25A-FKS gasoline amperages (this vehicle).

| Pos | Amps | Name | Circuit |
|---:|---:|---|---|
| 28 | 20A | **IG2 MAIN** | Ignition main |
| 29 | 30A | DC CUT | — |
| 40 | 50A | **J/B-B** | **Junction box bus — feeds the cabin block** |
| 41 | 80A | EPS | Electric power steering |
| 42 | 60A | **R/B NO.1** | Relay block main |
| 43 | 120/140A | **ALT** | Alternator / charging main |
| 48 | 10A | **ECU IG2 NO.2** | ECU |
| 49 | 10A | **ECU IG2 NO.1** | ECU |

Full engine-room table (53 positions) is in the sources listed below; only the feed path and
IG2 branches matter for repowering.

---

## Back-power sets

**Tier 1 — required for the CDR download**

```
OBD  7.5A   ·  ECU-B NO.1  5A  ·  ECU-B NO.2  10A  ·  A/BAG-IG2  10A
```

**Tier 2 — add for Techstream and the forward camera**

```
ECU-IG1 NO.1  5A   ·  ECU-IG1 NO.2  7.5A  ·  ECU-IG1 NO.3  7.5A
ECU-IG1 NO.4  10A  ·  ECU-IG2 NO.3  5A    ·  METER-IG2  5A
ECU-ACC  5A        ·  AM2  7.5A
```

**Tier 3 — engine room, only if the bus will not come up**

```
ECU IG2 NO.1  10A  ·  ECU IG2 NO.2  10A  ·  IG2 MAIN  20A
```

---

## Blade color code (SAE mini / low-profile mini)

| Amps | Color |
|---:|---|
| 5A | Tan |
| 7.5A | Brown |
| 10A | Red |
| 15A | Blue |
| 20A | Yellow |
| 25A | Clear / natural |
| 30A | Green |

---

## Unresolved

1. **Which `ECU-IG1` branch feeds the forward recognition camera.** No fuse on this platform is named
   CAMERA, FCM, PCS, RDA or TSS. Only the Toyota EWD *Power Source* section names it. Power all four
   branches and the question is moot.
2. **Actual position numbers.** Box lid only. See the warning at the top.

---

## Sources

- fuse-box.info — RAV4 XA50 2019–2025 — https://fuse-box.info/toyota/toyota-rav4-xa50-2019-2025-fuses (primary table)
- StartMyCar — 2021 RAV4 — https://www.startmycar.com/us/toyota/rav4/info/fusebox/2021 (conflicting positions)
- fuseandrelay.com — RAV4 2019–2026 — https://fuseandrelay.com/toyota/rav4-5g.html (box designations)
- 2021 RAV4 Owner's Manual pp. 616–618 (`2021-RAV4-Owners-Manual.pdf`) — box locations and access

Third-party tables are secondary sources. Cite the on-vehicle lid photograph in any report.
