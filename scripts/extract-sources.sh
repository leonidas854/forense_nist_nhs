#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p fuentes/textos
for source in fuentes/*.pdf; do
  name="$(basename "$source" .pdf)"
  pdftotext -layout "$source" "fuentes/textos/$name.txt"
done
