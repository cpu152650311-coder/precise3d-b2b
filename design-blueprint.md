# Design Blueprint — Precise3D B2B

## DESIGN READ
**设计定位:** B2B export website 面向 overseas distributors, retailers, and bulk procurement buyers, 采用 industrial precision + dark premium 设计风格, 强调 product-forward imagery, clean data presentation, and trust-building visual hierarchy.

## COLOR PALETTE

| Role | Hex | Usage |
|------|-----|-------|
| Primary (Deep Navy) | `#0B1120` | Page background, hero bg |
| Surface | `#111827` | Cards, sections |
| Surface Elevated | `#1E293B` | Hover cards, modals |
| Border Subtle | `#1F2A3D` | Dividers, card borders |
| Accent (Electric Blue) | `#2563EB` | Primary CTAs, links, highlights |
| Accent Glow | `#3B82F6` | Hover states, gradients |
| Accent Secondary (Teal) | `#06B6D4` | Secondary accents, data viz |
| Text Primary | `#F1F5F9` | Headings, body text |
| Text Muted | `#94A3B8` | Captions, metadata |
| Text Dim | `#64748B` | Placeholder, disabled |
| Success | `#10B981` | Stats, trust indicators |
| Warning | `#F59E0B` | Highlights, badges |

## TYPOGRAPHY

| Role | Stack | Weight |
|------|-------|--------|
| Display / H1 | `system-ui, -apple-system, 'Segoe UI', sans-serif` | 700 |
| H2–H3 | same | 600 |
| Body | same | 400 |
| Mono / Specs | `'SF Mono', 'Cascadia Code', 'Consolas', monospace` | 500 |
| Labels / Overline | `system-ui` | 500, letter-spacing: 0.05em |

Scale (desktop): 14/16/18/20/24/32/40/56/72px

## SPACING & RADIUS

- Grid: 8px base
- Section padding: 80px vertical
- Card padding: 32px
- Card radius: 12px
- Button radius: 8px
- Input radius: 6px

## PAGE COLLECTION (6 pages)

| # | Page | Route | Purpose |
|---|------|-------|---------|
| 1 | Home | `/index.html` | Hero, trust bar, featured products, stats, solutions preview, CTA |
| 2 | Products | `/products/index.html` | Full product catalog with specs table, comparison |
| 3 | About | `/about/index.html` | Company story, factory tour, certifications, OEM capabilities |
| 4 | Solutions | `/solutions/index.html` | Industry verticals, bulk programs, partner tiers |
| 5 | Contact | `/contact/index.html` | Inquiry form (name/email/message), office info |
| 6 | Blog | `/blog/index.html` | Blog framework placeholder |

## BLOCK MANIFEST

| Block | File | Purpose |
|-------|------|---------|
| header | `blocks/header.html` | Sticky nav with logo, links, CTA button |
| hero | `blocks/hero.html` | Full-viewport hero with product visual |
| features-grid | `blocks/features-grid.html` | Bento-style grid for key features |
| product-card | `blocks/product-card.html` | Reusable product card |
| stats-strip | `blocks/stats-strip.html` | Horizontal stat counters |
| cta-banner | `blocks/cta-banner.html` | Full-width CTA section |
| footer | `blocks/footer.html` | 4-column footer with links |

## IMAGE DIRECTION

**Style:** Clean industrial product photography. Dark backgrounds with rim lighting. Precision-focused compositions. Macro detail shots of printed objects. Modern factory environments with natural light. No people faces visible — hands/arms operating machines only.

**Color grade:** Cool blue tones, high contrast, deep shadows with crisp highlights.

**8 images planned:**
1. hero-product — 3D printer in dark studio, mid-print, dramatic rim light
2. product-a — Flagship model hero shot on dark surface
3. product-b — Mid-range model angled product shot
4. product-c — Entry-level model clean product shot
5. print-detail — Macro close-up of high-quality 3D printed object
6. factory-line — Modern manufacturing facility, assembly line
7. solution-edu — 3D printers in education/classroom setting
8. solution-proto — Engineering prototyping workspace with printer
