# Source Research Notes — user-supplied references

> ## ⚠ READ §7 FIRST
> A **Toyota Service Manual** (42,638 pages, full text layer) was supplied after §§1–6 were written
> and **supersedes them**. Two open items are now closed with Toyota-authoritative citations:
> the forward recognition camera runs on **`ECU-IG1 NO. 3`**, and there is **no trunk fuse box**.
> §4b's `ECU-IG1 NO.4` hypothesis is **wrong** — it is retained below only to show the reasoning
> that the service manual overturned. Do not act on it.

Research conducted 2026-09-02 against three sources supplied for the VIN 2T3A1RFV8MC233488
inspection. This document records what each source is, what was extracted, what could not be
obtained, and — most importantly — what the sources **corroborate or contradict** in the existing
fuse tables.

Contents summary up front:

| Source | Obtained? | Value |
|---|---|---|
| fixmycarinfo.com — XA50 Wiring Diagrams PDF | ❌ **No** — Cloudflare bot challenge | Would have resolved both open items |
| YouTube `1Ic0Eb_s3UA` — Simon Car Fixer | ⚠️ Partial — metadata + frames, no audio/captions | Raises a **trunk** question (§3) |
| YouTube `OMTHy6pHQvY` — Auto User Guide | ⚠️ Partial — metadata + frames, no audio/captions | **Corroborates the fuse numbering** (§4) |

---

## 1. The headline result

*(Written before the service manual arrived — see §7 for what actually settled these.)*

An independent third source **confirms the fuse-box.info position numbering** that the field
sheet had flagged as unverified, and gave a lead on the forward-camera fuse. Details in §4. Neither
finding is Toyota-authoritative, so the box-lid photograph still governs for positions.

---

## 2. fixmycarinfo.com — "Toyota Rav4 XA50 2018-2021 – Wiring Diagrams.pdf"

**Not obtained.** Blocked at every route attempted:

| Method | Result |
|---|---|
| `curl` direct to the PDF URL | HTTP 403 — Cloudflare "Just a moment…" interstitial |
| `curl` with viewer-page referer + browser UA | HTTP 403 — same challenge |
| Headless Chromium (Playwright, proxy-configured) | `ERR_CONNECTION_RESET` on navigation; request API returned the same 403, no `cf_clearance` cookie issued |
| WebFetch | HTTP 403 |

**This is a bot challenge, not a copyright block and not an egress-policy denial** — the host is
reachable and returns Cloudflare's JS interstitial rather than a refusal. Cloudflare requires a
real browser session to solve a JS proof-of-work; the automated browser could not complete it
through this environment's egress relay.

**Consequence:** the two open items this document would have closed remain open. If you open the
viewer link yourself in a normal browser, the download button (`sButton=true` in that URL) should
work, and the *Power Source* section is the part worth extracting.

**Caveat if you do get it:** the title says "XA50 2018-2021", which is the right generation. Verify
that before relying on it — the last widely circulated "RAV4 wiring diagram" PDF encountered during
this research was a 2GR-FE V6 car, an entirely different platform.

---

## 3. Video 1 — `1Ic0Eb_s3UA`

| Field | Value |
|---|---|
| Title | The fuse box location on a 2021 Toyota RAV4 |
| Channel | Simon Car Fixer (`@simoncarfixer`) |
| Published | 2022-04-09 |
| Duration | 1:38 |
| Views | ~15,200 |
| Captions | **None** — no manual or auto captions published |
| Description | Empty |

**Chapters (author-supplied):**

| Time | Chapter |
|---|---|
| 0:00 | Intro |
| 0:07 | Fuse box location |
| 0:52 | Trunk location |

**Visual content** reconstructed from storyboard frames
(`video-frames/video1-simoncarfixer-contact-sheet.png`, 160×90 per frame):

1. **0:00–0:10** — exterior, hood raised, engine bay overview
2. **0:10–0:35** — engine-room fuse box: cover released and lifted, populated fuse field visible
   (blue/pink/red/tan blades), then **several sustained frames of the underside of the box lid
   showing the printed legend with the Toyota logo**
3. **0:35–0:50** — a second engine-bay box, again with lid legend frames
4. **0:50–1:00** — cabin: driver's seat, steering wheel, dashboard
5. **1:00–1:25** — a footwell / lower-trim area with panel removed
6. **1:25–1:38** — **cargo area**: rear cargo floor, a spare-tire-well-shaped cover, hand reaching in

### ⚠ The trunk question — a correction to earlier guidance

I previously told you flatly that this vehicle has **no luggage-compartment junction block**, on the
grounds that the box is Hybrid/Prime-only. This video's third chapter is titled "Trunk location" and
its final ~13 seconds are shot in the cargo area.

Where that leaves things:

- The **owner's manual for this VIN is authoritative and documents exactly three fuse box
  locations** — engine compartment Type A, engine compartment Type B, and left side instrument panel
  (pp. 616–617). The index confirms fuses appear only at p.616. **No trunk box is documented.**
- At 160×90 I **cannot** determine whether the video's trunk segment shows a fuse box, the tool kit,
  the jack, or the spare well itself. The audio would say, and there are no captions.

**Net:** my original statement is still the best-supported reading, but I stated it with more
certainty than the evidence carries. Treat it as *"not documented for this VIN"* rather than
*"does not exist"*, and **spend thirty seconds looking in the cargo area on arrival.** It costs
nothing and closes the question.

---

## 4. Video 2 — `OMTHy6pHQvY` — the useful one

| Field | Value |
|---|---|
| Title | Toyota RAV4 (2020 – 2022) Fuses & Fuse Box Diagram and Location User Guide |
| Channel | Auto User Guide (`@Auto-UserGuide`) |
| Published | 2024-11-06 |
| Duration | 6:02 |
| Views | ~19,000 |
| Captions | **None** |
| Reference link | https://www.autouserguide.com/toyota/fuse-diagrams-2022-toyota-rav4-fuses-and-relay-guide/ |

The linked page was fetched and inspected: it carries the owner's-manual illustrations and the video
embed, but **not** the fuse tables — those exist only as graphics inside the video itself.

**Screen content** (`video-frames/video2-autouserguide-contact-sheet.png`): the video is a slow pan
down a fuse table paired with a **36-position two-column position map** — which independently
confirms the IJB geometry already recorded (1–18 left column, 19–36 right column, numbered top to
bottom).

### 4a. Position numbering — corroborated

The table's circuit descriptions were compared against the fuse-box.info naming that the field sheet
flagged as unverified. **Every position legible in the frames agrees:**

| Pos | This video's description | fuse-box.info name | Agrees? |
|---:|---|---|:--:|
| 22 | Brake light | STOP | ✅ |
| 23 | Tailgate opening, unlock entry and start system, immobilizer, steering wheel lock | AM2 (starter system) | ✅ |
| 24 | Alarm, Hazard | HAZ | ✅ |
| 25 | VSC OFF switch, instrument cluster, switch illumination, cup holder lights… | PANEL (instrument panel lights) | ✅ |
| 26 | Side light, license plate light, fog light | TAIL | ✅ |
| 27 | Power windows front left door | DOOR F/L | ✅ |
| 28 | Power windows front right door | DOOR F/R | ✅ |
| 29 | Power socket, cigarette lighter | P/OUTLET NO.1 | ✅ |
| 30 | Gear selector lock | SFT LOCK-ACC | ✅ |
| 31 | Glass washer | WASHER | ✅ |

Ten independent agreements, zero contradictions. **This substantially resolves the numbering
conflict in favour of fuse-box.info and against StartMyCar**, whose scheme would have placed
`A/BAG-IG2` at 31 and `OBD` at 3.

### 4b. The forward-camera fuse — a lead that turned out to be WRONG (see §7a)

One entry in the low-30s carries an unusually long circuit list. Legible fragments include:

> "Dynamic cruise control radar, engine control unit, intelligent entry and start system, EPS,
> front fog light, fuel flap, active air flap control system, headlights, headlight range control,
> hybrid system, lighting, immobilizer, intelligent parking system, interior lighting, **lane
> control system**, automatic turn-off system for turn signals, buzzer light, navigation, power
> windows, **anticollision system**, rear fog light, power mirrors, seat belt indicator, gear
> selector lock, sunroof, SRS, starting system, steering lock, side light, telematics system,
> anti-theft system, tire pressure monitoring system, direction indicators, pedestrian warning
> system (noise generator), VSC, wireless charging system"

**"Anticollision system" is the Pre-Collision System and "lane control system" is Lane Departure
Alert — both are forward recognition camera functions.** The entry's blade chip renders **red = 10A**.

Cross-referencing: the only 10A `ECU-IG1` branch in the IJB is **`ECU-IG1 NO.4` at position 33**.

**Assessment: `ECU-IG1 NO.4` (10A) is the most probable forward-camera supply.**

Confidence qualifiers, stated plainly:
- The position digit renders ambiguously as **32 or 33** at 160×90. fuse-box.info lists no 32.
- The source is a third-party content aggregator, not Toyota.
- The entry also lists "hybrid system", so this table is a merged multi-variant listing, not one
  built for a gas A25A-FKS car.

**This does not change the recommended procedure.** Powering all four `ECU-IG1` branches remains
correct and makes the question moot. The value of this lead is that if you need the branch *named*
in a report, `ECU-IG1 NO.4` is now the hypothesis to confirm against the TIS EWD — rather than
starting from nothing.

---

## 5. What could not be obtained, and why

| Wanted | Blocked by |
|---|---|
| XA50 wiring diagram PDF | Cloudflare JS challenge; unsolvable by headless browser through this relay |
| Video captions / transcripts | Neither video publishes manual or automatic captions |
| Video audio | YouTube requires a PO token for media streams from this environment; only 160×90 storyboards were retrievable |
| Full-resolution fuse table from video 2 | Exists only as in-video graphics; the linked page does not carry it |

The storyboard route worked only after switching yt-dlp to the `mweb` player client and installing a
Deno JS runtime — the default client returned "Sign in to confirm you're not a bot".

---

## 6. Net effect on the open items

| Open item | Before | After |
|---|---|---|
| Fuse position numbers | Two sources in conflict, unresolved | **Ten-position independent corroboration** of fuse-box.info. Lid photo still governs, but the tables are now much more trustworthy. |
| Forward-camera branch | No candidate at all | **`ECU-IG1 NO.4` (10A) is the leading hypothesis.** Confirm against TIS EWD if it must be named. |
| Trunk fuse box | Asserted absent | **Downgraded to "not documented for this VIN"** — check the cargo area on site. |

---

## Sources

- https://fixmycarinfo.com/…/Toyota-Rav4-XA50-2018-2021-–-Wiring-Diagrams.pdf (inaccessible — Cloudflare)
- https://www.youtube.com/watch?v=1Ic0Eb_s3UA — Simon Car Fixer
- https://www.youtube.com/watch?v=OMTHy6pHQvY — Auto User Guide
- https://www.autouserguide.com/toyota/fuse-diagrams-2022-toyota-rav4-fuses-and-relay-guide/
- `2021-RAV4-Owners-Manual.pdf` pp. 616–618 (authoritative for box locations)

Video metadata as retrieved is preserved in `video-frames/video1-metadata.json` and
`video-frames/video2-metadata.json`; storyboard contact sheets alongside them.

---

# 7. ADDENDUM — Toyota Service Manual obtained (2026-09-02)

A fourth source was supplied after the above was written: the **2021–2022 Toyota RAV4 Service
Manual**, 412 MB, delivered via Dropbox direct link. It downloaded cleanly in 31 seconds and carries
a **full text layer across 42,638 pages**. This is a TIS export and it supersedes every third-party
source in this folder for circuit-to-fuse assignments.

Key pages are extracted to `RAV4-SM-power-source-extract.pdf` (8 pages).

## 7a. Forward recognition camera — RESOLVED, and my earlier guess was wrong

**`ECU-IG1 NO. 3` FUSE.** Confirmed on two independent Pre-Collision System diagrams:

> **p. 7947** — *"\*1 FORWARD RECOGNITION CAMERA · \*2 MILLIMETER WAVE RADAR SENSOR ASSEMBLY ·
> \*3 INSTRUMENT PANEL JUNCTION BLOCK ASSEMBLY — **ECU-IG1 NO. 3 FUSE** · \*4 DLC3"*
> (System diagram, w/o Stop and Start System)

> **p. 38318** — same assignment, on the diagram covering both Gasoline and HV models, which also
> lists the Airbag Sensor Assembly and DLC3.

`ECU-IG1 NO.3` is **7.5A at position 14**.

**This overturns §4b.** The hypothesis there — `ECU-IG1 NO.4` (10A, pos. 33), inferred from a
third-party table's "anticollision system" wording — **was wrong**. The inference was reasonable
from the evidence available at the time, but it picked the wrong branch. Toyota's own diagram is
now the citable answer, and no inference is needed.

This is the practical difference the service manual makes: the earlier advice was "power all four
`ECU-IG1` branches because we cannot tell which". Now `ECU-IG1 NO.3` is named and citable. Powering
all four is still the efficient field move — three extra taps, zero doubt — but the report can name
the branch.

## 7b. Airbag control module — confirmed at the connector

**`A/BAG-IG2` FUSE**, corroborated four ways in the SM (pp. 19432, 20127, 37213, 38232) and, most
directly, at the module connector itself:

> **p. 37232** — *"G70-36 · IG2 · **A/BAG-IG2 fuse**"*

That same page carries the **full ACM connector pinout**, which is a better squib inventory than the
VIN decode. Circuits named include:

| Terminal | Circuit |
|---|---|
| G70-12/13 | DK−/DK+ — Lower No.1 instrument panel airbag (driver knee) |
| G70-28/29 | Front airbag sensor RH |
| G70-30/31 | Front airbag sensor LH |
| N21-7/8 | Curtain shield airbag LH |
| N21-15/16 | Front seat airbag LH |
| N21-25/26 | Front seat adjuster LH (seat position sensor) |
| N21-29/30 | Floor side airbag sensor LH |
| N21-31/32 | Side airbag pressure sensor LH |
| M15-1/2 | Curtain shield airbag RH |
| **M15-5/6** | **FCP+/FCP− — Front seat cushion airbag RH** |
| M15-9/10 | Front seat airbag RH |
| M15-25/26 | Side airbag pressure sensor RH |
| M15-27/28 | Floor side airbag sensor RH |

Note M15-5/6 independently confirms the **passenger seat cushion airbag** flagged from the VIN decode.

## 7c. Trunk fuse box — RESOLVED, there is none

Every junction and relay block named anywhere in the 42,638 pages was enumerated:

| Block | Present on this vehicle? |
|---|---|
| Instrument Panel Junction Block | ✅ |
| No.1 Engine Room Relay Block | ✅ |
| No.3 Relay Block | ✅ |
| HV Battery Junction Block | ❌ HV models only — part of the battery pack, not a cabin box |

A regex for any **luggage / rear / trunk** junction or relay block returns **zero hits**.

Combined with the owner's manual listing exactly three box locations, this closes §3. My original
statement was correct; the mid-research downgrade to "not documented" was over-cautious. Whatever
the Simon Car Fixer video shows in its "Trunk location" chapter, it is not a fuse box.

## 7d. Still not resolved: box positions

The service manual names fuses by **name**, never by box position — position maps live in the EWD and
on the physical lid. So the position-number caveat stands unchanged: **photograph the lid.** The
difference now is that it only matters for *locating* a fuse, not for *identifying* which one you
need.

## 7e. Provenance note

The file carries a `GetTheMANUALS.org` watermark, i.e. it is a redistributed copy of Toyota
copyrighted service literature rather than a TIS-licensed download. It was supplied by you and is
held here as a local working set only — it is gitignored along with the other third-party material
and is not pushed to the remote. If the fuse assignment needs to be cited in a filed report, cite
the equivalent TIS page from a licensed subscription rather than this copy.
