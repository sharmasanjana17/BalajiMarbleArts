import os

def create_pdf(filename):
    pages_data = []

    # Helper to build page stream
    # PDF coordinates: (0, 0) is bottom-left, (612, 792) is standard Letter page
    
    # Page 1: COVER
    p1 = []
    # Dark Background
    p1.append("0.082 0.082 0.082 rg 0 0 612 792 re f")
    # Outer Gold Frame
    p1.append("0.776 0.631 0.357 RG 1.5 w 36 36 540 720 re S")
    p1.append("0.776 0.631 0.357 RG 0.5 w 42 42 528 708 re S")
    # Corner Diamonds
    for cx, cy in [(42, 42), (570, 42), (42, 750), (570, 750)]:
        p1.append(f"0.957 0.847 0.620 rg {cx} {cy+4} m {cx+4} {cy} l {cx} {cy-4} l {cx-4} {cy} l f")
    
    # Monogram Outline Graphic (Simplified Vector Representation in PDF)
    # Base Plinth
    p1.append("0.776 0.631 0.357 rg 256 500 100 8 re f")
    p1.append("0.957 0.847 0.620 rg 270 512 72 3 re f")
    # Pillar Shaft
    p1.append("0.776 0.631 0.357 rg 268 515 16 110 re f")
    p1.append("0.082 0.082 0.082 RG 1.5 w 276 520 m 276 615 l S")
    # Capital
    p1.append("0.776 0.631 0.357 rg 262 625 28 8 re f")
    # Arches
    p1.append("0.776 0.631 0.357 RG 8 w 284 570 m 320 570 336 585 336 600 c 336 615 320 625 284 625 c S")
    p1.append("0.776 0.631 0.357 RG 8 w 284 515 m 325 515 342 530 342 548 c 342 565 325 570 284 570 c S")
    # Keystone
    p1.append("0.957 0.847 0.620 rg 295 565 m 310 565 l 322 585 l 334 565 l 339 565 l 324 590 l 320 590 l f")

    # Typography
    p1.append("BT /F2 32 Tf 0.776 0.631 0.357 rg 140 400 Td (BALAJI MARBLE ARTS) Tj ET")
    p1.append("BT /F1 12 Tf 0.957 0.847 0.620 rg 185 370 Td (BRAND IDENTITY & DESIGN GUIDELINES) Tj ET")
    
    # Divider Rule
    p1.append("0.776 0.631 0.357 RG 1 w 150 345 m 462 345 l S")
    p1.append("0.957 0.847 0.620 rg 306 345 m 309 349 l 312 345 l 309 341 l f")

    # Subtext / Meta
    p1.append("BT /F1 10 Tf 0.8 0.8 0.8 rg 215 280 Td (VERSION 1.0  |  NOVEMBER 2026) Tj ET")
    p1.append("BT /F1 9 Tf 0.6 0.6 0.6 rg 170 260 Td (OFFICIAL CORPORATE & ARCHITECTURAL STANDARDS) Tj ET")
    p1.append("BT /F1 9 Tf 0.6 0.6 0.6 rg 195 90 Td (CONFIDENTIAL & PROPRIETARY DOCUMENT) Tj ET")
    p1.append("BT /F1 8 Tf 0.5 0.5 0.5 rg 210 75 Td (c 2026 BALAJI MARBLE ARTS. ALL RIGHTS RESERVED.) Tj ET")

    pages_data.append("\n".join(p1))

    # Page 2: BRAND STORY & 3 CONCEPTS EVALUATION
    p2 = []
    # Header
    p2.append("0.082 0.082 0.082 rg 0 740 612 52 re f")
    p2.append("BT /F2 16 Tf 0.776 0.631 0.357 rg 45 756 Td (BALAJI MARBLE ARTS) Tj ET")
    p2.append("BT /F1 10 Tf 0.957 0.847 0.620 rg 420 756 Td (SECTION 01: BRAND IDENTITY) Tj ET")
    p2.append("0.776 0.631 0.357 RG 1 w 0 740 m 612 740 l S")

    # Content
    p2.append("BT /F2 18 Tf 0.082 0.082 0.082 rg 45 690 Td (Brand Philosophy & Origin) Tj ET")
    p2.append("BT /F1 10 Tf 0.2 0.2 0.2 rg 45 665 Td (BALAJI MARBLE ARTS represents high-end natural stone contracting, architectural stonemasonry,) Tj ET")
    p2.append("BT /F1 10 Tf 0.2 0.2 0.2 rg 45 650 Td (and Italian marble / granite craftsmanship. The brand stands on three immutable pillars:) Tj ET")
    p2.append("BT /F2 10 Tf 0.776 0.631 0.357 rg 45 630 Td (PERMANENCE, ARCHITECTURAL BALANCE, and UNCOMPROMISING LUXURY.) Tj ET")

    p2.append("0.9 0.9 0.9 RG 1 w 45 610 m 567 610 l S")

    # Concept Comparison
    p2.append("BT /F2 15 Tf 0.082 0.082 0.082 rg 45 580 Td (Concept Development & Selection) Tj ET")
    p2.append("BT /F1 9.5 Tf 0.3 0.3 0.3 rg 45 558 Td (Three unique architectural directions were conceptualized and evaluated for the brand identity:) Tj ET")

    # Concept 1 Card (Winner)
    p2.append("0.95 0.93 0.89 rg 45 425 522 110 re f")
    p2.append("0.776 0.631 0.357 RG 1.5 w 45 425 522 110 re S")
    p2.append("BT /F2 12 Tf 0.776 0.631 0.357 rg 60 510 Td (CONCEPT 01: THE ARCHITECTURAL PILLAR & KEYSTONE MONOGRAM [SELECTED WINNER]) Tj ET")
    p2.append("BT /F1 9 Tf 0.2 0.2 0.2 rg 60 490 Td (Structure: Classical Doric fluted stone column integrated as the vertical stem of the letter 'B',) Tj ET")
    p2.append("BT /F1 9 Tf 0.2 0.2 0.2 rg 60 475 Td (intersecting an architectural chiseled keystone chevron forming the 'M' and subtle 'A' apex.) Tj ET")
    p2.append("BT /F1 9 Tf 0.2 0.2 0.2 rg 60 460 Td (Rationale: Highest timelessness, instantly recognizable, scalable from 16px to monumental facade) Tj ET")
    p2.append("BT /F1 9 Tf 0.2 0.2 0.2 rg 60 445 Td (signage, waterjet brass inlays, and stone embossing.) Tj ET")

    # Concept 2 Card
    p2.append("0.98 0.98 0.98 rg 45 320 522 85 re f")
    p2.append("0.85 0.85 0.85 RG 1 w 45 320 522 85 re S")
    p2.append("BT /F2 11 Tf 0.4 0.4 0.4 rg 60 385 Td (CONCEPT 02: THE GEOMETRIC BOOKMATCHED SLAB) Tj ET")
    p2.append("BT /F1 9 Tf 0.35 0.35 0.35 rg 60 368 Td (Structure: Symmetrical 45-degree mitered stone slabs forming an isometric diamond monogram.) Tj ET")
    p2.append("BT /F1 9 Tf 0.35 0.35 0.35 rg 60 353 Td (Evaluation: Ultra-modern and sleek, but leans slightly industrial/tiling rather than monumental) Tj ET")
    p2.append("BT /F1 9 Tf 0.35 0.35 0.35 rg 60 338 Td (architectural luxury craftsmanship.) Tj ET")

    # Concept 3 Card
    p2.append("0.98 0.98 0.98 rg 45 215 522 85 re f")
    p2.append("0.85 0.85 0.85 RG 1 w 45 215 522 85 re S")
    p2.append("BT /F2 11 Tf 0.4 0.4 0.4 rg 60 280 Td (CONCEPT 03: THE MONUMENTAL ROMAN ARCH) Tj ET")
    p2.append("BT /F1 9 Tf 0.35 0.35 0.35 rg 60 263 Td (Structure: Classical triumphal Roman vault framing intertwined serif B and M letterforms.) Tj ET")
    p2.append("BT /F1 9 Tf 0.35 0.35 0.35 rg 60 248 Td (Evaluation: Grand and ornamental, but high density reduces legibility on small-scale digital) Tj ET")
    p2.append("BT /F1 9 Tf 0.35 0.35 0.35 rg 60 233 Td (screens and favicons.) Tj ET")

    # Footer
    p2.append("BT /F1 8 Tf 0.5 0.5 0.5 rg 45 40 Td (BALAJI MARBLE ARTS  |  BRAND IDENTITY GUIDELINES) Tj ET")
    p2.append("BT /F1 8 Tf 0.5 0.5 0.5 rg 540 40 Td (PAGE 02) Tj ET")

    pages_data.append("\n".join(p2))

    # Page 3: ANATOMY & GEOMETRY
    p3 = []
    # Header
    p3.append("0.082 0.082 0.082 rg 0 740 612 52 re f")
    p3.append("BT /F2 16 Tf 0.776 0.631 0.357 rg 45 756 Td (BALAJI MARBLE ARTS) Tj ET")
    p3.append("BT /F1 10 Tf 0.957 0.847 0.620 rg 420 756 Td (SECTION 02: LOGO ANATOMY) Tj ET")
    p3.append("0.776 0.631 0.357 RG 1 w 0 740 m 612 740 l S")

    p3.append("BT /F2 18 Tf 0.082 0.082 0.082 rg 45 690 Td (Anatomy of the Monogram) Tj ET")
    p3.append("BT /F1 9.5 Tf 0.3 0.3 0.3 rg 45 668 Td (Every curve, stroke, and angle of the mark is derived from classical architectural proportions.) Tj ET")

    # Feature List
    features = [
        ("01. Fluted Doric Column (Left Stem)", "Forms the authoritative vertical spine of 'B', paying homage to Greek and Roman marble architecture."),
        ("02. Semicircular Vault Arches (Bowls of B)", "Twin geometric stone arches representing structural vaulting and the soft curves of polished marble edging."),
        ("03. Chiseled Keystone Chevron ('M' Inlay)", "The keystone locked between the arches forms the central V of 'M' and the apex of 'A' (Balaji Marble Arts)."),
        ("04. Architectural Capital & Cornice (Top)", "Beveled entablature at the top crowning the column, establishing monumental stability."),
        ("05. Heavy Plinth Foundation (Base)", "A grounded, weighted pedestal representing solid cut marble blocks and quarry permanence."),
        ("06. Dual Diamond Cut Joint Pins", "Two 45-degree diamond stone markers symbolizing precision stone joining and brass inlay craftsmanship.")
    ]

    y_pos = 620
    for title, desc in features:
        p3.append(f"0.776 0.631 0.357 rg 45 {y_pos+2} 6 6 re f")
        p3.append(f"BT /F2 11 Tf 0.082 0.082 0.082 rg 60 {y_pos} Td ({title}) Tj ET")
        p3.append(f"BT /F1 9 Tf 0.35 0.35 0.35 rg 60 {y_pos-16} Td ({desc}) Tj ET")
        p3.append(f"0.92 0.92 0.92 RG 0.5 w 45 {y_pos-26} m 567 {y_pos-26} l S")
        y_pos -= 50

    # Clearspace Guide
    p3.append(f"BT /F2 15 Tf 0.082 0.082 0.082 rg 45 {y_pos-10} Td (Clearspace & Minimum Sizing Rules) Tj ET")
    p3.append(f"BT /F1 9 Tf 0.3 0.3 0.3 rg 45 {y_pos-30} Td (To maintain visual dignity, always preserve an exclusion zone equal to 'X' (the height of the base plinth)) Tj ET")
    p3.append(f"BT /F1 9 Tf 0.3 0.3 0.3 rg 45 {y_pos-45} Td (around all four sides of the logo. No text, graphic, or trim line may encroach upon this clearspace.) Tj ET")

    p3.append(f"0.96 0.96 0.96 rg 45 {y_pos-120} 522 60 re f")
    p3.append(f"0.8 0.8 0.8 RG 1 w 45 {y_pos-120} 522 60 re S")
    p3.append(f"BT /F2 9.5 Tf 0.776 0.631 0.357 rg 60 {y_pos-75} Td (MINIMUM SIZES:) Tj ET")
    p3.append(f"BT /F1 9 Tf 0.2 0.2 0.2 rg 60 {y_pos-95} Td (Primary Logo: Print = 35mm wide | Digital = 140px wide) Tj ET")
    p3.append(f"BT /F1 9 Tf 0.2 0.2 0.2 rg 60 {y_pos-110} Td (Horizontal Logo: Print = 45mm wide | Digital = 160px wide | Monogram Icon: 24px) Tj ET")

    # Footer
    p3.append("BT /F1 8 Tf 0.5 0.5 0.5 rg 45 40 Td (BALAJI MARBLE ARTS  |  BRAND IDENTITY GUIDELINES) Tj ET")
    p3.append("BT /F1 8 Tf 0.5 0.5 0.5 rg 540 40 Td (PAGE 03) Tj ET")

    pages_data.append("\n".join(p3))

    # Page 4: COLOR PALETTE
    p4 = []
    # Header
    p4.append("0.082 0.082 0.082 rg 0 740 612 52 re f")
    p4.append("BT /F2 16 Tf 0.776 0.631 0.357 rg 45 756 Td (BALAJI MARBLE ARTS) Tj ET")
    p4.append("BT /F1 10 Tf 0.957 0.847 0.620 rg 420 756 Td (SECTION 03: COLOR SYSTEM) Tj ET")
    p4.append("0.776 0.631 0.357 RG 1 w 0 740 m 612 740 l S")

    p4.append("BT /F2 18 Tf 0.082 0.082 0.082 rg 45 690 Td (Official Brand Color Palette) Tj ET")
    p4.append("BT /F1 9.5 Tf 0.3 0.3 0.3 rg 45 668 Td (The palette is inspired by natural stone: Nero Marquina black marble, brass inlays, and white Statuario.) Tj ET")

    # Swatch 1: Obsidian Black
    p4.append("0.082 0.082 0.082 rg 45 530 115 110 re f")
    p4.append("0.776 0.631 0.357 RG 1 w 45 530 115 110 re S")
    p4.append("BT /F2 10 Tf 0.082 0.082 0.082 rg 175 625 Td (OBSIDIAN BLACK (PRIMARY DARK)) Tj ET")
    p4.append("BT /F1 8.5 Tf 0.3 0.3 0.3 rg 175 605 Td (HEX: #151515  |  RGB: 21, 21, 21) Tj ET")
    p4.append("BT /F1 8.5 Tf 0.3 0.3 0.3 rg 175 590 Td (CMYK: 70, 65, 60, 85  |  Pantone Black 6 C) Tj ET")
    p4.append("BT /F1 8 Tf 0.45 0.45 0.45 rg 175 570 Td (Usage: Backgrounds, luxury collateral, high-contrast black monochrome stamping.) Tj ET")

    # Swatch 2: Metallic Gold
    p4.append("0.776 0.631 0.357 rg 45 395 115 110 re f")
    p4.append("0.55 0.43 0.22 RG 1 w 45 395 115 110 re S")
    p4.append("BT /F2 10 Tf 0.082 0.082 0.082 rg 175 490 Td (METALLIC ANTIQUE GOLD (PRIMARY ACCENT)) Tj ET")
    p4.append("BT /F1 8.5 Tf 0.3 0.3 0.3 rg 175 470 Td (HEX: #C6A15B  |  RGB: 198, 161, 91) Tj ET")
    p4.append("BT /F1 8.5 Tf 0.3 0.3 0.3 rg 175 455 Td (CMYK: 20, 30, 75, 10  |  Pantone 465 C / 871 Metallic) Tj ET")
    p4.append("BT /F1 8 Tf 0.45 0.45 0.45 rg 175 435 Td (Usage: Primary emblem, foil stamping, CNC brass stone inlays, illuminated signage.) Tj ET")

    # Swatch 3: Champagne Gold Highlight
    p4.append("0.957 0.847 0.620 rg 45 260 115 110 re f")
    p4.append("0.776 0.631 0.357 RG 1 w 45 260 115 110 re S")
    p4.append("BT /F2 10 Tf 0.082 0.082 0.082 rg 175 355 Td (CHAMPAGNE GOLD (METALLIC HIGHLIGHT)) Tj ET")
    p4.append("BT /F1 8.5 Tf 0.3 0.3 0.3 rg 175 335 Td (HEX: #F4D89E  |  RGB: 244, 216, 158) Tj ET")
    p4.append("BT /F1 8.5 Tf 0.3 0.3 0.3 rg 175 320 Td (CMYK: 5, 15, 45, 0  |  Pantone 7506 C) Tj ET")
    p4.append("BT /F1 8 Tf 0.45 0.45 0.45 rg 175 300 Td (Usage: Gradient upper stops, bevel lighting, jewel accents.) Tj ET")

    # Swatch 4: Ivory Statuario
    p4.append("0.957 0.941 0.906 rg 45 125 115 110 re f")
    p4.append("0.8 0.8 0.8 RG 1 w 45 125 115 110 re S")
    p4.append("BT /F2 10 Tf 0.082 0.082 0.082 rg 175 220 Td (IVORY STATUARIO (LIGHT NEUTRAL)) Tj ET")
    p4.append("BT /F1 8.5 Tf 0.3 0.3 0.3 rg 175 200 Td (HEX: #F4F0E7  |  RGB: 244, 240, 231) Tj ET")
    p4.append("BT /F1 8.5 Tf 0.3 0.3 0.3 rg 175 185 Td (CMYK: 2, 3, 7, 0  |  Pantone Warm Gray 1 C) Tj ET")
    p4.append("BT /F1 8 Tf 0.45 0.45 0.45 rg 175 165 Td (Usage: Secondary text on dark backgrounds, luxury paper stocks, marble veining.) Tj ET")

    # Footer
    p4.append("BT /F1 8 Tf 0.5 0.5 0.5 rg 45 40 Td (BALAJI MARBLE ARTS  |  BRAND IDENTITY GUIDELINES) Tj ET")
    p4.append("BT /F1 8 Tf 0.5 0.5 0.5 rg 540 40 Td (PAGE 04) Tj ET")

    pages_data.append("\n".join(p4))

    # Page 5: TYPOGRAPHY & APPLICATION RULES
    p5 = []
    # Header
    p5.append("0.082 0.082 0.082 rg 0 740 612 52 re f")
    p5.append("BT /F2 16 Tf 0.776 0.631 0.357 rg 45 756 Td (BALAJI MARBLE ARTS) Tj ET")
    p5.append("BT /F1 10 Tf 0.957 0.847 0.620 rg 410 756 Td (SECTION 04: TYPOGRAPHY & RULES) Tj ET")
    p5.append("0.776 0.631 0.357 RG 1 w 0 740 m 612 740 l S")

    p5.append("BT /F2 18 Tf 0.082 0.082 0.082 rg 45 690 Td (Typography System) Tj ET")

    # Type 1
    p5.append("BT /F2 13 Tf 0.776 0.631 0.357 rg 45 660 Td (PRIMARY LOGOTYPE: CINZEL / TRAJAN PRO (BOLD SERIF)) Tj ET")
    p5.append("BT /F1 9 Tf 0.3 0.3 0.3 rg 45 642 Td (Characteristics: Classical Roman lapidary inscriptions, noble proportions, wide letter-spacing (+180).) Tj ET")
    p5.append("BT /F2 20 Tf 0.082 0.082 0.082 rg 45 615 Td (BALAJI) Tj ET")

    p5.append("0.9 0.9 0.9 RG 0.5 w 45 595 m 567 595 l S")

    # Type 2
    p5.append("BT /F2 13 Tf 0.776 0.631 0.357 rg 45 565 Td (SECONDARY SPECIALTY: MONTSERRAT / GEOMETRIC SANS) Tj ET")
    p5.append("BT /F1 9 Tf 0.3 0.3 0.3 rg 45 547 Td (Characteristics: Clean architectural modernist balance, all-caps, tracking (+140).) Tj ET")
    p5.append("BT /F1 14 Tf 0.776 0.631 0.357 rg 45 522 Td (MARBLE ARTS) Tj ET")

    p5.append("0.9 0.9 0.9 RG 0.5 w 45 500 m 567 500 l S")

    # Do's and Don'ts
    p5.append("BT /F2 15 Tf 0.082 0.082 0.082 rg 45 465 Td (Brand Integrity: Essential Do's and Don'ts) Tj ET")

    dos = [
        "DO use the official Gold gradient logo on obsidian black or dark stone surfaces.",
        "DO use the Black monochrome version for official letterheads, contracts, and light backgrounds.",
        "DO use the White / Ivory version over dark natural stone photography.",
        "DO ensure the exact spelling: BALAJI MARBLE ARTS."
    ]
    donts = [
        "DO NOT stretch, condense, skew, or distort the monogram geometry.",
        "DO NOT substitute the palette with bright non-stone colors (e.g., red, cyan, neon).",
        "DO NOT place the logo over busy, low-contrast patterned marble without a dark overlay.",
        "DO NOT alter the relative positioning between the monogram emblem and the logotype."
    ]

    # Do Box
    p5.append("0.95 0.97 0.95 rg 45 305 250 135 re f")
    p5.append("0.3 0.6 0.3 RG 1 w 45 305 250 135 re S")
    p5.append("BT /F2 11 Tf 0.2 0.5 0.2 rg 60 420 Td (PERMITTED USAGE (DO)) Tj ET")
    y_d = 400
    for d in dos:
        p5.append(f"BT /F1 7.5 Tf 0.2 0.2 0.2 rg 60 {y_d} Td (- {d}) Tj ET")
        y_d -= 22

    # Don't Box
    p5.append("0.98 0.94 0.94 rg 315 305 252 135 re f")
    p5.append("0.8 0.3 0.3 RG 1 w 315 305 252 135 re S")
    p5.append("BT /F2 11 Tf 0.7 0.2 0.2 rg 330 420 Td (PROHIBITED ALTERATIONS (DON'T)) Tj ET")
    y_d = 400
    for d in donts:
        p5.append(f"BT /F1 7.5 Tf 0.2 0.2 0.2 rg 330 {y_d} Td (- {d}) Tj ET")
        y_d -= 22

    # Architectural Signage
    p5.append("BT /F2 13 Tf 0.082 0.082 0.082 rg 45 260 Td (Architectural Signage & Material Specifications) Tj ET")
    p5.append("BT /F1 8.5 Tf 0.3 0.3 0.3 rg 45 240 Td (- Waterjet Brass Inlay: 3mm solid brass profile waterjet cut and flush-mounted into marble floor.) Tj ET")
    p5.append("BT /F1 8.5 Tf 0.3 0.3 0.3 rg 45 224 Td (- Laser Stone Engraving: 1.5mm chiseled V-groove with liquid gold enamel infill.) Tj ET")
    p5.append("BT /F1 8.5 Tf 0.3 0.3 0.3 rg 45 208 Td (- Exterior Showroom Signage: Brushed titanium gold stainless steel letters with 3000K warm LED halo.) Tj ET")

    # Summary box
    p5.append("0.082 0.082 0.082 rg 45 80 522 95 re f")
    p5.append("0.776 0.631 0.357 RG 1 w 45 80 522 95 re S")
    p5.append("BT /F2 11 Tf 0.776 0.631 0.357 rg 60 150 Td (MASTER ASSET DIRECTORY SUMMARY) Tj ET")
    p5.append("BT /F1 8.5 Tf 0.9 0.9 0.9 rg 60 132 Td (Primary SVGs: final/primary/ (Gold, Dark, White variations)) Tj ET")
    p5.append("BT /F1 8.5 Tf 0.9 0.9 0.9 rg 60 118 Td (Horizontal SVGs: final/horizontal/ (Navbar, signage, stationery headers)) Tj ET")
    p5.append("BT /F1 8.5 Tf 0.9 0.9 0.9 rg 60 104 Td (Stacked & Icon SVGs: final/stacked/, final/icon/ (Favicon, app icon, luxury circular medallion)) Tj ET")
    p5.append("BT /F1 8.5 Tf 0.9 0.9 0.9 rg 60 90 Td (High-Resolution Previews: png/ (All transparent background PNGs rendered at 300 DPI)) Tj ET")

    # Footer
    p5.append("BT /F1 8 Tf 0.5 0.5 0.5 rg 45 40 Td (BALAJI MARBLE ARTS  |  BRAND IDENTITY GUIDELINES) Tj ET")
    p5.append("BT /F1 8 Tf 0.5 0.5 0.5 rg 540 40 Td (PAGE 05) Tj ET")

    pages_data.append("\n".join(p5))

    # Compile PDF Objects
    objects = []
    
    # 1: Catalog
    # 2: Pages
    # 3: Font Helvetica
    # 4: Font Helvetica-Bold
    # 5: Font Times-Bold
    # 6..10: Page objects
    # 11..15: Content streams
    
    num_pages = len(pages_data)
    font_f1_id = 3
    font_f2_id = 4
    
    page_ids = [5 + i for i in range(num_pages)]
    content_ids = [5 + num_pages + i for i in range(num_pages)]
    
    kids_str = " ".join([f"{pid} 0 R" for pid in page_ids])
    
    pdf_objs = {}
    pdf_objs[1] = f"<< /Type /Catalog /Pages 2 0 R >>"
    pdf_objs[2] = f"<< /Type /Pages /Kids [{kids_str}] /Count {num_pages} >>"
    pdf_objs[3] = f"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    pdf_objs[4] = f"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"
    
    for i in range(num_pages):
        pid = page_ids[i]
        cid = content_ids[i]
        pdf_objs[pid] = f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents {cid} 0 R /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> >>"
        stream_bytes = pages_data[i].encode("latin1")
        pdf_objs[cid] = f"<< /Length {len(stream_bytes)} >>\nstream\n{pages_data[i]}\nendstream"
        
    # Write PDF bytes
    out = bytearray()
    out.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    
    offsets = {}
    for obj_id in sorted(pdf_objs.keys()):
        offsets[obj_id] = len(out)
        out.extend(f"{obj_id} 0 obj\n{pdf_objs[obj_id]}\nendobj\n".encode("latin1"))
        
    xref_offset = len(out)
    total_objs = max(pdf_objs.keys()) + 1
    out.extend(f"xref\n0 {total_objs}\n".encode("latin1"))
    out.extend(b"0000000000 65535 f \n")
    for obj_id in range(1, total_objs):
        off = offsets[obj_id]
        out.extend(f"{off:010d} 00000 n \n".encode("latin1"))
        
    out.extend(f"trailer\n<< /Size {total_objs} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("latin1"))
    
    with open(filename, "wb") as f:
        f.write(out)
        
    print(f"Generated PDF: {filename} ({len(out)} bytes)")

if __name__ == "__main__":
    out_pdf = r"c:\Users\Admin1\Desktop\Marble Contractor Site\brand_identity\guidelines\Balaji_Marble_Arts_Brand_Guidelines.pdf"
    create_pdf(out_pdf)

