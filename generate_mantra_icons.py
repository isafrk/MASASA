import os, base64
from PIL import Image, ImageDraw, ImageFont

# Create high-res 512x512 icon for Mantra Labs Financial
size = 512
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 1. Dark Obsidian Container with Gold/Amber border
corner_radius = 110
bg_color = (6, 6, 8, 255) # Deep Obsidian
draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=corner_radius, fill=bg_color)

# Outer Gold Accent Border
gold = (245, 166, 35, 255) # #f5a623
gold_soft = (245, 166, 35, 120)
draw.rounded_rectangle([(8, 8), (size - 9, size - 9)], radius=corner_radius - 8, outline=gold_soft, width=6)

# 2. Geometric Architectural "M" for MANTRA
# Draw stylized institutional chevron / double-pillar "M"
# Left pillar: (120, 360) -> (120, 150) -> (200, 150) -> (200, 360)
# Right pillar: (312, 360) -> (312, 150) -> (392, 150) -> (392, 360)
# Center V-keystone: (200, 150) -> (256, 250) -> (312, 150)

# Golden gradient lines for "M"
# Pillar 1
draw.polygon([(110, 370), (110, 140), (175, 140), (175, 370)], fill=gold)
# Pillar 2
draw.polygon([(337, 370), (337, 140), (402, 140), (402, 370)], fill=gold)
# Center diagonal left
draw.polygon([(175, 140), (256, 275), (290, 275), (175, 195)], fill=(255, 200, 80, 255))
# Center diagonal right
draw.polygon([(337, 140), (256, 275), (222, 275), (337, 195)], fill=(255, 200, 80, 255))

# Top Crown Diamond Accent
draw.polygon([(256, 110), (276, 135), (256, 160), (236, 135)], fill=(255, 255, 255, 255))

# Output icons
img_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
img_192.save("D:/PORTFOLIO_NEO_BRUTALISM/icon.png", format="PNG")
img_192.save("D:/PORTFOLIO_NEO_BRUTALISM/apple-touch-icon.png", format="PNG")
img_192.save("D:/PORTFOLIO_NEO_BRUTALISM/favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (192, 192)])

# SVG Vector
svg_code = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="mGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffd56b"/>
      <stop offset="100%" stop-color="#f5a623"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="110" fill="#060608"/>
  <rect x="8" y="8" width="496" height="496" rx="102" fill="none" stroke="#f5a623" stroke-width="6" stroke-opacity="0.5"/>
  <polygon points="110,370 110,140 175,140 175,370" fill="url(#mGold)"/>
  <polygon points="337,370 337,140 402,140 402,370" fill="url(#mGold)"/>
  <polygon points="175,140 256,275 290,275 175,195" fill="#ffe599"/>
  <polygon points="337,140 256,275 222,275 337,195" fill="#ffe599"/>
  <polygon points="256,110 276,135 256,160 236,135" fill="#ffffff"/>
</svg>'''

with open("D:/PORTFOLIO_NEO_BRUTALISM/icon.svg", "w", encoding="utf-8") as f:
    f.write(svg_code)

print("Mantra Labs Icon generated successfully!")
