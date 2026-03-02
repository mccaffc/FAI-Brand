# FAI Chart Design Guide
## Typography Hierarchy & Brand Colors for Data Visualization

*Quick reference for creating charts, graphs, and data visualizations*

---

## Brand Colors

### Primary Palette

Use these three colors as the foundation for all charts:

| Color Name | Hex Code | RGB | Usage in Charts |
|------------|----------|-----|-----------------|
| **International Orange** | `#FF4F00` | RGB(255, 79, 0) | Primary data series, emphasis bars, key metrics, call-outs |
| **Cod Gray** | `#121212` | RGB(18, 18, 18) | Dark backgrounds, axis lines, text labels on light backgrounds |
| **Pure White** | `#FFFFFF` | RGB(255, 255, 255) | Light backgrounds, text on dark backgrounds, gridlines (at low opacity) |

**Primary Color Notes:**
- **International Orange** is the signature color—energetic and attention-grabbing
- It's closer to a hazard sign than a sunset (saturated, forward-leaning)
- Use it sparingly for maximum impact in charts
- Not red, not vermillion, not burnt orange—the exact hex is `#FF4F00`

### Secondary & Tertiary Palette

For multi-series charts or when you need additional colors:

| Color Name | Suggested Hex | Usage |
|------------|---------------|-------|
| **Sky Blue** | `#4A90E2` (approximate) | Secondary data series, comparison metrics |
| **Amber/Golden Yellow** | `#F5A623` (approximate) | Tertiary data series, highlights |
| **Warm Gray** | `#6B6B6B` | Supporting data, less important series |
| **Teal** | `#50C5B7` (approximate) | Quaternary data series |

**Extended Palette Notes:**
- The brand book v03 doesn't codify exact hex values for secondary colors
- The values above are approximations based on the illustration system
- Use these for variety when showing multiple data series
- Maintain International Orange as the primary/most important series

### Color Order for Multi-Series Charts

When showing multiple data series, use this priority order:

1. **International Orange** (`#FF4F00`) — Most important data series
2. **Sky Blue** — Secondary series
3. **Amber/Golden Yellow** — Tertiary series
4. **Teal** — Quaternary series
5. **Warm Gray** — Supporting/comparison data

### Background Recommendations

**For presentations and screens:**
- Use **Cod Gray** (`#121212`) backgrounds with white text and orange accents
- Creates the distinctive FAI dark-mode aesthetic
- High contrast for readability in conference rooms

**For print and reports:**
- Use **Pure White** (`#FFFFFF`) backgrounds with Cod Gray text and orange accents
- Better for photocopying and long-form reading
- More conservative for policy documents

---

## Typography Hierarchy

### The Pentatonic Scale

FAI uses a **pentatonic type scale**—five predetermined sizes that work together harmoniously. Like the five notes of a musical scale, any combination looks intentional.

| Size (pt) | Line Height | Usage in Charts | Font Family | Weight |
|-----------|-------------|-----------------|-------------|--------|
| **36pt** | 120% (43pt) | Chart titles, main headlines | IBM Plex Serif | Bold |
| **21pt** | 130% (27pt) | Chart subtitles, section headers | IBM Plex Serif | Bold |
| **12pt** | 140% (17pt) | Axis titles, legend headers | IBM Plex Serif | Bold |
| **11pt** | 140% (15pt) | Data labels, body text annotations | IBM Plex Serif | Regular |
| **10pt** | 140% (14pt) | Axis labels, footnotes, data sources | IBM Plex Sans | Regular |

### Typeface Families

**IBM Plex Serif** — Primary typeface for charts
- Use for: titles, subtitles, axis titles, data labels
- Bold for emphasis (titles, headers)
- Regular for body text and annotations

**IBM Plex Sans** — Supporting typeface
- Use for: axis labels, footnotes, captions, data sources
- Provides contrast with serif headlines
- Better legibility at small sizes (10pt)

**Schmalfette Grotesk** — Display only (optional)
- Ultra-condensed grotesque
- Use ONLY for large-format poster charts or special presentations
- Not for standard business charts (too loud)
- Optical kerning, +20 tracking
- Limit to 2–3 lines, 2–3 words per line

### Typography Best Practices for Charts

**Titles (36pt or 21pt):**
```
36pt IBM Plex Serif Bold, 120% line-height
Keep to one line if possible
Use International Orange (#FF4F00) for emphasis words
```

**Axis Titles (12pt):**
```
12pt IBM Plex Serif Bold
Sentence case preferred over ALL CAPS
```

**Data Labels (11pt):**
```
11pt IBM Plex Serif Regular
Use when space allows
Directly label data points instead of relying solely on legend
```

**Axis Labels (10pt):**
```
10pt IBM Plex Sans Regular
Abbreviate long labels if needed
Rotate 45° for crowded horizontal axis labels
```

**Footnotes & Sources (10pt):**
```
10pt IBM Plex Sans Regular
Place at bottom-left of chart
Format: "Source: [Organization], [Year]"
```

---

## Chart-Specific Guidelines

### Bar Charts
- **Primary bars:** International Orange (`#FF4F00`)
- **Comparison bars:** Sky Blue or Warm Gray
- **Backgrounds:** White or Cod Gray depending on context
- **Gridlines:** Light gray (`#E0E0E0`) at 20% opacity on white; white at 10% opacity on dark
- **Data labels:** 11pt IBM Plex Serif Regular, placed at end of bar

### Line Charts
- **Primary line:** International Orange, 3pt stroke weight
- **Secondary lines:** Sky Blue, Teal, 2pt stroke weight
- **Gridlines:** Minimal, horizontal only
- **Markers:** Use circles (4pt diameter) at data points
- **Legend:** 12pt IBM Plex Serif Bold for headers, 11pt Regular for items

### Pie Charts
- **Order by size:** Largest slice at 12 o'clock, proceed clockwise
- **Color order:** International Orange → Sky Blue → Amber → Teal → Warm Gray
- **Labels:** Direct labels on slices when space allows (11pt)
- **Avoid:** More than 5 slices (use "Other" category)

### Area Charts
- **Fill opacity:** 60% for primary area, 40% for secondary areas
- **Border stroke:** 2pt solid in full-opacity color
- **Stacking:** Bottom-to-top priority: Orange → Blue → Amber → Teal

---

## Accessibility

### Color Contrast
All text must meet **WCAG AA standards** (4.5:1 contrast ratio minimum):

✅ **Good Combinations:**
- International Orange (`#FF4F00`) on White background: 3.9:1 ⚠️ (use for large text only)
- Cod Gray (`#121212`) on White background: 16.8:1 ✓
- White (`#FFFFFF`) on Cod Gray background: 16.8:1 ✓
- White on International Orange: 4.4:1 ✓ (large text)

⚠️ **Caution:**
- International Orange on white is borderline for body text
- For data labels in orange, use 12pt or larger
- Consider Cod Gray for better contrast on white backgrounds

### Color Blindness
- Don't rely on color alone to convey information
- Use patterns, labels, or shapes in addition to color
- Orange/Blue combination works well for deuteranopia (most common)
- Avoid red/green combinations entirely

---

## Examples

### Standard Chart Title Block

```
[36pt IBM Plex Serif Bold, #FF4F00]
Startup Investment Declined 40% in 2025

[21pt IBM Plex Serif Bold, #121212]
Venture capital funding across all sectors

[10pt IBM Plex Sans Regular, #6B6B6B]
Source: National Venture Capital Association, 2025
```

### Chart with Orange Accent

```
Title: 36pt IBM Plex Serif Bold, Cod Gray
Subtitle: 21pt IBM Plex Serif Bold, Cod Gray
Key stat in title: International Orange
Background: White
Primary data: International Orange bars
Comparison data: Sky Blue bars
Gridlines: Light gray, 20% opacity
Axis labels: 10pt IBM Plex Sans Regular
```

---

## Quick Checklist

Before finalizing any chart, verify:

- [ ] Using pentatonic scale sizes only (36, 21, 12, 11, 10pt)
- [ ] IBM Plex Serif for titles and labels
- [ ] IBM Plex Sans for axis labels and footnotes
- [ ] International Orange (`#FF4F00`) used strategically
- [ ] Cod Gray (`#121212`) or White background
- [ ] Sufficient color contrast (WCAG AA minimum)
- [ ] Direct labels on data when possible
- [ ] Source attribution at 10pt
- [ ] No more than 5 colors in chart
- [ ] Clean, uncluttered design with white space

---

## Tools & Resources

**Fonts:**
- IBM Plex available free from [IBM's GitHub](https://github.com/IBM/plex) or Google Fonts
- Schmalfette Grotesk (licensed, contact Chris for access)

**Color Pickers:**
- International Orange: `#FF4F00` / RGB(255, 79, 0)
- Cod Gray: `#121212` / RGB(18, 18, 18)

**Testing:**
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) for WCAG compliance
- [Coblis Color Blindness Simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/)

---

*For questions or to request chart templates, contact Chris McCaffery, Creative Director.*
