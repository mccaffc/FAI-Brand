# FAI Brand Strategy Brief
## Cowork Handoff Document — February 2026

> **Purpose:** This document captures the findings from a comprehensive brand audit and strategic assessment of the Foundation for American Innovation (FAI), conducted in preparation for a leadership retreat. It is intended to serve as a project brief for continued work in Cowork, where Claude can help build out deliverables including a retreat presentation, brand system architecture, and implementation roadmap.

---

## 1. Project Context

### Who's driving this
**Chris McCaffery, Creative Director** at the Foundation for American Innovation. Chris manages all design and communications responsibilities: print design, brand management, publication oversight, event materials, and vendor coordination. He reports into a leadership team that includes:

- **Zach Graves** — Executive Director
- **Max Bodach** - Executive Vice President, also Chris' best friend, second in command at the organization 
- **David Bahr** — Managing Director of External Relations (final approval on standard design assets)
- **Rachel Altman** — Director of Outreach (handles social promotion of publications)

### What's happening
FAI's leadership retreat is in a few weeks. Chris is using this as the moment to prepare a strategic vision for reimagining FAI's brand and creative operations. The core argument: FAI has grown 4x in 18 months and now operates at a level of influence that its startup-era, tiny think-tank brand infrastructure doesn't reflect.

### The ask
Build the strategic framework — principles, deliverable taxonomy, system architecture, governance model, implementation roadmap — that Chris can use to prepare for the retreat and lead into a comprehensive brand refresh.

---

## 2. Organizational Background

### History
- **Founded 2014** as Lincoln Labs / Lincoln Network in Silicon Valley
- Originally a libertarian-leaning tech advocacy organization
- **Rebranded** to Foundation for American Innovation (date unclear, but "lincoln-network" LinkedIn handle and "joinlincoln.org" email artifacts remain)
- **501(c)(3) nonprofit**, now primarily DC-based with SF mailing address still in footer
- Has grown from small org to arguably the most influential tech-policy think tank on the right

### Current positioning
FAI occupies a genuinely distinctive niche: it bridges Silicon Valley and Washington, convenes tech founders and Senate committee chairs, throws raves at DC nightclubs and hosts Supreme Court scholars at academic symposia. Inc. Magazine profiled them as "the rave-throwing think tank shaping the tech-right."

### Recent influence markers
- Energy Secretary Chris Wright keynoted their summit
- Actively staffing Trump administration with tech-policy talent
- Defended DOE Loan Programs Office
- Inc. Magazine feature
- Y Combinator CEO and other Silicon Valley principals engage regularly
- Major institutional funders: Bradley Foundation, Walton Family, Scaife, Hewlett, Arnold Ventures, Stand Together

### Policy areas
AI, tech innovation, national security, governance/congressional reform, education, energy/infrastructure

### Programs & products
- **FAI Labs** — Technology tools (thefai.org/labs)
- **The Dynamist** — Podcast
- **The SCIF** — Newsletter
- **Policy Hackers** — Fellowship program
- **Schoolahoop** — School choice platform (spinning off)
- **Project Nickel** — Public school spending transparency
- **BIPBounty** — Bitcoin bug bounties
- **Reboot** — Annual conference (10th anniversary gala held Sept 2024, Fort Mason SF)
- **Energy Imperatives Summit** — Co-hosted with American Affairs, ACC

---

## 3. Brand Audit Findings

### 3.1 Website (thefai.org)

**Platform:** Next.js frontend, Sanity CMS backend

**Visual presentation:**
- Dark background, white text, FAI wordmark
- Hero tagline: "No Innovation without Representation"
- Sub-tagline: "We are technologists and policy entrepreneurs working to advance a more perfect union between technology and the American republic."
- Clean but generic — reads as "competent startup landing page" rather than "institution shaping federal policy"

**Structural issues:**
- Staff page loads dynamically, blank without JavaScript
- Footer prominently lists **San Francisco mailing address** (2443 Fillmore St) despite being DC-based
- Privacy policy still references **"joinlincoln.org"** email addresses
- LinkedIn link in footer goes to **/company/lincoln-network/** handle
- Publications appear as blog-style HTML posts with minimal distinctive design treatment
- Books section showcases associated titles but with standard e-commerce-style thumbnails

**Navigation structure:** About, Policy Areas, Publications, Programs, Donate

### 3.2 Sub-brands & Microsites

Each operates as an **independent visual entity** with no unified family relationship:

| Property | URL | Platform | Visual relationship to FAI |
|---|---|---|---|
| Energy Imperatives Summit | energyimperatives.org | WordPress (TEAMTRI.com vendor) | Independent logo, own visual language |
| Reboot conference | rebootconference.org | Unknown | Separate identity |
| The Dynamist podcast | Various platforms | N/A | Independent artwork per platform |
| A Future for the Family | Unknown | Unknown | Cross-institutional, own identity |
| FAI Labs | thefai.org/labs | Same CMS | Sub-page, minimal differentiation |
| Event pages | lu.ma | Luma | Default Luma branding |
| Bookshop | bookshop.org/shop/FAI | Bookshop.org | Third-party platform |

### 3.3 Social Media

| Platform | Handle/URL | Notes |
|---|---|---|
| X (Twitter) | @JoinFAI | "Join" framing reads as recruitment, not institutional |
| LinkedIn | /company/lincoln-network/ | **Still old brand name** |
| YouTube | @JoinFAI | Same "Join" framing |
| RSS | thefai.org/rss | Available |

Social graphics: Functional but not visually distinctive. No apparent template system or consistent visual language across platforms.

### 3.4 Publications

**Digital:** Primarily blog-style HTML on the website. Reports, commentary, and public filings are categorized but not visually differentiated. No unified publication design system.

**Print:** This is where Chris's typographic craft shows — recent and upcoming print work includes:
- Copyright Symposium Print Booklet (due Feb 27)
- Congress after Chevron symposium materials
- Various event programs

**Known gap:** Asana tasks confirm internal recognition that publication design needs systematization:
- "Design Review" task to audit publications for compliance with guidelines
- "Establish web-native paper template" (due March 31)
- "Brand Book Refresh" (due June 30)

### 3.5 Events

Events are FAI's highest-visibility touchpoint — what press and power-players actually see and experience:

- **Reboot: The New Reality** — 10th anniversary gala, Fort Mason SF, Sept 2024
- **Energy Imperatives Summit** — Co-hosted, multi-day policy summit
- **Nuclear rave** — Flash nightclub, Washington DC
- **Congress after Chevron** — Academic panels
- **Salon dinners** — Across SF, DC, NYC, Miami, Austin

Each event develops its own visual identity ad hoc rather than drawing from a coherent system. The Energy Imperatives Summit is particularly notable for having a fully independent visual language designed by an external vendor.

### 3.6 Legacy Artifacts

Remnants of the Lincoln Network era that haven't been cleaned up:
- LinkedIn handle: /company/lincoln-network/
- Privacy policy email: joinlincoln.org references
- Various historical references across the web
- "JoinFAI" handle framing (inherited from "JoinLincoln" convention?)

### 3.7 Google Drive Brand Materials

A Drive search for brand/style guide/logo assets returned:
- "Holy Family-Notre Dame logo" folder (personal project, not FAI)
- "AIG 2025 Logo" folder

No comprehensive FAI brand guidelines document was found in Drive, consistent with Chris's statement that brand guidelines were never completed.

---

## 4. Existing Internal Infrastructure

Chris has already built operational foundations that the brand system should integrate with:

### Design Asset Production SOP
- **Standard assets:** David Bahr gives final approval; Chris has creative autonomy
- **Elevated assets:** Zach and Max approve
- **Copy:** Robert and David handle

### Publications Process SOP
- Chris manages production
- Hannah Rowan handles copyediting
- Joey uploads to web
- Rachel Altman handles social promotion

### Other systems
- Printer turnaround data documented
- Vendor relationships tracked in Airtable
- Asana for task/project management (46 incomplete tasks as of early Feb 2026)

---

## 5. Strategic Assessment

### The core tension
FAI's **actual identity** — edgy, intellectually serious, convening Silicon Valley and Washington, throwing raves and hosting Supreme Court scholars — is far more interesting and distinctive than its current visual presentation communicates. The brand has the substance of a major policy institution but the visual infrastructure of a startup that hasn't gotten around to finishing its style guide.

### What the brand system needs to do

1. **Project institutional gravitas** commensurate with FAI's actual influence (Energy Secretaries, Senate committees, major foundation funding)
2. **Preserve the distinctive edge** that makes FAI different from every other DC think tank (the rave-throwing, tech-native, Silicon Valley DNA)
3. **Unify a sprawling ecosystem** of events, publications, programs, podcasts, and microsites into a recognizable family
4. **Scale with limited resources** — Chris is effectively a one-person creative department managing an institutional-scale output
5. **Work across wildly different contexts** — from a nuclear rave at a nightclub to a copyright law symposium to a donor report to a podcast thumbnail

### Key gaps to close

| Gap | Current state | Target state |
|---|---|---|
| Brand guidelines | Incomplete, never finished | Comprehensive brand book governing all touchpoints |
| Sub-brand architecture | Independent, unrelated visual identities | Defined family system (endorsed, co-branded, or sub-branded) |
| Publication design | Ad hoc, blog-style web + craft print | Unified system for web-native papers and print |
| Event branding | Ad hoc per event | Flexible system that allows event personality within family |
| Digital templates | None apparent | Social, presentation, newsletter, email templates |
| Website | Functional but generic | Distinctive, reflecting actual institutional caliber |
| Legacy cleanup | Lincoln Network artifacts persist | Complete migration to FAI identity |
| Donor/development materials | Unknown | Professional suite for major foundation relationships |

---

## 6. Recommended Strategic Framework

### Brand architecture model
FAI needs a **branded house with flexible sub-brands** — everything should be recognizably FAI, but events like Reboot and Energy Imperatives can have distinct personalities within the system. Think: how Google's material design system allows YouTube, Maps, and Gmail to feel different while being unmistakably Google.

### Proposed deliverable taxonomy

**Tier 1: Foundation (build first)**
- Completed brand guidelines / brand book
- Logo system (primary, secondary, sub-brand lockups)
- Color system (primary palette + extended palette for sub-brands/events)
- Typography system (primary + secondary faces, web + print specs)
- Voice and tone guidelines

**Tier 2: Core templates (build second)**
- Publication templates (web-native paper, print booklet, report)
- Presentation deck template (the FAI deck Chris is already updating)
- Social media templates (per platform)
- Email/newsletter template (The SCIF)
- Event branding toolkit (flexible system, not one-off designs)
- Letterhead, business cards, basic stationery

**Tier 3: Extended applications (build third)**
- Sub-brand guidelines (Reboot, Energy Imperatives, Dynamist, FAI Labs)
- Donor/development materials suite
- Swag and gift standards
- Environmental/event signage system
- Video/motion graphics standards
- Website redesign brief (informed by brand system)

### Governance model
- Chris retains creative autonomy per existing SOP
- Brand book becomes the reference standard for all external vendors
- New sub-brand or event identities require Chris's design review
- Annual brand audit (the "Design Review" task, formalized)

### Implementation roadmap (proposed)

| Phase | Timeline | Deliverables |
|---|---|---|
| **Retreat presentation** | Feb 2026 | Strategic framework, buy-in from leadership |
| **Brand book v1** | March–June 2026 | Core guidelines (aligns with June 30 Asana deadline) |
| **Template rollout** | April–July 2026 | Publication, social, presentation templates |
| **Sub-brand integration** | Summer 2026 | Reboot, Energy Imperatives, Dynamist aligned |
| **Website brief** | Fall 2026 | Redesign informed by completed brand system |
| **Full system live** | End of 2026 | All touchpoints operating within unified system |

---

## 7. Open Questions for Leadership

These are decisions Chris will need buy-in on at the retreat:

1. **Brand positioning statement:** Does leadership agree on the "edgy institutional" positioning, or do they want to tilt more toward traditional think tank gravitas?
2. **Sub-brand autonomy:** How much visual independence should events like Reboot and Energy Imperatives retain?
3. **Website:** Is a redesign on the table, or is the current site locked in for the near term?
4. **Budget:** What resources are available for the brand refresh — external design support, printing, vendor fees?
5. **Legacy cleanup:** Is there a plan to migrate the LinkedIn handle and clean up Lincoln Network artifacts?
6. **Naming conventions:** Should products like Schoolahoop and BIPBounty carry FAI branding as they mature?

---

## 8. Key Asana Tasks (Current)

For reference, these are the brand-related tasks already in Chris's Asana queue:

| Task | Due date | Status |
|---|---|---|
| Copyright Symposium Print Booklet | Feb 27, 2026 | In progress |
| Update FAI deck | Feb 27, 2026 | In progress |
| Design Review (publication audit) | TBD | Planned |
| Establish web-native paper template | March 31, 2026 | Planned |
| Brand Book Refresh | June 30, 2026 | Planned |

---

## Appendix: Sources Consulted

- thefai.org (full site crawl: homepage, about, publications, staff, privacy, terms)
- energyimperatives.org
- InfluenceWatch profile of FAI
- Inc. Magazine profile ("rave-throwing think tank")
- Apple Podcasts / Spotify (The Dynamist)
- Luma event pages
- LinkedIn (/company/lincoln-network/)
- X (@JoinFAI)
- Google Drive (brand/logo asset search)
- Asana task list (Chris's incomplete items)
- FAI's internal SOPs (Design Asset Production, Publications Process)

---

*Document generated February 5, 2026 from a Claude conversation with Chris McCaffery.*
*For questions about methodology or to request the original conversation transcript, contact Chris.*
