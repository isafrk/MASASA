# -*- coding: utf-8 -*-
"""
Fix all duplicate images on mantralabs.web.id index.html and individual article files.
Replaces the repeated red candlestick chart with 100% curated unique high-resolution images.
"""

import os
import re
import glob

INDEX_FILE = r"D:\PORTFOLIO_NEO_BRUTALISM\index.html"
ARTICLES_DIR = r"D:\PORTFOLIO_NEO_BRUTALISM\articles"

CURATED_IMAGES = [
    ("us-china", "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=800&q=80"), # Global currency & trade
    ("ai-hyperscaler", "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80"), # Semiconductor wafer microchip
    ("federal-reserve", "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=800&q=80"), # Wall street financial terminals
    ("institutional-etf", "https://images.unsplash.com/photo-1518546305927-5a555bb7020d?auto=format&fit=crop&w=800&q=80"), # Bitcoin dark vault coin
    ("india-approves", "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=800&q=80"), # High voltage power transmission lines
    ("silver-and-palladium", "https://images.unsplash.com/photo-1605792657660-596af9009e82?auto=format&fit=crop&w=800&q=80"), # Silver & precious metals
    ("italy-vs-france", "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=800&q=80"), # Stadium arena under lights
    ("who-pays-for-china", "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80"), # Industrial cargo container shipping
    ("my-friend-hates", "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=800&q=80"), # Modern professional workspace
    ("okxice", "https://images.unsplash.com/photo-1642543492481-44e81e3914a7?auto=format&fit=crop&w=800&q=80"), # Tokenized crypto trading terminal
    ("deutsche-bank", "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?auto=format&fit=crop&w=800&q=80"), # Institutional bank corporate tower
    ("decrypt", "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&w=800&q=80"), # Solana web3 digital asset network
    ("bitcoin-ripe", "https://images.unsplash.com/photo-1622979135225-d2ba269bc1df?auto=format&fit=crop&w=800&q=80"), # Crypto liquidity token
    ("grok-build", "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80"), # Cyber code leak telemetry
    ("plurai", "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=800&q=80"), # Autonomous AI neural network
    ("botpsy", "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80"), # Cyber edge compute processor
    ("softbank", "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80")  # Enterprise server data center facility
]

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Replace images card by card based on href
for key, img_url in CURATED_IMAGES:
    # Find card containing key
    pattern = rf'(<a href="[^"]*{key}[^"]*".*?)(<img src="[^"]*")'
    # In index.html img comes BEFORE the card title!
    # Card pattern: <div style="margin:-24px..."><img src="...photo-1611974789855...".*?<a href="[^"]*key[^"]*"
    card_regex = rf'(<img src=")[^"]*(" alt="[^"]*".*?<a href="/articles/[^"]*{key}[^"]*")'
    match = re.search(card_regex, html, re.DOTALL)
    if match:
        html = html[:match.start()] + match.group(1) + img_url + match.group(2) + html[match.end():]
        print(f"[✓] Replaced index image for: {key}")

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html successfully!")

# Also patch article files
for key, img_url in CURATED_IMAGES:
    for art_path in glob.glob(os.path.join(ARTICLES_DIR, f"*{key}*.html")):
        with open(art_path, "r", encoding="utf-8") as f:
            art_html = f.read()
        # Replace og:image and main img src
        art_html = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{img_url}">', art_html)
        art_html = re.sub(r'<img src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3[^"]*"', f'<img src="{img_url}"', art_html)
        with open(art_path, "w", encoding="utf-8") as f:
            f.write(art_html)
        print(f"[✓] Replaced article image in: {os.path.basename(art_path)}")
