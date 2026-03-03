#!/usr/bin/env python3
"""
Phase 3: FAI Banner Generator (v4)

Generates on-brand 6x3 grid banner compositions from simplified shape tiles.

v4 changes (composition scoring):
  - Generate-and-score approach: produces many candidate compositions, scores
    each on 8 aesthetic axes, keeps the highest-scoring result.
  - 8-axis scoring system: anchor triangle, shape repetition, directional flow,
    weight balance, negative space, color temperature zoning, shape family
    grouping, hero tile placement.
  - Weight map composition templates for macro-structure guidance.
  - Score details emitted in JSON sidecar for tuning and validation.

Composition philosophy:
  - Pick 1-3 shape families per banner (not all 17) -- creates coherent motif
  - Systematic rotation patterns (pinwheel, spiral, mirror, flow) -- tilework feel
  - Family repetition IS the composition; color variation provides interest
  - Flat SVG output: <g transform="translate scale [rotate]"> instead of nested <svg>

Templates:
  pinwheel   -- one or two families, 4-rotation pinwheel tiling
  spiral     -- one or two families, rotation advances each column
  mirror     -- one or two families, reflected across vertical centre
  flow       -- one family, alternating 0/180 creates flowing linked shapes
  focal      -- two or three families, heavier tiles cluster at centre
  scatter    -- two or three families, free rotation, light & varied

Usage:
    python generate_banner.py --energy medium --seed 42
    python generate_banner.py --batch 50
    python generate_banner.py --energy high --template pinwheel --seed 7
    python generate_banner.py --candidates 100 --energy medium
"""

import argparse
import copy
import json
import math
import random
import sys
from collections import Counter
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fai_colors import BRAND_COLORS, WARM_COLORS, COOL_COLORS, NEUTRAL_COLORS, HEX_TO_NAME

# -- Constants -------------------------------------------------
SVG_NS = "http://www.w3.org/2000/svg"
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST   = BASE_DIR / "tiles-manifest-v2.json"
DEFAULT_TILES_DIR  = BASE_DIR / "output" / "shapes-simplified"
DEFAULT_OUTPUT_DIR = BASE_DIR / "output" / "banners-generated"

GRID_COLS   = 6
GRID_ROWS   = 3
TOTAL_SLOTS = GRID_COLS * GRID_ROWS   # 18
TILE_VB_W   = 200
TILE_VB_H   = 200
CELL_W      = 320   # 1920 / 6  -- exact integer
CELL_H      = 320   # 960 / 3   -- exact integer
CELL_SCALE  = CELL_W / TILE_VB_W   # 1.6

ROTATIONS = [0, 90, 180, 270]

# -- Composition Scoring Constants -----------------------------
SCORING_WEIGHTS = {
    "anchor":    0.10,
    "rhythm":    0.20,
    "direction": 0.15,
    "weight":    0.15,
    "negative":  0.10,
    "temp":      0.10,
    "family":    0.10,
    "hero":      0.10,
}

# Rule-of-thirds power positions on the 6x3 grid (col, row)
POWER_POSITIONS = {(1, 0), (4, 0), (3, 1), (0, 2), (5, 2)}

# Color contrast intensity for anchor/hero scoring
COLOR_CONTRAST = {
    "international_orange": 1.0,
    "celestial_blue":       0.8,
    "chrome_yellow":        0.7,
    "cod_gray":             0.4,
    "timberwolf":           0.2,
    "smoke_white":          0.15,
    "white":                0.1,
}

# Color temperature classification for zoning score
COLOR_TEMPERATURE = {
    "international_orange": "warm",
    "chrome_yellow":        "warm",
    "celestial_blue":       "cool",
    "timberwolf":           "cool",
    "cod_gray":             "neutral",
    "white":                "neutral",
    "smoke_white":          "neutral",
}

# Directional flow compatibility -- horizontal adjacency (A left of B)
HORIZONTAL_FLOW = {
    ("right", "right"):     0.9,
    ("right", "left"):      0.5,
    ("left",  "right"):     0.2,
    ("left",  "left"):      0.9,
    ("right", "neutral"):   0.7,
    ("neutral", "right"):   0.6,
    ("left",  "neutral"):   0.7,
    ("neutral", "left"):    0.6,
    ("right", "center"):    0.85,
    ("center", "right"):    0.5,
    ("left",  "center"):    0.5,
    ("center", "left"):     0.85,
    ("neutral", "neutral"): 0.6,
    ("center", "center"):   0.7,
    ("outward", "outward"): 0.4,
    ("center", "outward"):  0.3,
    ("outward", "center"):  0.3,
    ("outward", "neutral"): 0.5,
    ("neutral", "outward"): 0.5,
    ("up",   "up"):         0.8,
    ("down", "down"):       0.8,
    ("up",   "down"):       0.4,
    ("down", "up"):         0.4,
    ("up",   "neutral"):    0.65,
    ("down", "neutral"):    0.65,
    ("neutral", "up"):      0.65,
    ("neutral", "down"):    0.65,
}

# Directional flow -- vertical adjacency (A above B)
VERTICAL_FLOW = {
    ("down", "down"):       0.9,
    ("down", "up"):         0.5,
    ("up",   "down"):       0.2,
    ("up",   "up"):         0.9,
    ("down", "neutral"):    0.7,
    ("neutral", "down"):    0.6,
    ("up",   "neutral"):    0.7,
    ("neutral", "up"):      0.6,
    ("down", "center"):     0.85,
    ("center", "down"):     0.5,
    ("up",   "center"):     0.5,
    ("center", "up"):       0.85,
    ("neutral", "neutral"): 0.6,
    ("center", "center"):   0.7,
    ("outward", "outward"): 0.4,
    ("center", "outward"):  0.3,
    ("outward", "center"):  0.3,
    ("outward", "neutral"): 0.5,
    ("neutral", "outward"): 0.5,
    ("right", "right"):     0.8,
    ("left",  "left"):      0.8,
    ("right", "left"):      0.4,
    ("left",  "right"):     0.4,
    ("right", "neutral"):   0.65,
    ("left",  "neutral"):   0.65,
    ("neutral", "right"):   0.65,
    ("neutral", "left"):    0.65,
}

# Weight map composition templates (H=heavy, M=medium, L=light)
WEIGHT_MAP_TEMPLATES = {
    "diagonal_sweep": [
        ["L", "L", "M", "H", "M", "L"],
        ["L", "M", "H", "M", "L", "L"],
        ["M", "H", "M", "L", "L", "L"],
    ],
    "central_burst": [
        ["L", "M", "M", "M", "M", "L"],
        ["M", "H", "H", "H", "H", "M"],
        ["L", "M", "M", "M", "M", "L"],
    ],
    "corner_anchor": [
        ["H", "H", "M", "L", "L", "L"],
        ["H", "M", "L", "L", "L", "M"],
        ["M", "L", "L", "L", "M", "H"],
    ],
    "horizontal_banding": [
        ["H", "H", "H", "H", "H", "H"],
        ["L", "L", "L", "L", "L", "L"],
        ["M", "M", "M", "M", "M", "M"],
    ],
    "scattered_focal": [
        ["L", "M", "L", "L", "H", "L"],
        ["M", "L", "L", "M", "L", "M"],
        ["L", "L", "H", "L", "M", "L"],
    ],
}
WEIGHT_BAND_RANGES = {"H": (0.5, 1.0), "M": (0.25, 0.55), "L": (0.0, 0.35)}

# -- Rotation edge source mapping ------------------------------
# After rotation R, new edge P comes from original edge SOURCE[R][P].
EDGE_ROTATION_SOURCE = {
    0:   {"top": "top",    "right": "right",  "bottom": "bottom", "left": "left"},
    90:  {"top": "right",  "right": "bottom", "bottom": "left",   "left": "top"},
    180: {"top": "bottom", "right": "left",   "bottom": "top",    "left": "right"},
    270: {"top": "left",   "right": "top",    "bottom": "right",  "left": "bottom"},
}


def rotate_edges(edge_type: dict, coverage: dict, rotation: int) -> tuple[dict, dict]:
    src = EDGE_ROTATION_SOURCE[rotation]
    new_type = {e: edge_type[src[e]] for e in ("top", "right", "bottom", "left")}
    new_cov  = {e: coverage[src[e]]  for e in ("top", "right", "bottom", "left")}
    return new_type, new_cov


# -- Rotation patterns -----------------------------------------
# Each function (row, col) -> rotation index into ROTATIONS [0-3]
ROTATION_PATTERN_FNS: dict[str, Optional[callable]] = {
    "pinwheel":  lambda r, c: (r * 2 + c) % 4,
    "spiral":    lambda r, c: c % 4,
    "mirror":    lambda r, c: c % 4 if c < GRID_COLS // 2 else (GRID_COLS - 1 - c) % 4,
    "flow":      lambda r, c: (r + c) % 2 * 2,   # alternates 0 / 180
    "diagonal":  lambda r, c: (r + c) % 4,
    "checker90": lambda r, c: (r + c) % 2 * 2,
    "free":      None,
}

# -- Template configuration ------------------------------------
TEMPLATES = ["pinwheel", "spiral", "mirror", "flow", "focal", "scatter"]

TEMPLATE_CONFIG: dict[str, dict] = {
    "pinwheel":  {"primary_fam": (1, 2), "accent_fam": (0, 1), "rotation": "pinwheel",  "motif": True},
    "spiral":    {"primary_fam": (1, 2), "accent_fam": (0, 1), "rotation": "spiral",    "motif": True},
    "mirror":    {"primary_fam": (1, 2), "accent_fam": (0, 1), "rotation": "mirror",    "motif": True},
    "flow":      {"primary_fam": (1, 1), "accent_fam": (0, 2), "rotation": "flow",      "motif": True},
    "focal":     {"primary_fam": (2, 3), "accent_fam": (1, 2), "rotation": "free",      "motif": False},
    "scatter":   {"primary_fam": (2, 4), "accent_fam": (0, 2), "rotation": "free",      "motif": False},
}

TEMPLATE_ENERGY_WEIGHTS: dict[str, dict[str, int]] = {
    "low":    {"flow": 4, "mirror": 3, "pinwheel": 2, "spiral": 2, "focal": 1, "scatter": 0},
    "medium": {"pinwheel": 3, "flow": 3, "spiral": 3, "mirror": 2, "focal": 2, "scatter": 1},
    "high":   {"pinwheel": 3, "spiral": 3, "scatter": 3, "diagonal": 0, "focal": 2, "mirror": 2, "flow": 1},
}

# Families whose tiles are especially good for motif repetition (flowing shapes)
FLOW_FAMILIES = {"wave", "curve", "lines", "cascade", "ramp", "angle"}
# Families with strong geometric shapes good for pinwheel/spiral
GEOMETRIC_FAMILIES = {"square", "rectangle", "circle", "mirror", "float", "composition"}

ALL_COLOR_TOKENS   = list(BRAND_COLORS.keys())
COLOR_TOKEN_TO_HEX = BRAND_COLORS.copy()
TILE_FG_HEX        = "#121212"


# -- Data Classes ----------------------------------------------
@dataclass
class RotatedTile:
    tile: dict
    rotation: int
    edges: dict
    coverage: dict


@dataclass
class CellAssignment:
    col: int
    row: int
    tile_id: str
    tile_filename: str
    rotation: int
    fg_color: str
    bg_color: str
    fg_name: str
    bg_name: str


@dataclass
class BannerResult:
    output_path: Optional[str]
    seed: int
    energy: str
    template: str
    primary_families: list
    accent_families: list
    rotation_pattern: str
    continuity_strength: float
    dimensions: tuple
    color_bias: Optional[str]
    cells: list
    generated_at: str
    score: float = 0.0
    score_detail: dict = field(default_factory=dict)
    num_candidates: int = 1


# -- Manifest --------------------------------------------------
def load_manifest(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


# -- Rotated Tile Pool -----------------------------------------
def build_rotated_pool(tiles: list[dict]) -> list[RotatedTile]:
    """All (tile, rotation) candidates, de-duplicating symmetric rotations."""
    pool = []
    for tile in tiles:
        if tile.get("shape_family") == "lines" and "clear" in tile.get("id", ""):
            continue
        sym = tile.get("symmetry", "none")
        edge_type = tile.get("edge_type", {k: False for k in ("top", "right", "bottom", "left")})
        edge_cov  = tile.get("edge_coverage", {k: 0.0  for k in ("top", "right", "bottom", "left")})

        if sym == "both":
            rots = [0]
        elif sym in ("horizontal", "vertical"):
            rots = [0, 90]
        elif sym == "rotational":
            rots = [0, 90]
        else:
            rots = ROTATIONS

        for r in rots:
            re_type, re_cov = rotate_edges(edge_type, edge_cov, r)
            pool.append(RotatedTile(tile=tile, rotation=r, edges=re_type, coverage=re_cov))
    return pool


# -- Direction Inference ---------------------------------------
def infer_dominant_direction(tile: dict) -> str:
    """Infer the dominant visual direction from edge coverage data."""
    ec = tile.get("edge_coverage", {"top": 0, "right": 0, "bottom": 0, "left": 0})
    sym = tile.get("symmetry", "none")

    if sym == "both":
        return "neutral"

    t = ec.get("top", 0)
    r = ec.get("right", 0)
    b = ec.get("bottom", 0)
    le = ec.get("left", 0)
    total = t + r + b + le

    if total < 0.1:
        return "neutral"

    if sym == "vertical":
        v_bias = b - t
        return ("down" if v_bias > 0 else "up") if abs(v_bias) > 0.15 else "neutral"

    if sym == "horizontal":
        h_bias = r - le
        return ("right" if h_bias > 0 else "left") if abs(h_bias) > 0.15 else "neutral"

    h_bias = r - le
    v_bias = b - t

    if abs(h_bias) < 0.15 and abs(v_bias) < 0.15:
        if total > 2.5:
            return "outward"
        if total > 1.2:
            return "center"
        return "neutral"

    if abs(h_bias) >= abs(v_bias):
        return "right" if h_bias > 0 else "left"
    return "down" if v_bias > 0 else "up"


# -- Family focus selection ------------------------------------
def pick_family_focus(
    tiles: list[dict],
    template: str,
    rng: random.Random,
) -> tuple[list[str], list[str]]:
    """
    Select primary and accent shape families for this banner.

    For motif templates (pinwheel, spiral, mirror, flow):
      - 1-2 primary families -- nearly all tiles come from these
      - 0-1 accent families -- occasional contrast tile

    For spatial templates (focal, scatter):
      - 2-4 primary families -- broader variety
    """
    cfg = TEMPLATE_CONFIG[template]
    n_primary_lo, n_primary_hi = cfg["primary_fam"]
    n_accent_lo,  n_accent_hi  = cfg["accent_fam"]
    is_motif = cfg["motif"]

    # Build family pool
    family_tiles: dict[str, list] = {}
    for t in tiles:
        f = t.get("shape_family", "")
        if not f or (f == "lines" and "clear" in t.get("id", "")):
            continue
        family_tiles.setdefault(f, []).append(t)

    families = list(family_tiles.keys())
    # Weight by family size, bias toward flow/geometric families for motif templates
    weights = []
    for f in families:
        w = len(family_tiles[f])
        if is_motif:
            if f in FLOW_FAMILIES:
                w *= 2
            elif f in GEOMETRIC_FAMILIES:
                w *= 1.5
        weights.append(w)

    # Pick primary families
    n_primary = rng.randint(n_primary_lo, n_primary_hi)
    primary = []
    pool = list(zip(families, weights))
    while len(primary) < n_primary and pool:
        chosen = rng.choices([f for f, _ in pool], weights=[w for _, w in pool], k=1)[0]
        if chosen not in primary:
            primary.append(chosen)
        pool = [(f, w) for f, w in pool if f != chosen or len(primary) >= n_primary]
        if chosen in primary and len(primary) < n_primary:
            pool = [(f, w) for f, w in pool if f != chosen]

    # Pick accent families (different from primary)
    n_accent = rng.randint(n_accent_lo, n_accent_hi)
    accent_pool = [(f, len(family_tiles[f])) for f in families if f not in primary]
    accent = []
    for _ in range(n_accent):
        if not accent_pool:
            break
        chosen = rng.choices([f for f, _ in accent_pool], weights=[w for _, w in accent_pool], k=1)[0]
        accent.append(chosen)
        accent_pool = [(f, w) for f, w in accent_pool if f != chosen]

    return primary, accent


# -- Tile placement (family-focused, pattern-driven) -----------
def score_candidate(
    cand: RotatedTile,
    placed: dict,
    row: int, col: int,
    primary_families: list[str],
    accent_families: list[str],
    target_rotation: Optional[int],
    rotation_counts: dict,
    pos_weight: float = 1.0,
) -> float:
    score = 1.0
    family = cand.tile.get("shape_family", "")

    # -- Family focus scoring (the key driver) --
    if family in primary_families:
        score += 8.0
    elif family in accent_families:
        score += 2.0
    else:
        score -= 15.0   # Effectively excluded

    # -- Rotation scoring --
    if target_rotation is not None:
        # Pattern rotation: strong preference for exact match
        if cand.rotation == target_rotation:
            score += 5.0
        else:
            score -= 3.0
    else:
        # Free rotation: mild preference for less-used rotations
        cnt = rotation_counts.get(cand.rotation, 0)
        score += max(0.0, 2.0 - cnt * 0.5)

    # -- Edge matching with neighbours (lighter weight -- pattern dominates) --
    if col > 0 and (row, col - 1) in placed:
        left = placed[(row, col - 1)]
        if cand.edges["left"] and left.edges["right"]:
            score += 1.5 * (cand.coverage["left"] + left.coverage["right"]) / 2
        elif not cand.edges["left"] and not left.edges["right"]:
            score += 0.3
        else:
            score -= 0.3

    if row > 0 and (row - 1, col) in placed:
        top = placed[(row - 1, col)]
        if cand.edges["top"] and top.edges["bottom"]:
            score += 1.5 * (cand.coverage["top"] + top.coverage["bottom"]) / 2
        elif not cand.edges["top"] and not top.edges["bottom"]:
            score += 0.3
        else:
            score -= 0.3

    # -- Position weight (only meaningful for focal template) --
    tile_weight = cand.tile.get("visual_weight", 0.1)
    score += pos_weight * tile_weight

    return max(0.01, score)


def make_position_weights(template: str) -> list[float]:
    """Position weights for focal template (heavier tiles preferred at centre)."""
    weights = [1.0] * TOTAL_SLOTS
    if template == "focal":
        for pos in range(TOTAL_SLOTS):
            r, c = pos // GRID_COLS, pos % GRID_COLS
            dist = math.sqrt((c - 2.5) ** 2 + (r - 1.0) ** 2)
            weights[pos] = max(0.3, 2.5 - dist * 0.55)
    return weights


def scored_tile_placement(
    rotated_pool: list[RotatedTile],
    template: str,
    primary_families: list[str],
    accent_families: list[str],
    rng: random.Random,
    top_k: int = 12,
) -> list[dict]:
    """
    Place 18 tiles using family focus + rotation pattern.
    Returns list of {row, col, tile, rotation, edges, coverage}.
    """
    cfg = TEMPLATE_CONFIG[template]
    rot_fn = ROTATION_PATTERN_FNS.get(cfg["rotation"])
    pos_weights = make_position_weights(template)

    placed: dict[tuple, RotatedTile] = {}
    rotation_counts: dict[int, int] = {}
    result = []

    for pos in range(TOTAL_SLOTS):   # row-major
        row, col = pos // GRID_COLS, pos % GRID_COLS
        pw = pos_weights[pos]

        # Determine target rotation from pattern
        target_rotation = ROTATIONS[rot_fn(row, col)] if rot_fn is not None else None

        scores = [
            score_candidate(c, placed, row, col, primary_families, accent_families,
                            target_rotation, rotation_counts, pw)
            for c in rotated_pool
        ]

        # Weighted random from top-k
        indexed = sorted(enumerate(scores), key=lambda x: -x[1])[:top_k]
        top_i = [i for i, _ in indexed]
        top_s = [s for _, s in indexed]
        chosen_idx = rng.choices(top_i, weights=top_s, k=1)[0]
        chosen = rotated_pool[chosen_idx]

        placed[(row, col)] = chosen
        rotation_counts[chosen.rotation] = rotation_counts.get(chosen.rotation, 0) + 1

        result.append({
            "row": row, "col": col,
            "tile": chosen.tile,
            "rotation": chosen.rotation,
            "edges": chosen.edges,
            "coverage": chosen.coverage,
        })

    return result


# -- Color Pool ------------------------------------------------
def build_color_pool(
    energy: str,
    manifest: dict,
    rng: random.Random,
    color_bias: Optional[str] = None,
) -> list[dict]:
    spec = manifest["energy_levels"][energy]
    if energy == "low":
        return _build_low_palette(spec, rng, color_bias)
    elif energy == "medium":
        return _build_medium_palette(spec, rng, color_bias)
    else:
        return _build_high_palette(spec, rng, color_bias)


def _build_low_palette(spec, rng, bias):
    dominant = rng.choice(spec["required_dominant"])
    bg_pool = ["white", "smoke_white"] if dominant == "cod_gray" else ["cod_gray"]
    bg_dom = rng.choice(bg_pool)
    n_accent = rng.randint(*spec["accent_tile_range"])
    cells = [{"fg": dominant, "bg": bg_dom}] * (TOTAL_SLOTS - n_accent)
    cells += [{"fg": "international_orange", "bg": dominant}] * n_accent
    rng.shuffle(cells)
    return cells


def _build_medium_palette(spec, rng, bias):
    num_colors = rng.randint(*spec["color_count_range"])
    required = ["international_orange", "cod_gray"]
    pool = [c for c in ALL_COLOR_TOKENS if c not in required]
    rng.shuffle(pool)
    chosen = required + pool[:num_colors - len(required)]
    if bias and bias not in chosen:
        chosen[-1] = bias
    return _distribute_colors(chosen, TOTAL_SLOTS, spec["max_single_color_tiles"], spec["orange_tile_range"], rng)


def _build_high_palette(spec, rng, bias):
    num_colors = rng.randint(*spec["color_count_range"])
    required = ["international_orange", "celestial_blue", "chrome_yellow"]
    pool = [c for c in ALL_COLOR_TOKENS if c not in required]
    rng.shuffle(pool)
    chosen = required + pool[:num_colors - len(required)]
    if bias and bias not in chosen:
        chosen[-1] = bias
    return _distribute_colors(chosen, TOTAL_SLOTS, 5, spec["orange_tile_range"], rng, min_per_color=1)


def _distribute_colors(colors, total, max_per_color, orange_range, rng, min_per_color=0):
    counts = {c: min_per_color for c in colors}
    remaining = total - sum(counts.values())
    if "international_orange" in counts:
        tgt = rng.randint(*orange_range)
        add = max(0, tgt - counts["international_orange"])
        counts["international_orange"] += add
        remaining -= add
    while remaining > 0:
        cands = [c for c in colors if counts[c] < max_per_color] or list(colors)
        c = rng.choice(cands)
        counts[c] += 1
        remaining -= 1
    cells = []
    for fg_name, cnt in counts.items():
        for _ in range(cnt):
            cells.append({"fg": fg_name, "bg": _pick_contrasting_bg(fg_name, colors, rng)})
    rng.shuffle(cells)
    return cells


def _pick_contrasting_bg(fg_name, available, rng):
    fg_hex = COLOR_TOKEN_TO_HEX[fg_name]
    if fg_hex in WARM_COLORS or fg_name in ("international_orange", "chrome_yellow"):
        preferred = ["cod_gray", "white", "smoke_white"]
    elif fg_hex in COOL_COLORS:
        preferred = ["cod_gray", "white", "smoke_white", "international_orange"]
    elif fg_name == "cod_gray":
        preferred = ["white", "smoke_white", "international_orange"]
    elif fg_name in ("white", "smoke_white", "timberwolf"):
        preferred = ["cod_gray", "international_orange", "celestial_blue"]
    else:
        preferred = [c for c in available if c != fg_name]
    candidates = [c for c in preferred if c != fg_name] or \
                 [c for c in available if c != fg_name] or ["cod_gray"]
    return rng.choice(candidates)


# -- Adjacency Constraint -------------------------------------
def apply_adjacency_constraints(
    cells: list[dict],
    rng: random.Random,
    max_iter: int = 150,
) -> list[dict]:
    """Reorder cells to minimise same-fg adjacent pairs. Sets _row/_col."""
    grid = [list(cells[r * GRID_COLS:(r + 1) * GRID_COLS]) for r in range(GRID_ROWS)]
    for _ in range(max_iter):
        if _count_violations(grid) == 0:
            break
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                if _has_conflict(grid, r, c):
                    v_before = _count_violations(grid)
                    sr, sc = rng.randint(0, GRID_ROWS - 1), rng.randint(0, GRID_COLS - 1)
                    if (sr, sc) != (r, c):
                        grid[r][c], grid[sr][sc] = grid[sr][sc], grid[r][c]
                        if _count_violations(grid) >= v_before:
                            grid[r][c], grid[sr][sc] = grid[sr][sc], grid[r][c]
    result = []
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            item = dict(grid[r][c])
            item["_row"] = r
            item["_col"] = c
            result.append(item)
    return result


def _count_violations(grid):
    return sum(1 for r in range(GRID_ROWS) for c in range(GRID_COLS) if _has_conflict(grid, r, c))


def _has_conflict(grid, r, c):
    fg = grid[r][c]["fg"]
    return (c + 1 < GRID_COLS and grid[r][c + 1]["fg"] == fg) or \
           (r + 1 < GRID_ROWS and grid[r + 1][c]["fg"] == fg)


# -- Color Continuity ------------------------------------------
def build_continuity_pairs(
    placement: list[dict],
    continuity_strength: float,
    rng: random.Random,
) -> list[tuple]:
    """Pairs of adjacent cells where both tiles touch the shared edge."""
    grid = {(p["row"], p["col"]): p for p in placement}
    pairs = []
    for p in placement:
        r, c = p["row"], p["col"]
        if c + 1 < GRID_COLS and (r, c + 1) in grid:
            nb = grid[(r, c + 1)]
            if p["edges"]["right"] and nb["edges"]["left"]:
                if rng.random() < continuity_strength:
                    pairs.append(((r, c), (r, c + 1)))
        if r + 1 < GRID_ROWS and (r + 1, c) in grid:
            nb = grid[(r + 1, c)]
            if p["edges"]["bottom"] and nb["edges"]["top"]:
                if rng.random() < continuity_strength:
                    pairs.append(((r, c), (r + 1, c)))
    return pairs


def apply_color_continuity(
    color_cells: list[dict],
    continuity_pairs: list[tuple],
    rng: random.Random,
) -> list[dict]:
    """Force same fg for edge-matched pairs. Must be called after adjacency solver."""
    pos_map = {(c["_row"], c["_col"]): c for c in color_cells}
    for (r1, c1), (r2, c2) in continuity_pairs:
        ca = pos_map.get((r1, c1))
        cb = pos_map.get((r2, c2))
        if ca is None or cb is None:
            continue
        shared_fg = ca["fg"]
        if cb["fg"] != shared_fg:
            cb["fg"] = shared_fg
            if cb["bg"] == shared_fg:
                cb["bg"] = _pick_contrasting_bg(shared_fg, ALL_COLOR_TOKENS, rng)
    return color_cells


# -- Composition Scoring ---------------------------------------

def _get_adjacent_pairs(composition: dict) -> list[tuple]:
    """Return all horizontally and vertically adjacent cell pairs."""
    pairs = []
    for (c, r) in composition:
        if (c + 1, r) in composition:
            pairs.append(((c, r), (c + 1, r), "horizontal"))
        if (c, r + 1) in composition:
            pairs.append(((c, r), (c, r + 1), "vertical"))
    return pairs


def _get_neighbors(pos: tuple, composition: dict) -> list[tuple]:
    """Return grid positions of all neighbors of pos that exist in composition."""
    c, r = pos
    return [p for p in [(c - 1, r), (c + 1, r), (c, r - 1), (c, r + 1)]
            if p in composition]


def anchor_triangle_score(composition: dict) -> float:
    """Score: do high-intensity tiles form a well-distributed triangle?"""
    intensities = []
    for pos, cell in composition.items():
        vw = cell["tile"].get("visual_weight", 0.3)
        cc = COLOR_CONTRAST.get(cell["fg_name"], 0.3)
        intensities.append((pos, vw * cc))

    intensities.sort(key=lambda x: -x[1])
    anchors = [pos for pos, _ in intensities[:3]]

    if len(anchors) < 2:
        return 0.5

    # Check distribution across column thirds and rows
    col_thirds = [a[0] // 2 for a in anchors]  # 0-1->0, 2-3->1, 4-5->2
    rows = [a[1] for a in anchors]

    third_spread = len(set(col_thirds)) / min(3, len(anchors))
    row_spread = len(set(rows)) / min(3, len(anchors))

    # Penalize adjacent anchors
    adjacency_penalty = 0.0
    for i, a in enumerate(anchors):
        for b in anchors[i + 1:]:
            if abs(a[0] - b[0]) + abs(a[1] - b[1]) <= 1:
                adjacency_penalty += 0.2

    return max(0.0, min(1.0, (third_spread + row_spread) / 2 - adjacency_penalty))


def shape_repetition_score(composition: dict) -> float:
    """Score: rhythmic shape repetition (3-5 unique shapes ideal for 18 slots)."""
    shape_counts = Counter(cell["tile"]["id"] for cell in composition.values())
    n_unique = len(shape_counts)
    n_singletons = sum(1 for c in shape_counts.values() if c == 1)

    # Ideal: 3-5 unique shapes
    if 3 <= n_unique <= 5:
        unique_score = 1.0
    else:
        unique_score = max(0.0, 1.0 - abs(n_unique - 4) * 0.15)

    # Penalize excessive singletons
    singleton_penalty = max(0, (n_singletons - 2) * 0.2)

    return max(0.0, unique_score - singleton_penalty)


def directional_flow_score(composition: dict) -> float:
    """Score: directional sympathy between adjacent tiles."""
    pairs = _get_adjacent_pairs(composition)
    if not pairs:
        return 0.5

    scores = []
    for pos_a, pos_b, axis in pairs:
        dir_a = infer_dominant_direction(composition[pos_a]["tile"])
        dir_b = infer_dominant_direction(composition[pos_b]["tile"])
        lookup = HORIZONTAL_FLOW if axis == "horizontal" else VERTICAL_FLOW
        pair_score = lookup.get((dir_a, dir_b), 0.5)
        scores.append(pair_score)

    return sum(scores) / len(scores)


def weight_balance_score(composition: dict) -> float:
    """Score: even distribution of visual weight across rows and halves."""
    row_weights = [0.0] * GRID_ROWS
    left_weight, right_weight = 0.0, 0.0

    for (c, r), cell in composition.items():
        vw = cell["tile"].get("visual_weight", 0.3)
        row_weights[r] += vw
        if c < GRID_COLS // 2:
            left_weight += vw
        else:
            right_weight += vw

    max_row = max(row_weights)
    min_row = min(row_weights)
    row_ratio = min_row / max_row if max_row > 0 else 1.0
    row_score = min(1.0, row_ratio / 0.6)

    total = left_weight + right_weight
    if total > 0:
        lr_ratio = min(left_weight, right_weight) / max(left_weight, right_weight)
        lr_score = min(1.0, lr_ratio / 0.6)
    else:
        lr_score = 1.0

    return (row_score + lr_score) / 2


def negative_space_score(composition: dict) -> float:
    """Score: proportion and clustering of light/negative-space tiles."""
    light_positions = [
        pos for pos, cell in composition.items()
        if cell["tile"].get("visual_weight", 0.3) < 0.35
    ]
    n_light = len(light_positions)

    if 4 <= n_light <= 6:
        count_score = 1.0
    elif 3 <= n_light <= 7:
        count_score = 0.7
    else:
        count_score = max(0.0, 0.4 - abs(n_light - 5) * 0.1)

    if len(light_positions) >= 2:
        distances = []
        for i, a in enumerate(light_positions):
            for b in light_positions[i + 1:]:
                distances.append(abs(a[0] - b[0]) + abs(a[1] - b[1]))
        avg_dist = sum(distances) / len(distances)
        cluster_score = max(0.0, 1.0 - (avg_dist / 4.0))
    else:
        cluster_score = 0.5

    return (count_score + cluster_score) / 2


def color_temperature_score(composition: dict) -> float:
    """Score: spatial coherence of warm/cool color zones (not salt-and-pepper)."""
    warm_positions = [
        pos for pos, cell in composition.items()
        if COLOR_TEMPERATURE.get(cell["fg_name"]) == "warm"
    ]
    cool_positions = [
        pos for pos, cell in composition.items()
        if COLOR_TEMPERATURE.get(cell["fg_name"]) == "cool"
    ]

    def avg_internal_distance(positions):
        if len(positions) < 2:
            return 0.0
        dists = []
        for i, a in enumerate(positions):
            for b in positions[i + 1:]:
                dists.append(abs(a[0] - b[0]) + abs(a[1] - b[1]))
        return sum(dists) / len(dists)

    warm_cohesion = max(0.0, 1.0 - avg_internal_distance(warm_positions) / 4.0)
    cool_cohesion = max(0.0, 1.0 - avg_internal_distance(cool_positions) / 4.0)

    return (warm_cohesion + cool_cohesion) / 2


def shape_family_grouping_score(composition: dict) -> float:
    """Score: same-family tiles form loose clusters (~55% same-family adjacency)."""
    pairs = _get_adjacent_pairs(composition)
    if not pairs:
        return 0.5

    same_family = sum(
        1 for a, b, _ in pairs
        if composition[a]["tile"].get("shape_family") == composition[b]["tile"].get("shape_family")
    )
    ratio = same_family / len(pairs)

    # Bell curve centered on 0.55
    return max(0.0, 1.0 - ((ratio - 0.55) ** 2) * 10)


def hero_tile_score(composition: dict) -> float:
    """Score: one clear focal point in a strong position with neighbor contrast."""
    hero_pos = max(
        composition.keys(),
        key=lambda p: (
            composition[p]["fg_name"] == "international_orange",
            composition[p]["tile"].get("visual_weight", 0.0),
        ),
    )
    hero = composition[hero_pos]

    pos_score = 1.0 if hero_pos in POWER_POSITIONS else 0.5

    neighbors = _get_neighbors(hero_pos, composition)
    contrast_scores = []
    for n_pos in neighbors:
        neighbor = composition[n_pos]
        weight_diff = abs(
            hero["tile"].get("visual_weight", 0.3) -
            neighbor["tile"].get("visual_weight", 0.3)
        )
        color_diff = 1.0 if neighbor["fg_name"] != hero["fg_name"] else 0.0
        contrast_scores.append((weight_diff + color_diff) / 2)

    neighbor_score = (sum(contrast_scores) / len(contrast_scores)) if contrast_scores else 0.5

    return (pos_score + neighbor_score) / 2


def score_composition(composition: dict) -> tuple[float, dict]:
    """
    Score a candidate composition on 8 aesthetic axes.
    Returns (total_score, detail_dict).
    """
    detail = {
        "anchor":    anchor_triangle_score(composition),
        "rhythm":    shape_repetition_score(composition),
        "direction": directional_flow_score(composition),
        "weight":    weight_balance_score(composition),
        "negative":  negative_space_score(composition),
        "temp":      color_temperature_score(composition),
        "family":    shape_family_grouping_score(composition),
        "hero":      hero_tile_score(composition),
    }

    total = sum(SCORING_WEIGHTS[k] * v for k, v in detail.items())
    return total, detail


# -- Flat SVG Assembly -----------------------------------------
def parse_tile_svg(path: Path) -> etree._Element:
    return etree.parse(str(path), etree.XMLParser(remove_comments=True)).getroot()


def assemble_banner_svg(
    cells: list[CellAssignment],
    tiles_dir: Path,
    dimensions: tuple[int, int],
) -> etree._Element:
    """
    Compose a flat banner SVG (no nested <svg> elements):

      For each cell:
        <rect x y width height fill=bg/>          -- solid background
        <g transform="translate(x,y) scale(1.6) [rotate(N,100,100)]">
          <path d="..." fill=fg/>                  -- tile shape
        </g>

    The scale(1.6) maps tile viewBox [0,200] -> cell [0,320].
    Rotation is around tile centre (100,100) in tile space.
    """
    banner_w, banner_h = dimensions

    root = etree.Element("svg", attrib={
        "xmlns":   SVG_NS,
        "version": "1.1",
        "width":   str(banner_w),
        "height":  str(banner_h),
        "viewBox": f"0 0 {banner_w} {banner_h}",
    })

    tile_cache: dict[str, Optional[etree._Element]] = {}

    for cell in sorted(cells, key=lambda c: c.row * GRID_COLS + c.col):
        x = cell.col * CELL_W
        y = cell.row * CELL_H

        # Background
        etree.SubElement(root, "rect", attrib={
            "x": str(x), "y": str(y),
            "width": str(CELL_W), "height": str(CELL_H),
            "fill": cell.bg_color,
        })

        # Foreground path
        cache_key = cell.tile_filename
        if cache_key not in tile_cache:
            try:
                tile_cache[cache_key] = parse_tile_svg(tiles_dir / cell.tile_filename)
            except Exception:
                tile_cache[cache_key] = None

        tile_root = tile_cache[cache_key]
        if tile_root is None:
            continue

        path_elem = tile_root.find(f"{{{SVG_NS}}}path")
        if path_elem is None:
            continue   # empty tile (Clear)

        # Build flat transform: translate -> scale -> [rotate in tile space]
        scale = CELL_SCALE   # 1.6
        if cell.rotation != 0:
            transform = f"translate({x},{y}) scale({scale}) rotate({cell.rotation},100,100)"
        else:
            transform = f"translate({x},{y}) scale({scale})"

        g = etree.SubElement(root, "g", attrib={"transform": transform})
        path_copy = copy.deepcopy(path_elem)
        path_copy.set("fill", cell.fg_color)
        g.append(path_copy)

    return root


# -- Candidate Generation (data only) -------------------------
def _generate_candidate(
    manifest: dict,
    rotated_pool: list[RotatedTile],
    energy: str,
    rng: random.Random,
    color_bias: Optional[str],
    continuity_strength: float,
    template: Optional[str],
) -> dict:
    """Generate a single candidate composition (data only, no SVG rendering)."""
    # 1. Choose template
    if template:
        chosen_template = template
    else:
        weights_map = TEMPLATE_ENERGY_WEIGHTS[energy]
        tmps = [t for t in TEMPLATES if t in weights_map]
        wts = [weights_map[t] for t in tmps]
        chosen_template = rng.choices(tmps, weights=wts, k=1)[0]

    rotation_pattern = TEMPLATE_CONFIG[chosen_template]["rotation"]

    # 2. Pick family focus
    primary_families, accent_families = pick_family_focus(
        manifest["tiles"], chosen_template, rng
    )

    # 3. Place tiles
    placement = scored_tile_placement(
        rotated_pool, chosen_template, primary_families, accent_families, rng
    )
    placement_sorted = sorted(placement, key=lambda p: p["row"] * GRID_COLS + p["col"])
    placement_map = {(p["row"], p["col"]): p for p in placement_sorted}

    # 4. Build color pool and run adjacency solver
    color_cells = build_color_pool(energy, manifest, rng, color_bias)
    color_cells = apply_adjacency_constraints(color_cells, rng)

    # 5. Apply continuity (after positions are fixed)
    cont_pairs = build_continuity_pairs(placement_sorted, continuity_strength, rng)
    if cont_pairs:
        color_cells = apply_color_continuity(color_cells, cont_pairs, rng)

    # 6. Build unified composition dict for scoring and CellAssignment list
    composition = {}
    cell_assignments = []
    for item in color_cells:
        r, c = item["_row"], item["_col"]
        p = placement_map[(r, c)]
        fg_name, bg_name = item["fg"], item["bg"]

        composition[(c, r)] = {
            "tile": p["tile"],
            "rotation": p["rotation"],
            "fg_name": fg_name,
            "bg_name": bg_name,
        }

        cell_assignments.append(CellAssignment(
            col=c, row=r,
            tile_id=p["tile"]["id"],
            tile_filename=p["tile"]["filename"],
            rotation=p["rotation"],
            fg_color=COLOR_TOKEN_TO_HEX[fg_name],
            bg_color=COLOR_TOKEN_TO_HEX[bg_name],
            fg_name=fg_name,
            bg_name=bg_name,
        ))

    return {
        "template": chosen_template,
        "rotation_pattern": rotation_pattern,
        "primary_families": primary_families,
        "accent_families": accent_families,
        "continuity_strength": continuity_strength,
        "composition": composition,
        "cell_assignments": cell_assignments,
    }


# -- Core Generator --------------------------------------------
def generate_banner(
    manifest_path: Path = DEFAULT_MANIFEST,
    tiles_dir: Path = DEFAULT_TILES_DIR,
    energy: str = "medium",
    seed: Optional[int] = None,
    dimensions: tuple[int, int] = (1920, 960),
    color_bias: Optional[str] = None,
    continuity_strength: float = 0.7,
    template: Optional[str] = None,
    num_candidates: int = 50,
) -> tuple[BannerResult, etree._Element]:
    manifest = load_manifest(manifest_path)

    if seed is None:
        seed = random.randint(0, 2 ** 31 - 1)

    # Build rotated pool once (shared across all candidates)
    rotated_pool = build_rotated_pool(manifest["tiles"])

    # Generate and score candidates
    best = None
    best_score = -1.0
    best_detail = {}
    best_seed = seed

    for i in range(num_candidates):
        candidate_seed = seed + i
        rng = random.Random(candidate_seed)

        candidate = _generate_candidate(
            manifest, rotated_pool, energy, rng,
            color_bias, continuity_strength, template,
        )

        total, detail = score_composition(candidate["composition"])

        if total > best_score:
            best_score = total
            best_detail = detail
            best = candidate
            best_seed = candidate_seed

    # Assemble the best candidate into SVG
    banner_root = assemble_banner_svg(best["cell_assignments"], tiles_dir, dimensions)

    result = BannerResult(
        output_path=None,
        seed=best_seed,
        energy=energy,
        template=best["template"],
        primary_families=best["primary_families"],
        accent_families=best["accent_families"],
        rotation_pattern=best["rotation_pattern"],
        continuity_strength=best["continuity_strength"],
        dimensions=dimensions,
        color_bias=color_bias,
        cells=[asdict(c) for c in best["cell_assignments"]],
        generated_at=datetime.now(timezone.utc).isoformat(),
        score=round(best_score, 4),
        score_detail={k: round(v, 4) for k, v in best_detail.items()},
        num_candidates=num_candidates,
    )
    return result, banner_root


# -- Batch Generation ------------------------------------------
def generate_batch(
    n: int = 20,
    manifest_path: Path = DEFAULT_MANIFEST,
    tiles_dir: Path = DEFAULT_TILES_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    energy_mix: Optional[dict] = None,
    dimensions: tuple[int, int] = (1920, 960),
    starting_seed: Optional[int] = None,
    continuity_strength: float = 0.7,
    template: Optional[str] = None,
    num_candidates: int = 20,
) -> list[BannerResult]:
    if energy_mix is None:
        energy_mix = {"low": 0.3, "medium": 0.5, "high": 0.2}
    output_dir.mkdir(parents=True, exist_ok=True)

    allocations: list[str] = []
    for level, frac in energy_mix.items():
        allocations.extend([level] * round(n * frac))
    while len(allocations) < n:
        allocations.append("medium")
    allocations = allocations[:n]
    random.Random(starting_seed or 0).shuffle(allocations)

    results = []
    for i, energy_level in enumerate(allocations):
        seed = (starting_seed or 1000) + i * num_candidates
        result, banner_root = generate_banner(
            manifest_path=manifest_path,
            tiles_dir=tiles_dir,
            energy=energy_level,
            seed=seed,
            dimensions=dimensions,
            continuity_strength=continuity_strength,
            template=template,
            num_candidates=num_candidates,
        )
        fname = f"banner-{i+1:03d}-{energy_level}-{result.template}-s{result.seed}"
        svg_path = output_dir / f"{fname}.svg"
        svg_path.write_bytes(etree.tostring(banner_root, xml_declaration=True, encoding="UTF-8", pretty_print=True))
        result.output_path = str(svg_path)

        json_path = output_dir / f"{fname}.json"
        with open(json_path, "w") as f:
            json.dump(asdict(result), f, indent=2)

        results.append(result)
        if (i + 1) % 10 == 0 or (i + 1) == n:
            print(f"  Generated {i+1}/{n} (score: {result.score:.3f})")

    return results


# -- Main ------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="FAI Banner Generator v4")
    parser.add_argument("--energy", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--dimensions", type=int, nargs=2, default=[1920, 960])
    parser.add_argument("--color-bias", type=str, default=None)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--template", choices=TEMPLATES, default=None)
    parser.add_argument("--continuity-strength", type=float, default=0.7)
    parser.add_argument("--candidates", type=int, default=50,
                        help="Number of candidates to generate and score (default: 50)")

    parser.add_argument("--batch", type=int, default=None)
    parser.add_argument("--energy-mix", type=str, default=None)
    parser.add_argument("--starting-seed", type=int, default=None)

    parser.add_argument("--manifest",   type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--tiles-dir",  type=Path, default=DEFAULT_TILES_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)

    args = parser.parse_args()

    if args.batch:
        energy_mix = json.loads(args.energy_mix) if args.energy_mix else None
        print(f"Generating {args.batch} banners ({args.candidates} candidates each)...")
        results = generate_batch(
            n=args.batch,
            manifest_path=args.manifest,
            tiles_dir=args.tiles_dir,
            output_dir=args.output_dir,
            energy_mix=energy_mix,
            dimensions=tuple(args.dimensions),
            starting_seed=args.starting_seed,
            continuity_strength=args.continuity_strength,
            template=args.template,
            num_candidates=args.candidates,
        )
        print(f"\nBatch complete -> {args.output_dir}")
        tmpl_counts = Counter(r.template for r in results)
        fam_counts  = Counter(f for r in results for f in r.primary_families)
        scores = [r.score for r in results]
        print(f"Score range: {min(scores):.3f} - {max(scores):.3f} "
              f"(mean {sum(scores)/len(scores):.3f})")
        for t, c in sorted(tmpl_counts.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")
        print("Primary families:", dict(sorted(fam_counts.items(), key=lambda x: -x[1])[:8]))

    else:
        print(f"Generating banner (energy={args.energy}, seed={args.seed}, "
              f"candidates={args.candidates})...")
        result, banner_root = generate_banner(
            manifest_path=args.manifest,
            tiles_dir=args.tiles_dir,
            energy=args.energy,
            seed=args.seed,
            dimensions=tuple(args.dimensions),
            color_bias=args.color_bias,
            continuity_strength=args.continuity_strength,
            template=args.template,
            num_candidates=args.candidates,
        )

        out_dir = args.output_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        svg_path = Path(args.output) if args.output else \
                   out_dir / f"banner-{args.energy}-{result.template}-s{result.seed}.svg"
        svg_path.write_bytes(etree.tostring(banner_root, xml_declaration=True, encoding="UTF-8", pretty_print=True))
        result.output_path = str(svg_path)
        with open(svg_path.with_suffix(".json"), "w") as f:
            json.dump(asdict(result), f, indent=2)

        print(f"Banner:    {svg_path}")
        print(f"Template:  {result.template}  ({result.rotation_pattern} rotation)")
        print(f"Families:  primary={result.primary_families}  accent={result.accent_families}")
        print(f"Seed:      {result.seed}")
        print(f"Score:     {result.score:.4f}  (best of {result.num_candidates} candidates)")
        for axis, val in sorted(result.score_detail.items()):
            w = SCORING_WEIGHTS[axis]
            print(f"  {axis:12s} {val:.3f}  (x{w:.2f} = {val*w:.3f})")
        rot_counts = Counter(c["rotation"] for c in result.cells)
        print(f"Rotations: {dict(sorted(rot_counts.items()))}")
        fg_counts  = Counter(c["fg_name"] for c in result.cells)
        print("Fg colors:", dict(sorted(fg_counts.items(), key=lambda x: -x[1])))


if __name__ == "__main__":
    main()
