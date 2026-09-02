#!/usr/bin/env bash
# Re-fetch the third-party reference documents for VIN 2T3A1RFV8MC233488.
#
# These files are third-party copyrighted publications. They are deliberately NOT
# committed to this repository — this script reproduces the local working set instead.
# See README.md for what each file is and why the electrical wiring diagram is absent.
#
# Usage:  bash references/fetch-sources.sh

set -euo pipefail
cd "$(dirname "$0")"
mkdir -p fuse-box-diagrams

UA="Mozilla/5.0"

get() {
  local dest="$1" url="$2" referer="${3:-}"
  if [ -s "$dest" ]; then
    printf '  skip  %s (already present)\n' "$dest"
    return 0
  fi
  printf '  get   %s\n' "$dest"
  if [ -n "$referer" ]; then
    curl -fsSL -A "$UA" -e "$referer" -o "$dest" "$url"
  else
    curl -fsSL -A "$UA" -o "$dest" "$url"
  fi
}

echo "Toyota / Bosch documents:"
get "2021-RAV4-Owners-Manual.pdf" \
    "https://cdn.dealereprocess.org/cdn/servicemanuals/toyota/2021-rav4.pdf"
get "2021-RAV4-Quick-Reference-Guide.pdf" \
    "https://assets.sia.toyota.com/publications/en/om-s/OM21V1QRG/pdf/OM21V1QRG.pdf"
get "Bosch-CDR-v24.3-Vehicle-Coverage-List.pdf" \
    "https://cdr.boschdiagnostics.com/cdr/sites/default/files/CDR_v24.3_Vehicle_Coverage_List_R1_0_0.pdf"
get "Toyota-ERG-general.pdf" \
    "https://techinfo.toyota.com/techInfoPortal/staticcontent/en/techinfo/html/prelogin/erg/Toyota_ERG_printout.pdf"

echo "Fuse box layout images (third-party redraws, not Toyota lid art):"
FB="https://fuse-box.info/wp-content/uploads/2026/05"
get "fuse-box-diagrams/IJB-instrument-panel-diagram.png" \
    "$FB/Toyota-RAV4-XA50-2019-2025-in1-fuse-box-diagram.png" "https://fuse-box.info/"
get "fuse-box-diagrams/IJB-instrument-panel-location.png" \
    "$FB/Toyota-RAV4-XA50-2019-2025-in1_loc-fuse-box-location.png" "https://fuse-box.info/"
get "fuse-box-diagrams/ERJB1-engine-room-diagram.png" \
    "$FB/Toyota-RAV4-XA50-2019-2025-en1-fuse-box-diagram.png" "https://fuse-box.info/"
get "fuse-box-diagrams/ERJB1-engine-room-location.png" \
    "$FB/Toyota-RAV4-XA50-2019-2025-en1_loc-fuse-box-location.png" "https://fuse-box.info/"
get "fuse-box-diagrams/ERJB2-engine-room-2-diagram.png" \
    "$FB/Toyota-RAV4-XA50-2019-2025-en2-fuse-box-diagram.png" "https://fuse-box.info/"

echo
echo "Done. Not fetched (no legitimate free source):"
echo "  - XA50 Electrical Wiring Diagram, Power Source section"
echo "    Obtain via a short-term TIS subscription: https://techinfo.toyota.com"
