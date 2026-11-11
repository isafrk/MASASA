import re, json, os

INDEX_PATH = r"D:\PORTFOLIO_NEO_BRUTALISM\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Favicons & Open Graph / Twitter Card Injection
FAVICON_TAGS = """  <link rel="icon" type="image/x-icon" href="https://mantralabs.web.id/favicon.ico">
  <link rel="icon" type="image/png" sizes="192x192" href="https://mantralabs.web.id/icon.png">
  <link rel="icon" type="image/svg+xml" href="https://mantralabs.web.id/icon.svg">
  <link rel="apple-touch-icon" href="https://mantralabs.web.id/apple-touch-icon.png">
  <link rel="shortcut icon" href="https://mantralabs.web.id/favicon.ico">
  <link rel="help" type="text/plain" href="https://mantralabs.web.id/llms.txt">
  <meta property="og:image" content="https://mantralabs.web.id/icon.png">
  <meta property="og:image:width" content="512">
  <meta property="og:image:height" content="512">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@mantralabs">
  <meta name="twitter:title" content="MANTRA LABS // Financial News & Global Macro Intelligence">
  <meta name="twitter:description" content="Deep-dive institutional analysis on capital markets, commodities, crypto, bilateral trade policies, and AI infrastructure.">
  <meta name="twitter:image" content="https://mantralabs.web.id/icon.png">
"""

ORGANIZATION_SCHEMA = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "NewsMediaOrganization",
        "@id": "https://mantralabs.web.id/#organization",
        "name": "Mantra Labs Financial Intelligence",
        "url": "https://mantralabs.web.id/",
        "logo": "https://mantralabs.web.id/icon.png",
        "sameAs": [
          "https://gameonradar.online",
          "https://gomoragame.my.id"
        ],
        "description": "Institutional financial news agency and geopolitical intelligence desk covering commodities, equities, and sovereign macro risk."
      },
      {
        "@type": "WebSite",
        "@id": "https://mantralabs.web.id/#website",
        "url": "https://mantralabs.web.id/",
        "name": "MANTRA LABS",
        "publisher": { "@id": "https://mantralabs.web.id/#organization" },
        "description": "Institutional financial intelligence covering equities, digital assets, energy supply chains, gold and oil wartime dynamics, and bilateral economic statecraft."
      }
    ]
  }
  </script>
"""

# Insert favicons before </head>
if 'rel="shortcut icon"' not in html:
    html = html.replace('</head>', FAVICON_TAGS + '\n' + ORGANIZATION_SCHEMA + '\n</head>')

# 2. Add H1 Tag to Hero Section (Fix H1 count: 0)
# Look for featured-section
OLD_FEATURED_HEAD = """    <section class="featured-section">
      <div class="featured-card">
        <div class="featured-badge-row">
          <span class="badge-label">LEAD ANALYSIS</span>
          <span class="badge-cat">COMMODITIES & GEOPOLITICS</span>
        </div>
        <h2 class="featured-title">"""

NEW_FEATURED_HEAD = """    <section class="featured-section">
      <div style="margin-bottom: 20px;">
        <h1 style="font-family: var(--font-head); font-size: 24px; color: var(--amber); letter-spacing: 0.5px; font-weight: 700; margin: 0 0 6px 0;">INSTITUTIONAL MACRO RESEARCH & GLOBAL FINANCIAL DISPATCHES</h1>
        <p style="font-family: var(--font-mono); font-size: 13px; color: var(--text-muted); margin: 0;">Sovereign risk conduits, capital flows, commodities, and bilateral economic statecraft.</p>
      </div>
      <div class="featured-card">
        <div class="featured-badge-row">
          <span class="badge-label">LEAD ANALYSIS</span>
          <span class="badge-cat">COMMODITIES & GEOPOLITICS</span>
        </div>
        <h2 class="featured-title">"""

if '<h1>' not in html and '<h1 ' not in html:
    html = html.replace(OLD_FEATURED_HEAD, NEW_FEATURED_HEAD)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: index.html patched with Favicons, Open Graph, Organization Schema, and H1 Heading!")
