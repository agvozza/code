#!/usr/bin/env python3
"""Flight parameter calculator for corridor and area photogrammetry missions.

Given an altitude and an overlap spec, computes GSD, image footprint, flight
line spacing, trigger distance, the maximum ground speed that still holds the
requested forward overlap at a given shutter interval, and image count per mile
of corridor.

Defaults are the DJI Mavic 3 Classic (Hasselblad L2D-20c). See
docs/roadway-uas-flight.md for how these numbers are used.

    tools/flight-calc.py                        # default roadway altitude ladder
    tools/flight-calc.py --alt-ft 400 200 100 50
    tools/flight-calc.py --alt-m 120 60 30 --front 80 --side 70
    tools/flight-calc.py --alt-ft 120 --interval 5      # RAW interval
"""

import argparse
import sys

FT_PER_M = 3.280839895

# sensor_w_mm, image_w_px, image_h_px, focal_mm
CAMERAS = {
    "mavic3classic": (17.3, 5280, 3956, 12.29),   # 4/3 CMOS, 24mm equiv
    "mavic3e":       (17.3, 5280, 3956, 12.29),   # same optic, mechanical shutter
    "mini4pro":      (9.6,  8064, 6048, 6.7),
}


def compute(alt_m, cam, front, side, interval):
    sensor_w, img_w, img_h, focal = cam
    pitch_mm = sensor_w / img_w
    # pitch_mm / focal_mm is dimensionless, so this is already metres/pixel.
    gsd = pitch_mm / focal * alt_m                    # metres/pixel

    fp_w = img_w * gsd                                # across-track, metres
    fp_h = img_h * gsd                                # along-track, metres

    advance = fp_h * (1.0 - front / 100.0)            # metres between shots
    spacing = fp_w * (1.0 - side / 100.0)             # metres between lines
    max_speed = advance / interval if interval > 0 else float("inf")

    return {
        "alt_m": alt_m,
        "alt_ft": alt_m * FT_PER_M,
        "gsd_cm": gsd * 100.0,
        "gsd_in": gsd * 39.3701,
        "fp_w_m": fp_w,
        "fp_w_ft": fp_w * FT_PER_M,
        "fp_h_m": fp_h,
        "fp_h_ft": fp_h * FT_PER_M,
        "advance_m": advance,
        "advance_ft": advance * FT_PER_M,
        "spacing_m": spacing,
        "spacing_ft": spacing * FT_PER_M,
        "max_speed_ms": max_speed,
        "max_speed_mph": max_speed * 2.236936,
        "img_per_mile_per_line": 1609.344 / advance,
    }


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Photogrammetry flight parameter calculator.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("\n\n", 1)[1],
    )
    g = p.add_mutually_exclusive_group()
    g.add_argument("--alt-ft", nargs="+", type=float, help="altitude(s) AGL in feet")
    g.add_argument("--alt-m", nargs="+", type=float, help="altitude(s) AGL in metres")
    p.add_argument("--front", type=float, default=85.0,
                   help="forward overlap %%; Pix4D corridor spec is 85 (default: %(default)s)")
    p.add_argument("--side", type=float, default=60.0,
                   help="side overlap %%; Pix4D corridor spec is 60 (default: %(default)s)")
    p.add_argument("--interval", type=float, default=2.0,
                   help="shutter interval in seconds (default: %(default)s)")
    p.add_argument("--camera", default="mavic3classic", choices=sorted(CAMERAS),
                   help="camera preset (default: %(default)s)")
    p.add_argument("--lines", type=int, default=2,
                   help="flight lines across the corridor, for image counts (default: %(default)s)")
    p.add_argument("--units", choices=("ft", "m", "both"), default="both")
    a = p.parse_args(argv)

    for name, val in (("--front", a.front), ("--side", a.side)):
        if not 0 <= val < 100:
            p.error(f"{name} must be in [0, 100), got {val}")
    if a.interval <= 0:
        p.error(f"--interval must be positive, got {a.interval}")
    if a.lines < 1:
        p.error(f"--lines must be at least 1, got {a.lines}")

    if a.alt_m:
        alts = a.alt_m
    elif a.alt_ft:
        alts = [v / FT_PER_M for v in a.alt_ft]
    else:
        alts = [v / FT_PER_M for v in (400, 200, 100, 50)]
    if any(v <= 0 for v in alts):
        p.error("altitudes must be positive")

    cam = CAMERAS[a.camera]
    rows = [compute(v, cam, a.front, a.side, a.interval) for v in alts]

    print(f"camera {a.camera}   overlap {a.front:g}% fwd / {a.side:g}% side   "
          f"interval {a.interval:g}s   {a.lines} line(s)")
    print()
    hdr = (f"{'AGL':>12}  {'GSD':>13}  {'footprint W':>15}  "
           f"{'line spacing':>15}  {'shot every':>14}  {'max speed':>14}  {'img/mi':>7}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        alt = f"{r['alt_ft']:.0f} ft/{r['alt_m']:.0f} m"
        gsd = f"{r['gsd_cm']:.2f} cm/{r['gsd_in']:.2f} in"
        fpw = f"{r['fp_w_ft']:.0f} ft/{r['fp_w_m']:.0f} m"
        spc = f"{r['spacing_ft']:.0f} ft/{r['spacing_m']:.0f} m"
        adv = f"{r['advance_ft']:.0f} ft/{r['advance_m']:.0f} m"
        spd = f"{r['max_speed_ms']:.1f} m/s"
        n = r["img_per_mile_per_line"] * a.lines
        print(f"{alt:>12}  {gsd:>13}  {fpw:>15}  {spc:>15}  {adv:>14}  {spd:>14}  {n:>7.0f}")

    print()
    print("max speed is the fastest you can fly and still hold the requested forward")
    print("overlap at the given interval. Flying faster silently thins your overlap.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
