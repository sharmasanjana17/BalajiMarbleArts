import os

BASE_DIR = r"c:\Users\Admin1\Desktop\Marble Contractor Site\brand_identity"

def ensure_dirs():
    dirs = [
        os.path.join(BASE_DIR, "final", "primary"),
        os.path.join(BASE_DIR, "final", "horizontal"),
        os.path.join(BASE_DIR, "final", "stacked"),
        os.path.join(BASE_DIR, "final", "icon"),
        os.path.join(BASE_DIR, "png"),
        os.path.join(BASE_DIR, "guidelines"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

# Shared definitions for Gradients
DEFS_GOLD = '''  <defs>
    <linearGradient id="goldLinear" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F4D89E" />
      <stop offset="25%" stop-color="#DFBA73" />
      <stop offset="50%" stop-color="#C6A15B" />
      <stop offset="75%" stop-color="#E5C583" />
      <stop offset="100%" stop-color="#9E7B35" />
    </linearGradient>
    <linearGradient id="goldVertical" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F7E2B5" />
      <stop offset="35%" stop-color="#DFBA73" />
      <stop offset="70%" stop-color="#C6A15B" />
      <stop offset="100%" stop-color="#8C6A24" />
    </linearGradient>
    <linearGradient id="goldSubtle" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#DFBA73" />
      <stop offset="50%" stop-color="#F4D89E" />
      <stop offset="100%" stop-color="#C6A15B" />
    </linearGradient>
    <filter id="subtleGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000000" flood-opacity="0.35" />
    </filter>
  </defs>'''

DEFS_DARK = '''  <defs>
    <linearGradient id="darkLinear" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2C2C2C" />
      <stop offset="50%" stop-color="#151515" />
      <stop offset="100%" stop-color="#0A0A0A" />
    </linearGradient>
  </defs>'''

DEFS_WHITE = '''  <defs>
    <linearGradient id="whiteLinear" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="60%" stop-color="#F4F0E7" />
      <stop offset="100%" stop-color="#E2DDD2" />
    </linearGradient>
  </defs>'''

# Monogram Symbol Geometry generator
def get_monogram_svg(mode="gold", scale=1.0, tx=0, ty=0):
    """
    Generates the pure vector symbol:
    - Base Plinth
    - Left Fluted Doric Pillar (Column)
    - Interlocking B Bowls
    - Central Keystone M Chevron
    - Architectural Capital
    - Diamond Accent Stones
    """
    if mode == "gold":
        fill_main = "url(#goldLinear)"
        fill_vert = "url(#goldVertical)"
        stroke_line = "#151515"
        stroke_hilight = "#F7E2B5"
        accent_color = "#F7E2B5"
        opacity_shadow = "0.55"
    elif mode == "dark":
        fill_main = "#151515"
        fill_vert = "#151515"
        stroke_line = "#FFFFFF"
        stroke_hilight = "#333333"
        accent_color = "#151515"
        opacity_shadow = "0.7"
    else: # white
        fill_main = "#FFFFFF"
        fill_vert = "#F4F0E7"
        stroke_line = "#151515"
        stroke_hilight = "#E8E2D5"
        accent_color = "#FFFFFF"
        opacity_shadow = "0.4"

    return f'''    <!-- Architectural Monogram Symbol (Doric Pillar & Keystone BM Monogram) -->
    <g transform="translate({tx}, {ty}) scale({scale})">
      <!-- Plinth Foundation Base -->
      <path d="M -95, 115 L 95, 115 L 85, 122 L -85, 122 Z" fill="{fill_main}" opacity="0.75" />
      <line x1="-70" y1="110" x2="70" y2="110" stroke="{fill_main}" stroke-width="2.5" stroke-linecap="round" />

      <!-- Left Architectural Pillar / Fluted Marble Column -->
      <!-- Column Base Plinth -->
      <path d="M -68, 105 L -36, 105 L -40, 95 L -64, 95 Z" fill="{fill_vert}" />
      <!-- Main Column Shaft -->
      <path d="M -64, 95 L -40, 95 L -40, -90 L -64, -90 Z" fill="{fill_vert}" />
      <!-- Flute Groove Lines -->
      <line x1="-56" y1="90" x2="-56" y2="-85" stroke="{stroke_line}" stroke-width="2" opacity="{opacity_shadow}" />
      <line x1="-48" y1="90" x2="-48" y2="-85" stroke="{stroke_hilight}" stroke-width="1.2" opacity="0.65" />
      <!-- Capital / Cornice -->
      <path d="M -68, -90 L -36, -90 L -32, -100 L -72, -100 Z" fill="{fill_vert}" />

      <!-- Central & Right Monogram Structure: Architectural 'B' & 'M' Chevron Slabs -->
      <!-- Top Geometric Arch / Upper Bowl of 'B' -->
      <path d="M -32, -90 
               L 28, -90 
               C 58, -90 76, -72 76, -42 
               C 76, -16 58, -2 30, -2 
               L -32, -2 Z
               M -16, -74
               L 24, -74
               C 44, -74 58, -62 58, -42
               C 58, -22 44, -18 24, -18
               L -16, -18 Z" 
            fill="{fill_main}" />

      <!-- Bottom Geometric Arch / Lower Bowl of 'B' (Interlocking with M) -->
      <path d="M -32, -2 
               L 36, -2 
               C 68, -2 88, 18 88, 52 
               C 88, 84 66, 104 32, 104 
               L -32, 104 Z
               M -16, 14
               L 30, 14
               C 50, 14 68, 28 68, 52
               C 68, 76 50, 88 30, 88
               L -16, 88 Z" 
            fill="{fill_vert}" />

      <!-- Center Architectural Keystone & Chiseled M-Chevron Inlay -->
      <path d="M -16, -2 
               L 18, -2 
               L 42, 38 
               L 66, -2 
               L 76, -2 
               L 46, 52 
               L 38, 52 Z" 
            fill="{fill_main}" opacity="0.95" />

      <!-- Fine Diamond Cut Accent Stones / Slab Joint Pins -->
      <polygon points="45,-98 52,-90 45,-82 38,-90" fill="{accent_color}" />
      <polygon points="45,108 52,116 45,124 38,116" fill="{accent_color}" />
    </g>'''

# 1. PRIMARY LOGO (Gold, Dark, White)
def build_primary_logo(mode="gold"):
    defs = DEFS_GOLD if mode == "gold" else (DEFS_DARK if mode == "dark" else DEFS_WHITE)
    monogram = get_monogram_svg(mode, scale=1.0, tx=450, ty=200)
    
    if mode == "gold":
        balaji_color = "url(#goldVertical)"
        sub_color = "#DFBA73"
        rule_color = "url(#goldSubtle)"
        diamond_color = "#F7E2B5"
    elif mode == "dark":
        balaji_color = "#151515"
        sub_color = "#2A2A2A"
        rule_color = "#151515"
        diamond_color = "#151515"
    else: # white
        balaji_color = "#FFFFFF"
        sub_color = "#F4F0E7"
        rule_color = "#FFFFFF"
        diamond_color = "#FFFFFF"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 620" width="100%" height="100%">
{defs}
  <!-- BALAJI MARBLE ARTS - PRIMARY LOGO ({mode.upper()}) -->
  <!-- Transparent Background for versatile production placement -->
  <g id="logo-root">
{monogram}

    <!-- Typography: BALAJI MARBLE ARTS -->
    <g transform="translate(450, 410)" text-anchor="middle">
      <!-- Brand Name: BALAJI -->
      <text y="0" 
            fill="{balaji_color}" 
            font-family="'Cinzel', 'Trajan Pro', 'Playfair Display', 'Georgia', serif" 
            font-size="62" 
            font-weight="700" 
            letter-spacing="18" 
            style="text-transform: uppercase;">BALAJI</text>

      <!-- Brand Specialty Tagline: MARBLE ARTS -->
      <text y="54" 
            fill="{sub_color}" 
            font-family="'Montserrat', 'Cinzel', 'Helvetica Neue', sans-serif" 
            font-size="19" 
            font-weight="500" 
            letter-spacing="14" 
            style="text-transform: uppercase;">MARBLE ARTS</text>

      <!-- Architectural Stone Divider Rules & Center Diamond -->
      <g transform="translate(0, 78)">
        <line x1="-220" y1="0" x2="-25" y2="0" stroke="{rule_color}" stroke-width="1.2" opacity="0.75" />
        <polygon points="0,-4 4,0 0,4 -4,0" fill="{diamond_color}" />
        <line x1="25" y1="0" x2="220" y2="0" stroke="{rule_color}" stroke-width="1.2" opacity="0.75" />
      </g>
    </g>
  </g>
</svg>'''

# 2. HORIZONTAL LOGO (Gold, Dark, White)
def build_horizontal_logo(mode="gold"):
    defs = DEFS_GOLD if mode == "gold" else (DEFS_DARK if mode == "dark" else DEFS_WHITE)
    monogram = get_monogram_svg(mode, scale=0.62, tx=130, ty=100)
    
    if mode == "gold":
        balaji_color = "url(#goldVertical)"
        sub_color = "#DFBA73"
        divider_color = "url(#goldVertical)"
        rule_color = "url(#goldSubtle)"
        diamond_color = "#F7E2B5"
    elif mode == "dark":
        balaji_color = "#151515"
        sub_color = "#2A2A2A"
        divider_color = "#151515"
        rule_color = "#151515"
        diamond_color = "#151515"
    else: # white
        balaji_color = "#FFFFFF"
        sub_color = "#F4F0E7"
        divider_color = "#FFFFFF"
        rule_color = "#FFFFFF"
        diamond_color = "#FFFFFF"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 200" width="100%" height="100%">
{defs}
  <!-- BALAJI MARBLE ARTS - HORIZONTAL LOGO ({mode.upper()}) -->
  <g id="logo-horizontal-root">
{monogram}

    <!-- Vertical Architectural Divider Line -->
    <line x1="230" y1="28" x2="230" y2="172" stroke="{divider_color}" stroke-width="1.5" opacity="0.45" />
    <polygon points="230,22 233,26 230,30 227,26" fill="{diamond_color}" />
    <polygon points="230,170 233,174 230,178 227,174" fill="{diamond_color}" />

    <!-- Typography Block -->
    <g transform="translate(265, 0)">
      <!-- Primary: BALAJI -->
      <text x="0" y="98" 
            fill="{balaji_color}" 
            font-family="'Cinzel', 'Trajan Pro', 'Playfair Display', 'Georgia', serif" 
            font-size="56" 
            font-weight="700" 
            letter-spacing="14" 
            style="text-transform: uppercase;">BALAJI</text>

      <!-- Sub: MARBLE ARTS -->
      <text x="2" y="142" 
            fill="{sub_color}" 
            font-family="'Montserrat', 'Cinzel', 'Helvetica Neue', sans-serif" 
            font-size="18" 
            font-weight="500" 
            letter-spacing="11" 
            style="text-transform: uppercase;">MARBLE ARTS</text>

      <!-- Sub Accent Rule -->
      <g transform="translate(2, 160)">
        <line x1="0" y1="0" x2="330" y2="0" stroke="{rule_color}" stroke-width="1.2" opacity="0.75" />
        <polygon points="340,0 344,-4 348,0 344,4" fill="{diamond_color}" />
      </g>
    </g>
  </g>
</svg>'''

# 3. STACKED LOGO (Gold, Dark, White)
def build_stacked_logo(mode="gold"):
    defs = DEFS_GOLD if mode == "gold" else (DEFS_DARK if mode == "dark" else DEFS_WHITE)
    monogram = get_monogram_svg(mode, scale=0.88, tx=350, ty=170)
    
    if mode == "gold":
        balaji_color = "url(#goldVertical)"
        sub_color = "#DFBA73"
        rule_color = "url(#goldSubtle)"
        diamond_color = "#F7E2B5"
    elif mode == "dark":
        balaji_color = "#151515"
        sub_color = "#2A2A2A"
        rule_color = "#151515"
        diamond_color = "#151515"
    else: # white
        balaji_color = "#FFFFFF"
        sub_color = "#F4F0E7"
        rule_color = "#FFFFFF"
        diamond_color = "#FFFFFF"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 560" width="100%" height="100%">
{defs}
  <!-- BALAJI MARBLE ARTS - STACKED LOGO ({mode.upper()}) -->
  <g id="logo-stacked-root">
{monogram}

    <!-- Typography: Centered Stacked -->
    <g transform="translate(350, 360)" text-anchor="middle">
      <!-- BALAJI -->
      <text y="0" 
            fill="{balaji_color}" 
            font-family="'Cinzel', 'Trajan Pro', 'Playfair Display', 'Georgia', serif" 
            font-size="54" 
            font-weight="700" 
            letter-spacing="16" 
            style="text-transform: uppercase;">BALAJI</text>

      <!-- MARBLE ARTS -->
      <text y="48" 
            fill="{sub_color}" 
            font-family="'Montserrat', 'Cinzel', 'Helvetica Neue', sans-serif" 
            font-size="17" 
            font-weight="500" 
            letter-spacing="12" 
            style="text-transform: uppercase;">MARBLE ARTS</text>

      <!-- Architectural Underline -->
      <g transform="translate(0, 68)">
        <line x1="-180" y1="0" x2="-20" y2="0" stroke="{rule_color}" stroke-width="1.2" opacity="0.75" />
        <polygon points="0,-4 4,0 0,4 -4,0" fill="{diamond_color}" />
        <line x1="20" y1="0" x2="180" y2="0" stroke="{rule_color}" stroke-width="1.2" opacity="0.75" />
      </g>
    </g>
  </g>
</svg>'''

# 4. ICON-ONLY MONOGRAM (Gold, Dark, White)
def build_icon_logo(mode="gold"):
    defs = DEFS_GOLD if mode == "gold" else (DEFS_DARK if mode == "dark" else DEFS_WHITE)
    monogram = get_monogram_svg(mode, scale=1.45, tx=256, ty=256)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
{defs}
  <!-- BALAJI MARBLE ARTS - ICON MONOGRAM ({mode.upper()}) -->
  <g id="icon-monogram-root">
{monogram}
  </g>
</svg>'''

# 5. LUXURY MEDALLION / BADGE MONOGRAM
def build_badge_logo():
    monogram = get_monogram_svg("gold", scale=1.05, tx=256, ty=256)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
{DEFS_GOLD}
  <defs>
    <path id="textCircleTop" d="M 70, 256 A 186 186 0 0 1 442, 256" fill="none" />
    <path id="textCircleBottom" d="M 442, 256 A 186 186 0 0 1 70, 256" fill="none" />
  </defs>

  <!-- Luxury Circular Medallion Background -->
  <circle cx="256" cy="256" r="250" fill="#151515" />

  <!-- Outer Double Gold Rim with Architectural Knurling -->
  <circle cx="256" cy="256" r="246" fill="none" stroke="url(#goldVertical)" stroke-width="3" />
  <circle cx="256" cy="256" r="236" fill="none" stroke="url(#goldLinear)" stroke-width="1.5" stroke-dasharray="2,5" />
  <circle cx="256" cy="256" r="218" fill="none" stroke="url(#goldVertical)" stroke-width="2" />

  <!-- Inner Medallion Border -->
  <circle cx="256" cy="256" r="156" fill="none" stroke="url(#goldSubtle)" stroke-width="1.5" opacity="0.8" />
  <circle cx="256" cy="256" r="150" fill="none" stroke="url(#goldLinear)" stroke-width="0.8" stroke-dasharray="3,3" opacity="0.6" />

  <!-- Cardinal Diamond Studs -->
  <polygon points="256,15 261,21 256,27 251,21" fill="#F7E2B5" />
  <polygon points="256,485 261,491 256,497 251,491" fill="#F7E2B5" />
  <polygon points="15,256 21,251 27,256 21,261" fill="#F7E2B5" />
  <polygon points="485,256 491,251 497,256 491,261" fill="#F7E2B5" />

  <!-- Circular Curved Embossed Typography -->
  <text fill="url(#goldLinear)" 
        font-family="'Cinzel', 'Trajan Pro', serif" 
        font-size="16.5" 
        font-weight="700" 
        letter-spacing="7">
    <textPath href="#textCircleTop" startOffset="50%" text-anchor="middle">BALAJI MARBLE ARTS</textPath>
  </text>

  <text fill="#DFBA73" 
        font-family="'Montserrat', sans-serif" 
        font-size="11" 
        font-weight="600" 
        letter-spacing="5">
    <textPath href="#textCircleBottom" startOffset="50%" text-anchor="middle">EST. 2026 • ARCHITECTURAL STONE</textPath>
  </text>

  <!-- Central Architectural Monogram -->
{monogram}
</svg>'''

def main():
    ensure_dirs()
    
    files = {
        # Primary
        os.path.join(BASE_DIR, "final", "primary", "balaji-logo-primary-gold.svg"): build_primary_logo("gold"),
        os.path.join(BASE_DIR, "final", "primary", "balaji-logo-primary-dark.svg"): build_primary_logo("dark"),
        os.path.join(BASE_DIR, "final", "primary", "balaji-logo-primary-white.svg"): build_primary_logo("white"),
        
        # Horizontal
        os.path.join(BASE_DIR, "final", "horizontal", "balaji-logo-horizontal-gold.svg"): build_horizontal_logo("gold"),
        os.path.join(BASE_DIR, "final", "horizontal", "balaji-logo-horizontal-dark.svg"): build_horizontal_logo("dark"),
        os.path.join(BASE_DIR, "final", "horizontal", "balaji-logo-horizontal-white.svg"): build_horizontal_logo("white"),
        
        # Stacked
        os.path.join(BASE_DIR, "final", "stacked", "balaji-logo-stacked-gold.svg"): build_stacked_logo("gold"),
        os.path.join(BASE_DIR, "final", "stacked", "balaji-logo-stacked-dark.svg"): build_stacked_logo("dark"),
        os.path.join(BASE_DIR, "final", "stacked", "balaji-logo-stacked-white.svg"): build_stacked_logo("white"),
        
        # Icon / Monogram
        os.path.join(BASE_DIR, "final", "icon", "balaji-monogram-gold.svg"): build_icon_logo("gold"),
        os.path.join(BASE_DIR, "final", "icon", "balaji-monogram-dark.svg"): build_icon_logo("dark"),
        os.path.join(BASE_DIR, "final", "icon", "balaji-monogram-white.svg"): build_icon_logo("white"),
        os.path.join(BASE_DIR, "final", "icon", "balaji-monogram-badge.svg"): build_badge_logo(),
    }
    
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated: {os.path.basename(path)}")

if __name__ == "__main__":
    main()

