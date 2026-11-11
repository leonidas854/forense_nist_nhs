#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p fuentes descargas
fetch() {
  local target="$1" digest="$2" url="$3"
  if [ -f "$target" ] && printf "%s  %s\n" "$digest" "$target" | sha256sum --check --status; then
    echo "Verificado: $target"; return
  fi
  curl --fail --location --proto "=https" --proto-redir "=https" --retry 2 --connect-timeout 30 --max-time 1800 --output "$target.part" "$url"
  printf "%s  %s\n" "$digest" "$target.part" | sha256sum --check
  mv "$target.part" "$target"
}
fetch fuentes/NIST.CSWP.29.pdf 3c31f46fee98cac0c4323453e5109291a213b4de7fef8c058af9bf67f717433c https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf
fetch fuentes/NIST.IR.8374r1.pdf f32db66cfa000a8986b9c0f0b58b6e0f6bf825ce252b3b0c5757d75c0131fddf https://nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8374r1.pdf
fetch fuentes/NIST.SP.800-61r3.pdf e5593d6bb85daecec7e8d9549400c7b3473bcc3f06e469c82218073afa7fba2d https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
fetch fuentes/NAO-WannaCry-NHS.pdf 34e516b2e22d456f3adf8ed303eb9929161dee3ce6bf1958b10d9633da2c24e4 https://www.nao.org.uk/wp-content/uploads/2017/10/Investigation-WannaCry-cyber-attack-and-the-NHS.pdf
fetch fuentes/NHS-lessons-learned-2018.pdf 47087f5d192c74d9785b653ba74ce6926bff049a23984725dbdfb5f8aac62f3c https://www.england.nhs.uk/aac/wp-content/uploads/2018/02/lessons-learned-review-wannacry-ransomware-cyber-attack-cio-review.pdf
fetch descargas/SysinternalsSuite.zip e7f49d1f4477e416b3051636dc44929b20ae025b46a1ee4cd8c1f1e869af6ae6 https://download.sysinternals.com/files/SysinternalsSuite.zip
fetch descargas/ghidra_12.2_PUBLIC_20261016.zip 2c2cd776db3c1f6a097ba418922378ac3649cadd5e844a6f5f088ae628a7be67 https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.2_build/ghidra_12.2_PUBLIC_20261016.zip
fetch descargas/Wireshark-4.6.9-x64.exe bf9b5ce8a89f244c376a9b1a946276eaa06463dde3e33069a34d7f102f5878cf https://2.na.dl.wireshark.org/win64/Wireshark-4.6.9-x64.exe
fetch descargas/floss-v3.2.0-windows.zip c0c73bb99d043fedd8e913038b65d1591fd6308cd938d8a91df87b733b369af5 https://github.com/mandiant/flare-floss/releases/download/v3.2.0/floss-v3.2.0-windows.zip
fetch descargas/OpenJDK25U-jdk_x64_windows_hotspot_25.0.5_8.zip 636bdc13dc649ddc7d5921c5c7d23cca6e44fd19d662b45cc9c02135a6c96c42 https://github.com/adoptium/temurin25-binaries/releases/download/jdk-25.0.5%2B8/OpenJDK25U-jdk_x64_windows_hotspot_25.0.5_8.zip
fetch descargas/winpmem_mini_x64_rc2.exe a4d516b6fcaf3b5b1d4ee709ce86f8eabf1d8028b3a83101479b7568b933d21b https://github.com/Velocidex/WinPmem/releases/download/v4.0.rc1/winpmem_mini_x64_rc2.exe
if [ ! -d descargas/volatility3/.git ]; then
  git clone --depth 1 --branch v2.28.2 https://github.com/volatilityfoundation/volatility3.git descargas/volatility3
fi
test "$(git -C descargas/volatility3 rev-parse HEAD)" = "881e970121c16f0932fb9d16fbd5fb258cbcbf75"
sha256sum -c config/SHA256SUMS
