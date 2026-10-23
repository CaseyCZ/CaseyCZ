#!/usr/bin/env python3
import base64
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSIONS_FILE = ROOT / "versions.json"
UA = "CaseyCZ-profile-version-sync/1.0"


def fetch_text(url, token=None):
    headers = {"User-Agent": UA}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/vnd.github+json"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8")


def fetch_json(url, token=None):
    return json.loads(fetch_text(url, token))


def package_version(repo, branch):
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/package.json"
    return str(fetch_json(url)["version"])


def readme_badge_version(repo, branch, path):
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
    text = fetch_text(url)
    match = re.search(r"VERZE-v([0-9]+(?:\.[0-9]+)+)", text)
    if not match:
        raise RuntimeError(f"Version badge not found in {repo}/{path}")
    return match.group(1)



def release_badge_version(repo, branch, path):
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
    text = fetch_text(url)
    match = re.search(r"RELEASE-v([0-9]+(?:\.[0-9]+)+)", text)
    if not match:
        raise RuntimeError(f"Release badge not found in {repo}/{path}")
    return match.group(1)


def optional_version(key, source, current):
    """Keep the previous valid version if a new public source is temporarily offline."""
    try:
        value = str(source())
        if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)+", value):
            raise ValueError(f"Unexpected version format: {value}")
        return value
    except (OSError, ValueError, RuntimeError, KeyError, TimeoutError) as exc:
        print(f"{key}: {exc}; keeping previous value {current}")
        return current


def pitv_version():
    text = fetch_text(
        "https://raw.githubusercontent.com/CaseyCZ/PiTV/Master/pitv/pitv.py"
    )
    match = re.search(r'^VERSION\s*=\s*["\']([^"\']+)["\']', text, re.M)
    if not match:
        raise RuntimeError("PiTV VERSION not found")
    return match.group(1)


def hb_control_version(current):
    token = os.environ.get("HB_CONTROL_TOKEN", "").strip()
    if not token:
        print("HB_CONTROL_TOKEN not configured; keeping current HB Control version.")
        return current

    data = fetch_json(
        "https://api.github.com/repos/CaseyCZ/HB-Control/contents/release.json?ref=Master",
        token,
    )
    payload = json.loads(base64.b64decode(data["content"]).decode("utf-8"))
    version = str(payload["version"])
    build = int(payload["build"])
    return {
        "version": version,
        "build": build,
        "display": f"{version} · build {build}",
    }


def main():
    current = json.loads(VERSIONS_FILE.read_text(encoding="utf-8"))

    updated = {
        "hb_control": hb_control_version(current.get("hb_control", {})),
        "pitv": pitv_version(),
        "games": package_version("CaseyCZ/GameS-Calendar-Website", "main"),
        "lockscreen": readme_badge_version(
            "CaseyCZ/Scriptable", "Master", "apps/LockScreenGenerator/README.md"
        ),
        "sports_info": readme_badge_version(
            "CaseyCZ/Scriptable", "Master", "apps/Sports-Info/README.md"
        ),
        "stremio_sosac": package_version("CaseyCZ/stremio.sosac", "Master"),
        "sosac_subtitles": package_version(
            "CaseyCZ/stremio.sosac.subtitles", "Master"
        ),
        "tube_tv": optional_version(
            "tube_tv",
            lambda: release_badge_version("CaseyCZ/TubeTV", "Master", "README.md"),
            current.get("tube_tv", "1.0.0"),
        ),
        "stremio_addons": optional_version(
            "stremio_addons",
            lambda: package_version("CaseyCZ/stremio.addons", "Master"),
            current.get("stremio_addons", "0.2.1"),
        ),
        "sports_live": optional_version(
            "sports_live",
            lambda: readme_badge_version(
                "CaseyCZ/Scriptable", "Master", "apps/Sports-Live/README.md"
            ),
            current.get("sports_live", "0.3.3"),
        ),
        "piskvorky": optional_version(
            "piskvorky",
            lambda: readme_badge_version(
                "CaseyCZ/Scriptable", "Master", "apps/Piskvorky-Deluxe/README.md"
            ),
            current.get("piskvorky", "1.1.0"),
        ),
        "breakout": optional_version(
            "breakout",
            lambda: readme_badge_version(
                "CaseyCZ/Scriptable", "Master", "apps/Breakout-Deluxe/README.md"
            ),
            current.get("breakout", "1.2.0"),
        ),
        "pong": optional_version(
            "pong",
            lambda: readme_badge_version(
                "CaseyCZ/Scriptable", "Master", "apps/Pong-Fotbal/README.md"
            ),
            current.get("pong", "1.1.0"),
        ),
    }

    VERSIONS_FILE.write_text(
        json.dumps(updated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for name, value in updated.items():
        print(f"{name}: {value}")


if __name__ == "__main__":
    main()
