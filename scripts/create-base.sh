#!/usr/bin/env bash
# Crea únicamente hardware vacío. No contiene ni distribuye Windows.
set -euo pipefail
cd "$(dirname "$0")/.."
base='forense-nhs-win10-base'
mkdir -p local/vms
if VBoxManage showvminfo "$base" >/dev/null 2>&1; then
  echo "Ya existe $base; no se modifica. Consulta docs/laboratorio.md." >&2
  exit 1
fi
VBoxManage createvm --name "$base" --ostype Windows10_64 --basefolder "$PWD/local/vms" --register
VBoxManage modifyvm "$base" --memory 4096 --cpus 2 --vram 128 --ioapic on --graphicscontroller vboxsvga --audio-enabled off --clipboard-mode disabled --drag-and-drop disabled --vrde off --usb-ohci off --usb-ehci off --usb-xhci off
for i in {1..8}; do VBoxManage modifyvm "$base" "--nic$i" none; done
VBoxManage createmedium disk --filename "$PWD/local/vms/$base/windows10.vdi" --size 65536 --format VDI
VBoxManage storagectl "$base" --name SATA --add sata --controller IntelAhci --portcount 3 --bootable on
VBoxManage storageattach "$base" --storagectl SATA --port 0 --device 0 --type hdd --medium "$PWD/local/vms/$base/windows10.vdi"
./lab package --base "$base" --output "$PWD/local/windows10-installer.box"
./lab box add --name nhs/windows10-installer "$PWD/local/windows10-installer.box"
python3 scripts/check_isolation.py "$base"
