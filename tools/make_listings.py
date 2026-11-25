"""Build listing assets (cover, layout preview, delivery ZIP, listing.md) for every edition and the bundle."""
import gzip
import re
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent / "products" / "mixing-templates"
FONT = "C:/Windows/Fonts/arialbd.ttf"
FONT_R = "C:/Windows/Fonts/arial.ttf"
PAL = ["#E0463C", "#4C7BD9", "#E8A33D", "#4CA03A", "#9A5CC8"]
PRICE, BUNDLE = "$5.00", "$12.99"

E = {
    "band-guitar": dict(
        als="Band Mixing Template.als", name="Band / Guitar Mixing Template", l1="BAND / GUITAR", l2="MIXING TEMPLATE",
        tag="Drums, bass, guitars and vocals", rtn="Room Reverb, Plate Reverb, Delay",
        built=["EQ Eight with role-based high-passes", "Per-role compressor settings", "Drum Bus with Drum Buss", "Limiter on the Main track"],
        built_md=["EQ Eight with role-based high-pass and tone settings on every track", "Compressor settings chosen per role", "Drum Bus track with Drum Buss for glue", "Limiter on the Main track"],
        title="Band Guitar Mixing Template for Ableton Live 12 Suite | Rock Drums Bass Guitars Vocals | Stock Devices Only | Instant Download",
        short="A ready-to-mix Ableton Live 12 Suite session for bands: drums, bass, guitars and vocals, with returns and starting settings already set. Stock devices only.",
        tags="ableton template, ableton live 12, band mixing, rock mixing template, guitar mixing, mixing template, ableton project, music production, home studio, stock devices, instant download, drum mixing, vocal mixing",
    ),
    "hiphop-rnb": dict(
        als="HipHop RnB Vocal Mixing Template.als", name="Hip-Hop / R&B Vocal Mixing Template", l1="HIP-HOP / R&B", l2="VOCAL MIXING TEMPLATE",
        tag="Beat + vocal stack", rtn="Vocal Plate, Slap Echo, Hall, Throw Delay",
        built=["EQ Eight with role-based high-passes", "Per-role compressor settings", "808 sidechained to the melody", "Limiter on the Main track"],
        built_md=["EQ Eight with a role-based high-pass on the tracks", "Compressor settings chosen per role", "808 sidechained so it ducks the melody/sample", "Limiter on the Main track"],
        title="Hip Hop RnB Vocal Mixing Template for Ableton Live 12 Suite | Vocal Chain Template | Stock Devices Only | Instant Download",
        short="A ready-to-mix Ableton Live 12 Suite session for hip-hop and R&B vocals: tracks, groups, returns and starting settings already set. Stock devices only.",
        tags="ableton template, ableton live 12, hip hop mixing, rnb vocal chain, vocal mixing template, mixing template, ableton project, music production, beat maker, producer template, stock devices, instant download, 808",
    ),
    "edm-pop": dict(
        als="EDM Pop Mixing Template.als", name="EDM / Pop Mixing Template", l1="EDM / POP", l2="MIXING TEMPLATE",
        tag="Drums, bass, synths, vocals, FX", rtn="Reverb, Delay, Parallel Compression",
        built=["EQ Eight with role-based high-passes", "Per-role compressor settings", "Kick sidechains Bass and Synths", "Limiter on the Main track"],
        built_md=["EQ Eight with role-based high-passes", "Compressor settings chosen per role", "Kick sidechain ducking on the Bass and Synths groups", "Limiter on the Main track"],
        title="EDM Pop Mixing Template for Ableton Live 12 Suite | Sidechain Kick Bass Synths Vocals FX | Stock Devices Only | Instant Download",
        short="A ready-to-mix Ableton Live 12 Suite session for EDM and pop: drums, bass, synths, vocals and FX with sidechain ducking and returns already set. Stock devices only.",
        tags="ableton template, ableton live 12, edm mixing template, pop mixing, sidechain template, mixing template, ableton project, music production, producer template, stock devices, instant download, house music, synth mixing",
    ),
}


def f(size, bold=True):
    return ImageFont.truetype(FONT if bold else FONT_R, size)


def tracks(als):
    xml = gzip.open(als, "rt", encoding="utf-8").read()
    groups, returns, cur = [], [], None
    for m in re.finditer(
        r'<(GroupTrack|AudioTrack|MidiTrack|ReturnTrack) Id="\d+"[^>]*>.*?<EffectiveName Value="([^"]*)"', xml, re.S
    ):
        kind, name = m.groups()
        if kind == "GroupTrack":
            cur = (name, [])
            groups.append(cur)
        elif kind == "ReturnTrack":
            returns.append(name)
        elif cur:
            cur[1].append(name)
    return groups, returns


def cover(key, c, out):
    groups, _ = tracks(ROOT / key / c["als"])
    W, H = 2000, 1500
    im = Image.new("RGB", (W, H), "#17171c")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 24, H], fill=PAL[0])
    d.text((120, 150), c["l1"], font=f(150), fill="white")
    d.text((120, 330), c["l2"], font=f(100), fill="white")
    d.text((120, 500), "Ableton Live 12 Suite  |  Stock devices only", font=f(60, False), fill="#c8c8d0")
    d.text((120, 590), "Drop in your stems and start mixing.", font=f(60, False), fill="#c8c8d0")
    n = len(groups)
    cw = min(760, (W - 240 - 40 * (n - 1)) // n)
    x, y = 120, 760
    for i, (g, members) in enumerate(groups):
        col = PAL[i % len(PAL)]
        d.rounded_rectangle([x, y, x + cw, y + 66], 12, fill=col)
        d.text((x + 20, y + 8), g, font=f(44), fill="white")
        yy = y + 84
        for m in members:
            d.line([x, yy, x, yy + 38], fill=col, width=5)
            d.text((x + 20, yy), m[: max(8, cw // 22)], font=f(34, False), fill="#e8e8ee")
            yy += 48
        x += cw + 40
    d.text((120, H - 110), "Includes Quick Guide PDF", font=f(48), fill="#8a8a96")
    im.save(out / "cover.png")


def layout(key, c, out):
    groups, returns = tracks(ROOT / key / c["als"])
    W, H = 2000, 1500
    im = Image.new("RGB", (W, H), "#f6f6f8")
    d = ImageDraw.Draw(im)
    d.text((100, 70), "What's inside", font=f(100), fill="#17171c")
    n = len(groups)
    cw = min(820, (W - 200 - 40 * (n - 1)) // n)
    x, y = 100, 230
    for i, (g, members) in enumerate(groups):
        col = PAL[i % len(PAL)]
        d.rounded_rectangle([x, y, x + cw, y + 72], 14, fill=col)
        d.text((x + 22, y + 10), g, font=f(48), fill="white")
        yy = y + 96
        for m in members:
            d.line([x, yy, x, yy + 42], fill=col, width=6)
            d.text((x + 22, yy + 2), m[: max(8, cw // 20)], font=f(36, False), fill="#222")
            yy += 54
        x += cw + 40
    y = 960
    d.text((100, y), "Return tracks", font=f(60), fill="#17171c")
    for i, r in enumerate(returns):
        d.text((100, y + 90 + i * 58), r, font=f(40, False), fill="#222")
    d.text((1100, y), "Built in", font=f(60), fill="#17171c")
    for i, line in enumerate(c["built"]):
        d.text((1100, y + 90 + i * 58), line, font=f(40, False), fill="#222")
    im.save(out / "preview-layout.png")


def package(key, c, out):
    z = out / (c["als"][:-4] + ".zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(ROOT / key / c["als"], c["als"])
        zf.write(ROOT / key / "Quick Guide.pdf", "Quick Guide.pdf")
    return z


def listing_md(key, c, groups, returns, out):
    lay = "\n".join(f"- **{g} group:** {', '.join(m)}" for g, m in groups)
    rt = ", ".join(r.split("-", 1)[-1] for r in returns)
    built = "\n".join(f"- {b}" for b in c["built_md"])
    zname = c["als"][:-4] + ".zip"
    (out / "listing.md").write_text(f"""# {c['name']} - listing (DRAFT, not published)

**Price:** {PRICE} (launch price). Bundle of all three editions: {BUNDLE}. Same price on Etsy, Ko-fi and Gumroad.

## Title (Etsy, 140 chars max)
{c['title']}

## Short description (Ko-fi / Gumroad)
{c['short']}

## Description
**Stop rebuilding the same session every song.**
Open the template, drop in your stems, and start mixing.

**What's included**
- 1 Ableton Live 12 Suite session (.als)
- 1 Quick Guide PDF (one page)

**Layout**
{lay}
- **{len(returns)} return tracks:** {rt}
- 120 BPM (change to match your song)

**Built in**
{built}

**Requirements**
- Ableton Live 12 Suite
- Uses only Live's built-in devices. No third-party plugins, no outside samples.

**License:** personal use. Use it for your own music. No reselling, sharing or redistributing the files.

**Note:** this is a starting point, not a finished mix. Adjust levels, EQ and compression to your material.

## Tags (Etsy, 13)
{c['tags']}

## Files to upload
- Delivery: `{zname}`
- Images: `cover.png` (first), `preview-layout.png`, plus your Gemini thumbnail; add a screen capture of the open template when you have one

## Before you post
- [ ] You audio-test the template with your own stems
- [ ] You approve the Quick Guide wording and price
""", encoding="utf-8")


def bundle():
    out = ROOT / "listing" / "bundle"
    out.mkdir(parents=True, exist_ok=True)
    W, H = 2000, 1500
    im = Image.new("RGB", (W, H), "#17171c")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 24, H], fill=PAL[0])
    d.text((120, 150), "MIXING TEMPLATE", font=f(150), fill="white")
    d.text((120, 330), "BUNDLE x3", font=f(150), fill=PAL[2])
    d.text((120, 540), "Ableton Live 12 Suite  |  Stock devices only", font=f(60, False), fill="#c8c8d0")
    y = 780
    for i, k in enumerate(E):
        d.rounded_rectangle([120, y, 1100, y + 100], 16, fill=PAL[i])
        d.text((150, y + 18), E[k]["name"], font=f(48), fill="white")
        y += 130
    d.text((120, H - 110), "3 templates + 3 Quick Guide PDFs", font=f(48), fill="#8a8a96")
    im.save(out / "cover.png")
    z = out / "Mixing Template Bundle.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for k, c in E.items():
            zf.write(ROOT / k / c["als"], f"{c['name']}/{c['als']}")
            zf.write(ROOT / k / "Quick Guide.pdf", f"{c['name']}/Quick Guide.pdf")
    items = "\n".join(f"- **{c['name']}** - {c['tag']}" for c in E.values())
    (out / "listing.md").write_text(f"""# Mixing Template Bundle (3 editions) - listing (DRAFT, not published)

**Price:** {BUNDLE} (each template alone is {PRICE}). Same price on Etsy, Ko-fi and Gumroad.

## Title (Etsy, 140 chars max)
Ableton Live 12 Mixing Template Bundle | Band, Hip Hop RnB, EDM Pop | 3 Templates | Stock Devices Only | Instant Download

## Short description (Ko-fi / Gumroad)
Three ready-to-mix Ableton Live 12 Suite sessions in one download: Band/Guitar, Hip-Hop/R&B Vocal and EDM/Pop. Stock devices only.

## Description
**Three mixing templates, one download.**
Pick the one that fits your song, drop in your stems, and start mixing.

**What's included**
{items}
- 3 Quick Guide PDFs (one page each)

**Every template has**
- Groups, tracks and return tracks laid out for the genre
- EQ Eight and Compressor settings chosen per role
- Limiter on the Main track
- 120 BPM (change to match your song)

**Requirements**
- Ableton Live 12 Suite
- Uses only Live's built-in devices. No third-party plugins, no outside samples.

**License:** personal use. Use it for your own music. No reselling, sharing or redistributing the files.

**Note:** these are starting points, not finished mixes. Adjust levels, EQ and compression to your material.

## Tags (Etsy, 13)
ableton template, ableton live 12, mixing template bundle, ableton project, hip hop mixing, band mixing, edm template, rnb vocal chain, music production, producer template, stock devices, instant download, template pack

## Files to upload
- Delivery: `Mixing Template Bundle.zip`
- Images: `cover.png` (first) plus your Gemini thumbnail

## Before you post
- [ ] You audio-test the templates with your own stems
- [ ] You approve the Quick Guide wording and price
""", encoding="utf-8")
    print("bundle zip", round(z.stat().st_size / 1024), "KB")


if __name__ == "__main__":
    for key, c in E.items():
        out = ROOT / "listing" / key
        out.mkdir(parents=True, exist_ok=True)
        groups, returns = tracks(ROOT / key / c["als"])
        cover(key, c, out)
        layout(key, c, out)
        z = package(key, c, out)
        listing_md(key, c, groups, returns, out)
        print(key, "zip", round(z.stat().st_size / 1024), "KB")
    bundle()
