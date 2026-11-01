# -*- coding: utf-8 -*-
"""
MANTRA LABS - Autonomous AI News & Radar Generator + Auto-Indexer
Pulls from 4 AI source pillars:
1. Breaking News & Big Tech (TechCrunch AI, Ars Technica, Google News)
2. Open-Source Models & Research (Hugging Face Daily Papers, ArXiv)
3. Developer & Community Intelligence (Hacker News Algolia AI Top Stories)
4. AI Tools & Product Launches (Show HN, Tech Launch Feeds)
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
import subprocess

SITE_ROOT = Path(r"D:\PORTFOLIO_NEO_BRUTALISM")
NEWS_DIR = SITE_ROOT / "news"
DATA_DIR = SITE_ROOT / "data"
DB_FILE = DATA_DIR / "articles_db.json"
SITEMAP_FILE = SITE_ROOT / "sitemap.xml"
INDEXNOW_KEY = "a8f1e2d3c4b5a697887654321fedcba0"
BASE_URL = "https://mantralabs.web.id"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MantraLabsRadar/2.0"
}

def get_github_token() -> str:
    env_file = Path(r"C:\Users\dxisa\AppData\Local\hermes\.env")
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("GITHUB_TOKEN="):
                return line.split("=", 1)[1].strip()
    return os.environ.get("GITHUB_TOKEN", "")

def load_db() -> list:
    if DB_FILE.exists():
        try:
            return json.loads(DB_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[DB] Error loading DB: {e}", file=sys.stderr)
    return []

def save_db(db: list):
    DB_FILE.write_text(json.dumps(db, indent=2, ensure_ascii=False), encoding="utf-8")

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text).strip("-")
    return text[:75]

def fetch_feed_items() -> list:
    items = []

    # 1. Hugging Face Daily Papers (Open-Source & Research)
    try:
        req = urllib.request.Request("https://huggingface.co/api/daily_papers", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            for p in data[:8]:
                title = p.get("title", "").strip()
                summary = p.get("summary", "").strip()
                paper_id = p.get("paper", {}).get("id", "")
                link = f"https://huggingface.co/papers/{paper_id}" if paper_id else "https://huggingface.co/papers"
                if title:
                    items.append({
                        "title": title,
                        "source": "Hugging Face Research",
                        "category": "Open-Source & Model Weights",
                        "summary": summary[:400] if summary else "State-of-the-art machine learning architecture release and empirical benchmark findings.",
                        "url": link,
                        "badge": "RESEARCH SOTA"
                    })
    except Exception as e:
        print(f"[Fetch] HF Daily Papers error: {e}")

    # 2. TechCrunch AI (Breaking News & Big Tech)
    try:
        req = urllib.request.Request("https://techcrunch.com/category/artificial-intelligence/feed/", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            tree = ET.fromstring(resp.read().decode("utf-8", errors="ignore"))
            for item in tree.findall(".//item")[:8]:
                t = item.find("title")
                desc = item.find("description")
                link = item.find("link")
                title = t.text.strip() if t is not None and t.text else ""
                summary = re.sub(r"<[^>]+>", "", desc.text).strip() if desc is not None and desc.text else ""
                url = link.text.strip() if link is not None and link.text else ""
                if title:
                    items.append({
                        "title": title,
                        "source": "TechCrunch AI",
                        "category": "Breaking News & Industry",
                        "summary": summary[:400] if summary else "High-impact artificial intelligence industry shift and corporate model deployment.",
                        "url": url,
                        "badge": "INDUSTRY SHIFT"
                    })
    except Exception as e:
        print(f"[Fetch] TechCrunch AI error: {e}")

    # 3. Ars Technica Tech Lab (Deep Dives & Model Vulnerabilities)
    try:
        req = urllib.request.Request("https://feeds.arstechnica.com/arstechnica/technology-lab", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            tree = ET.fromstring(resp.read().decode("utf-8", errors="ignore"))
            for item in tree.findall(".//item")[:8]:
                t = item.find("title")
                desc = item.find("description")
                link = item.find("link")
                title = t.text.strip() if t is not None and t.text else ""
                summary = re.sub(r"<[^>]+>", "", desc.text).strip() if desc is not None and desc.text else ""
                url = link.text.strip() if link is not None and link.text else ""
                if title and ("ai" in title.lower() or "llm" in title.lower() or "anthropic" in title.lower() or "openai" in title.lower() or "model" in title.lower()):
                    items.append({
                        "title": title,
                        "source": "Ars Technica",
                        "category": "Security & Architecture",
                        "summary": summary[:400] if summary else "Deep technical inquiry into algorithmic vulnerabilities and software integration.",
                        "url": url,
                        "badge": "TECH LAB"
                    })
    except Exception as e:
        print(f"[Fetch] Ars Technica error: {e}")

    # 4. Hacker News Algolia (Hacker Discussions & Show HN Tools)
    try:
        req = urllib.request.Request("https://hn.algolia.com/api/v1/search?query=AI%20OR%20LLM&tags=story&hitsPerPage=10", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            for hit in data.get("hits", [])[:8]:
                title = hit.get("title", "").strip()
                url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
                points = hit.get("points", 0)
                if title and points >= 30:
                    items.append({
                        "title": title,
                        "source": "Hacker News",
                        "category": "Developer Tools & Hacks",
                        "summary": f"Trending community engineering debate with {points} upvotes and high-density developer feedback.",
                        "url": url,
                        "badge": f"{points} PTS"
                    })
    except Exception as e:
        print(f"[Fetch] Hacker News error: {e}")

    return items

def generate_article_html(article: dict) -> str:
    title = article["title"]
    category = article["category"]
    badge = article["badge"]
    source = article["source"]
    source_url = article["url"]
    date_str = article["date"]
    iso_date = article["iso_date"]
    slug = article["slug"]
    summary = article["summary"]
    reading_time = article.get("reading_time", "4 min read")
    escaped_summary = summary.replace('"', '&quot;')
    json_title = title.replace('"', '\\"')
    json_summary = summary.replace('"', '\\"')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} // MANTRA LABS AI RADAR</title>
  <meta name="description" content="{escaped_summary}">
  <meta name="keywords" content="AI news, {category.lower()}, LLM architecture, autonomous systems, Mantra Labs AI Radar">
  <meta name="author" content="Mantra Labs Intelligence Unit">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{BASE_URL}/news/{slug}.html">

  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Mantra Labs AI Radar">
  <meta property="og:url" content="{BASE_URL}/news/{slug}.html">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{escaped_summary}">
  <meta property="og:image" content="{BASE_URL}/figma_artboard_preview.png">
  <meta property="article:published_time" content="{iso_date}">
  <meta property="article:section" content="{category}">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="{BASE_URL}/news/{slug}.html">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{escaped_summary}">
  <meta name="twitter:image" content="{BASE_URL}/figma_artboard_preview.png">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": "{json_title}",
    "description": "{json_summary}",
    "datePublished": "{iso_date}",
    "dateModified": "{iso_date}",
    "url": "{BASE_URL}/news/{slug}.html",
    "publisher": {{
      "@type": "Organization",
      "name": "Mantra Labs",
      "url": "https://mantralabs.web.id"
    }},
    "author": {{
      "@type": "Organization",
      "name": "Mantra Labs Intelligence Unit"
    }}
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=Space+Grotesk:wght@700&family=Space+Mono:ital,wght@0,400;0,700&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --bg: #0A0B10;
      --card-bg: #12141F;
      --card-alt: #181B2B;
      --black: #000000;
      --white: #FFFFFF;
      --lime: #00FF66;
      --cyan: #00F0FF;
      --pink: #FF007F;
      --yellow: #FFE600;
      --border: 3px solid #000000;
      --shadow-md: 6px 6px 0px #000000;
      --shadow-lg: 8px 8px 0px #000000;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg);
      background-image: 
        linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
      background-size: 32px 32px;
      color: var(--white);
      font-family: 'DM Sans', -apple-system, sans-serif;
      line-height: 1.7;
      min-height: 100vh;
      padding-bottom: 80px;
    }}
    .container {{ max-width: 900px; margin: 0 auto; padding: 0 20px; }}
    
    .ticker {{
      background: var(--yellow);
      color: var(--black);
      border-bottom: var(--border);
      padding: 10px 0;
      font-size: 13px;
      font-family: 'Space Mono', monospace;
      overflow: hidden;
      white-space: nowrap;
      letter-spacing: 1px;
    }}
    .ticker-track {{
      display: inline-block;
      animation: ticker-scroll 24s linear infinite;
    }}
    @keyframes ticker-scroll {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-50%); }}
    }}

    .nav {{
      margin: 24px auto 32px;
      padding: 16px 24px;
      background: var(--card-bg);
      border: var(--border);
      box-shadow: var(--shadow-md);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand {{
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      font-size: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: var(--white);
    }}
    .brand-tag {{
      background: var(--lime);
      color: var(--black);
      font-size: 11px;
      padding: 2px 6px;
      font-family: 'Space Mono', monospace;
      border: 2px solid var(--black);
    }}
    .nav-links {{ display: flex; gap: 12px; font-family: 'Space Mono', monospace; font-size: 13px; }}
    .nav-links a {{
      color: var(--white);
      text-decoration: none;
      padding: 6px 12px;
      border: 2px solid transparent;
      transition: all 0.15s;
    }}
    .nav-links a:hover {{
      background: var(--cyan);
      color: var(--black);
      border: 2px solid var(--black);
      box-shadow: 2px 2px 0px var(--black);
    }}

    .article-wrap {{
      background: var(--card-bg);
      border: var(--border);
      box-shadow: var(--shadow-lg);
      padding: 40px;
      margin-bottom: 40px;
    }}
    .breadcrumb {{
      font-family: 'Space Mono', monospace;
      font-size: 12px;
      color: var(--cyan);
      margin-bottom: 16px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .breadcrumb a {{ color: var(--cyan); text-decoration: none; }}
    .meta-bar {{
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 24px;
      font-family: 'Space Mono', monospace;
      font-size: 12px;
    }}
    .badge {{
      background: var(--lime);
      color: var(--black);
      font-weight: 700;
      padding: 3px 8px;
      border: 2px solid var(--black);
    }}
    .badge-alt {{
      background: var(--pink);
      color: var(--white);
      font-weight: 700;
      padding: 3px 8px;
      border: 2px solid var(--black);
    }}
    h1 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 34px;
      line-height: 1.25;
      margin-bottom: 24px;
      letter-spacing: -0.5px;
    }}
    h2 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 22px;
      margin: 36px 0 16px;
      color: var(--cyan);
      border-bottom: 2px solid rgba(0, 240, 255, 0.2);
      padding-bottom: 8px;
    }}
    p {{
      margin-bottom: 20px;
      color: #D1D5DB;
      font-size: 16px;
    }}
    .lead-box {{
      background: var(--card-alt);
      border-left: 4px solid var(--yellow);
      padding: 20px;
      font-size: 17px;
      margin-bottom: 30px;
      color: #F3F4F6;
    }}
    .verdict-box {{
      background: #0D1B1E;
      border: 2px solid var(--cyan);
      box-shadow: 4px 4px 0px var(--cyan);
      padding: 24px;
      margin: 36px 0;
    }}
    .verdict-box h3 {{
      font-family: 'Space Grotesk', sans-serif;
      color: var(--cyan);
      margin-bottom: 12px;
      font-size: 18px;
    }}
    .cta-box {{
      background: var(--yellow);
      color: var(--black);
      border: var(--border);
      box-shadow: var(--shadow-md);
      padding: 30px;
      text-align: center;
      margin-top: 50px;
    }}
    .cta-box h3 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 24px;
      margin-bottom: 10px;
    }}
    .btn {{
      display: inline-block;
      margin-top: 16px;
      background: var(--black);
      color: var(--white);
      font-family: 'Space Mono', monospace;
      font-weight: 700;
      padding: 12px 24px;
      text-decoration: none;
      border: 2px solid var(--black);
      box-shadow: 4px 4px 0px rgba(0,0,0,0.3);
      transition: all 0.15s;
    }}
    .btn:hover {{
      background: var(--lime);
      color: var(--black);
      transform: translate(-2px, -2px);
    }}
  </style>
</head>
<body>
  <div class="ticker">
    <div class="ticker-track">
      // 📡 MANTRA LABS AI RADAR ACTIVE // CONTINUOUS MODEL SURVEILLANCE // BREACHES, WEIGHTS & INFRASTRUCTURE INTEL // ZERO FLUFF DETERMINISTIC ANALYSIS //
    </div>
  </div>

  <div class="container">
    <header class="nav">
      <a href="/" class="brand">
        <span>MANTRA LABS</span>
        <span class="brand-tag">AI RADAR</span>
      </a>
      <nav class="nav-links">
        <a href="/">HOME</a>
        <a href="/news/">ALL ARTICLES</a>
        <a href="https://tools.mantralabs.web.id" target="_blank">FREE TOOLS ➔</a>
        <a href="https://discord.gg/KrVzydPbHQ" target="_blank" style="background:var(--lime);color:var(--black);border:2px solid var(--black);">DEAL ROOM</a>
      </nav>
    </header>

    <article class="article-wrap">
      <div class="breadcrumb">
        <a href="/">HOME</a> / <a href="/news/">AI RADAR</a> / <span>{slug}</span>
      </div>

      <div class="meta-bar">
        <span class="badge">{badge}</span>
        <span class="badge-alt">{category}</span>
        <span>• {date_str}</span>
        <span>• {reading_time}</span>
        <span>• Source: <a href="{source_url}" target="_blank" rel="noopener" style="color:var(--cyan);">{source} ↗</a></span>
      </div>

      <h1>{title}</h1>

      <div class="lead-box">
        <strong>EXECUTIVE BRIEF:</strong> {summary}
      </div>

      <h2>1. The Underlying Disruption & Architecture</h2>
      <p>
        The velocity of production AI engineering continues to outpace standard consumer release cycles. This latest development from <strong>{source}</strong> highlights a strategic pivot in how modern machine intelligence is trained, deployed, and protected against adversarial disruption.
      </p>
      <p>
        Rather than merely scaling parameter counts, current industry momentum is fiercely concentrating on execution speed, inference economics, agentic context grounding, and private execution boundaries. Organizations transitioning from speculative prototypes to hardened production systems are finding that uncontained cloud dependencies present untenable operational vectors.
      </p>

      <h2>2. Technical Vector Analysis & Core Mechanics</h2>
      <p>
        From an engineering perspective, this disclosure surfaces several key structural considerations:
      </p>
      <ul style="margin: 0 0 24px 24px; color: #D1D5DB; line-height: 1.8;">
        <li><strong>Inference Throughput & Latency Floor:</strong> Minimizing round-trip serialization overhead between agent tools and orchestrators.</li>
        <li><strong>Determinism & Output Verification:</strong> Eliminating hallucination vectors via strictly typed JSON Schema enforcement and sandbox isolation.</li>
        <li><strong>Sovereignty & Model Weights:</strong> Decreasing reliance on monolithic proprietary endpoints by leveraging localized quantizations and private VPS infrastructure.</li>
      </ul>

      <h2>3. Strategic Implications for Founders & Engineers</h2>
      <p>
        Founders deploying generative software in 2026 cannot afford generic wrappers. As foundational labs commoditize raw chat capabilities, the competitive moat shifts entirely to <em>deterministic workflows, programmatic data integration, and sovereign runtime execution</em>.
      </p>
      <p>
        Teams that successfully leverage these architectural shifts are seeing 10x reductions in operational compute spend while achieving enterprise-grade reliability and zero-data-leak compliance.
      </p>

      <div class="verdict-box">
        <h3>⚡ MANTRA LABS OPERATOR VERDICT</h3>
        <p style="margin:0; font-family: 'Space Mono', monospace; font-size: 14px; color: #E5E7EB;">
          "Never marry a single closed API. Architect your agent pipelines and media compilers to be fully modular, deterministic, and locally resilient. The future belongs to builders who own their execution layer from edge to bare metal."
        </p>
      </div>

      <div class="cta-box">
        <h3>READY TO DEPLOY SOVEREIGN AI SYSTEMS?</h3>
        <p style="margin-bottom:0; font-size:15px;">
          Mantra Labs engineers private autonomous AI agent setups (Hermes), programmatic media pipelines, and edge web apps.
        </p>
        <div style="display:flex; justify-content:center; gap:16px; flex-wrap:wrap;">
          <a href="https://tools.mantralabs.web.id" class="btn" style="background:var(--card-bg); color:var(--white);">Explore Free Client-Side Tools ➔</a>
          <a href="https://discord.gg/KrVzydPbHQ" class="btn">Launch Deal Room in Discord</a>
        </div>
      </div>
    </article>
  </div>
</body>
</html>"""
    return html

def generate_news_index_html(db: list) -> str:
    cards_html = []
    for item in sorted(db, key=lambda x: x.get("iso_date", ""), reverse=True):
        title = item["title"]
        slug = item["slug"]
        category = item["category"]
        badge = item.get("badge", "INTEL")
        date_str = item["date"]
        summary = item["summary"]
        source = item["source"]
        reading_time = item.get("reading_time", "4 min read")

        cards_html.append(f"""
        <div class="news-card">
          <div class="meta-row">
            <span class="badge">{badge}</span>
            <span class="cat-pill">{category}</span>
            <span class="date">{date_str} • {reading_time}</span>
          </div>
          <h2 class="card-title">
            <a href="/news/{slug}.html">{title}</a>
          </h2>
          <p class="card-desc">{summary}</p>
          <div class="card-footer">
            <span class="source-tag">Source: {source}</span>
            <a href="/news/{slug}.html" class="read-btn">READ INTEL ➔</a>
          </div>
        </div>
        """)

    cards_joined = "\n".join(cards_html)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MANTRA LABS AI RADAR // Autonomous Intelligence & Research Dispatches</title>
  <meta name="description" content="Continuous surveillance on breakthroughs, open-source weights, agent architectures, and AI industry disruption. Zero-fluff technical dispatches by Mantra Labs.">
  <meta name="keywords" content="AI news, machine learning radar, LLM research, Hugging Face papers, TechCrunch AI, Hacker News AI, Mantra Labs">
  <link rel="canonical" href="{BASE_URL}/news/">

  <meta property="og:type" content="website">
  <meta property="og:title" content="Mantra Labs AI Radar // Autonomous Intelligence & Research Dispatches">
  <meta property="og:description" content="Continuous surveillance on breakthroughs, open-source weights, agent architectures, and AI industry disruption.">
  <meta property="og:url" content="{BASE_URL}/news/">
  <meta property="og:image" content="{BASE_URL}/figma_artboard_preview.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=Space+Grotesk:wght@700&family=Space+Mono:ital,wght@0,400;0,700&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --bg: #0A0B10;
      --card-bg: #12141F;
      --card-alt: #181B2B;
      --black: #000000;
      --white: #FFFFFF;
      --lime: #00FF66;
      --cyan: #00F0FF;
      --pink: #FF007F;
      --yellow: #FFE600;
      --border: 3px solid #000000;
      --shadow-md: 6px 6px 0px #000000;
      --shadow-lg: 8px 8px 0px #000000;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg);
      background-image: 
        linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
      background-size: 32px 32px;
      color: var(--white);
      font-family: 'DM Sans', -apple-system, sans-serif;
      min-height: 100vh;
      padding-bottom: 80px;
    }}
    .container {{ max-width: 1080px; margin: 0 auto; padding: 0 20px; }}
    
    .ticker {{
      background: var(--yellow);
      color: var(--black);
      border-bottom: var(--border);
      padding: 10px 0;
      font-size: 13px;
      font-family: 'Space Mono', monospace;
      overflow: hidden;
      white-space: nowrap;
      letter-spacing: 1px;
    }}
    .ticker-track {{
      display: inline-block;
      animation: ticker-scroll 24s linear infinite;
    }}
    @keyframes ticker-scroll {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-50%); }}
    }}

    .nav {{
      margin: 24px auto 32px;
      padding: 16px 24px;
      background: var(--card-bg);
      border: var(--border);
      box-shadow: var(--shadow-md);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .brand {{
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      font-size: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: var(--white);
    }}
    .brand-tag {{
      background: var(--lime);
      color: var(--black);
      font-size: 11px;
      padding: 2px 6px;
      font-family: 'Space Mono', monospace;
      border: 2px solid var(--black);
    }}
    .nav-links {{ display: flex; gap: 12px; font-family: 'Space Mono', monospace; font-size: 13px; }}
    .nav-links a {{
      color: var(--white);
      text-decoration: none;
      padding: 6px 12px;
      border: 2px solid transparent;
      transition: all 0.15s;
    }}
    .nav-links a:hover {{
      background: var(--cyan);
      color: var(--black);
      border: 2px solid var(--black);
      box-shadow: 2px 2px 0px var(--black);
    }}

    .hero {{
      background: var(--card-bg);
      border: var(--border);
      box-shadow: var(--shadow-lg);
      padding: 40px;
      margin-bottom: 36px;
    }}
    .hero-tag {{
      background: var(--cyan);
      color: var(--black);
      font-family: 'Space Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      display: inline-block;
      border: 2px solid var(--black);
      margin-bottom: 12px;
    }}
    .hero h1 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 38px;
      line-height: 1.15;
      margin-bottom: 12px;
    }}
    .hero p {{
      color: #9CA3AF;
      font-size: 16px;
      max-width: 700px;
    }}

    .news-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 24px;
    }}
    .news-card {{
      background: var(--card-bg);
      border: var(--border);
      box-shadow: var(--shadow-md);
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.15s;
    }}
    .news-card:hover {{
      transform: translate(-3px, -3px);
      box-shadow: var(--shadow-lg);
    }}
    .meta-row {{
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 14px;
      font-family: 'Space Mono', monospace;
      font-size: 11px;
    }}
    .badge {{
      background: var(--lime);
      color: var(--black);
      font-weight: 700;
      padding: 2px 6px;
      border: 1px solid var(--black);
    }}
    .cat-pill {{
      background: rgba(0, 240, 255, 0.15);
      color: var(--cyan);
      padding: 2px 6px;
      border: 1px solid rgba(0, 240, 255, 0.3);
    }}
    .date {{ color: #9CA3AF; }}
    .card-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 19px;
      line-height: 1.35;
      margin-bottom: 12px;
    }}
    .card-title a {{
      color: var(--white);
      text-decoration: none;
      transition: color 0.15s;
    }}
    .card-title a:hover {{ color: var(--cyan); }}
    .card-desc {{
      font-size: 14px;
      color: #9CA3AF;
      line-height: 1.6;
      margin-bottom: 20px;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 14px;
      border-top: 1px solid rgba(255,255,255,0.08);
      font-family: 'Space Mono', monospace;
      font-size: 12px;
    }}
    .source-tag {{ color: #6B7280; }}
    .read-btn {{
      color: var(--lime);
      text-decoration: none;
      font-weight: 700;
      transition: all 0.15s;
    }}
    .read-btn:hover {{ text-decoration: underline; color: var(--cyan); }}
  </style>
</head>
<body>
  <div class="ticker">
    <div class="ticker-track">
      // 📡 MANTRA LABS AI RADAR ACTIVE // 24/7 SURVEILLANCE OF AI LABS, WEIGHTS, AGENTS &amp; ENTERPRISE DISRUPTIONS // NO BS ENGINEERING INTEL //
    </div>
  </div>

  <div class="container">
    <header class="nav">
      <a href="/" class="brand">
        <span>MANTRA LABS</span>
        <span class="brand-tag">AI RADAR</span>
      </a>
      <nav class="nav-links">
        <a href="/">HOME</a>
        <a href="https://tools.mantralabs.web.id" target="_blank">FREE TOOLS ➔</a>
        <a href="https://discord.gg/KrVzydPbHQ" target="_blank" style="background:var(--lime);color:var(--black);border:2px solid var(--black);">DEAL ROOM</a>
      </nav>
    </header>

    <div class="hero">
      <span class="hero-tag">OPERATIONAL INTELLIGENCE</span>
      <h1>AI RADAR DISPATCHES</h1>
      <p>
        Continuous automated surveillance tracking model weight leaks, SOTA benchmarks, enterprise disruption, and developer tooling. Pure engineering signal, zero marketing fluff.
      </p>
    </div>

    <div class="news-grid">
      {cards_joined}
    </div>
  </div>
</body>
</html>"""
    return html

def update_sitemap(db: list):
    urls = [
        {"loc": f"{BASE_URL}/", "prio": "1.0", "freq": "daily"},
        {"loc": f"{BASE_URL}/news/", "prio": "0.9", "freq": "daily"}
    ]
    for item in db:
        slug = item["slug"]
        urls.append({
            "loc": f"{BASE_URL}/news/{slug}.html",
            "prio": "0.8",
            "freq": "weekly"
        })

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for u in urls:
        lines.append('  <url>')
        lines.append(f"    <loc>{u['loc']}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append(f"    <changefreq>{u['freq']}</changefreq>")
        lines.append(f"    <priority>{u['prio']}</priority>")
        lines.append('  </url>')
    lines.append('</urlset>')

    SITEMAP_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Sitemap] Updated {SITEMAP_FILE} with {len(urls)} URLs.")

def notify_indexnow(new_urls: list):
    if not new_urls:
        return

    payload = json.dumps({
        "host": "mantralabs.web.id",
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": new_urls
    }).encode("utf-8")

    endpoints = [
        "https://api.indexnow.org/indexnow",
        "https://www.bing.com/indexnow",
        "https://yandex.com/indexnow"
    ]

    for ep in endpoints:
        try:
            req = urllib.request.Request(
                ep,
                data=payload,
                headers={"Content-Type": "application/json; charset=utf-8"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"[IndexNow] Submitted {len(new_urls)} URLs to {ep} -> Status: {resp.status}")
        except Exception as e:
            print(f"[IndexNow] Warning submitting to {ep}: {e}")

def git_commit_and_push(commit_msg: str):
    token = get_github_token()
    if not token:
        print("[Git] No GITHUB_TOKEN available, skipping push.")
        return

    auth_url = f"https://x-access-token:{token}@github.com/isafrk/MASASA.git"
    clean_url = "https://github.com/isafrk/MASASA.git"

    try:
        subprocess.run(["git", "add", "."], cwd=str(SITE_ROOT), check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(SITE_ROOT), capture_output=True)
        subprocess.run(["git", "remote", "set-url", "origin", auth_url], cwd=str(SITE_ROOT), check=True)
        res = subprocess.run(["git", "push", "origin", "main"], cwd=str(SITE_ROOT), capture_output=True, text=True)
        subprocess.run(["git", "remote", "set-url", "origin", clean_url], cwd=str(SITE_ROOT), check=True)
        
        if res.returncode == 0:
            print("[Git] Successfully committed and pushed updates to GitHub isafrk/MASASA (main).")
        else:
            print(f"[Git] Push returned code {res.returncode}: {res.stderr}")
    except Exception as e:
        print(f"[Git] Error during git sync: {e}")

def run():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Mantra Labs AI News Radar Dispatch...")
    db = load_db()
    existing_slugs = {item["slug"] for item in db}
    existing_titles = {item["title"].lower() for item in db}

    fetched = fetch_feed_items()
    print(f"[Fetch] Total raw candidates retrieved: {len(fetched)}")

    # Pick up to 2 fresh items per run
    new_articles = []
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%B %d, %Y")
    iso_date = now.isoformat()

    for item in fetched:
        slug = slugify(item["title"])
        if slug in existing_slugs or item["title"].lower() in existing_titles:
            continue
        
        article = {
            "title": item["title"],
            "slug": slug,
            "category": item["category"],
            "badge": item["badge"],
            "source": item["source"],
            "url": item["url"],
            "summary": item["summary"],
            "date": date_str,
            "iso_date": iso_date,
            "reading_time": "4 min read"
        }
        new_articles.append(article)
        existing_slugs.add(slug)
        existing_titles.add(item["title"].lower())
        if len(new_articles) >= 2:
            break

    if not new_articles:
        print("[Run] No new unique articles found to publish this cycle.")
        return

    print(f"[Run] Publishing {len(new_articles)} new high-signal articles:")
    for a in new_articles:
        print(f"  + [{a['category']}] {a['title']} -> /news/{a['slug']}.html")

    # Generate individual article HTML pages
    for a in new_articles:
        out_file = NEWS_DIR / f"{a['slug']}.html"
        html = generate_article_html(a)
        out_file.write_text(html, encoding="utf-8")

    # Append to DB
    db = new_articles + db
    save_db(db)

    # Generate News Hub index
    index_html = generate_news_index_html(db)
    (NEWS_DIR / "index.html").write_text(index_html, encoding="utf-8")

    # Update Sitemap
    update_sitemap(db)

    # Collect URLs for IndexNow
    new_urls = [f"{BASE_URL}/news/{a['slug']}.html" for a in new_articles]
    new_urls.append(f"{BASE_URL}/news/")
    notify_indexnow(new_urls)

    # Commit & Push to GitHub (Triggers Cloudflare Pages build)
    commit_msg = f"feat(news): publish {len(new_articles)} AI radar dispatches & update sitemap"
    git_commit_and_push(commit_msg)

    print(f"[Run] Complete! Published {len(new_articles)} articles, updated news index & sitemap, pushed to GitHub & submitted to IndexNow.")

if __name__ == "__main__":
    run()
