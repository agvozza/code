#!/bin/sh
# Reassembles "Toyota TechStream & CDR 900.pdf", which is split here because
# the original 194.9 MB file exceeds GitHub's 100 MB per-file limit.
#
# Usage: sh rejoin.sh [output-directory]     (defaults to the parent directory)
set -e

name='Toyota TechStream & CDR 900.pdf'
dir=$(dirname "$0")
out=${1:-$dir/..}

cat "$dir/$name".part[0-9][0-9] > "$out/$name"

if command -v sha256sum >/dev/null 2>&1; then
    expected=$(cut -d' ' -f1 < "$dir/sha256sum.txt")
    actual=$(sha256sum < "$out/$name" | cut -d' ' -f1)
elif command -v shasum >/dev/null 2>&1; then
    expected=$(cut -d' ' -f1 < "$dir/sha256sum.txt")
    actual=$(shasum -a 256 < "$out/$name" | cut -d' ' -f1)
else
    echo "Wrote $out/$name (no sha256 tool found, checksum not verified)"
    exit 0
fi

if [ "$expected" = "$actual" ]; then
    echo "Wrote $out/$name (sha256 verified)"
else
    echo "Checksum mismatch for $out/$name" >&2
    echo "  expected $expected" >&2
    echo "  actual   $actual" >&2
    exit 1
fi
