# #483 RTK video: who and what he cites

Video: **"ESP32 precision GPS receiver (incl. RTK-GPS Tutorial). How to earn money with it (DePIN)"** by Andreas Spiess. Main channel, uploaded 2024-05-05, 22:18 long, about 1.05M views. Full transcript: [`transcripts/main-483-Oc1LBFDj2MA.md`](transcripts/main-483-Oc1LBFDj2MA.md).

**Short answer:** he cites **no other YouTubers and no academic papers**. He cites **one book**, **one industry report**, **four people or organisations** (three of whom are named only through links), plus **two of his own earlier videos**. Each one is researched below.

## What he cites

| # | Reference | How it appears | Type |
|---|---|---|---|
| 1 | *You Are Here*, Hiawatha Bray | Said aloud ("I strongly suggest reading or listening to 'You Are Here'"), and it's the "Book about navigation" link | Book |
| 2 | Michael Ammann (`mazgch`) | "When I got this board from Michael, a viewer…", plus the `github.com/mazgch/hpg` link | Person / project |
| 3 | Onocoy's president, "one of the founders of u-blox, a no-nonsense guy also with a Swiss accent" | Said aloud; not named | Person |
| 4 | EUSPA EO & GNSS Market Report 2022 | Description link only | Industry report |
| 5 | SimeonOnSecurity | Description link (base-station guide) | Blogger / guide author |
| 6 | `incarvr6` (esp32-ntrip-DUO) | Description link | Open-source developer |
| 7 | His **Helium video** (#384) | "People who watched my Helium video know that I was not happy about this company" | Own video |
| 8 | His **GPS timing video** (#336) | "I made a video on how you can use this precise timing for cheap in your lab" | Own video |

Companies he mentions only in passing: Garmin (his first GPS in 1995), u-blox (corrections service), SparkFun (receivers and libraries), Helium, RTK2GO and Onocoy. He also uses an Aaronia **Spectran** SDR to show that GPS signals sit below the noise floor.

---

## 1. Book: *You Are Here: From the Compass to GPS, the History and Future of How We Find Ourselves*
- **Author:** Hiawatha Bray, technology writer at the *Boston Globe*. He got curious about the GPS in his own phone and wrote the book from that.
- **Publisher:** Basic Books, 2014. About 272 pages, ISBN 9780465080984. Spiess's affiliate link goes to the **audiobook** edition.
- **Contents:** Navigation history from Polynesian stick charts and the compass, through radio navigation (LORAN, Decca), inertial navigation, and the Transit/TIMATION programmes that led to **GPS**. The second half covers phone location tracking and its **privacy** implications.
- **Reception:** *Scientific American* reviewed it. An RF-navigation blogger (Aether Czar) called it "a masterful history" that strikes a middle course between technical depth and accessibility, and singled out the radio-navigation chapter.
- **Why he recommends it:** It's the "how it all began" backstory for the history chapter (1:46–2:39).
- Sources: [Scientific American review](https://www.scientificamerican.com/article/book-review-you-are-here-from-the-compass-to-gps-the-history-and-future-of-how-we-find-ourselves), [Aether Czar review](https://aetherczar.com/review-you-are-here-hiawatha-bray/), [Bookshare listing](https://bookshare.org/browse/book/4063865)

## 2. Michael Ammann (GitHub `mazgch`)
- His GitHub profile says **Michael Ammann, u-blox AG, Switzerland**, so the "viewer" who sent the board is a u-blox insider.
- **The board** is his **HPG solution** ([mazgch/hpg](https://github.com/mazgch/hpg)): a NINA-W106 (ESP32) with a ZED-F9R (L1/L2 RTK plus dead reckoning), NEO-D9S (L-band satellite corrections), LARA-R6 (LTE) and an ANN-MB antenna. It's Arduino firmware with a captive portal, SD logging and a web monitor. It takes corrections over WiFi (NTRIP), LTE or satellite, which matches the transmission methods 2, 3 and 4 in the video. u-blox later productised it as the **XPLR-HPG-2**.
- His other repos are forks of the SparkFun u-blox GNSS and SARA-R5 Arduino libraries and u-blox's `ubxlib`, so he works on the bridge between u-blox and SparkFun.
- Whether he's related to Daniel Ammann (#3) is **not established**. The surname is shared, but nothing found connects them.

## 3. Onocoy's president: Daniel Ammann
- **Who:** co-founder of **u-blox** in 1997 (with fellow ETH Zürich people, including Andreas Thiel and Jean-Pierre Wyss). He has an ETH Zürich electrical-engineering degree and was a research assistant there. He ran u-blox's positioning business and sat on its Executive Committee until **January 2019**.
- **Now:** **President of the onocoy association**, which he co-founded with **Thomas Nigg**, a former u-blox sales and marketing executive. Dealroom dates the founding to 2021 and MarketScreener to 2022. He is also **Chairman of Fixposition AG**, an ETH spin-off making GNSS + visual-inertial positioning sensors. He spoke at ION Alberta (May 2023) on onocoy as "scalable correction services by leveraging web3 methods."
- **Why it matters to Spiess:** it's the credibility argument. Unlike Helium, Onocoy is run by GNSS-industry veterans, lets makers build their own hardware ("do not sell overpriced miners"), and sells into an existing paid market for correction data.
- Sources: [GPS World author page](https://www.gpsworld.com/author/daniel-ammann), [MarketScreener](https://ch.marketscreener.com/insider/DANIEL-AMMANN-A0G1LT/), [Dealroom: onocoy](https://app.dealroom.co/companies/onocoy), [Startupticker: Fixposition](https://www.startupticker.ch/en/news/fixposition-plans-global-expansion-with-seed-funds), [ION Alberta 2023](https://alberta.ion.org/2023/05/23/ion-alberta-virtual-meeting-tuesday-may-23-2023/), [Netzwoche 2019](https://www.netzwoche.ch/news/2019-01-15/chiphersteller-u-blox-baut-management-um)

## 4. EUSPA EO and GNSS Market Report, 2022 (Issue 1)
- **Publisher:** EU Agency for the Space Programme (EUSPA, formerly GSA). It's the first combined Earth Observation + GNSS edition and covers 17 market segments. [PDF](https://www.euspa.europa.eu/sites/default/files/uploads/euspa_market_report_2022.pdf) (54 MB)
- **Key numbers** (from the report text):
  - GNSS + EO downstream revenues crossed **€200 bn in 2021** and are set to reach about **€500 bn by 2031**.
  - GNSS **installed base** goes from **6.5 bn devices (2021) to 10.6 bn (2031)**. Annual shipments grow from 1.8 bn to 2.5 bn units.
  - **Augmentation services** (corrections, i.e. the market Onocoy and RTK2GO sit in) grow about **7 %/yr, from €25 bn (2021) to about €51 bn (2031)**.
  - Added-value services grow from €126 bn to €354 bn. Services overall reach €405 bn, over 82 % of GNSS revenue by 2031.
  - Galileo was already in over 30 % of receiver models. The trend is toward multi-frequency receivers and Galileo's free **High Accuracy Service (HAS)**.
- **Why he cites it:** it backs up his claim that "selling RTK correction data seems to be a multi-million-dollar business already now." In fact the report puts augmentation in the **tens of billions of euros**.

## 5. SimeonOnSecurity
- He wrote the linked guide, *Budget DIY GPS/GNSS Base Station with ESP32 and UM980*, which is the build Spiess followed.
- It's a prolific security and homelab blog that publishes a lot on **GNSS DePIN "mining"** (Onocoy, RTKDirect, Geodnet, "quadruple mining"), with mirrors on Hackster, Instructables, Hackaday.io and dev.to. He maintains [`docker-rtklib-onocoy-rtkdirect`](https://github.com/simeononsecurity/docker-rtklib-onocoy-rtkdirect).
- The site doesn't clearly identify the person behind it. Some guides include affiliate or discount codes for gnss.store, so treat the hardware recommendations with that in mind.
- Guide: [simeononsecurity.com](https://simeononsecurity.com/guides/budget-diy-gps-gnss-base-station-setup-esp32-um980/)

## 6. incarvr6: `esp32-ntrip-DUO`
- Spiess's "Base software for t[wo] services" (his setup feeds **Onocoy and RTK2GO** at the same time).
- It's a fork of `MichaelEFlip/esp32-xbee-1`, which comes from `nebkat/esp32-xbee`. It runs two NTRIP servers simultaneously. Prebuilt for ESP32/S2/S3/C3, flashed through web.esphome.io, built on ESP-IDF 5.4. About 74 stars and still a work in progress.
- There's no public identity for the author. Repo: [github.com/incarvr6/esp32-ntrip-DUO](https://github.com/incarvr6/esp32-ntrip-DUO)

## 7. His own Helium video: #384 "LoRaWAN + Cryptocurrency Miner = Helium. A good idea?" (2021-05-23)
- https://youtu.be/nerQCrOam5U. He built a hotspot (RAK concentrator + Pi 4) and was sceptical because there was "no real business behind transferring LoRa messages."
- In the description he linked a critical piece: Tamas Szabo's Medium article *"Why the Helium network is one of the most centralized and most overvalued cryptocurrency"*. Helium's own docs note the network later migrated to Solana (April 2023).
- In #483 he reuses this as his DePIN yardstick. DePIN means replacing venture investors with token-paid crowd infrastructure, and it's only worth it with a real paying market behind it. He judges that RTK corrections have one.

## 8. His own GPS timing video: #336 "How to get Precise Timing and Frequency to our Lab… GPSDO, BG7TBL" (2020-05-31)
- https://youtu.be/a393cqhdZpM. Full transcript in `transcripts/main-336-a393cqhdZpM.md`.
- Walks the ladder from crystal (about 10⁻⁵) to TCXO (0.5 ppm) to OCXO (±5 ppb) to **GPSDO** (approaching 10⁻¹¹, rubidium-class, for about $235). Chinese BG7TBL GPSDOs reuse **second-hand cell-tower OCXOs** (CTS). Leo Bodnar's GPSDO is programmable with square-wave outputs. Trick: a u-blox NEO-6/7/8 `TIMEPULSE` pin, set through u-center CFG-TP5, outputs up to 24 MHz GPS-locked. This is the background for his "GPS synchronizes most of our clocks… jamming is a major threat" remark.

---

## Expert notes: where the video simplifies or slips
These come from my GNSS knowledge rather than a single source, and are worth knowing if you use the video as a teaching reference.

1. **Selective Availability ended on 2 May 2000** by presidential order, not "after the Gulf War" (1991). The ~100 m accuracy he remembers from 1995 was due to SA.
2. **Correlation peak width:** one C/A chip is about **1 µs, roughly 300 m**. He says "about 1 ns or 30 meters", which is internally inconsistent (1 ns is about 30 cm). Receivers then resolve the peak to a small fraction of a chip.
3. **Satellite positions come from the ephemeris**, not the almanac. The almanac is coarse data for all satellites (a full set takes about 12.5 min at 50 bps). The ephemeris is each satellite's precise orbit (about 30 s, refreshed every 2 h). The backup battery keeps both, plus time.
4. **RTK baseline:** he says less than 20 km. Many references use 10–35 km depending on ionosphere and receiver. Multi-band helps.
5. **u-blox satellite service (PointPerfect, SSR/PPP-RTK):** he says "below one meter". u-blox markets it as **a few centimetres after convergence** in covered regions. That isn't instant RTK-fixed, but it's far better than sub-meter.
6. **Cost claims (2024):** his DIY base was under $300, versus about $700 for an Onocoy-approved miner and "thousands" for commercial stations. Prices and Onocoy rewards (ONO token since July 2025) have moved since.
