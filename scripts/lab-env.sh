#!/usr/bin/env bash
# Registro privado del proyecto: no heredar comparticiones globales del usuario.
LAB_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export VBOX_USER_HOME="$LAB_ROOT/local/virtualbox"
# Linux: separar también el servidor IPC; VBOX_USER_HOME solo puede reutilizar
# un VBoxSVC ya iniciado con la configuración habitual del usuario.
LAB_REGISTRY_ID="$(printf '%s' "$LAB_ROOT" | sha256sum | cut -c1-12)"
export VBOX_IPC_SOCKETID="$(id -un)-nhs-$LAB_REGISTRY_ID"
export VAGRANT_EXPERIMENTAL=none_communicator
mkdir -p "$VBOX_USER_HOME"
