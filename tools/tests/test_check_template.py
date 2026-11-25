import gzip
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check_template import check_template  # noqa: E402

# Armed-track flag, found empirically in saved .als files under the User Library:
# <IsArmed Value="true" /> (vs Value="false") inside <Recorder> of a track's
# <MainSequencer>/<DeviceChain>. 48 true / 1182 false across 60 sets.


def build(creator="Ableton Live 12.4.2", returns=3, groups=3, limiter=True,
          extra_track="", extra_master="", devices=0, armed=False):
    master_dev = "<Limiter />" if limiter else "<Compressor2 />"
    xml = f'<Ableton Creator="{creator}"><LiveSet><Tracks>'
    xml += "<GroupTrack />" * groups
    xml += "<MidiTrack><Recorder><IsArmed Value=\"%s\" /></Recorder>" % ("true" if armed else "false")
    xml += "<DeviceChain><Devices>" + "<Eq8 />" * devices + "</Devices></DeviceChain></MidiTrack>"
    xml += "<ReturnTrack />" * returns
    xml += extra_track
    xml += "</Tracks><MainTrack><DeviceChain><DeviceChain><Devices>"
    xml += master_dev + extra_master
    xml += "</Devices></DeviceChain></DeviceChain></MainTrack></LiveSet></Ableton>"
    return xml


def write(tmp_path, xml):
    p = tmp_path / "t.als"
    with gzip.open(p, "wb") as f:
        f.write(xml.encode("utf-8"))
    return str(p)


def has(problems, text):
    return any(text in p for p in problems)


def test_clean_set_passes(tmp_path):
    assert check_template(write(tmp_path, build())) == []


def test_vst3_preset_fails(tmp_path):
    p = write(tmp_path, build(extra_track='<Vst3Preset Id="0" />'))
    assert has(check_template(p), "third-party plugin")


@pytest.mark.parametrize("tag", ["VstPreset", "AuPreset"])
def test_vst2_and_au_fail(tmp_path, tag):
    p = write(tmp_path, build(extra_track=f"<{tag} />"))
    assert has(check_template(p), "third-party plugin")


def test_absolute_path_fails(tmp_path):
    p = write(tmp_path, build(extra_track=r'<Path Value="C:\Users\great\x.wav"/>'))
    assert has(check_template(p), "absolute path")


def test_missing_master_limiter_fails(tmp_path):
    assert has(check_template(write(tmp_path, build(limiter=False))), "master limiter")


def test_armed_track_fails(tmp_path):
    assert has(check_template(write(tmp_path, build(armed=True))), "armed")


def test_fewer_than_three_returns_fails(tmp_path):
    assert has(check_template(write(tmp_path, build(returns=2))), "return tracks")


def test_not_live_12_fails(tmp_path):
    assert has(check_template(write(tmp_path, build(creator="Ableton Live 11.3"))), "Live 12")


def test_device_count_over_120_fails(tmp_path):
    assert has(check_template(write(tmp_path, build(devices=120))), "device count")
