# FAI Brand — Project Notes for Claude

## Project
Foundation for American Innovation (FAI) brand system and illustration pipeline.

## Base path
`FAI Brand Resources/FAI Illustrations/Brand Illustrations Cleanup/`

## What's been built (Phases 1–3 complete)
- **Phase 1** (`scripts/clean_svgs.py`): Cleans all SVGs to 7-color brand compliance
- **Phase 2** (`scripts/build_manifest.py`): Builds `tiles-manifest.json` with visual metadata
- **Phase 3** (`scripts/generate_banner.py`): Generates 6×3 grid banners with energy levels
- **Contact sheet** (`scripts/generate_contact_sheet.py`): HTML preview of generated banners

## Next steps (planned, not yet implemented)
See plan at `.claude/plans/stateless-stargazing-volcano.md` (global ~/.claude/plans/).

**Part A — Tile simplification** (`scripts/simplify_tiles.py`):
Every tile should become a single `<path>` element — no background rects, no clipPaths.
Most clipPaths are no-ops; ~6 tiles (Mirror family circles) need real geometric clipping.
NaN path data in 15 tiles (Cascade, Centric) needs sanitizing first.
Dependencies: `pip install svgpathtools shapely`

**Part B — Banner composition** (update `scripts/generate_banner.py`):
- Tile rotation (0/90/180/270°) — quadruples effective tile library
- Edge-matching: pair tiles so shapes connect visually across cell boundaries
- Color continuity: same fg color on matched edges = shapes appear to span cells
- Compositional templates: river, focal, symmetric, gradient, checkerboard
- Pixel-perfect integer cell positions (320×320px, no floats)

## Brand colors (7 permitted fills only)
- International Orange: `#FF4F00`
- Cod Gray: `#121212`
- White: `#FFFFFF`
- Smoke White: `#F3F3F3`
- Chrome Yellow: `#FFA300`
- Celestial Blue: `#4997D0`
- Timberwolf: `#D9D9D6`

## Key paths
- Cleaned tiles: `output/shapes-clean/`
- Generated banners: `output/banners-generated/`
- Contact sheet: `output/contact-sheets/contact-sheet.html`
- Tile manifest: `tiles-manifest.json`
- Scripts: `scripts/`
