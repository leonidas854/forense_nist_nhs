#!/usr/bin/env python3
"""Comprueba la configuración actual de una VM, sin modificarla."""
import argparse
import re
import subprocess
import sys
from pathlib import Path


def audit(text):
    values = {}
    for line in text.splitlines():
        key, sep, value = line.partition('=')
        if sep:
            values[key.strip().strip('"')] = value.strip().strip('"')
    expected = {f'nic{i}': 'none' for i in range(1, 9)}
    expected.update(clipboard='disabled', clipboard_file_transfers='off',
                    draganddrop='disabled', vrde='off',
                    usb='off', ehci='off', xhci='off')
    problems = [f'{key}: {values.get(key, "ausente")} (esperado: {want})'
                for key, want in expected.items() if values.get(key) != want]
    problems.extend(f'Carpeta compartida: {value}' for key, value in values.items()
                    if re.match(r'SharedFolder(Name|Path)', key))
    return problems


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('vm', nargs='?', default='forense-nhs-win10')
    args = parser.parse_args()
    wrapper = Path(__file__).resolve().parent / 'vbox-lab.sh'
    result = subprocess.run(['bash', str(wrapper), 'showvminfo', args.vm, '--machinereadable'],
                            capture_output=True, text=True)
    if result.returncode:
        sys.exit(result.stderr.strip() or 'No se pudo consultar la VM')
    problems = audit(result.stdout)
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        sys.exit(1)
    print('OK: 8 NIC desactivadas; sin carpetas compartidas, clipboard, drag/drop, USB ni VRDE.')
    print('Verifica configuración de VirtualBox; no certifica ausencia de escapes del hipervisor.')
