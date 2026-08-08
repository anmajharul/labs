import os
import sys
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

def generate_svg_banner(
    image_path: str,
    output_svg_path: str,
    dark_mode: bool = True,
    name: str = "Majharul Islam",
    username: str = "anmajharul",
    role: str = "Transportation Researcher & Civil Engineer",
    location: str = "Dhaka, Bangladesh",
    education: str = "B.Sc. in Civil Eng. (BUBT)",
    status: str = "Modeling + Simulating + Publishing",
    toolchain: str = "PTV Vissim, Python, R, SPSS, C++",
    core_lang: str = "Python, R, C++, MATLAB, SQL",
    core_frontend: str = "HTML5, CSS3, JavaScript, React",
    core_backend: str = "FastAPI, Flask, Node.js",
    core_database: str = "PostgreSQL, SQLite, Pandas",
    core_infra: str = "Git, Docker, Vercel, Linux",
    grid_mail: str = "anmajharul.bd@gmail.com",
    grid_portfolio: str = "anmajharul.bd",
    grid_linkedin: str = "linkedin.com/in/anmajharul",
    grid_github: str = "github.com/anmajharul",
    grid_facebook: str = "facebook.com/anmajharul"
):
    # Palette definition
    if dark_mode:
        bg_color = "#0A101F"
        chrome_color = "#22D3EE"
        portrait_color = "#A78BFA"
        accent_color = "#10B981"
        text_dim = "#94A3B8"
        text_bright = "#F8FAFC"
        panel_bg = "#0F172A"
        border_color = "#1E293B"
    else:
        bg_color = "#F8FAFC"
        chrome_color = "#0891B2"
        portrait_color = "#7C3AED"
        accent_color = "#059669"
        text_dim = "#64748B"
        text_bright = "#0F172A"
        panel_bg = "#FFFFFF"
        border_color = "#E2E8F0"

    # Process portrait image
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    img_cropped = img.crop((left, top, left + min_dim, top + min_dim))
    
    output_width = 300
    output_height = 340
    img_resized = img_cropped.resize((output_width, output_height), Image.Resampling.LANCZOS)
    
    gray = img_resized.convert("L")
    enhancer = ImageEnhance.Contrast(gray)
    gray_sharp = enhancer.enhance(1.4).filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    arr = np.array(gray_sharp, dtype=float)

    if dark_mode:
        # Clear background threshold for dark mode
        rgb_arr = np.array(img_resized, dtype=float)
        bg_color_sample = np.mean(rgb_arr[:15, :15], axis=(0, 1))
        dist = np.sqrt(np.sum((rgb_arr - bg_color_sample)**2, axis=2))
        mask = dist > 30.0
        mask_img = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
        mask_arr = np.array(mask_img, dtype=float) / 255.0
        arr = arr * mask_arr

    # Dithering
    h_grid, w_grid = arr.shape
    dithered = np.zeros((h_grid, w_grid), dtype=int)
    err_matrix = arr.copy()
    
    for y in range(h_grid):
        x_range = range(w_grid) if y % 2 == 0 else range(w_grid - 1, -1, -1)
        direction = 1 if y % 2 == 0 else -1
        for x in x_range:
            old_val = err_matrix[y, x]
            new_val = 255 if old_val > 120 else 0
            dithered[y, x] = 1 if new_val == 255 else 0
            err = old_val - new_val
            if 0 <= x + direction < w_grid:
                err_matrix[y, x + direction] += err * (7.0 / 16.0)
            if y + 1 < h_grid:
                if 0 <= x - direction < w_grid:
                    err_matrix[y + 1, x - direction] += err * (3.0 / 16.0)
                err_matrix[y + 1, x] += err * (5.0 / 16.0)
                if 0 <= x + direction < w_grid:
                    err_matrix[y + 1, x + direction] += err * (1.0 / 16.0)

    # Build SVG path runs for portrait dots
    rect_width = 380
    rect_height = 480
    start_x = 40
    start_y = 90
    
    dx = rect_width / w_grid
    dy = rect_height / h_grid
    
    path_d_list = []
    for y in range(h_grid):
        for x in range(w_grid):
            val = dithered[y, x]
            # Dark mode: draw lit pixels (1), Light mode: draw dark pixels (0)
            target = 1 if dark_mode else 0
            if val == target:
                px = round(start_x + x * dx, 2)
                py = round(start_y + y * dy, 2)
                path_d_list.append(f"M{px},{py}h1v1h-1z")
                
    portrait_path_d = "".join(path_d_list)

    # SVG Metadata & Structure
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" width="100%" height="100%">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&amp;family=Inter:wght@400;600;700&amp;display=swap');
    .bg {{ fill: {bg_color}; }}
    .panel {{ fill: {panel_bg}; stroke: {border_color}; stroke-width: 1.5px; rx: 12px; }}
    .title-bar {{ font-family: 'Fira Code', monospace; font-size: 13px; font-weight: 600; fill: {text_dim}; }}
    .live-badge {{ font-family: 'Fira Code', monospace; font-size: 11px; font-weight: 700; fill: #EF4444; }}
    .live-dot {{ fill: #EF4444; }}
    .handle-pill {{ fill: {chrome_color}; rx: 12px; }}
    .handle-text {{ font-family: 'Fira Code', monospace; font-size: 13px; font-weight: 700; fill: {bg_color}; }}
    .section-hdr {{ font-family: 'Fira Code', monospace; font-size: 12px; font-weight: 700; fill: {chrome_color}; letter-spacing: 1px; }}
    .label-text {{ font-family: 'Fira Code', monospace; font-size: 13.5px; font-weight: 500; fill: {text_dim}; }}
    .value-text {{ font-family: 'Fira Code', monospace; font-size: 13.5px; font-weight: 600; fill: {text_bright}; }}
    .value-accent {{ font-family: 'Fira Code', monospace; font-size: 13.5px; font-weight: 600; fill: {accent_color}; }}
    .dotted-leader {{ stroke: {border_color}; stroke-dasharray: 2,4; stroke-width: 1.5px; }}
    .portrait-dot {{ fill: {portrait_color}; shape-rendering: crispEdges; }}
    @keyframes pulse {{
      0% {{ opacity: 1; }}
      50% {{ opacity: 0.3; }}
      100% {{ opacity: 1; }}
    }}
    .pulsing {{ animation: pulse 2s infinite ease-in-out; }}
  </style>

  <!-- Background Canvas -->
  <rect width="1180" height="610" class="bg" rx="16" />

  <!-- Terminal Window Chrome -->
  <rect x="15" y="15" width="1150" height="580" class="panel" />
  
  <!-- Window Header -->
  <circle cx="40" cy="42" r="6" fill="#EF4444" />
  <circle cx="58" cy="42" r="6" fill="#F59E0B" />
  <circle cx="76" cy="42" r="6" fill="#10B981" />
  
  <text x="105" y="46" class="title-bar">profile.sh --live</text>
  
  <!-- Pulsing LIVE Badge -->
  <circle cx="1020" cy="42" r="4" class="live-dot pulsing" />
  <text x="1032" y="46" class="live-badge">LIVE</text>
  
  <!-- Handle Pill -->
  <rect x="1075" y="28" width="75" height="26" class="handle-pill" />
  <text x="1112" y="45" text-anchor="middle" class="handle-text">@{username}</text>

  <!-- Horizontal Separator -->
  <line x1="15" y1="65" x2="1165" y2="65" stroke="{border_color}" stroke-width="1.5" />

  <!-- LEFT PANEL: VISUAL.MAP (Portrait Frame) -->
  <rect x="30" y="80" width="400" height="500" rx="8" fill="{bg_color}" stroke="{border_color}" stroke-width="1" />
  <text x="45" y="102" class="section-hdr">VISUAL.MAP // DITHERED PORTRAIT</text>
  
  <!-- Portrait Canvas Path -->
  <g transform="translate(10, 20)">
    <path d="{portrait_path_d}" class="portrait-dot" />
  </g>

  <!-- RIGHT PANEL: SYSTEM.INFO Readout -->
  <g transform="translate(460, 95)">
    <!-- SYSTEM READOUT HEADER -->
    <text x="0" y="10" class="section-hdr">SYSTEM.INFO // RESEARCH &amp; DEV SPECIFICATION</text>

    <!-- ROWS (y spacing: 25px) -->
    <!-- Row 1: Subject -->
    <text x="0" y="40" class="label-text">Subject</text>
    <line x1="80" y1="36" x2="480" y2="36" class="dotted-leader" />
    <text x="680" y="40" text-anchor="end" class="value-text" textLength="190" lengthAdjust="spacingAndGlyphs">{name}</text>

    <!-- Row 2: Role -->
    <text x="0" y="65" class="label-text">Role</text>
    <line x1="50" y1="61" x2="330" y2="61" class="dotted-leader" />
    <text x="680" y="65" text-anchor="end" class="value-accent" textLength="340" lengthAdjust="spacingAndGlyphs">{role}</text>

    <!-- Row 3: Origin -->
    <text x="0" y="90" class="label-text">Origin</text>
    <line x1="70" y1="86" x2="500" y2="86" class="dotted-leader" />
    <text x="680" y="90" text-anchor="end" class="value-text" textLength="170" lengthAdjust="spacingAndGlyphs">{location}</text>

    <!-- Row 4: Education -->
    <text x="0" y="115" class="label-text">Education</text>
    <line x1="95" y1="111" x2="430" y2="111" class="dotted-leader" />
    <text x="680" y="115" text-anchor="end" class="value-text" textLength="240" lengthAdjust="spacingAndGlyphs">{education}</text>

    <!-- Row 5: Status -->
    <text x="0" y="140" class="label-text">Status</text>
    <line x1="70" y1="136" x2="370" y2="136" class="dotted-leader" />
    <text x="680" y="140" text-anchor="end" class="value-accent" textLength="300" lengthAdjust="spacingAndGlyphs">{status}</text>

    <!-- Row 6: ToolChain -->
    <text x="0" y="165" class="label-text">ToolChain</text>
    <line x1="90" y1="161" x2="370" y2="161" class="dotted-leader" />
    <text x="680" y="165" text-anchor="end" class="value-text" textLength="300" lengthAdjust="spacingAndGlyphs">{toolchain}</text>

    <!-- STACK READOUT HEADER -->
    <text x="0" y="215" class="section-hdr">STACK.SPECS // TECH ARSENAL</text>

    <!-- Row 7: Languages -->
    <text x="0" y="245" class="label-text">Core.Lang</text>
    <line x1="95" y1="241" x2="420" y2="241" class="dotted-leader" />
    <text x="680" y="245" text-anchor="end" class="value-text" textLength="250" lengthAdjust="spacingAndGlyphs">{core_lang}</text>

    <!-- Row 8: Frontend -->
    <text x="0" y="270" class="label-text">Core.Frontend</text>
    <line x1="130" y1="266" x2="410" y2="266" class="dotted-leader" />
    <text x="680" y="270" text-anchor="end" class="value-text" textLength="260" lengthAdjust="spacingAndGlyphs">{core_frontend}</text>

    <!-- Row 9: Backend -->
    <text x="0" y="295" class="label-text">Core.Backend</text>
    <line x1="120" y1="291" x2="430" y2="291" class="dotted-leader" />
    <text x="680" y="295" text-anchor="end" class="value-text" textLength="240" lengthAdjust="spacingAndGlyphs">{core_backend}</text>

    <!-- Row 10: Database -->
    <text x="0" y="320" class="label-text">Core.Database</text>
    <line x1="130" y1="316" x2="440" y2="316" class="dotted-leader" />
    <text x="680" y="320" text-anchor="end" class="value-text" textLength="230" lengthAdjust="spacingAndGlyphs">{core_database}</text>

    <!-- Row 11: Infra -->
    <text x="0" y="345" class="label-text">Core.Infra</text>
    <line x1="105" y1="341" x2="460" y2="341" class="dotted-leader" />
    <text x="680" y="345" text-anchor="end" class="value-text" textLength="210" lengthAdjust="spacingAndGlyphs">{core_infra}</text>

    <!-- NETWORK READOUT HEADER -->
    <text x="0" y="395" class="section-hdr">GRID.NETWORK // ENDPOINTS</text>

    <!-- Row 12: Mail -->
    <text x="0" y="425" class="label-text">Grid.Mail</text>
    <line x1="95" y1="421" x2="420" y2="421" class="dotted-leader" />
    <text x="680" y="425" text-anchor="end" class="value-accent" textLength="250" lengthAdjust="spacingAndGlyphs">{grid_mail}</text>

    <!-- Row 13: Portfolio -->
    <text x="0" y="450" class="label-text">Grid.Portfolio</text>
    <line x1="140" y1="446" x2="520" y2="446" class="dotted-leader" />
    <text x="680" y="450" text-anchor="end" class="value-accent" textLength="150" lengthAdjust="spacingAndGlyphs">{grid_portfolio}</text>

    <!-- Row 14: LinkedIn -->
    <text x="0" y="475" class="label-text">Grid.LinkedIn</text>
    <line x1="130" y1="471" x2="430" y2="471" class="dotted-leader" />
    <text x="680" y="475" text-anchor="end" class="value-text" textLength="240" lengthAdjust="spacingAndGlyphs">{grid_linkedin}</text>
  </g>
</svg>'''

    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Exported SVG: {output_svg_path}")

if __name__ == "__main__":
    generate_svg_banner("anmajharul_photo.jpeg", "dark.svg", dark_mode=True)
    generate_svg_banner("anmajharul_photo.jpeg", "light.svg", dark_mode=False)
