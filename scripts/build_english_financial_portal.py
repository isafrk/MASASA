# -*- coding: utf-8 -*-
"""
MANTRA LABS - English Autonomous Financial Editorial & RSS Rewriter
Rewrites all financial news stories into English with:
- Zero em-dashes (—).
- Institutional Bloomberg / Financial Times tone.
- Dedicated section: "MANTRA LABS STRATEGIC OPINION".
"""

import os
import sys
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
import subprocess

SITE_ROOT = Path(r"D:\PORTFOLIO_NEO_BRUTALISM")
ARTICLES_DIR = SITE_ROOT / "articles"
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR = SITE_ROOT / "data"
DB_FILE = DATA_DIR / "financial_articles.json"
SOURCES_FILE = DATA_DIR / "20_trusted_news_sources.json"
SITEMAP_FILE = SITE_ROOT / "sitemap.xml"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MantraLabsBot/2.0"
}

def clean_text(text: str) -> str:
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", "", text)
    clean = clean.replace("—", "-").replace("–", "-")
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean

def slugify(title: str) -> str:
    clean = clean_text(title).lower()
    clean = re.sub(r"[^a-z0-9\s-]", "", clean)
    clean = re.sub(r"[\s-]+", "-", clean).strip("-")
    return clean[:70]

def fetch_rss_feed(feed_url: str):
    try:
        req = urllib.request.Request(feed_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as r:
            xml_data = r.read().decode("utf-8", errors="ignore")
            root = ET.fromstring(xml_data)
            items = []
            for item in root.findall(".//item"):
                title_el = item.find("title")
                link_el = item.find("link")
                desc_el = item.find("description")
                
                title = clean_text(title_el.text if title_el is not None and title_el.text else "")
                link = link_el.text.strip() if link_el is not None and link_el.text else ""
                desc = clean_text(desc_el.text if desc_el is not None and desc_el.text else "")
                
                if title and len(title) > 15:
                    items.append({
                        "title": title,
                        "link": link,
                        "description": desc
                    })
            return items
    except Exception as e:
        print(f"[!] Feed fetch failed ({feed_url[:40]}): {e}")
        return []

def rewrite_into_english_mantra_article(raw_item: dict, niche_name: str, source_name: str):
    title_raw = clean_text(raw_item["title"])
    desc_raw = clean_text(raw_item["description"]) or title_raw
    
    slug = slugify(title_raw)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%B %d, %Y")
    iso_date = now.isoformat()
    
    # Contextual category & opinion synthesis in English
    if "Minyak" in niche_name or "Emas" in niche_name or "Geopolitik" in niche_name or "Commodities" in niche_name:
        category = "COMMODITIES & GEOPOLITICS"
        badge = "RISK BRIEFING"
        block1_sub = "1. Energy Supply Dynamics and Physical Flow Bottlenecks"
        block1_p1 = f"Recent intelligence reported by {source_name} emphasizes: {title_raw}. In global commodity markets, this development underscores the acute vulnerability of transit choke points to geopolitical escalation."
        block1_p2 = f"Market observations indicate: {desc_raw}. Heightened uncertainty immediately translates into higher maritime insurance premiums and wider bid-ask spreads across physical prompt barrels."
        
        block2_sub = "2. Monetary Liquidity and Inflation Transmission"
        block2_p1 = "Energy price spikes do not remain isolated within commodities desks; they act as a direct conduit for imported inflation across major consuming economies. As central banks reassess policy easing cycles, elevated crude oil prices support safe-haven demand for physical gold bullion."
        
        opini_sub = "3. Mantra Labs Strategic Opinion"
        opini_p1 = "At Mantra Labs, our quantitative models interpret persistent Middle Eastern supply tensions as a multi-quarter catalyst accelerating central bank de-dollarization and bilateral barter settlements."
        opini_p2 = "Asset managers should maintain tactical hedges via energy futures and non-correlated hard assets while trimming exposure to dollar-indebted emerging market corporates."

    elif "Bilateral" in niche_name or "Hubungan" in niche_name:
        category = "ECONOMIC POLICY & DIPLOMACY"
        badge = "MACRO STRATEGY"
        block1_sub = "1. Bilateral Trade Realignments and Currency Frameworks"
        block1_p1 = f"According to diplomatic dispatches tracked via {source_name}: {title_raw}. Trade negotiations between global powers are increasingly focused on bilateral settlement mechanisms independent of traditional clearing networks."
        block1_p2 = f"Primary reporting confirms: {desc_raw}. The expansion of local currency swaps and alternative payment channels represents a deliberate defensive architecture against unilateral sanctions."
        
        block2_sub = "2. Structural Supply Chain Fragmentation"
        block2_p1 = "Bilateral trade frictions and reciprocal tariff barriers continue to reshape international trade flows from cost-efficiency toward geopolitical resilience. Capital allocators face heightened regulatory friction across cross-border mergers and foreign direct investment."
        
        opini_sub = "3. Mantra Labs Strategic Opinion"
        opini_p1 = "Our institutional thesis is that the erosion of single-currency hegemony is structural rather than cyclical. Multilateral initiatives like mBridge and expanded bilateral currency agreements will permanently diminish offshore dollar demand."
        opini_p2 = "Corporations operating in Southeast Asia and emerging hubs must establish diversified multi-currency treasuries and dynamic supply chain redundancy."

    elif "Crypto" in niche_name:
        category = "CRYPTO & DIGITAL ASSETS"
        badge = "DIGITAL LIQUIDITY"
        block1_sub = "1. Institutional Inflow and On-Chain Liquidity Footprint"
        block1_p1 = f"Market telemetry synthesized from {source_name} documents: {title_raw}. Orderbook depth across major venues reflects institutional positioning following spot exchange-traded vehicle approvals."
        block1_p2 = f"On-chain forensic metrics demonstrate: {desc_raw}. Net issuance constraints post-halving continue to interact with systematic capital allocator demand."
        
        block2_sub = "2. Macro Interest Rate Sensitivity"
        block2_p1 = "Bitcoin and major digital assets have fully integrated into global macroeconomic liquidity cycles. Variations in sovereign bond yields and expectations around Federal Reserve balance sheet runoff dictate market beta."
        
        opini_sub = "3. Mantra Labs Strategic Opinion"
        opini_p1 = "Mantra Labs views the current market phase as institutional accumulation rather than retail froth. High-frequency leverage flushes provide disciplined entry windows for long-duration capital."
        opini_p2 = "Risk managers must enforce stringent counterparty limits, prioritize self-custodied spot assets, and avoid unhedged exposure to low-liquidity governance tokens."

    elif "AI" in niche_name or "Teknologi" in niche_name:
        category = "ARTIFICIAL INTELLIGENCE & TECH"
        badge = "FRONTIER RESEARCH"
        block1_sub = "1. Compute Acceleration and Frontier Infrastructure Expansion"
        block1_p1 = f"Technology intelligence from {source_name} details: {title_raw}. The relentless expansion of artificial intelligence compute frontiers demands massive capital expenditure across advanced silicon packaging and high-bandwidth interconnects."
        block1_p2 = f"Technical reports corroborate: {desc_raw}. Semiconductor foundries and cloud hyperscalers are locked in a multi-billion-dollar race to secure high-performance accelerator capacity."
        
        block2_sub = "2. Power Grid Bottlenecks and Nuclear Energy Integration"
        block2_p1 = "The critical bottleneck facing datacenter development has shifted decisively from chip availability to electrical power interconnects. Hyperscalers are contracting dedicated power generation from nuclear and geothermal assets to guarantee uninterrupted inferencing uptime."
        
        opini_sub = "3. Mantra Labs Strategic Opinion"
        opini_p1 = "Our view is that public markets will increasingly penalize unmonetized foundation model expenditure in favor of purpose-built autonomous execution architectures with demonstrable enterprise ROI."
        opini_p2 = "Enterprises that fail to embed agentic execution models into core quantitative and operational workflows will face structural margin degradation against AI-native incumbents."

    else: # Equities & Capital Markets
        category = "EQUITIES & CAPITAL MARKETS"
        badge = "MARKET PULSE"
        block1_sub = "1. Equity Market Sentiment and Factor Rotations"
        block1_p1 = f"Capital market dispatches from {source_name} observe: {title_raw}. Benchmark indices are calibrating valuation multiples against sovereign yield volatility and incoming corporate earnings guidance."
        block1_p2 = f"Trading desk color notes: {desc_raw}. Cross-asset correlations reflect ongoing sector rotation as active managers realign cash flow duration."
        
        block2_sub = "2. Cost of Capital in a Restricted Monetary Regime"
        block2_p1 = "With risk-free rates holding above historical averages, speculative valuation premiums remain compressed. Balance sheet quality, net cash generation, and durable pricing power differentiate market leaders from interest-rate-sensitive laggards."
        
        opini_sub = "3. Mantra Labs Strategic Opinion"
        opini_p1 = "Mantra Labs advises institutional investors to look beyond broad market momentum. Current index consolidation provides an advantageous backdrop for accumulating resilient franchises trading at significant multiples discounts."
        opini_p2 = "Maintain disciplined equity factor allocations and ensure downside protection against potential sovereign yield repricing events."

    summary = f"Institutional intelligence briefing by Mantra Labs analyzing {source_name} reporting on {title_raw}. Examining transmission mechanisms, macro liquidity, and strategic portfolio positioning."
    
    return {
        "id": str(int(now.timestamp())),
        "slug": slug,
        "category": category,
        "badge": badge,
        "title": title_raw,
        "date": date_str,
        "iso_date": iso_date,
        "reading_time": "6 min read",
        "summary": summary,
        "source": source_name,
        "source_url": raw_item["link"],
        "content_blocks": [
            {
                "subheading": block1_sub,
                "paragraphs": [block1_p1, block1_p2]
            },
            {
                "subheading": block2_sub,
                "paragraphs": [block2_p1]
            },
            {
                "subheading": opini_sub,
                "paragraphs": [opini_p1, opini_p2]
            }
        ]
    }

# 5 English Core Articles
ENGLISH_CORE_ARTICLES = [
    {
        "id": "c1",
        "slug": "gold-oil-middle-east-war-risk-transmission-macro-assets",
        "category": "COMMODITIES & GEOPOLITICS",
        "badge": "LEAD ANALYSIS",
        "title": "Middle East War Escalation, Crude Oil Spikes, and Gold: The Macro Transmission Channels to Global Risk Assets",
        "date": "November 11, 2026",
        "iso_date": "2026-11-11T03:30:00Z",
        "reading_time": "7 min read",
        "summary": "As military tensions flare along critical maritime corridors, crude oil and physical gold react through two distinct economic conduits: physical supply disruption and sovereign risk hedging.",
        "content_blocks": [
            {
                "subheading": "1. Critical Maritime Choke Points and Physical Oil Disruption",
                "paragraphs": [
                    "Crude oil price surges during geopolitical conflicts are not mere speculative volatility. Over 20 percent of daily global petroleum liquid consumption transits the Strait of Hormuz. When maritime tanker security is compromised or regional refining infrastructure faces direct threats, geopolitical risk premiums immediately price into Brent and WTI futures.",
                    "Physical supply bottlenecks trigger soaring tanker freight rates, escalated insurance premiums, and higher landed feedstock costs across major manufacturing economies in Asia and Europe, sparking imported inflationary pressures."
                ]
            },
            {
                "subheading": "2. Gold as the Ultimate Sovereign Hedge Free of Counterparty Risk",
                "paragraphs": [
                    "While crude oil represents an industrial input and consumption commodity, physical gold operates as a premier monetary reserve asset. In eras of military escalation, unilateral sanctions, and sovereign asset freezes, institutional allocators and non-aligned central banks aggressively accumulate gold reserves.",
                    "Gold carries zero counterparty liability and cannot be seized or inflated by foreign issuers. Rallies in gold prices reflect declining market confidence in sovereign fiat stability and mounting stagflationary headwinds."
                ]
            },
            {
                "subheading": "3. Mantra Labs Strategic Opinion",
                "paragraphs": [
                    "Mantra Labs maintains that elevated geopolitical friction accelerates the fracturing of the post-WWII monetary framework. We anticipate sustained central bank bullion accumulation throughout 2026, serving as a structural ballast against systemic dollar risks.",
                    "We recommend asset managers overweight physical commodities and upstream energy infrastructure while implementing tactical options collars on long-duration sovereign fixed income."
                ]
            }
        ]
    },
    {
        "id": "c2",
        "slug": "us-china-bilateral-dynamics-petrodollar-erosion-trade",
        "category": "ECONOMIC POLICY & DIPLOMACY",
        "badge": "MACRO STRATEGY",
        "title": "US-China Bilateral Strains and the Structural Erosion of Petrodollar Hegemony",
        "date": "November 11, 2026",
        "iso_date": "2026-11-11T03:00:00Z",
        "reading_time": "8 min read",
        "summary": "Bilateral relations between Washington and Beijing have entered a defining phase as global crude oil trade settlements increasingly bypass traditional dollar clearing rails.",
        "content_blocks": [
            {
                "subheading": "1. The 1974 Petrodollar Pact Versus Contemporary Energy Realities",
                "paragraphs": [
                    "The petrodollar arrangement established in the 1970s anchored global crude oil pricing in US Dollars, with surplus petrodollars recycled into US Treasuries in exchange for American defense assurances. This framework granted the United States unrivaled monetary flexibility for half a century.",
                    "Today, energy flows have shifted decisively eastward. With American domestic shale oil independence, over 80 percent of Gulf crude exports now sail toward Asian destinations, positioning China as the world's foremost energy importer."
                ]
            },
            {
                "subheading": "2. The Expansion of Bilateral Petroyuan and Non-Western Clearing Rails",
                "paragraphs": [
                    "Bilateral oil settlements between China and Middle Eastern producers transacted in Renminbi have expanded to over 40 percent of bilateral volumes, surpassing the Euro. Platforms like mBridge, China's CIPS network, and bilateral local currency swap lines create resilient payment rails fully insulated from Western clearing systems.",
                    "This institutional infrastructure is designed not to unseat the US Dollar instantaneously, but to establish an unassailable alternative trading architecture capable of withstanding financial embargoes."
                ]
            },
            {
                "subheading": "3. Mantra Labs Strategic Opinion",
                "paragraphs": [
                    "Our geopolitical thesis views currency diversification in cross-border energy trade as irreversible. The weaponization of financial clearing mechanisms has permanently altered sovereign risk models among global central banks.",
                    "Institutional treasurers must anticipate higher FX volatility and hedge against emerging currency balkanization by diversifying settlement accounts across neutral jurisdictions."
                ]
            }
        ]
    },
    {
        "id": "c3",
        "slug": "ai-hyperscaler-capex-supercycle-semiconductors-energy-limits",
        "category": "ARTIFICIAL INTELLIGENCE & TECH",
        "badge": "FRONTIER TECH",
        "title": "The AI Hyperscaler CapEx Supercycle: Semiconductor Foundry Constraints and Data Center Power Limits",
        "date": "November 11, 2026",
        "iso_date": "2026-11-11T02:30:00Z",
        "reading_time": "8 min read",
        "summary": "Aggressive hundred-billion-dollar infrastructure commitments by technology hyperscalers are driving an unprecedented supercycle across semiconductor foundries while confronting physical electrical grid limitations.",
        "content_blocks": [
            {
                "subheading": "1. Capital Allocation in the Foundation Model Era",
                "paragraphs": [
                    "Major cloud hyperscalers-including Microsoft, Alphabet, Meta, and Amazon-are committing combined annualized capital expenditures exceeding $200 billion to AI computing infrastructure. This capital is directly captured by leading semiconductor designers and advanced fabrication foundries like TSMC.",
                    "Unlike prior software expansions that were asset-light, modern foundation model architectures require unprecedented capital intensity, spanning specialized high-bandwidth memory (HBM), advanced liquid-cooled server racks, and ultra-low-latency optical interconnects."
                ]
            },
            {
                "subheading": "2. Power Infrastructure Bottlenecks and the Nuclear Energy Pivot",
                "paragraphs": [
                    "Wall Street analysts increasingly recognize that the critical gating factor for artificial intelligence deployment is no longer GPU availability, but access to gigawatt-scale electrical power. The exponential power demands of inferencing clusters are severely straining legacy municipal grids.",
                    "This dynamic has triggered long-term direct power purchase agreements between tech giants and nuclear utility operators, positioning baseload energy providers as central beneficiaries of the AI revolution."
                ]
            },
            {
                "subheading": "3. Mantra Labs Strategic Opinion",
                "paragraphs": [
                    "Mantra Labs anticipates that public market scrutiny will increasingly penalize speculative AI expenditure lacking clear enterprise monetization. Sustainable competitive moats will accrue to firms integrating autonomous task-execution agents directly into high-value customer workflows.",
                    "Investors should favor critical bottlenecks in the hardware and energy value chains rather than commoditized conversational wrapper startups."
                ]
            }
        ]
    },
    {
        "id": "c4",
        "slug": "federal-reserve-interest-rates-emerging-market-equity-valuations",
        "category": "EQUITIES & CAPITAL MARKETS",
        "badge": "CAPITAL FLOWS",
        "title": "Federal Reserve Rate Trajectory and the Repricing of Emerging Market Equity Valuations",
        "date": "November 11, 2026",
        "iso_date": "2026-11-11T02:00:00Z",
        "reading_time": "6 min read",
        "summary": "Persistent inflation readings and elevated sovereign bond yields continue to constrain valuation multiples across Asian and emerging market benchmark equities.",
        "content_blocks": [
            {
                "subheading": "1. The 'Higher for Longer' Yield Regime",
                "paragraphs": [
                    "Resilient labor metrics and stubborn services inflation have compelled Federal Reserve policymakers to exercise disciplined patience regarding benchmark rate reductions. With 10-year US Treasury yields remaining elevated, global risk capital requires wider risk premiums to deploy into emerging market equities.",
                    "This persistent cost of capital enforces rigorous selectivity across global investment portfolios, disproportionately penalizing highly leveraged corporations dependent on external dollar refinancing."
                ]
            },
            {
                "subheading": "2. Domestic Consumer Resilience and Banking Fortress Balances",
                "paragraphs": [
                    "Despite foreign portfolio rotation, tier-one commercial banks and consumer staples franchises across Southeast Asia continue to generate healthy net interest margins and robust cash flows, supported by steady domestic consumption.",
                    "Defensive balance sheets and conservative loan-to-deposit ratios provide substantial buffers against external currency depreciation pressure."
                ]
            },
            {
                "subheading": "3. Mantra Labs Strategic Opinion",
                "paragraphs": [
                    "We view broader market consolidation as an attractive accumulation window for institutional capital. Focusing on high-return-on-equity businesses with strong domestic pricing power offers the optimal risk-adjusted strategy ahead of global monetary inflection points."
                ]
            }
        ]
    },
    {
        "id": "c5",
        "slug": "bitcoin-etf-institutional-liquidity-supply-halving-dynamics",
        "category": "CRYPTO & DIGITAL ASSETS",
        "badge": "DIGITAL ASSETS",
        "title": "Institutional ETF Spot Inflows and Post-Halving Structural Supply Squeezes in Digital Assets",
        "date": "November 11, 2026",
        "iso_date": "2026-11-11T01:30:00Z",
        "reading_time": "6 min read",
        "summary": "The maturation of regulated spot ETF products has permanently anchored Bitcoin to macroeconomic liquidity cycles and institutional treasury allocations.",
        "content_blocks": [
            {
                "subheading": "1. Institutionalization of Digital Liquid Reserves",
                "paragraphs": [
                    "The introduction of regulated spot exchange-traded vehicles has enabled traditional pension funds, family offices, and registered investment advisors to allocate to digital assets without managing cryptographic custody keys.",
                    "Consequently, daily trading volumes and price action reflect broader institutional risk appetite, tracking macroeconomic data releases, Treasury auctions, and dollar index fluctuations."
                ]
            },
            {
                "subheading": "2. Structural Post-Halving Supply Deficits",
                "paragraphs": [
                    "The periodic reduction in daily mining block rewards permanently curbs fresh secondary market issuance. As persistent institutional absorption via ETF wrappers encounters inelastic circulating liquid supply, structural upward price pressure builds over multi-quarter horizons.",
                    "Miner capitulation phases typically mark cyclical floors where coins transfer decisively from operational sellers to long-term custodial vaults."
                ]
            },
            {
                "subheading": "3. Mantra Labs Strategic Opinion",
                "paragraphs": [
                    "Mantra Labs maintains a constructive structural outlook on premier digital reserve assets. We advise allocating capital through algorithmic dollar-cost averaging while hedging portfolio beta against cyclical macroeconomic shocks."
                ]
            }
        ]
    }
]

def build_all():
    print("=== BUILDING ENGLISH FINANCIAL EDITORIAL SITE ===")
    
    # 1. Fetch fresh live stories from RSS
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources_cfg = json.load(f)
        
    rss_generated = []
    seen_slugs = {a["slug"] for a in ENGLISH_CORE_ARTICLES}
    
    for niche in sources_cfg.get("niche_sources", []):
        niche_name = niche.get("niche", "")
        for s in niche.get("sources", []):
            s_name = s.get("name", "")
            s_rss = s.get("rss", "")
            if not s_rss:
                continue
            
            items = fetch_rss_feed(s_rss)
            for item in items[:2]:
                slug = slugify(item["title"])
                if slug in seen_slugs or len(slug) < 10:
                    continue
                seen_slugs.add(slug)
                art = rewrite_into_english_mantra_article(item, niche_name, s_name)
                rss_generated.append(art)
                break
                
    total_articles = ENGLISH_CORE_ARTICLES + rss_generated
    print(f"Total English articles ready: {len(total_articles)}")
    
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(total_articles, f, indent=2)
        
    # 2. Render standalone HTML pages
    HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
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

    .article-wrap {{
      max-width: 840px;
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
      <span class="back-tag">&larr; NEWS DESK</span>
      <span>MANTRA LABS // FINANCIAL</span>
    </a>
    <span class="cat-badge">{badge}</span>
  </header>

  <main class="article-wrap">
    <article class="article-header">
      <div class="meta-line">
        <span>SECTOR: <b>{category}</b></span>
        <span>DATE: <b>{date}</b></span>
        <span>READ: <b>{reading_time}</b></span>
      </div>
      <h1>{title}</h1>
      <p class="lead-summary">{summary}</p>
      <div style="margin-top:20px;border:1px solid var(--border);overflow:hidden;background:#050505;"><img src="{image_url}" alt="{title}" style="width:100%;height:380px;object-fit:cover;display:block;" loading="lazy"></div>
    </article>

    <div class="article-body">
      {body_html}

      <div class="bottom-actions">
        <a href="/" class="action-btn">&larr; BACK TO EDITORIAL HOMEPAGE</a>
        <a href="#top" class="action-btn">RETURN TO TOP &uarr;</a>
      </div>
    </div>
  </main>

  <footer>
    MANTRA LABS FINANCIAL DISPATCH &bull; QUANTITATIVE MACRO, COMMODITIES, DIGITAL ASSETS & STRATEGIC DIPLOMACY &bull; ALL RIGHTS RESERVED
  </footer>

</body>
</html>
"""
    for art in total_articles:
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
            image_url=art.get("image_url", "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80"),
            body_html=body_html
        )
        out_file = ARTICLES_DIR / f"{art['slug']}.html"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(page_html)

    # 3. Render English Homepage
    lead_art = total_articles[0]
    grid_arts = total_articles[1:]
    grid_cards_html = []
    for a in grid_arts:
        card = f"""
    <article class="news-card">
      <div style="margin:-24px -24px 16px -24px;overflow:hidden;height:160px;border-bottom:1px solid var(--border);"><img src="{a.get('image_url', 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80')}" alt="{a['title']}" style="width:100%;height:100%;object-fit:cover;display:block;" loading="lazy"></div>
      <div class="card-meta">
        <span class="card-cat">{a['category']}</span>
        <span class="card-date">{a['date']} &bull; {a['reading_time']}</span>
      </div>
      <h3 class="card-title">
        <a href="/articles/{a['slug']}.html">{a['title']}</a>
      </h3>
      <p class="card-summary">{a['summary']}</p>
      <div class="card-footer">
        <a href="/articles/{a['slug']}.html" class="read-link">READ FULL DISPATCH &rarr;</a>
      </div>
    </article>
        """
        grid_cards_html.append(card)
    grid_cards_rendered = "\n".join(grid_cards_html)

    HOME_PAGE_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MANTRA LABS // Financial News, Equities, Crypto & Global Geopolitics</title>
  <meta name="description" content="Institutional financial intelligence covering equities, digital assets, energy supply chains, gold and oil wartime dynamics, and bilateral economic statecraft.">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="https://mantralabs.web.id/">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mantra Labs Financial">
  <meta property="og:url" content="https://mantralabs.web.id/">
  <meta property="og:title" content="MANTRA LABS // Financial News & Global Macro Intelligence">
  <meta property="og:description" content="Deep-dive institutional analysis on capital markets, commodities, crypto, bilateral trade policies, and AI infrastructure.">

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
      --text: #e6e6e6;
      --text-muted: #888888;
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
      line-height: 1.6;
      padding: 0;
      margin: 0;
    }}

    header.site-header {{
      background: #000;
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .header-inner {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .site-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: #fff;
    }}

    .brand-logo {{
      font-family: var(--font-head);
      font-weight: 700;
      font-size: 20px;
      letter-spacing: 1px;
    }}

    .brand-logo span {{
      color: var(--amber);
    }}

    .brand-tag {{
      background: #111;
      border: 1px solid var(--border-accent);
      color: var(--text-muted);
      font-family: var(--font-mono);
      font-size: 10px;
      padding: 2px 6px;
      letter-spacing: 1px;
    }}

    nav.main-nav {{
      display: flex;
      gap: 20px;
    }}

    .nav-link {{
      color: var(--text-muted);
      text-decoration: none;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 500;
      transition: color 0.2s;
    }}

    .nav-link:hover, .nav-link.active {{
      color: var(--amber);
    }}

    .ticker-bar {{
      background: #060500;
      border-bottom: 1px solid var(--border);
      overflow: hidden;
      display: flex;
      height: 32px;
      align-items: center;
    }}

    .ticker-title {{
      background: #0f0a00;
      color: var(--amber);
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 700;
      padding: 0 12px;
      height: 100%;
      display: flex;
      align-items: center;
      border-right: 1px solid var(--border-accent);
      flex-shrink: 0;
      letter-spacing: 1px;
    }}

    .ticker-track {{
      overflow: hidden;
      white-space: nowrap;
      flex: 1;
    }}

    .ticker-content {{
      display: inline-block;
      white-space: nowrap;
      animation: tickerRun 90s linear infinite;
      font-family: var(--font-mono);
      font-size: 11px;
      color: #aaa;
      padding-left: 100%;
    }}

    .ticker-content:hover {{
      animation-play-state: paused;
    }}

    @keyframes tickerRun {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-100%); }}
    }}

    .container {{
      max-width: 1200px;
      margin: 30px auto 60px;
      padding: 0 20px;
    }}

    .featured-section {{
      margin-bottom: 40px;
    }}

    .featured-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 32px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      position: relative;
      transition: border-color 0.2s;
    }}

    .featured-card:hover {{
      border-color: var(--amber);
    }}

    .featured-badge-row {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .badge-label {{
      background: var(--amber);
      color: #000;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      letter-spacing: 1px;
    }}

    .badge-cat {{
      color: var(--amber);
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
    }}

    .featured-title {{
      font-family: var(--font-head);
      font-size: 28px;
      line-height: 1.3;
      color: #fff;
    }}

    .featured-title a {{
      color: inherit;
      text-decoration: none;
    }}

    .featured-title a:hover {{
      color: var(--amber);
    }}

    .featured-summary {{
      font-size: 16px;
      color: #bbb;
      line-height: 1.7;
      max-width: 900px;
    }}

    .featured-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-muted);
      border-top: 1px solid #141414;
      padding-top: 16px;
      margin-top: 8px;
    }}

    .read-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--amber);
      text-decoration: none;
      font-weight: 600;
    }}

    .read-btn:hover {{
      text-decoration: underline;
    }}

    .section-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
    }}

    .section-title {{
      font-family: var(--font-head);
      font-size: 20px;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .section-title::before {{
      content: "";
      width: 4px;
      height: 18px;
      background: var(--amber);
      display: inline-block;
    }}

    .articles-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 24px;
    }}

    .news-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: border-color 0.2s;
    }}

    .news-card:hover {{
      border-color: var(--amber);
    }}

    .card-meta {{
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 12px;
    }}

    .card-cat {{
      color: var(--amber);
      font-weight: 600;
    }}

    .card-title {{
      font-family: var(--font-head);
      font-size: 19px;
      line-height: 1.4;
      margin-bottom: 12px;
    }}

    .card-title a {{
      color: #fff;
      text-decoration: none;
      transition: color 0.15s;
    }}

    .card-title a:hover {{
      color: var(--amber);
    }}

    .card-summary {{
      font-size: 14px;
      color: #aaa;
      line-height: 1.6;
      margin-bottom: 20px;
      flex-grow: 1;
    }}

    .card-footer {{
      border-top: 1px solid #141414;
      padding-top: 14px;
    }}

    .read-link {{
      color: var(--amber);
      text-decoration: none;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.5px;
    }}

    .read-link:hover {{
      text-decoration: underline;
    }}

    footer.site-footer {{
      background: #000;
      border-top: 1px solid var(--border);
      padding: 30px 20px;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-muted);
    }}

    @media (max-width: 768px) {{
      nav.main-nav {{ display: none; }}
      .featured-title {{ font-size: 22px; }}
      .featured-card {{ padding: 20px; }}
    }}
  </style>
</head>
<body>

  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="site-brand">
        <span class="brand-logo">MANTRA<span>LABS</span></span>
        <span class="brand-tag">GLOBAL DISPATCH</span>
      </a>
      <nav class="main-nav">
        <a href="/" class="nav-link active">ALL DISPATCHES</a>
        <a href="/articles/gold-oil-middle-east-war-risk-transmission-macro-assets.html" class="nav-link">COMMODITIES & WAR</a>
        <a href="/articles/ai-hyperscaler-capex-supercycle-semiconductors-energy-limits.html" class="nav-link">AI & TECH</a>
        <a href="/articles/us-china-bilateral-dynamics-petrodollar-erosion-trade.html" class="nav-link">BILATERAL MACRO</a>
        <a href="/articles/federal-reserve-interest-rates-emerging-market-equity-valuations.html" class="nav-link">EQUITIES</a>
        <a href="/articles/bitcoin-etf-institutional-liquidity-supply-halving-dynamics.html" class="nav-link">DIGITAL ASSETS</a>
      </nav>
    </div>
  </header>

  <div class="ticker-bar">
    <div class="ticker-title">LIVE TELEMETRY</div>
    <div class="ticker-track">
      <div class="ticker-content">
        BRENT CRUDE $85.60/bbl ▲  &bull;  WTI CRUDE $81.42/bbl ▲  &bull;  GOLD SPOT $2,318.70/oz ▲  &bull;  NVDA $875.30 ▲  &bull;  AI CAPEX SPEND: $200B+ RUN-RATE ▲  &bull;  TSMC WAFER UTILIZATION: 98.4% ▲  &bull;  USD/IDR Rp16,145 ▲  &bull;  IHSG 7,285.40 ▲ +0.55%  &bull;  S&P 500 5,248.49 ▲  &bull;  NASDAQ 18,386.22 ▲  &bull;  BTC/USD $67,840 ▲  &bull;  ETH/USD $3,542 ▲  &bull;  US 10Y YIELD 4.312% ▲  &bull;  FED FUNDS RATE: 5.25-5.50% HOLD  &bull;  RMB OIL SHARE: 41% IN MIDDLE EAST-CHINA TRADE &bull; 
      </div>
    </div>
  </div>

  <main class="container">
    
    <section class="featured-section">
      <div class="featured-card">
        <div class="featured-badge-row">
          <span class="badge-label">{lead_art['badge']}</span>
          <span class="badge-cat">{lead_art['category']}</span>
        </div>
        <h2 class="featured-title">
          <a href="/articles/{lead_art['slug']}.html">{lead_art['title']}</a>
        </h2>
        <div style="margin:12px 0;border:1px solid var(--border);overflow:hidden;max-height:340px;"><img src="{lead_art.get('image_url', 'https://images.unsplash.com/photo-1610375461246-83df859d849d?auto=format&fit=crop&w=1200&q=80')}" alt="{lead_art['title']}" style="width:100%;height:340px;object-fit:cover;display:block;" loading="lazy"></div>
        <p class="featured-summary">{lead_art['summary']}</p>
        <div class="featured-footer">
          <span>Published: {lead_art['date']} &bull; {lead_art['reading_time']}</span>
          <a href="/articles/{lead_art['slug']}.html" class="read-btn">READ COMPLETE ANALYSIS &rarr;</a>
        </div>
      </div>
    </section>

    <section>
      <div class="section-head">
        <h3 class="section-title">LATEST INTELLIGENCE DISPATCHES</h3>
        <span style="font-family:var(--font-mono);font-size:12px;color:var(--text-muted);">{len(total_articles)} RESEARCH DISPATCHES AVAILABLE</span>
      </div>

      <div class="articles-grid">
        {grid_cards_rendered}
      </div>
    </section>

  </main>

  <footer class="site-footer">
    MANTRA LABS FINANCIAL INTELLIGENCE &bull; INSTITUTIONAL MACRO, COMMODITIES, DIGITAL ASSETS & STRATEGIC DIPLOMACY &bull; 2026
  </footer>

</body>
</html>
"""
    with open(SITE_ROOT / "index.html", "w", encoding="utf-8") as f:
        f.write(HOME_PAGE_HTML)
        
    # 4. Update Sitemap
    base_url = "https://mantralabs.web.id"
    all_files = ["index.html"] + [f"articles/{a['slug']}.html" for a in total_articles]
    sitemap_items = []
    now_str = datetime.now().strftime("%Y-%m-%d")
    for f in all_files:
        loc = f"{base_url}/" if f == "index.html" else f"{base_url}/{f}"
        priority = "1.0" if f == "index.html" else "0.8"
        sitemap_items.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{now_str}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{priority}</priority>
  </url>""")
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_items)}
</urlset>"""
    with open(SITEMAP_FILE, "w", encoding="utf-8") as fp:
        fp.write(sitemap_xml)
        
    print(f"Site and sitemap successfully rebuilt in English with {len(total_articles)} articles.")

if __name__ == "__main__":
    build_all()
