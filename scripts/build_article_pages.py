import json
from pathlib import Path

SITE_ROOT = Path(r"D:\PORTFOLIO_NEO_BRUTALISM")
ARTICLES_DIR = SITE_ROOT / "articles"
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
DB_FILE = SITE_ROOT / "data" / "financial_articles.json"

with open(DB_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | MANTRA LABS FINANCIAL INTELLIGENCE</title>
  <meta name="description" content="{summary}">
  <meta name="author" content="Mantra Labs Macroeconomic Desk">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="https://mantralabs.web.id/articles/{slug}.html">

  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Mantra Labs Financial">
  <meta property="og:url" content="https://mantralabs.web.id/articles/{slug}.html">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{summary}">
  <meta property="article:published_time" content="{iso_date}">
  <meta property="article:section" content="{category}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

  <style>
    :root {{
      --bg: #030303;
      --bg-card: #080808;
      --border: #1a1a1a;
      --border-accent: #2e2410;
      --amber: #f5a623;
      --amber-soft: rgba(245, 166, 35, 0.1);
      --text: #e6e6e6;
      --text-muted: #888888;
      --positive: #00e676;
      --font-body: 'DM Sans', -apple-system, sans-serif;
      --font-head: 'Space Grotesk', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      font-size: 15px;
      line-height: 1.7;
      padding: 0;
      margin: 0;
    }}

    /* HEADER BAR */
    .top-nav {{
      border-bottom: 1px solid var(--border);
      background: #000000;
      padding: 14px 24px;
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .brand-link {{
      text-decoration: none;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: var(--font-head);
      font-weight: 700;
      font-size: 16px;
      letter-spacing: 0.5px;
    }}

    .brand-link:hover .back-tag {{
      background: var(--amber);
      color: #000;
    }}

    .back-tag {{
      background: #111;
      border: 1px solid var(--border-accent);
      color: var(--amber);
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 3px 8px;
      letter-spacing: 1px;
      transition: all 0.2s;
    }}

    .cat-badge {{
      background: var(--amber-soft);
      border: 1px solid var(--amber);
      color: var(--amber);
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 3px 8px;
      letter-spacing: 1px;
      font-weight: 600;
    }}

    /* MAIN CONTAINER */
    .article-wrap {{
      max-width: 820px;
      margin: 40px auto 80px;
      padding: 0 20px;
    }}

    .article-header {{
      margin-bottom: 32px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border);
    }}

    .meta-line {{
      display: flex;
      gap: 16px;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 16px;
    }}

    .meta-line span b {{
      color: var(--amber);
    }}

    h1 {{
      font-family: var(--font-head);
      font-size: 32px;
      line-height: 1.25;
      color: #ffffff;
      margin-bottom: 20px;
      letter-spacing: -0.5px;
    }}

    .lead-summary {{
      font-size: 17px;
      line-height: 1.6;
      color: #d0d0d0;
      background: #0a0800;
      border-left: 3px solid var(--amber);
      padding: 16px 20px;
    }}

    /* BODY */
    .article-body {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 36px 32px;
    }}

    .article-body h2 {{
      font-family: var(--font-head);
      font-size: 20px;
      color: var(--amber);
      margin: 32px 0 14px;
      padding-bottom: 8px;
      border-bottom: 1px solid #161616;
    }}

    .article-body h2:first-child {{
      margin-top: 0;
    }}

    .article-body p {{
      margin-bottom: 18px;
      color: #cccccc;
      font-size: 16px;
      line-height: 1.75;
    }}

    /* BOTTOM NAV */
    .bottom-actions {{
      margin-top: 36px;
      padding-top: 24px;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .action-btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #000;
      border: 1px solid var(--border-accent);
      color: var(--amber);
      padding: 10px 18px;
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s;
    }}

    .action-btn:hover {{
      background: var(--amber);
      color: #000;
    }}

    /* FOOTER */
    footer {{
      border-top: 1px solid var(--border);
      padding: 24px;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-muted);
      background: #000;
    }}

    @media (max-width: 640px) {{
      h1 {{ font-size: 24px; }}
      .article-body {{ padding: 24px 18px; }}
    }}
  </style>
</head>
<body>

  <header class="top-nav">
    <a href="/" class="brand-link">
      <span class="back-tag">&larr; BERANDA NEWS</span>
      <span>MANTRA LABS // FINANCIAL</span>
    </a>
    <span class="cat-badge">{badge}</span>
  </header>

  <main class="article-wrap">
    <article class="article-header">
      <div class="meta-line">
        <span>KATEGORI: <b>{category}</b></span>
        <span>TANGGAL: <b>{date}</b></span>
        <span>DURASI: <b>{reading_time}</b></span>
      </div>
      <h1>{title}</h1>
      <p class="lead-summary">{summary}</p>
    </article>

    <div class="article-body">
      {body_html}

      <div class="bottom-actions">
        <a href="/" class="action-btn">&larr; KEMBALI KE BERANDA FINANSIAL</a>
        <a href="#top" class="action-btn">KEMBALI KE ATAS &uarr;</a>
      </div>
    </div>
  </main>

  <footer>
    MANTRA LABS FINANCIAL NEWS &bull; RISET MAKROEKONOMI, KOMODITAS & KEBIJAKAN GLOBAL &bull; SEMUA HAK DILINDUNGI
  </footer>

</body>
</html>
"""

for art in articles:
    body_parts = []
    for blk in art["content_blocks"]:
        body_parts.append(f"<h2>{blk['subheading']}</h2>")
        for p in blk["paragraphs"]:
            body_parts.append(f"<p>{p}</p>")
    
    body_html = "\n      ".join(body_parts)
    page_html = HTML_TEMPLATE.format(
        title=art["title"],
        summary=art["summary"],
        slug=art["slug"],
        iso_date=art["iso_date"],
        category=art["category"],
        badge=art["badge"],
        date=art["date"],
        reading_time=art["reading_time"],
        body_html=body_html
    )

    out_file = ARTICLES_DIR / f"{art['slug']}.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"Generated standalone article: {out_file.name}")

print(f"\nAll {len(articles)} standalone HTML articles written successfully!")
