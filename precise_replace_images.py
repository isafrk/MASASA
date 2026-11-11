# -*- coding: utf-8 -*-
"""
Directly rebuild index.html cards with 100% unique curated images.
"""

INDEX_FILE = r"D:\PORTFOLIO_NEO_BRUTALISM\index.html"

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    html = f.read()

CARD_IMAGES = {
    "us-china-bilateral-dynamics": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=800&q=80",
    "ai-hyperscaler-capex-supercycle": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
    "federal-reserve-interest-rates": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=800&q=80",
    "bitcoin-etf-institutional-liquidity": "https://images.unsplash.com/photo-1518546305927-5a555bb7020d?auto=format&fit=crop&w=800&q=80",
    "india-approves-73-billion": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=800&q=80",
    "silver-and-palladium-lead": "https://images.unsplash.com/photo-1605792657660-596af9009e82?auto=format&fit=crop&w=800&q=80",
    "italy-vs-france": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=800&q=80",
    "who-pays-for-chinas": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80",
    "my-friend-hates-her-job": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=800&q=80",
    "okxice-to-debut": "https://images.unsplash.com/photo-1642543492481-44e81e3914a7?auto=format&fit=crop&w=800&q=80",
    "deutsche-bank-launches": "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?auto=format&fit=crop&w=800&q=80",
    "decrypt-becomes-first": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&w=800&q=80",
    "bitcoin-ripe-for-a-squeeze": "https://images.unsplash.com/photo-1622979135225-d2ba269bc1df?auto=format&fit=crop&w=800&q=80",
    "grok-build-coding-agent": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
    "plurai-wants-to-help": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=800&q=80",
    "botpsy-on-device": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80",
    "softbank-loses-37-billion": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80"
}

# Split by <article class="news-card">
parts = html.split('<article class="news-card">')
new_parts = [parts[0]]

for p in parts[1:]:
    # Find which article slug is inside this part
    found_slug = None
    for slug_key in CARD_IMAGES:
        if slug_key in p:
            found_slug = slug_key
            break
    
    if found_slug:
        img_url = CARD_IMAGES[found_slug]
        # Replace the first <img src="..."> in this card
        # Regex replace within p
        import re
        p_new = re.sub(r'<img src="[^"]*"', f'<img src="{img_url}"', p, count=1)
        new_parts.append(p_new)
        print(f"[✓] Successfully assigned unique image to card: {found_slug}")
    else:
        new_parts.append(p)

new_html = '<article class="news-card">'.join(new_parts)

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Saved index.html with 100% unique card images!")
