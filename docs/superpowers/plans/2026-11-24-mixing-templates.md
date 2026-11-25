# Mixing Templates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, verify and package three Live 12 Suite mixing templates (Band/guitar, Hip-hop/R&B vocals, EDM/pop) ready to list on Etsy, Ko-fi and Gumroad.

**Architecture:** A small Python validator (`check_template.py`) reads a saved `.als` (gzipped XML) and rejects anything not allowed by the spec (third-party plugins, outside samples, armed tracks, missing master limiter). Each template is built in the owner's open Live set via Producer Pal / AbletonMCP, saved, then must pass the validator before the owner's manual test. Listing assets come last.

**Tech Stack:** Ableton Live 12 Suite stock devices, Producer Pal / AbletonMCP, Python 3 (`-I`, stdlib + `pytest`), PDF via the pdf skill.

**Spec:** `docs/superpowers/specs/2026-11-24-mixing-templates-design.md`

## Global Constraints

- Live 12 Suite only. Stock Ableton devices only.
- No third-party plugins, no third-party or outside samples.
- Original work; no remakes of other artists' tracks.
- No custom on/off switches (Live already provides device on/off).
- Audience: bedroom producers and new users. Color-coded groups, clear track names.
- Three separate listings plus one bundle, on Etsy, Ko-fi and Gumroad.
- Price below the $23.99 Etsy competitor (UltimateMixing); exact prices come from the market research.
- Demos are short previews (about 30-60 seconds), not tutorials.
- Out of scope: guitar-specific templates, full tutorials, Standard/Intro editions.

## Review Focus

- **Armed tracks / input monitoring:** a template that opens with a track armed or monitoring set to In causes feedback on a buyer's interface. Expect every track unarmed with monitoring Auto or Off.
- **Absolute file paths:** an `.als` that references `C:\Users\great\...` breaks on the buyer's machine and on Mac. Expect no absolute paths at all.
- **Loud audio into the master:** a buyer dropping in a hot mix must not clip. Expect a master Limiter with ceiling at -0.3 dB.
- **Low-CPU laptops:** a heavy template stutters on opening. Expect total device count per template under 120 and no Hybrid Reverb or Spectral devices on returns.
- **Empty session defaults:** tempo, key and time signature are the first thing a buyer sees. Expect 120 BPM, 4/4, and an empty Arrangement with no stray clips.

---

## File Structure

- `tools/check_template.py` — validator (`check_template(path) -> list[str]`, plus CLI).
- `tools/tests/test_check_template.py` — pytest tests for the validator.
- `products/mixing-templates/band-guitar/Band Mixing Template.als`
- `products/mixing-templates/hiphop-rnb/HipHop RnB Vocal Mixing Template.als`
- `products/mixing-templates/edm-pop/EDM Pop Mixing Template.als`
- `products/mixing-templates/<edition>/Quick Guide.pdf` (one per edition)
- `products/mixing-templates/<edition>/demo/` — owner's screen recording + before/after audio.
- `products/mixing-templates/listing/` — cover, previews, descriptions, bundle.

All paths are under `C:\Users\great\ClaudeProjects\`. The folder is not a git repo, so the plan has no commit steps; each task ends with a checkable result instead.

---

### Task 1: Template validator

**Files:**
- Create: `tools/check_template.py`
- Test: `tools/tests/test_check_template.py`

**Interfaces:**
- Produces: `check_template(path: str) -> list[str]` returns a list of problem strings; empty list means pass. CLI: `python -I tools/check_template.py <file.als>` prints `PASS` (exit 0) or one `FAIL: <problem>` per line (exit 1).

- [ ] **Step 1: Write the failing tests** in `tools/tests/test_check_template.py`. Each test builds a minimal gzipped XML string and calls `check_template`:
  - `test_clean_set_passes`: root `Creator="Ableton Live 12.4.2"`, one master `<Limiter>`, three `<ReturnTrack>`, three `<GroupTrack>` → `[]`.
  - `test_vst3_preset_fails`: adds `<Vst3Preset Id="0">` → result contains a string with `"third-party plugin"`.
  - `test_vst2_and_au_fail`: `<VstPreset` and `<AuPreset` each → `"third-party plugin"`.
  - `test_absolute_path_fails`: a `<Path Value="C:\Users\great\x.wav"/>` → contains `"absolute path"`.
  - `test_missing_master_limiter_fails`: no `<Limiter>` under master → contains `"master limiter"`.
  - `test_armed_track_fails`: an armed track flag → contains `"armed"`. (Find the real XML flag first: save a Live set with one armed track and one unarmed track, gunzip both, diff them, and use the tag that differs. Record the tag name in a comment in the test.)
  - `test_fewer_than_three_returns_fails`: two returns → contains `"return tracks"`.
  - `test_not_live_12_fails`: `Creator="Ableton Live 11.3"` → contains `"Live 12"`.
  - `test_device_count_over_120_fails`: 121 device elements → contains `"device count"`.

- [ ] **Step 2: Run to verify they fail**

Run: `python -I -m pytest tools/tests/test_check_template.py -v`
Expected: all FAIL (module has no `check_template`).

- [ ] **Step 3: Implement `check_template(path: str) -> list[str]` in `tools/check_template.py`.** Open with `gzip`, parse with `xml.etree.ElementTree`, apply the rules in the tests. Use regex only for the plugin tags (`Vst3Preset`, `VstPreset`, `AuPreset`, `PluginDevice`) and absolute paths (`[A-Za-z]:\\` or leading `/Users/`). Device count = count of direct children of every `<Devices>` element.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -I -m pytest tools/tests/test_check_template.py -v`
Expected: all PASS.

- [ ] **Step 5: Prove the validator catches real files.** Run against an existing set that contains VST3 plugins:

Run: `python -I tools/check_template.py "C:\Users\great\Documents\Ableton\User Library\Templates\PolyphiaGuitar.als"`
Expected: exit 1 with at least one `FAIL: third-party plugin` line.

---

### Task 2: Band / guitar template

**Files:**
- Create: `products/mixing-templates/band-guitar/Band Mixing Template.als`

**Interfaces:**
- Consumes: `check_template(path) -> list[str]` from Task 1.
- Produces: the saved `.als` that Tasks 5-7 reference by that exact path.

**Track layout (decided here, final):**

| Group (color) | Tracks inside |
|---|---|
| Drums (red) | Kick, Snare, Toms, Overheads, Drum Bus |
| Bass (blue) | Bass DI, Bass Amp |
| Guitars (orange) | Rhythm Guitar L, Rhythm Guitar R, Lead Guitar, Clean Guitar |
| Vocals (green) | Lead Vocal, Backing Vocals |
| Returns | A Room Reverb, B Plate Reverb, C Delay |

Starter processing, stock devices only: EQ Eight and Compressor per channel where it applies; Drum Buss on the Drum Bus group; Glue Compressor on the Drums and Guitars groups; Reverb on A and B; Echo on C; master chain Glue Compressor then Limiter (ceiling -0.3 dB). No Amp or Cabinet in this template; amp tones belong to the tone pack.

- [ ] **Step 1: Create the structure via Producer Pal / AbletonMCP** in an empty Live set at 120 BPM, 4/4: groups, tracks, returns, colors and names exactly as in the table.
- [ ] **Step 2: Load the stock devices** listed above and set starting values by the guidance in the Ableton manual (use the Ableton Knowledge tool for each device's controls).
- [ ] **Step 3: Set every track unarmed with monitoring Auto, clear any clips, and save** as `products/mixing-templates/band-guitar/Band Mixing Template.als` using Collect All and Save to a clean folder, so no sample references remain.
- [ ] **Step 4: Run the validator**

Run: `python -I tools/check_template.py "products/mixing-templates/band-guitar/Band Mixing Template.als"`
Expected: `PASS`.

- [ ] **Step 5: Owner test.** Owner opens the file in Live 12 Suite, checks there are no missing-file or missing-plugin messages, drops in stems from one of their own songs, and confirms the mix plays without clipping on the master. Fix and re-run Step 4 for anything found.

---

### Task 3: Hip-hop / R&B vocal template

**Files:**
- Create: `products/mixing-templates/hiphop-rnb/HipHop RnB Vocal Mixing Template.als`

**Interfaces:**
- Consumes: `check_template` from Task 1.
- Produces: the saved `.als` at that exact path.

**Track layout (final):**

| Group (color) | Tracks inside |
|---|---|
| Beat (purple) | Kick, Snare / Clap, Hats, Percussion, 808, Melody / Sample, FX |
| Vocals (green) | Lead Vocal, Vocal Double, Ad-libs, Harmony, Vocal Bus |
| Returns | A Vocal Plate, B Slap Echo, C Hall, D Throw Delay |

Starter processing: EQ Eight, Compressor and Saturator on Lead Vocal; Glue Compressor on Vocal Bus; Compressor with the 808 as sidechain on Melody / Sample; Reverb on A and C; Echo on B and D; master chain Glue Compressor then Limiter (ceiling -0.3 dB).

- [ ] **Step 1: Create the structure** via Producer Pal / AbletonMCP at 120 BPM, 4/4, exactly as in the table.
- [ ] **Step 2: Load and set the stock devices**; wire the 808 sidechain on Melody / Sample's Compressor.
- [ ] **Step 3: Unarm all tracks, monitoring Auto, clear clips, Collect All and Save** to the path above.
- [ ] **Step 4: Run the validator**

Run: `python -I tools/check_template.py "products/mixing-templates/hiphop-rnb/HipHop RnB Vocal Mixing Template.als"`
Expected: `PASS`.

- [ ] **Step 5: Owner test.** Owner opens in Live 12 Suite, drops in a vocal and a beat from their own work, confirms the 808 sidechain pumps the Melody / Sample track and that nothing clips.

---

### Task 4: EDM / pop template

**Files:**
- Create: `products/mixing-templates/edm-pop/EDM Pop Mixing Template.als`

**Interfaces:**
- Consumes: `check_template` from Task 1.
- Produces: the saved `.als` at that exact path.

**Track layout (final):**

| Group (color) | Tracks inside |
|---|---|
| Drums (red) | Kick, Clap / Snare, Hats, Percussion |
| Bass (blue) | Sub Bass, Mid Bass |
| Synths (yellow) | Lead, Pad, Chords / Pluck |
| Vocals (green) | Lead Vocal, Backing Vocals, Vocal Chops |
| FX (grey) | Risers, Impacts |
| Returns | A Reverb, B Delay, C Parallel Compression |

Starter processing: Compressor on Bass and Synths groups with Kick as the sidechain source; EQ Eight on every channel; Reverb on A; Echo on B; Glue Compressor on C; master chain Glue Compressor then Limiter (ceiling -0.3 dB).

- [ ] **Step 1: Create the structure** via Producer Pal / AbletonMCP at 120 BPM, 4/4, exactly as in the table.
- [ ] **Step 2: Load and set the stock devices**; wire the Kick sidechain into the Bass and Synths group Compressors.
- [ ] **Step 3: Unarm all tracks, monitoring Auto, clear clips, Collect All and Save** to the path above.
- [ ] **Step 4: Run the validator**

Run: `python -I tools/check_template.py "products/mixing-templates/edm-pop/EDM Pop Mixing Template.als"`
Expected: `PASS`.

- [ ] **Step 5: Owner test.** Owner opens in Live 12 Suite, drops in a kick and a bass or synth loop, confirms the sidechain ducks the Bass and Synths groups and nothing clips.

---

### Task 5: Quick guide PDFs

**Files:**
- Create: `products/mixing-templates/<edition>/Quick Guide.pdf` for `band-guitar`, `hiphop-rnb`, `edm-pop`.

**Interfaces:**
- Consumes: the three saved `.als` files from Tasks 2-4 (track names and group colors are copied from them).

Each guide is one page, US Letter, and contains: how to open the template, a diagram of the groups and returns, a one-line description of each group, where to drop audio, and the personal-use license line.

- [ ] **Step 1: Draft each page** from the template's actual track list (read it from the saved `.als`, so the guide cannot drift from the file).
- [ ] **Step 2: Render with the pdf skill**, then check each file is exactly one page.

Run: `pdfinfo "products/mixing-templates/band-guitar/Quick Guide.pdf"`
Expected: `Pages: 1` (same for the other two).

- [ ] **Step 3: Owner reviews** each guide against the open template and approves the wording.

---

### Task 6: Demos

**Files:**
- Create: `products/mixing-templates/<edition>/demo/` with a screen recording (30-60 seconds) and before/after audio.

**Interfaces:**
- Consumes: the three saved templates and the owner's own stems.

- [ ] **Step 1: I write a short shot list per edition:** open template, drop in stems, play, toggle before/after. No narration script beyond one line of text overlay per step.
- [ ] **Step 2: Owner records each screen demo** using their own stems.
- [ ] **Step 3: Check each recording is between 30 and 60 seconds** and shows no personal data (file paths, email, account names) on screen.

---

### Task 7: Listings and bundle

**Files:**
- Create: `products/mixing-templates/listing/` with cover image, 3-5 preview images, description text and bundle copy per edition.

**Interfaces:**
- Consumes: the Quick Guide PDFs, demos, and the research-derived price points.

- [ ] **Step 1: Set final prices** from the market research (each below the $23.99 competitor; bundle at 20-30% off the sum, per the source PDF).
- [ ] **Step 2: Write each description:** what's included, file formats (`.als` + PDF), requirement (Live 12 Suite), stock devices only, personal-use terms.
- [ ] **Step 3: Create cover and preview images** showing the track list and group colors.
- [ ] **Step 4: Prepare the delivery file** per edition (ZIP of `.als` + guide) and confirm it fits each platform's upload limit; if not, use a branded delivery PDF with a download link.
- [ ] **Step 5: Owner reviews every listing before anything is published.** Nothing goes live without the owner's explicit approval.

---

### Task 8: Fresh-install test

**Files:**
- Test: owner's checklist (a copy of the final delivery ZIP on a clean folder or second machine).

- [ ] **Step 1: Unzip each delivery file into a new empty folder** and open the `.als` from there.
- [ ] **Step 2: Confirm** no missing-file or missing-plugin warnings, no armed tracks, tempo 120 BPM, master limiter present, and CPU stays comfortable on idle.
- [ ] **Step 3: Re-run the validator on the unzipped copies.**

Run: `python -I tools/check_template.py "<unzipped path>\<template>.als"`
Expected: `PASS` for all three.

---

## Self-review

- **Spec coverage:** three templates (Tasks 2-4), PDF guides (5), demos (6), listing assets and bundle (7), owner testing (2-4 Step 5, 8), stock-only and no-outside-samples constraints (enforced by Task 1), pricing from research (7). Out-of-scope items appear only in Global Constraints.
- **Consistency:** `check_template(path) -> list[str]` is the same in every task; file paths match the File Structure list.
- **Review Focus:** each of the five items has a check: armed tracks and absolute paths in Task 1 tests, master limiter in Task 1 tests and each template, CPU as the device-count rule, defaults in Steps 1 and 3 of each build task.
