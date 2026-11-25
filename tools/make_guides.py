"""Build one-page Quick Guide PDFs from the saved .als files (track names are read from the file)."""
import gzip
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent.parent / "products" / "mixing-templates"
PALETTE = ["#E0463C", "#4C7BD9", "#E8A33D", "#4CA03A", "#9A5CC8", "#2BB3C0"]

EDITIONS = {
    "band-guitar": {
        "als": "Band Mixing Template.als",
        "title": "Band Mixing Template",
        "sub": "Live 12 Suite | Drums, bass, guitars and vocals | stock devices only",
        "groups": {
            "Drums": "Kick, snare, toms, overheads and a Drum Bus that glues them. High-passed and tamed for a tight kit.",
            "Bass": "DI for low-end weight, Amp for grit. Compressed so the bass sits steady under the band.",
            "Guitars": "Two rhythm guitars (pan L/R), lead and clean. Mud cut near 250 Hz, presence boost for clarity.",
            "Vocals": "Lead and backing vocals with high-pass, de-mud and air.",
        },
        "returns": {
            "A-Room Reverb": "room reverb",
            "B-Plate Reverb": "plate reverb",
            "C-Delay": "delay",
        },
    },
    "hiphop-rnb": {
        "als": "HipHop RnB Vocal Mixing Template.als",
        "title": "Hip-Hop / R&B Vocal Mixing Template",
        "sub": "Live 12 Suite | Beat + vocal stack | stock devices only",
        "groups": {
            "Beat": "Kick, snare/clap, hats, percussion, 808, melody/sample and FX. The 808 ducks the melody so the low end stays clean.",
            "Vocals": "Lead, double, ad-libs, harmony and a Vocal Bus. High-passed and compressed per role, glued on the bus.",
        },
        "returns": {
            "A-Vocal Plate": "plate reverb",
            "B-Slap Echo": "short slapback delay",
            "C-Hall": "hall reverb",
            "D-Throw Delay": "long delay for throws",
        },
    },
    "edm-pop": {
        "als": "EDM Pop Mixing Template.als",
        "title": "EDM / Pop Mixing Template",
        "sub": "Live 12 Suite | Drums, bass, synths, vocals, FX | stock devices only",
        "groups": {
            "Drums": "Kick, clap/snare, hats and percussion. The kick drives the sidechain.",
            "Bass": "Sub and mid bass. Ducked by the kick so the drop hits clean.",
            "Synths": "Lead, pad and chords/pluck. Ducked by the kick for pump and space.",
            "Vocals": "Lead, backing and vocal chops with high-pass, compression and air.",
            "FX": "Risers and impacts for transitions.",
        },
        "returns": {
            "A-Reverb": "reverb",
            "B-Delay": "delay",
            "C-Parallel Compression": "squashed copy blended under the mix for punch",
        },
    },
}


def read_tracks(als: Path):
    xml = gzip.open(als, "rt", encoding="utf-8").read()
    out = []
    for m in re.finditer(
        r'<(GroupTrack|AudioTrack|MidiTrack|ReturnTrack) Id="\d+"[^>]*>.*?<EffectiveName Value="([^"]*)"', xml, re.S
    ):
        out.append((m.group(1), m.group(2)))
    return out


def structure(tracks):
    groups, returns, cur = [], [], None
    for kind, name in tracks:
        if kind == "GroupTrack":
            cur = (name, [])
            groups.append(cur)
        elif kind == "ReturnTrack":
            returns.append(name)
        elif cur is not None:
            cur[1].append(name)
    return groups, returns


def build(key, cfg):
    folder = ROOT / key
    groups, returns = structure(read_tracks(folder / cfg["als"]))
    missing = [g for g, _ in groups if g not in cfg["groups"]]
    assert not missing, f"{key}: no description for groups {missing}"
    out = folder / "Quick Guide.pdf"
    c = canvas.Canvas(str(out), pagesize=letter)
    w, h = letter
    m = 48
    c.setTitle(cfg["title"] + " - Quick Guide")
    c.setFillColor(colors.HexColor("#1b1b1f"))
    c.rect(0, h - 90, w, 90, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(m, h - 48, cfg["title"])
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#c8c8d0"))
    c.drawString(m, h - 68, cfg["sub"] + "  |  Quick Guide")

    body = ParagraphStyle("b", fontName="Helvetica", fontSize=9.5, leading=13, textColor=colors.HexColor("#222"))
    head = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=colors.HexColor("#111"))
    y = h - 118

    def para(text, style, x=m, width=w - 2 * m):
        nonlocal y
        p = Paragraph(text, style)
        _, ph = p.wrap(width, 1000)
        p.drawOn(c, x, y - ph)
        y -= ph

    para("1. Open it", head)
    y -= 4
    para(
        "Double-click the .als file (or File &gt; Open Live Set in Live 12 Suite). Save a copy with File &gt; Save Live Set As "
        "before you start, so the original stays clean. Tempo is 120 BPM; change it to match your song.",
        body,
    )
    y -= 12
    para("2. Where your audio goes", head)
    y -= 4
    para(
        "Drag your recorded or exported stems onto the track that matches each part. Every track already has EQ Eight and a "
        "Compressor set for its role. Start with the faders around where they are and adjust to taste.",
        body,
    )
    y -= 12
    para("3. Layout", head)
    y -= 8

    # groups diagram
    col_w = (w - 2 * m - 12 * (len(groups) - 1)) / len(groups)
    top = y
    maxh = 0
    for i, (gname, members) in enumerate(groups):
        x = m + i * (col_w + 12)
        col = colors.HexColor(PALETTE[i % len(PALETTE)])
        c.setFillColor(col)
        c.roundRect(x, top - 20, col_w, 20, 4, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 6, top - 14, gname)
        yy = top - 20
        c.setFillColor(colors.HexColor("#333"))
        c.setFont("Helvetica", 8.5)
        for name in members:
            yy -= 14
            c.setStrokeColor(col)
            c.setLineWidth(1)
            c.line(x, yy - 3, x, yy + 11)
            c.drawString(x + 6, yy, name[: int(col_w / 4.4)])
        maxh = max(maxh, top - yy + 4)
    y = top - maxh - 8

    # group descriptions
    for i, (gname, _) in enumerate(groups):
        col = PALETTE[i % len(PALETTE)]
        para(f'<font color="{col}"><b>{gname}</b></font> - {cfg["groups"][gname]}', body)
        y -= 3
    y -= 8
    para("Returns (send effects)", head)
    y -= 4
    for rname in returns:
        desc = cfg["returns"].get(rname, "")
        para(f"<b>{rname}</b> - {desc}", body)
        y -= 2
    y -= 8
    para("Tips", head)
    y -= 4
    para(
        "Turn the sends up on each track to taste. Watch the Main track meter and keep peaks under about -3 dB; "
        "a Limiter is already on Main as a safety net.",
        body,
    )

    c.setStrokeColor(colors.HexColor("#ccc"))
    c.line(m, 62, w - m, 62)
    foot = ParagraphStyle("f", fontName="Helvetica", fontSize=8, leading=10.5, textColor=colors.HexColor("#555"))
    p = Paragraph(
        "License: personal use. You may use this template for your own music; you may not resell, share or redistribute "
        "it or its files. Requires Ableton Live 12 Suite. Uses only Live's built-in devices; no outside samples or plugins.",
        foot,
    )
    _, ph = p.wrap(w - 2 * m, 100)
    p.drawOn(c, m, 56 - ph)
    assert y > 70, f"{key}: content overflows the page (y={y:.0f})"
    c.showPage()
    c.save()
    print("wrote", out)


if __name__ == "__main__":
    keys = sys.argv[1:] or list(EDITIONS)
    for k in keys:
        build(k, EDITIONS[k])
