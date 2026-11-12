# -*- coding: utf-8 -*-
import sys, json, os, re
sys.path.append(r"C:\Users\dxisa\AppData\Local\hermes\scripts")
from generate_ai_cover import generate_article_ai_image

DB_PATH = r"D:\PORTFOLIO_NEO_BRUTALISM\data\financial_articles.json"
IMG_DIR = r"D:\PORTFOLIO_NEO_BRUTALISM\articles\images"
ARTICLES_DIR = r"D:\PORTFOLIO_NEO_BRUTALISM\articles"
INDEX_PATH = r"D:\PORTFOLIO_NEO_BRUTALISM\index.html"

with open(DB_PATH, "r", encoding="utf-8") as f:
    articles = json.load(f)

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    index_html = f.read()

count = 0
for art in articles[:6]:
    slug = art["slug"]
    title = art.get("raw_title") or art.get("title")
    cat = art.get("category", "GLOBAL EQUITIES")
    print(f"[*] Generating AI image for: {title[:50]}...")
    
    rel_img = generate_article_ai_image(title, cat, IMG_DIR, slug)
    if rel_img:
        count += 1
        img_url = f"https://mantralabs.web.id{rel_img}"
        art["image_url"] = img_url
        
        # Patch article HTML
        art_file = os.path.join(ARTICLES_DIR, f"{slug}.html")
        if os.path.exists(art_file):
            with open(art_file, "r", encoding="utf-8") as af:
                a_html = af.read()
            a_html = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{img_url}">', a_html)
            a_html = re.sub(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{img_url}">', a_html)
            a_html = re.sub(r'<img src="[^"]*" alt="[^"]*" style="width:100%;height:360px', f'<img src="{rel_img}" alt="{title}" style="width:100%;height:360px', a_html)
            with open(art_file, "w", encoding="utf-8") as af:
                af.write(a_html)
            print(f"[✓] Patched article file: {slug}.html")

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=2)

print(f"\n[✓] Successfully generated and linked {count} unique AI images!")
