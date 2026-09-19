#!/usr/bin/env bash
set -euo pipefail
if [ "$(id -u)" -ne 0 ]; then echo "Použij: sudo ./scripts/install-waydroid.sh"; exit 1; fi
apt-get update
apt-get install -y curl ca-certificates
curl -fsSL https://repo.waydro.id -o /tmp/waydroid-repo.sh
bash /tmp/waydroid-repo.sh
apt-get update
apt-get install -y waydroid
printf '\nWaydroid nainstalován. Inicializuj podle požadovaného image:\n  sudo waydroid init\n\n'
