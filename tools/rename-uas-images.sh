#!/usr/bin/env bash
#
# rename-uas-images.sh - copy DJI imagery into the project naming convention.
#
# Originals are never modified or moved. Every file is copied byte-for-byte, so
# EXIF, XMP and DJI maker notes survive untouched, and a manifest records the
# mapping from the new name back to the camera's original.
#
# See docs/naming-convention.md

set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: rename-uas-images.sh SITE DATE FLIGHT SRC_DIR DEST_DIR

  SITE      3-6 char uppercase site code, e.g. HRBR01
  DATE      acquisition date, YYYYMMDD
  FLIGHT    flight id, F01..F99
  SRC_DIR   card dump for this one flight
  DEST_DIR  where to write the renamed copies (created if missing)

Produces:
  DEST_DIR/<SITE>_<DATE>_UAS_<FLIGHT>_<NNNN>.JPG   (+ .DNG where present)
  DEST_DIR/<SITE>_<DATE>_UAS_<FLIGHT>_manifest.csv

A JPEG and its RAW sibling always receive the same index. Images are ordered by
EXIF DateTimeOriginal when exiftool is installed, by filename otherwise.

Run once per flight: DJI restarts its counter at DJI_0001 on every flight, so
two flights sharing one folder will collide.
USAGE
}

case "${1:-}" in
  -h|--help) usage; exit 0 ;;
esac

if [ "$#" -ne 5 ]; then
  usage >&2
  exit 2
fi

site=$1
date=$2
flight=$3
src=$4
dest=$5

[[ $site   =~ ^[A-Z0-9]{3,6}$ ]] || { echo "error: SITE must be 3-6 uppercase alphanumerics, got '$site'" >&2; exit 2; }
[[ $date   =~ ^[0-9]{8}$ ]]      || { echo "error: DATE must be YYYYMMDD, got '$date'" >&2; exit 2; }
[[ $flight =~ ^F[0-9]{2}$ ]]     || { echo "error: FLIGHT must be F01..F99, got '$flight'" >&2; exit 2; }
[ -d "$src" ]                    || { echo "error: no such directory: $src" >&2; exit 2; }

mkdir -p "$dest"

prefix="${site}_${date}_UAS_${flight}"
manifest="${dest}/${prefix}_manifest.csv"

list=$(mktemp)
trap 'rm -f "$list"' EXIT

# Order by capture time where we can; DateTimeOriginal sorts lexicographically
# because exiftool formats it YYYY:MM:DD HH:MM:SS. Ties break on the path,
# which is also on the line.
if command -v exiftool >/dev/null 2>&1; then
  exiftool -q -q -m -f -ext jpg -ext jpeg \
           -p '$DateTimeOriginal|$Directory/$FileName' "$src" 2>/dev/null \
    | sort > "$list" || true
else
  echo "note: exiftool not found - ordering by filename instead of capture time" >&2
fi

if [ ! -s "$list" ]; then
  find "$src" -maxdepth 1 -type f \( -iname '*.jpg' -o -iname '*.jpeg' \) -print0 \
    | sort -z \
    | while IFS= read -r -d '' f; do printf 'unknown|%s\n' "$f"; done > "$list"
fi

printf 'new_filename,original_filename,capture_time\n' > "$manifest"

count=0
raws=0
while IFS='|' read -r ts path; do
  [ -n "${path:-}" ] || continue
  [ -f "$path" ] || continue

  count=$((count + 1))
  newbase=$(printf '%s_%04d' "$prefix" "$count")

  cp -- "$path" "${dest}/${newbase}.JPG"

  # Carry the RAW sibling across on the same index.
  for ext in DNG dng; do
    candidate="${path%.*}.${ext}"
    if [ -f "$candidate" ]; then
      cp -- "$candidate" "${dest}/${newbase}.DNG"
      raws=$((raws + 1))
      break
    fi
  done

  printf '%s,%s,%s\n' "${newbase}.JPG" "$(basename -- "$path")" "$ts" >> "$manifest"
done < "$list"

if [ "$count" -eq 0 ]; then
  echo "error: no JPEG images found in $src" >&2
  exit 1
fi

dng_total=$(find "$src" -maxdepth 1 -type f -iname '*.dng' | wc -l | tr -d '[:space:]')
if [ "$dng_total" -ne "$raws" ]; then
  echo "warning: $dng_total DNG(s) in source but $raws copied - some RAWs have no JPEG sibling" >&2
fi

echo "copied ${count} image(s) and ${raws} RAW(s) -> ${dest}"
echo "manifest: ${manifest}"
