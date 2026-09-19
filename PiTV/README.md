# PiTV 1.0

PiTV is a lightweight TV shell for **Ubuntu Server ARM64 on Raspberry Pi 4**. The Raspberry Pi stays a 24/7 server while HDMI shows a remote-friendly launcher.

## What is included

- fullscreen PiTV launcher, CaseyCZ/iOS Hub visual style
- lightweight **labwc Wayland compositor** (no GNOME/Ubuntu Desktop)
- HDMI-CEC remote: arrows, OK, Back, Home, TV power, active source, volume, mute
- 24/7 screensaver with moving clock, black screen and optional CEC TV standby
- Ethernet status + Wi-Fi scan/connect/disconnect through NetworkManager
- HDMI-only audio model for Raspberry Pi 4 (HDMI 1/2)
- Linux apps (Kodi etc.) from `/etc/pitv/apps.d/*.json`
- APK Inspector using `aapt` / `apktool`
- APK discovery from `/var/lib/pitv/apks/` and `~/PiTV/APKs/`
- Waydroid backend: install APK, launch Android app, full Android UI
- application visibility settings
- system health, temperature, RAM, disk, uptime and APT updates
- restart/power-off confirmations
- Tailscale status shown in About; Tailscale itself stays a background service
- SSH remains the maintenance/admin path

## Install

Ubuntu Server 24.04 ARM64 is the primary target.

```bash
unzip PiTV-v1.0.zip
cd PiTV-v1.0
sudo ./install.sh
sudo reboot
```

After boot: `tty1 -> autologin pitv -> dbus -> labwc -> PiTV`. SSH is unchanged.

## Kodi

```bash
sudo apt install kodi
```

`config/apps.d/kodi.json` is already included; PiTV shows the tile when Kodi is installed.

## APK

Copy APK files over SSH/SFTP/Tailscale:

```bash
sudo cp SmartTube.apk /var/lib/pitv/apks/
sudo chown pitv:pitv /var/lib/pitv/apks/SmartTube.apk
```

PiTV reads package name, label, launchable activity, SDK and Leanback/TV hints with `aapt`, then creates the launcher tile automatically.

### Waydroid

Waydroid is optional because PiTV also works as a pure Linux TV shell. To add the Android backend:

```bash
sudo ./scripts/install-waydroid.sh
sudo waydroid init
```

Then restart PiTV/Raspberry Pi. Selecting an APK tile installs it with `waydroid app install` when needed and launches the package. HOME on the CEC remote stops the foreground session and returns to PiTV.

> Raspberry Pi / Waydroid hardware compatibility still has to be verified on the exact Pi 4 image/kernel. PiTV detects a missing backend instead of failing the launcher.

## Settings

- Appearance
- Screensaver
- Network / Wi-Fi
- HDMI audio
- HDMI / CEC
- Applications
- Android / APK
- System / Updates
- Power
- About / Tailscale status

## TV remote behavior

PiTV owns HDMI-CEC. While Kodi or Android is in front, CEC navigation is relayed through `wtype`. HOME always returns to PiTV. Volume and mute are sent to the TV/receiver through CEC.

## Project layout

```text
pitv/pitv.py             launcher + settings UI
pitv/apk_backend.py      APK inspector / Waydroid adapter
system/pitv-helper       restricted privileged actions
system/pitv-session      Wayland session bootstrap
system/labwc/            compositor config/autostart
system/pitv-waydroid-launch Android foreground wrapper
config/apps.d/            Linux app definitions
scripts/install-waydroid.sh optional Android runtime setup
```

## License

MIT.
