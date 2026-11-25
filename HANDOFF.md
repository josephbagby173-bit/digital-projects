# Handoff — Digital Products (as of 2026-11-24, ~3:30pm)

Read this first in a new session. Repo: `C:\Users\great\ClaudeProjects\digital-products` (git initialized, **nothing committed yet**).

## Goal and constraints
- Owner wants **first income within 2 weeks to 1 month**; wanted at least one product listed the evening of 2026-11-24 (not met yet — see Next steps).
- Sell on **Etsy, Ko-fi and Gumroad**, **every product on all three** (owner does not want products split across platforms). Owner has existing (empty) shop accounts, an Ableton Discord audience for marketing, unlimited time, under $50 cash.
- Open to services and AI-powered offers too, not only products.
- Nothing is published without the owner's explicit approval. I can prepare listings; the owner posts them (or says to use the browser with their signed-in accounts).
- Owner prefers short answers and gets frustrated when I re-explain settled decisions. "Knock out" means "get done first", not "drop".

## Source material
- Owner's PDF: `C:\Users\great\Documents\AI Digital Product Ideas & Starting Plan Checklist.pdf` (5 ideas + benchmarks + 4-phase launch checklist). "Not set in stone."
- Superpowers plugin is enabled (brainstorming -> writing-plans -> subagent-driven-development used so far).

## Decisions made
Product lines (7) — see `products/` folders:
1. **Mixing templates** (3 editions, Live 12 Suite, stock only): Band/guitar, Hip-hop/R&B vocals, EDM/pop. Audience: bedroom producers/new users. Sold separately + discounted bundle. **Furthest along.**
2. **Tone pack**: rebuild the owner's 17 racks with stock Ableton devices (Amp, Cabinet, Pedal, etc.) + new tones using BIAS X AI chat presets purely as *reference* for chain structure. Never sell BIAS files; title tones by style, not artist names. Owner must test; needs a guitar signal (owner not ready to play yet -> recorded DI clips or defer).
3. **Rack Switcher** M4L device (`C:\Users\great\ClaudeProjects\ableton-rack-switcher`) — package + install docs.
4. **Claude + Ableton workflow guide** (prompts, CLAUDE.md, Producer Pal setup).
5. **Drum kit / loop pack**.
6. **AI art pack** (optional): music-themed PNGs; Etsy requires AI disclosure.
7. **Services + Discord launch**: 2 offers (custom rack/template setup, Claude/AI workflow setup).
Dropped: generic printable trackers, Minecraft guides (weak demand per PDF), existing guitar session templates (need a guitar to test).
Suggested order: services/Discord + shared setup/market research first (no building), then templates (in progress), tone pack as the main build, then Rack Switcher, guide, drum kit, art.

## Racks audit (owner's User Library `C:\Users\great\Documents\Ableton\User Library\Presets\Audio Effects\Audio Effect Rack`)
17 `.adg` racks, all contain third-party VST3 (14 use a Neural DSP amp plugin; also MixWave, MaestriWah, Neutron 5, OTT, Hypertune, Pitchmonster, Amplitube 5, Soothe2, BIAS X, one unidentified cab plugin). None sellable as-is; they are *references* to rebuild stock-only. Files were only read, never modified. Detection method: gunzip `.adg`, read `Vst3Preset` blocks, decode `ProcessorState` hex / `Uid`.

## Market data (Exa snippets, not full rankings)
- Stock-device guitar racks sell: Guitaritis $50, Power Chords $15 (207 sales), MixFlow $19, Friedman-style kit $10, many free/pay-what-you-want racks anchor prices low.
- Etsy "Templates Ableton": ~441 results; UltimateMixing Live 12 mixing template $23.99 (392 reviews). Many $2 artist-remake templates — avoid (IP risk).
- Ko-fi sample/preset packs show public sold counts (207, 160, 83, 44, 30). Niche identity sells.
- NOT yet researched: Claude+Ableton guide, Rack Switcher, AI art pack. Prices not finalized (plan: below $23.99 competitor, bundle 20-30% off).

## Repo status
```
digital-products/
  HANDOFF.md, README.md, .gitignore
  docs/superpowers/specs/2026-11-24-mixing-templates-design.md   (approved)
  docs/superpowers/plans/2026-11-24-mixing-templates.md          (approved; 8 tasks)
  tools/check_template.py + tools/tests/                          (validator; run tests with `python -m pytest tools/tests -q`, NOT -I)
  products/mixing-templates/band-guitar/Band Mixing Template.als
  products/mixing-templates/hiphop-rnb/HipHop RnB Vocal Mixing Template.als
  products/mixing-templates/edm-pop/EDM Pop Mixing Template.als
  products/{tone-pack,rack-switcher,claude-ableton-guide,drum-kit,ai-art-pack,services}/  (empty .gitkeep)
  products/mixing-templates/listing/                              (empty)
  .superpowers/sdd/progress.md + task reports                    (git-ignored ledger)
```
Plan progress: **Tasks 1-4 complete** (validator + 3 templates, all PASS the validator and copied into the repo). Controller-verified: 120 BPM, no Producer Pal track, no Max devices, master Limiter present. Remaining: Tasks 5 (PDF guides), 6 (demos, owner records), 7 (listings + bundle), 8 (fresh-install test).

## Status update (2026-11-24, evening) — supersedes "Open items" below where they conflict
- Owner checked the templates (plugins/devices function) and **waived the stem audio tests**: cheap generic template, fine as is. Task 6 demo and Task 8 fresh-install test not done.
- Band template got its tuning pass (role-based EQ Eight + compressor settings) and was re-saved; Hip-hop and EDM were not retouched. Quick Guide PDFs exist for all three (`tools/make_guides.py`).
- **Prices set by owner: $5 per template, $12.99 bundle of three**, same on Etsy, Ko-fi, Gumroad. Launch test: if it sells, build a more substantial next batch and reprice; if not, templates stay in the owner's own folder.
- Listing kits (cover, ZIP, listing.md) in `products/mixing-templates/listing/{band-guitar,hiphop-rnb,edm-pop,bundle}`; Gemini thumbnail prompts in `listing/gemini-prompts.md`. Rebuild with `python tools/make_listings.py`.
- **Marked LISTED on 2026-11-24 at the owner's instruction** (owner posts to the platforms; I have not verified the live listings).
- Why prices are low: competitors (DXT3R, BBK, UltimateMixing) have de-esser, pitch correction, parallel comp, master chain, vocal racks; ours is EQ+compressor per track. Next-batch upgrade ideas: labeled vocal chain rack, parallel compression, master chain with loudness notes, demo video.
- Desktop control hides the owner's other-monitor windows: avoid it (see memory feedback).

## Where files live (consolidated 2026-11-25)
- `products/mixing-templates/artwork/{band-guitar,hiphop-rnb,edm-pop,bundle}/` — PhotoCraft `.pcraft` sources + exported PNGs/thumbnails; `artwork/src/` = raw generated images. `hiphop-rnb/HipHoprnbtemplate-FNAL.png` is the final main thumbnail used on Ko-fi.
- `products/mixing-templates/band-guitar/GUITARSS.png` — screenshot of the Band template in Live (hip-hop's is `SS.png`).
- `brand/` — Great Homeless tag, profile picture, gothic banner.
- `archive/Band_Mixing_Template Project/` — the original Live project folder the templates were saved in. Its .als files match the repo copies except `Band_Mixing_Template.als` (the pre-tuning Band version, same as `.backup/`).
- Left in `Pictures` on purpose: wallpapers, Camera Roll, Saved Pictures, unrelated screenshots.
- Ko-fi: all 4 products live on ko-fi.com/greathomeless/shop; shop terms (no refunds, fix/replace) and profile About text set 2026-11-25. Hip-Hop listing text on Ko-fi still had the cut-off description at last check.

## Open items on the templates
- **Owner audio tests pending** for all three (drop in own stems: no clipping on master; Hip-hop 808 pumps Melody/Sample; EDM kick ducks Bass and Synths groups).
- **One tuning pass for all three** (owner's choice): Band template has flat EQ Eight + generic compressors; Hip-hop and EDM already have high-passes and per-role compressor values. Band and returns need the same treatment.
- Cosmetic: Live prefixes returns ("A-Room Reverb"); group colors snap to Live's palette.
- Validator does not check the -0.3 dB limiter ceiling or monitoring Auto; armed tracks are checked via `<IsArmed>` in each track's `<Recorder>`.
- Originals also sit in `C:\Users\great\ClaudeProjects\Band_Mixing_Template Project\` (Live saved all three .als there). Safe to delete once the owner no longer needs them; repo copies are the source of truth.

## Gotchas learned
- Live's "Save As" defaults to the last project folder. Tell the owner to type/choose the exact repo path, then verify with `find ... -mmin -20 -name "*.als"` before saying a file exists.
- **Windows Command Palette (PowerToys) blocks computer-use clicks** in Live ("frontmost app"). The owner must close it. Group tracks can only be made via Live's Edit > Group Tracks (no API); Ctrl+G key press is blocked by the tool, menu clicks work.
- Producer Pal (`mcp__Producer_Pal__ppal-*`) is the reliable build tool (tracks, devices, params, sidechain routing). AbletonMCP errors on this Live build.
- The build set always has a Producer Pal MIDI track; the owner deletes it before saving.
- Do NOT move `ClaudeProjects\tools\` — it holds the owner's `capcut-kit-main` and `kie-ai`. (I moved it by mistake once and restored it.)
- Subagent-driven execution used `sonnet`, one builder at a time (shared Live set), builder reports in `.superpowers/sdd/task-N-report.md`.

## Next steps (recommended)
1. Owner audio tests + decide whether to tune now or later.
2. **Task 7 first for the fastest listing**: pick one template (Hip-hop or Band), finalize price vs the $23.99 competitor, write listing copy, one-page PDF guide (Task 5), cover/preview images; owner posts to Etsy, Ko-fi, Gumroad.
3. Run the remaining market research (guide, Rack Switcher, art) and set prices.
4. Start services + Discord launch posts (no building needed).
5. Then plan the tone pack subproject (brainstorm -> spec -> plan) using the `guitar-tone-architect`, `sound-mimic`, Producer Pal, and the audit above.
6. Offer to `git commit` the repo when the owner asks.
