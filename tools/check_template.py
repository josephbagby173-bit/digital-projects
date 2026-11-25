"""Validate an Ableton Live .als mixing template (gzipped XML).

Usage: python -I tools/check_template.py <file.als>
Prints PASS (exit 0) or one "FAIL: <problem>" per line (exit 1).
"""
import gzip
import re
import sys
import xml.etree.ElementTree as ET

PLUGIN_RE = re.compile(r"<(Vst3Preset|VstPreset|AuPreset|PluginDevice)\b")
ABS_PATH_RE = re.compile(r"[A-Za-z]:\\|/Users/")
MAX_DEVICES = 120


def check_template(path: str) -> list[str]:
    problems: list[str] = []
    with gzip.open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="replace")
    root = ET.fromstring(raw)

    creator = root.get("Creator", "")
    if not re.match(r"Ableton Live 12(\D|$)", creator):
        problems.append(f"not made with Live 12 (Creator={creator!r})")

    for tag in sorted(set(PLUGIN_RE.findall(text))):
        problems.append(f"third-party plugin found ({tag})")

    if ABS_PATH_RE.search(text):
        problems.append("absolute path found in set")

    master = next(root.iter("MainTrack"), None)
    if master is None or next(master.iter("Limiter"), None) is None:
        problems.append("master limiter missing")

    if any(e.get("Value") == "true" for e in root.iter("IsArmed")):
        problems.append("armed track found")

    n_returns = sum(1 for _ in root.iter("ReturnTrack"))
    if n_returns < 3:
        problems.append(f"need at least 3 return tracks, found {n_returns}")

    n_devices = sum(len(d) for d in root.iter("Devices"))
    if n_devices > MAX_DEVICES:
        problems.append(f"device count {n_devices} exceeds {MAX_DEVICES}")

    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_template.py <file.als>", file=sys.stderr)
        return 2
    problems = check_template(argv[1])
    if not problems:
        print("PASS")
        return 0
    for p in problems:
        print(f"FAIL: {p}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
