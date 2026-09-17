# Glossary

Every acronym and term used across these documents, grouped by topic rather than
alphabetised — related ideas explain each other. Use Ctrl-F for lookup.

Terms in **bold** inside a definition are defined elsewhere in this glossary.

---

## Core concepts

**Photogrammetry** — Measuring real objects from photographs. Find the same
point in several overlapping images taken from different positions, intersect
the lines of sight, and you get its 3D position. Everything drone-based here
rests on this.

**SfM — Structure from Motion** — The algorithm family that does the above
automatically. It works out both the scene's shape ("structure") and where each
photo was taken from ("motion"), simultaneously, from the photos alone.

**Bundle adjustment** — The big simultaneous solve at the heart of SfM. It
adjusts every camera position, every camera angle, the lens parameters and every
3D point at once, minimising total error. When people say a model "solved" or
"aligned," this is what ran. Most systematic errors in this document are
bundle-adjustment failures.

**Tie point** — A feature automatically recognised in two or more overlapping
photos, used to link them. Thousands of tie points are what the bundle
adjustment actually chews on. Low-texture surfaces like fresh asphalt yield few
tie points, which is why pavement is hard.

**Self-calibration** — Letting the bundle adjustment solve the lens's
characteristics (focal length, distortion) from the photos themselves, instead
of using a pre-measured calibration. Convenient, and the source of **doming**
when the flight geometry is poor.

**Reprojection error** — Take a solved 3D point, project it back into the photos
mathematically, and measure how far that lands from where the feature actually
appears. Reported in pixels. Under 1 px is healthy.

**TLS — Terrestrial Laser Scanning** — Ground-based laser scanning from a
tripod, e.g. a FARO Focus. Directly measures millions of distances. Far more
accurate than photogrammetry but cannot see roofs and cannot cover ground
quickly.

**LiDAR — Light Detection and Ranging** — Measuring distance with laser pulses.
TLS is one kind; there are also airborne and mobile kinds.

**Registration** — Aligning separate laser scans into one coordinate system, so
scan 7 and scan 8 agree about where a wall is. The scanning equivalent of
alignment.

---

## Error modes

**Doming / bowl effect** — A systematic vertical distortion where the model bows
up or sags in the middle, typically tens of centimetres. Caused by the bundle
adjustment being unable to separate lens distortion from flying height when all
photos point straight down. Fixed by **oblique** imagery and varied heights. The
single most important error mode in non-**RTK** drone mapping.

**Banana effect** — Doming's cousin on a **corridor**: error accumulates along
the corridor's length and the whole strip bends. Fixed by **cross-ties**, two
flight lines, and control at both ends.

**Ghosting** — Where a moving object appears duplicated and semi-transparent in
an **orthomosaic**, because it was in different places in the photos being
blended. Classic symptom of traffic in roadway mapping.

**Rolling shutter** — A camera that exposes the image sensor progressively, line
by line, rather than all at once. A moving aircraft therefore records a slightly
skewed frame. The Mavic 3 Classic is rolling-shutter only. **Global** or
**mechanical shutter** exposes everything at once and avoids this.

**Component (RealityCapture)** — A group of photos RealityCapture managed to
align together. Ideally your project is one component. Long corridors often
fragment into several that must be manually linked — the main corridor failure
mode in that software.

---

## Flight and camera

**UAS / UAV** — Unmanned Aircraft System / Vehicle. The drone, plus (for UAS)
its controller and pilot. Used interchangeably with "drone."

**AGL — Above Ground Level** — Altitude measured from the ground directly below.
The number that determines your **GSD**. Distinct from **AMSL — Above Mean Sea
Level**, measured from sea level.

**GSD — Ground Sample Distance** — How much real ground one pixel covers. At
1.63 cm GSD each pixel is 1.63 cm across. The single most useful number in a
flight plan: it sets what you can resolve and how big a **GCP** target must be.

**Nadir** — Straight down. A nadir photo is taken with the camera pointing
directly at the ground, **gimbal** at −90°.

**Oblique** — Any angled shot. Usually described in *degrees off nadir* (35° off
nadir) or as a *gimbal pitch* (−55°). The two conventions are easy to confuse —
these documents use gimbal pitch, where −90° is straight down and 0° is
horizontal.

**Gimbal** — The motorised mount that holds the camera steady and lets you set
its pitch angle. "Gimbal −55°" means tilted 55° below horizontal.

**Forward / front overlap** — How much consecutive photos along a flight line
share. 85% means each photo covers 85% of the previous one.

**Side / lateral overlap** — The same idea between adjacent parallel flight
lines.

**Footprint** — The rectangle of ground a single photo covers, in real units.

**Crosshatch / cross-grid** — Flying a second grid perpendicular to the first.
Improves geometry; not sufficient alone against doming.

**Cross-tie** — On a corridor, a short perpendicular flight across the corridor
at intervals, tying the parallel longitudinal lines together.

**Corridor** — A long, narrow survey area: road, rail, pipeline, powerline.
Geometrically weak in the long direction, hence the special handling.

**Orbit** — Circling a structure while keeping the camera pointed at it. How you
capture a bridge pier or sign structure properly.

**VLOS / BVLOS** — Visual Line of Sight / Beyond. Part 107 requires you to keep
the aircraft in unaided sight. The binding constraint on corridor work.

**Part 107** — The FAA regulation governing commercial small-drone operation in
the US. Caps you at 400 ft **AGL**, with an exception near tall structures.

**ROW — Right of Way** — The public land corridor a road occupies, wider than
the pavement. Your survey should extend past it.

**AOI — Area of Interest** — The specific sub-area that matters most, warranting
lower, denser capture.

**ISO** — The camera's sensitivity to light. Higher ISO allows a faster shutter
in dim conditions but adds noise, which degrades feature matching. Keep it low.

**WB — White Balance** — The camera's interpretation of what colour "white" is
under the current light. Set it manually and lock it: if it drifts between
frames, the texture blends with visible colour seams.

**MP — Megapixel** — A million pixels. The Mavic 3 Classic's camera is 20 MP
(5280 × 3956).

**CPL — Circular Polarising filter** — Cuts glare, but its effect changes with
aircraft heading, so the same surface looks different on opposing flight lines.
Bad for photogrammetry. **ND — Neutral Density** filters just reduce light
evenly and are fine.

---

## Ground control

**GCP — Ground Control Point** — A marked, surveyed point on the ground, visible
in your photos, whose real coordinates you know. Feeding these into the bundle
adjustment anchors the model and corrects internal deformation. The mechanism
that ties drone data to scan data.

**Check point** — A surveyed point deliberately *withheld* from the solve, used
afterwards to measure true accuracy. Without check points you have no accuracy
number, only residuals.

**Residual** — How far the solve's answer for a point sits from its measured
position. Control point residuals measure fit; **check point** residuals measure
accuracy. Not the same thing.

**RMSE — Root Mean Square Error** — The standard way to summarise a set of
errors into one number. Check point RMSE is the accuracy figure you report.

**GNSS — Global Navigation Satellite System** — The general term for satellite
positioning. **GPS** is the American one; GNSS covers GPS, GLONASS, Galileo and
BeiDou together.

**RTK — Real-Time Kinematic** — A GNSS technique using a fixed base station to
correct the rover in real time, giving centimetre accuracy instead of metres.
**The Mavic 3 Classic does not have it** — the reason GCPs are mandatory here.

**PPK — Post-Processed Kinematic** — Same accuracy, corrections applied
afterwards rather than live.

**Geoid / ellipsoid** — Two different models of "sea level." GNSS natively
measures height above a mathematical **ellipsoid**; surveys usually want height
above the **geoid** (gravity-based, closer to true sea level). Mixing them
silently offsets your heights by metres.

**CRS — Coordinate Reference System** — The definition of what your coordinates
mean. **EPSG** codes (e.g. EPSG:6428) name specific ones. **UTM** and **State
Plane** are common projected systems.

**Scale bar** — An object of precisely known length placed in the scene, giving
the model absolute scale without full survey control.

**ICP — Iterative Closest Point** — An algorithm that aligns two point clouds by
repeatedly nudging one toward the other. Can only apply a rigid transform, so it
cannot undo **doming**.

---

## Data products

**Point cloud** — Millions of individual 3D points. The raw output of scanning
and of dense photogrammetric matching.

**Sparse cloud** — The initial thin cloud of **tie points** from alignment.
**Dense cloud** — the full-resolution result of dense matching afterwards.

**Structured / ordered point cloud** — A scan cloud that retains its original
grid arrangement and the scanner's position. **Unstructured** clouds have been
flattened to an anonymous list of points, losing information that downstream
tools could have used.

**Intensity** — How strongly each laser point reflected. Gives scans a
greyscale, material-dependent appearance independent of photographic colour.

**Normal** — The direction a surface faces at a given point. Needed for meshing
and lighting; computed more reliably from **structured** clouds.

**Mesh** — A surface of connected triangles, as opposed to loose points. What
you texture and render.

**Texture** — The photographic imagery wrapped onto a mesh.

**Decimation** — Deliberately reducing point or triangle count for
manageability. `DEC01` in these documents means decimated to 1 cm spacing.

**Orthomosaic** — Many aerial photos corrected for perspective and terrain, then
blended into a single map-accurate image you can measure directly. A **true
ortho** additionally corrects building and structure lean.

**DEM / DSM / DTM** — Digital Elevation / Surface / Terrain Model. **DSM**
includes everything (trees, buildings); **DTM** is bare ground with objects
removed; **DEM** is the generic term.

**3DGS / Gaussian splatting** — A recent technique representing a scene as
millions of soft coloured blobs rather than triangles. Photoreal, handles
vegetation well, but not reliably measurable. For looking at, not measuring.

**UE5 — Unreal Engine 5** — Epic's real-time 3D engine, used here to present
large reality-capture meshes interactively. **Twinmotion** is Epic's simpler
visualisation tool built on the same technology.

**Nanite** — Unreal Engine 5's system for rendering extremely high-polygon
meshes efficiently, letting you drop in a full-resolution scan mesh without
manual decimation.

**3D Tiles / Potree** — Formats for streaming huge point clouds and meshes into
a web browser progressively. How you hand a dataset to someone without
specialist software.

---

## File formats

**E57** — Open, standardised (**ASTM** E2807) point cloud exchange format. Holds
multiple scans with their positions, colour and **intensity**. The recommended
export from FARO Scene.

**LAS / LAZ** — The LiDAR industry standard. **LAZ** is the compressed version.
Universal, compact, but discards scan structure.

**FLS / LSPROJ** — FARO's native scan and project files.

**PTX / PTS** — Older plain-text point cloud formats. PTX keeps structure; both
are enormous.

**RCP / RCS** — Autodesk ReCap's formats, for Revit/Navisworks/Civil 3D.

**POD** — Bentley Pointools' point cloud format, for Bentley pipelines.

**XYZ** — Bare coordinate text. Loses everything else.

**ASCII** — Plain readable text, as opposed to binary. ASCII point cloud formats
(**PTS**, **PTX**, **XYZ**) are human-readable but many times larger and slower
to load than binary equivalents.

**DNG** — Adobe's RAW image format, what the Mavic writes alongside JPEG.
Unprocessed sensor data, maximum editing latitude, large files.

**EXIF** — Metadata embedded in an image file: camera settings, timestamp, GPS
position. Photogrammetry software reads it, so preserve it when renaming.

---

## Standards and organisations

**USIBD** — US Institute of Building Documentation. Publishes the **LOA**
specification.

**LOA — Level of Accuracy** — USIBD's five-tier framework (LOA10 ≈ 50 mm through
LOA50 ≈ 0.1 mm) for stating how accurate a documentation deliverable is. Quoted
at 2σ (95% confidence).

**2σ / 95% confidence** — A statistical statement that 95% of measurements fall
within the quoted range. Not a best case — a guarantee band.

**ASTM** — Standards body; publishes the **E57** specification as E2807.

**DOT** — Department of Transportation. **TxDOT**, **SCDOT**, **VDOT**, **TDOT**
are the Texas, South Carolina, Virginia and Tennessee agencies, several of which
publish UAS survey specifications. **FHWA** is the Federal Highway
Administration.

**Historic England** — UK heritage body whose *Geospatial Survey Specifications
for Cultural Heritage* (HEAG317) is a widely used survey specification.

---

## Software

**FARO Scene** — FARO's software for processing and registering laser scans.

**RealityCapture / RealityScan** — Epic's photogrammetry package. Strong at
dense reconstruction and at combining photos with laser scans. Free below $1M
annual revenue.

**Pix4D** — Photogrammetry suite. **PIX4Dmapper** is the long-standing desktop
product; **PIX4Dmatic** is the newer one built for large and linear projects.

**Agisoft Metashape** — Another major photogrammetry package; handles laser
scans from version 2.x.

**CloudCompare** — Free point cloud comparison and editing tool. **C2C** (cloud
to cloud) and **M3C2** are its distance-measurement methods; M3C2 is the
statistically rigorous one.

**Postshot** — Tool for training **3DGS** splats, able to import camera
positions from RealityCapture.

**exiftool** — Command-line utility for reading and writing **EXIF** metadata.
