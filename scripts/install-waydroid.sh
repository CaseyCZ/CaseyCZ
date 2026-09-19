#!/usr/bin/env bash
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "Použij: sudo ./scripts/install-waydroid.sh"
  exit 1
fi

apt-get update
apt-get install -y curl ca-certificates
curl -fsSL https://repo.waydro.id -o /tmp/waydroid-repo.sh
bash /tmp/waydroid-repo.sh
apt-get update
apt-get install -y waydroid

echo "Inicializuji Waydroid s GAPPS / Google Play…"
waydroid init -s GAPPS

printf '\nWaydroid + Google Play je inicializovaný.\n'
printf 'Při prvním spuštění může Google Play vyžadovat certifikaci zařízení.\n'
printf 'PiTV Store pak může otevřít YouTube, Spotify a Plex přímo v Google Play.\n\n'
