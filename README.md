# Digital Products

Products to sell on Etsy, Ko-fi and Gumroad (all products on all three platforms).

- `docs/superpowers/specs/` — design specs
- `docs/superpowers/plans/` — implementation plans
- `tools/` — validators (`check_template.py` for Live sets)
- `products/` — one folder per product line:
  - `mixing-templates/` (band-guitar, hiphop-rnb, edm-pop, listing)
  - `tone-pack/`, `rack-switcher/`, `claude-ableton-guide/`, `drum-kit/`, `ai-art-pack/`, `services/`

Run the validator: `python -I tools/check_template.py "<file.als>"`
Run its tests: `python -m pytest tools/tests -q`
