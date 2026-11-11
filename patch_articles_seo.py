import os, re, glob, json

ARTICLES_DIR = r"D:\PORTFOLIO_NEO_BRUTALISM\articles"

FAVICON_INJECTION = """  <link rel="icon" type="image/x-icon" href="https://mantralabs.web.id/favicon.ico">
  <link rel="icon" type="image/png" sizes="192x192" href="https://mantralabs.web.id/icon.png">
  <link rel="icon" type="image/svg+xml" href="https://mantralabs.web.id/icon.svg">
  <link rel="apple-touch-icon" href="https://mantralabs.web.id/apple-touch-icon.png">
  <link rel="shortcut icon" href="https://mantralabs.web.id/favicon.ico">
  <link rel="help" type="text/plain" href="https://mantralabs.web.id/llms.txt">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@mantralabs">
"""

patched_count = 0

for fpath in glob.glob(os.path.join(ARTICLES_DIR, "*.html")):
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    modified = False

    # 1. Truncate Title if > 65 chars
    title_match = re.search(r'<title>(.*?)</title>', html, re.I)
    if title_match:
        cur_title = title_match.group(1)
        # Separate site name
        parts = cur_title.split('|')
        raw_headline = parts[0].strip()
        site_name = " | MANTRA LABS"
        if len(raw_headline) + len(site_name) > 65:
            max_head = 65 - len(site_name) - 3
            truncated_headline = raw_headline[:max_head].strip() + "..."
            new_title = f"{truncated_headline}{site_name}"
            html = html.replace(f"<title>{cur_title}</title>", f"<title>{new_title}</title>")
            modified = True

    # 2. Truncate Meta Description if > 155 chars
    desc_match = re.search(r'<meta name="description" content="(.*?)">', html, re.I)
    if desc_match:
        cur_desc = desc_match.group(1)
        if len(cur_desc) > 155:
            new_desc = cur_desc[:150].strip() + "..."
            html = html.replace(f'<meta name="description" content="{cur_desc}">', f'<meta name="description" content="{new_desc}">')
            modified = True

    # 3. Inject Favicons & Twitter Card
    if 'rel="shortcut icon"' not in html:
        html = html.replace('</head>', FAVICON_INJECTION + '\n</head>')
        modified = True

    # 4. Inject NewsArticle Schema (JSON-LD) if missing
    if 'application/ld+json' not in html:
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.DOTALL)
        headline = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else "Mantra Labs Financial Dispatch"
        headline = headline.replace('"', '\\"')

        date_match = re.search(r'Published:\s*([A-Za-z0-9,\s]+)', html)
        pub_date = date_match.group(1).strip() if date_match else "November 11, 2026"

        img_match = re.search(r'<meta property="og:image" content="(.*?)">', html)
        img_url = img_match.group(1) if img_match else "https://mantralabs.web.id/icon.png"

        schema_json = f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": "{headline[:110]}",
    "image": [
      "{img_url}"
    ],
    "datePublished": "2026-11-11T08:00:00+00:00",
    "dateModified": "2026-11-11T08:00:00+00:00",
    "author": [{{
      "@type": "Organization",
      "name": "Mantra Labs Financial Intelligence",
      "url": "https://mantralabs.web.id"
    }}],
    "publisher": {{
      "@type": "NewsMediaOrganization",
      "name": "Mantra Labs",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://mantralabs.web.id/icon.png"
      }}
    }},
    "description": "{desc_match.group(1)[:150] if desc_match else headline}"
  }}
  </script>
"""
        html = html.replace('</head>', schema_json + '\n</head>')
        modified = True

    if modified:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        patched_count += 1

print(f"SUCCESS: Patched {patched_count} articles in D:/PORTFOLIO_NEO_BRUTALISM/articles!")
