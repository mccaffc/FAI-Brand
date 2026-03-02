# FAI Brand: Design Reading List
## Historical sources, typographic concepts, and visual references
*Compiled February 2026*

---

This reading list covers the design traditions, specific techniques, and conceptual frameworks that FAI's brand draws from. It's organized from foundational theory to specific implementation techniques, so you can read it in order or jump to whatever's most immediately useful.

---

## 1. Swiss International Typographic Style

This is the bedrock. FAI's entire visual language — the grid systems, the flat geometry, the high-contrast palettes, the tension between structure and expression — comes from the Swiss school.

**Josef Müller-Brockmann, *Grid Systems in Graphic Design* (1981)**
The single most important book on this list. Müller-Brockmann codified the grid system that underlies basically all serious graphic design since the 1960s. The FAI brand book's own layout (three-column grid, systematic spacing, hierarchical header) is a direct descendant. This book covers not just *how* to build grids but *why* — the philosophical argument that systematic design communicates seriousness and reliability. The copy appears in your moodboard. Read the whole thing.

**Josef Müller-Brockmann, *Pioneer of Swiss Graphic Design* (ed. Lars Müller, 1995)**
A monograph of his work. The concert posters for the Zurich Tonhalle (1950s–70s) are the direct ancestors of FAI's illustration system — abstract geometric compositions in limited palettes that somehow feel both rigorous and alive. The Beethoven poster series in particular shows how a constrained shape vocabulary can generate infinite variation.

**Richard Hollis, *Swiss Graphic Design: The Origins and Growth of an International Style* (2006)**
The history. Covers how the Swiss style emerged from the Bauhaus, how it became the corporate standard for mid-century multinationals (especially American ones), and why it still works. This gives you the "why this and not something else" argument for FAI's aesthetic choices.

**Kerry William Purcell, *Josef Müller-Brockmann* (2006, Phaidon)**
More comprehensive monograph. Good for seeing the full range of his work beyond the famous posters.

---

## 2. IBM Corporate Design and Paul Rand

The choice of IBM Plex as FAI's body typeface family is not an accident — it connects FAI to the most influential corporate identity program in American history. Understanding that lineage helps you understand what the typeface is doing rhetorically.

**Paul Rand, *A Designer's Art* (1985)**
Rand designed the IBM logo and identity system. This book covers his philosophy: that good design is the synthesis of form and content, that simplicity is the result of reduction rather than starting simple, and that corporate identity should project intelligence and confidence without being cold. FAI's brand is trying to do the same thing for a think tank.

**Gordon Bruce, *Eliot Noyes* (2006, Phaidon)**
Noyes was IBM's Director of Design, the person who hired Rand and created the design culture at IBM. He argued that design quality signals organizational quality — that a company that cares about its letterhead probably cares about its products. This is the exact argument Chris needs to make at the retreat about why brand infrastructure matters for FAI.

**IBM Design Language (online: ibm.com/design/language)**
The contemporary IBM design system. IBM Plex was designed by Mike Abbink specifically for this system. The site documents how Plex works across contexts, the spacing and sizing rationale, and the design principles. It's also the best reference for how a "branded house" system works in practice — IBM's sub-brands (Watson, Cloud, etc.) maintain distinct personalities within a unified family, which is exactly the model the strategy brief proposes for FAI.

---

## 3. The Typefaces

### Schmalfette Grotesk

**Schmalfette Grotesk** is a revival/digitization of a 19th-century ultra-condensed grotesque. "Schmalfette" means "narrow-bold" in German. The original was a wood type face used for posters and headlines. The specific digital version FAI uses appears to be from a foundry revival (likely from a source like TypeType, though I'd want to confirm which cut you're using).

The important thing to understand about ultra-condensed grotesques: they emerged from the poster tradition where you needed to pack maximum text into minimum width while maintaining readability at distance. They're inherently loud — they demand attention. Using one as your display face (rather than, say, a refined didone or a geometric sans) is a deliberate choice to signal energy and urgency. It's the typographic equivalent of the "edgy institutional" positioning.

**Indra Kupferschmid, *Lettering and Type: Creating Letters for Various Purposes and Media* (2014)**
Good technical reference on condensed and display type, including the historical lineage of grotesques.

### IBM Plex

**IBM Plex Design Philosophy (ibm.com/plex)**
Plex was released as an open-source family in 2017 to replace Helvetica Neue as IBM's corporate typeface. It comes in Serif, Sans, Sans Condensed, and Mono variants — all designed to work together as a system. The Serif was specifically designed to feel "engineered" — warm but precise, which maps to the kind of authority a policy publication needs.

The key detail for implementation: Plex's metrics were designed around IBM's 2x grid system. The tracking, line-height, and sizing values in the FAI brand book (120%, 130%, 140% line-heights at specific sizes) are derived from this grid logic.

---

## 4. The Pentatonic Type Scale

This is the concept you mentioned wanting to understand better. Here's how it works:

In music, a pentatonic scale uses five notes per octave instead of seven (or twelve). The result is that any combination of notes sounds harmonious — you literally can't play a wrong note. The most common pentatonic scale is C-D-E-G-A (the black keys on a piano).

Applied to typography, a pentatonic scale means choosing exactly five type sizes and using *only* those sizes across all materials. No arbitrary 13pt here, 17pt there. Just five sizes that relate to each other in a proportional system, so any combination looks intentional.

FAI's five sizes, from the brand book: **36pt – 21pt – 12pt – 11pt – 10pt**

The ratios aren't a strict mathematical progression (like a modular scale), but they define functional roles:
- 36pt = display/pull quote (the loud note)
- 21pt = subhead (the bridge)
- 12pt = heading (the structural note)
- 11pt = body (the workhorse)
- 10pt = caption/footnote (the quiet note)

**Tim Brown, "More Meaningful Typography" (A List Apart, 2011)**
The foundational article on modular type scales for the web. Brown argues for deriving type sizes from musical intervals (perfect fourth, perfect fifth, etc.) so that the sizes relate to each other proportionally. FAI's scale isn't strictly modular, but this is the intellectual origin of the concept. Free online at alistapart.com.

**Robert Bringhurst, *The Elements of Typographic Style* (4th ed., 2012)**
The bible. Chapter 8 ("Shaping the Page") covers type scales in depth, including the historical scales used by Renaissance typographers. Bringhurst argues that type sizes should relate to each other the way musical intervals do — by rational proportions, not arbitrary choice. This is the book to read if you want to understand *why* five sizes feel right and six or seven don't.

**Spencer Mortensen, type-scale.com**
An interactive tool for building modular type scales. You can plug in a base size and a ratio (major third, perfect fourth, etc.) and see the resulting scale. Useful for checking whether FAI's five sizes approximate a known musical interval. (Spoiler: the 11pt→12pt step is very tight, suggesting the scale prioritizes functional needs over strict mathematical purity, which is fine.)

---

## 5. Color Systems: Shades and Tints

The brand book documents a systematic shades-and-tints scale for orange and gray but doesn't explain the underlying logic. Here's what's going on:

A **tint** is a color mixed with white (lighter). A **shade** is a color mixed with black (darker). A **tone** is a color mixed with gray. A systematic scale generates these in even increments — typically 10% steps — so you have a predictable gradient from the full-saturation base color to white (tints) or black (shades).

**Josef Albers, *Interaction of Color* (1963, reprinted with app, 2013)**
The foundational text on how colors behave relative to each other. Albers demonstrates that the same color looks completely different depending on what surrounds it — which is critical when you're placing International Orange on Cod Gray versus Pure White versus sky blue. The app version includes the interactive exercises from his Yale course.

**Ethan Schoonover, Solarized (ethanschoonover.com/solarized)**
Not a book — a color system. Solarized is a 16-color palette designed with precise L*a*b* relationships between every shade. It's the clearest example of a "systematic" approach to shades and tints: every color in the system has a mathematically defined relationship to every other color. FAI's shade/tint scales follow a similar logic (even if they were likely built by eye rather than by formula).

**Sarah Drasner, "A Nerd's Guide to Color on the Web" (CSS-Tricks, 2016)**
Practical guide to building color scales for digital use. Covers HSL vs. RGB vs. LAB approaches to generating tints and shades, and why naive "just add white" approaches produce muddy results. Useful for building out the extended palette for sub-brands.

**Refactoring UI by Adam Wathan & Steve Schoger (refactoringui.com)**
Chapter 2 ("Color") is the most practical guide to building a full shade/tint scale from a single base color. Their method: define your base, then create 9 shades from near-white to near-black, adjusting hue and saturation (not just lightness) at each step to keep the colors vibrant. This is likely the method you'd use to extend FAI's orange and gray scales into the blue, amber, and teal palettes.

---

## 6. Geometric Illustration and Pattern Systems

The FAI illustration library is built from a modular shape vocabulary. This approach has deep roots.

**Karl Gerstner, *Designing Programmes* (1964, reissued by Lars Müller, 2019)**
The intellectual foundation for parametric/systematic design. Gerstner argued that instead of designing individual solutions, you should design *systems* that generate solutions — which is exactly what FAI's base-shapes-to-compositions workflow does. The book includes his famous "morphological box" method for systematically combining design variables. This is the book that explains why your illustration system works the way it does.

**Bruno Munari, *Design as Art* (1966, Penguin)**
Munari explored geometric abstraction as communication. His work bridges fine art and design in the same way FAI's illustrations bridge decorative pattern and brand communication. Short, readable, full of ideas about how abstract shapes carry meaning.

**Armin Hofmann, *Graphic Design Manual: Principles and Practice* (1965)**
Hofmann's Basel school approach to building complex compositions from simple geometric primitives (point, line, plane). The exercises in this book are essentially a tutorial in how to think the way the FAI illustration system thinks: start with a circle, a rectangle, a line — then combine, repeat, overlap, invert.

**Ikko Tanaka (monograph, any collection)**
Japanese graphic designer who built a career on flat, geometric, limited-palette compositions. His work for the Nihon Buyo performance series uses the same visual logic as FAI's freestyle illustrations: bold organic/geometric shapes, tight palettes, high figure-ground contrast. The Issey Miyake collaboration that appears in your moodboard is a Tanaka reference (Kazumasa Nagai, actually, but in the same tradition).

---

## 7. The Punk/Post-Punk Poster Tradition

The moodboard prominently features concert posters for Television, New Order, Rancid, and Talking Heads. This isn't random — it signals that FAI's design language should feel alive, urgent, and slightly transgressive, even while being systematic. The Swiss grid meets the gig poster.

**Swissted by Mike Joyce (swissted.com / book, 2014)**
This is almost certainly a direct reference point for the moodboard. Joyce redesigned punk and indie rock concert posters in the Swiss International Style — literally mapping the two traditions onto each other. The Television and New Order posters in your moodboard may be from this project. It's the single best visual reference for the specific fusion FAI is going for.

**Rick Poynor, *No More Rules: Graphic Design and Postmodernism* (2003)**
Covers the tension between Swiss rationalism and the expressive/chaotic energy of punk and postmodern design. FAI's brand sits exactly at this intersection.

---

## 8. Brand Architecture and Systems Thinking

These aren't about aesthetics — they're about how to structure a multi-brand ecosystem, which is the organizational problem behind the visual one.

**David Aaker, *Brand Portfolio Strategy* (2004)**
The standard reference on brand architecture models: branded house, house of brands, endorsed brands, sub-brands. FAI needs a "branded house with flexible sub-brands" (per the strategy brief), and Aaker's framework gives you the vocabulary to discuss that with leadership.

**Michael Bierut, *How to* (2015)**
Bierut (Pentagram partner) on how to structure design systems for large organizations. Not theoretical — full of case studies about the actual decisions that go into building a brand system that scales. The MIT Media Lab identity case study is particularly relevant: it shows how a generative system (like FAI's illustration library) can unify a complex institution.

---

## 9. One-Person Design Department Survival

Since Chris is effectively running institutional-scale output solo:

**Dan Mall, *Design That Scales* (A Book Apart, 2022)**
How to build design systems that let one person (or a very small team) maintain consistency across a large organization. Covers tokens, components, and governance — exactly the infrastructure FAI needs.

**Brad Frost, *Atomic Design* (2016, free at atomicdesign.bradfrost.com)**
The atoms → molecules → organisms → templates → pages framework for building design systems from small reusable parts. The FAI illustration system already works this way (base shapes → compositions), but the principle needs to extend to templates, layouts, and documents.

---

## How to Use This List

If you read five things: Müller-Brockmann's *Grid Systems*, Bringhurst's *Elements of Typographic Style*, Gerstner's *Designing Programmes*, Tim Brown's "More Meaningful Typography" article, and the Refactoring UI color chapter.

If you read one thing: *Grid Systems in Graphic Design*. Everything else in FAI's visual language descends from it.

For the pentatonic scale specifically: the Tim Brown article, then Bringhurst chapter 8, then play with type-scale.com. You'll have it internalized in an afternoon.

For the shades-and-tints system specifically: the Refactoring UI color chapter is the fastest path. Albers is the deep understanding.
