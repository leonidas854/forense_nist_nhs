#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/lab-env.sh"
if [[ "${1:-}" == '--gui' ]]; then
    shift
    exec VirtualBox "$@"
fi
exec VBoxManage "$@"
