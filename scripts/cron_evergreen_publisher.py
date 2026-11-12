# -*- coding: utf-8 -*-
"""
MANTRA LABS - Autonomous Evergreen Financial Article Generator
Designed to run via Cronjob (2x daily or on schedule).
Rotates systematically through the 5 core Mantra Labs evergreen pillars:
1. Commodities & Wartime Geopolitics (Gold & Oil, Strait of Hormuz)
2. Global Macro & Bilateral Statecraft (US-China Petrodollar / Petroyuan)
3. Artificial Intelligence & Computing Infrastructure (CapEx & Energy Grid)
4. Capital Markets & Sovereign Yields (Equities & Monetary Trajectories)
5. Digital Assets & Institutional Liquidity (Bitcoin Spot ETF & Post-Halving)

Output:
- Full English institutional analysis.
- Zero em-dashes (—).
- Dedicated 'Mantra Labs Strategic Opinion' section.
- Automatic git commit, push, and Cloudflare edge cache purge.
"""

import os
import sys
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import urllib.request

SITE_ROOT = Path(r"D:\PORTFOLIO_NEO_BRUTALISM")
ARTICLES_DIR = SITE_ROOT / "articles"
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR = SITE_ROOT / "data"
DB_FILE = DATA_DIR / "financial_articles.json"
SITEMAP_FILE = SITE_ROOT / "sitemap.xml"
STATE_FILE = DATA_DIR / "evergreen_cron_state.json"

EVERGREEN_TOPIC_PILLARS = [
    {
        "category": "COMMODITIES & GEOPOLITICS",
        "badge": "EVERGREEN MACRO",
        "title_template": "Strategic Petroleum Reserves and Global Supply Shocks: Physical Balancing Realities in Prolonged Geopolitical Conflicts",
        "reading_time": "7 min read",
        "summary": "An examination of how national emergency strategic petroleum stockpiles interact with private commercial storage during structural maritime transport disruptions.",
        "blocks": [
            ("1. The Architecture of Sovereign Energy Buffers", [
                "Strategic petroleum reserves were instituted following the 1973 oil embargo to provide member states with minimum 90-day net import coverage. In modern prolonged maritime crises, however, coordinated emergency releases offer only transient relief against structural physical export deficits.",
                "When maritime insurance underwriters declare regional transit corridors high-risk zones, physical prompt tanker availability contracts dramatically, rendering inland storage draws logistically complex to distribute globally."
            ]),
            ("2. Safe-Haven Gold Elasticity Under Sustained Embargoes", [
                "Historical analysis of multi-theatre wartime disruptions reveals that bullion prices decouple from real interest rate parity during periods of overt financial sanctions and reserve asset freezes.",
                "Sovereign central banks increasingly treat allocated physical gold vaulted in domestic jurisdictions as unassailable monetary capital immune to geopolitical weaponization."
            ]),
            ("3. Mantra Labs Strategic Opinion", [
                "Mantra Labs maintains that emergency reserve releases deplete sovereign defensive buffers without addressing underlying refining complexity or transit route vulnerability.",
                "Institutional portfolios should hold structural allocations to upstream energy producers and physical commodity royalties as systemic hedges against continuous supply fragmentation."
            ])
        ]
    },
    {
        "category": "ECONOMIC POLICY & DIPLOMACY",
        "badge": "EVERGREEN MACRO",
        "title_template": "Cross-Border Central Bank Digital Currencies and the Architecture of Post-Western Settlement Bilateralism",
        "reading_time": "8 min read",
        "summary": "How multi-central bank digital platforms and bilateral currency clearing lines permanently reduce reliance on traditional correspondent banking networks.",
        "blocks": [
            ("1. Technical Foundations of Wholesale CBDC Platforms", [
                "Wholesale central bank digital currency networks like Project mBridge enable real-time peer-to-peer foreign exchange settlement utilizing distributed ledger technology without passing through US intermediary clearing banks.",
                "By executing atomic settlement across participating sovereign central banks, bilateral counterparties eliminate settlement risk and bypass correspondent banking fees entirely."
            ]),
            ("2. Bilateral Trade Invoicing in Domestic Currencies", [
                "Bilateral currency swap agreements between major commodity exporters and Asian manufacturing hubs have expanded beyond emergency liquidity facilities into primary invoicing instruments.",
                "This transition allows energy importers to settle purchases in their own national currencies or bilateral credits, directly insulating their domestic economies from external foreign exchange shocks."
            ]),
            ("3. Mantra Labs Strategic Opinion", [
                "Our macro analysis indicates that the growth of alternative settlement platforms is structurally irreversible. While the US Dollar remains the primary unit of account, its dominance as the exclusive medium of exchange in global energy is eroding.",
                "Corporate treasurers must transition toward multi-clearing capabilities to maintain operational resilience in an increasingly multipolar trading environment."
            ])
        ]
    },
    {
        "category": "ARTIFICIAL INTELLIGENCE & TECH",
        "badge": "EVERGREEN MACRO",
        "title_template": "Autonomous AI Agent Workflows and the Restructuring of Institutional Financial Productivity",
        "reading_time": "7 min read",
        "summary": "How multi-step agentic execution frameworks are replacing manual data synthesis across quantitative research, risk underwriting, and regulatory compliance.",
        "blocks": [
            ("1. Beyond Passive Conversational Interfaces", [
                "The primary frontier of enterprise artificial intelligence deployment has shifted from static conversational models to autonomous agentic architectures capable of tool execution, multi-hop reasoning, and self-directed error recovery.",
                "In financial analysis, these systems autonomously parse unstructured regulatory disclosures, cross-validate cash flow reconciliations, and formulate stress-test scenarios in fractions of traditional analyst cycles."
            ]),
            ("2. Deterministic Verification and Hallucination Mitigation", [
                "Deploying agentic systems in high-stakes capital allocation mandates strict deterministic guardrails. Tier-one institutions enforce multi-agent verification loops where secondary judge agents audit primary output against source documents before execution.",
                "This verifiable chain-of-thought architecture ensures full compliance with fiduciary transparency standards and auditability mandates."
            ]),
            ("3. Mantra Labs Strategic Opinion", [
                "Mantra Labs projects that enterprise value creation in the software sector will concentrate among platforms orchestrating complex autonomous execution rather than raw API resale.",
                "Firms that systematically integrate autonomous agents into institutional decision workflows will secure durable productivity advantages over legacy manual competitors."
            ])
        ]
    },
    {
        "category": "EQUITIES & CAPITAL MARKETS",
        "badge": "EVERGREEN MACRO",
        "title_template": "Free Cash Flow Compounding and Balance Sheet Durability in Extended High-Cost-of-Capital Environments",
        "reading_time": "6 min read",
        "summary": "Why structural shifts in benchmark sovereign interest rates favor self-funding capital allocators over leveraged multiple expansion models.",
        "blocks": [
            ("1. The Demise of Speculative Multiple Expansion", [
                "The era of near-zero interest rates enabled unprofitable growth businesses to trade at elevated revenue multiples driven by cheap access to speculative refinancing capital.",
                "In a normalized interest rate regime where sovereign debt delivers meaningful risk-free yields, equity valuations must be justified by immediate free cash flow generation and organic return on invested capital."
            ]),
            ("2. The Competitive Advantage of Pristine Balance Sheets", [
                "Corporations with minimal floating-rate debt and substantial net cash reserves enjoy counter-cyclical advantages. They can fund research and development, execute accretive mergers, and repurchase undervalued shares while leveraged competitors face debt service crunches.",
                "This divergence creates profound dispersion between disciplined industry consolidators and capital-dependent laggards."
            ]),
            ("3. Mantra Labs Strategic Opinion", [
                "Mantra Labs recommends equity investors anchor selection criteria around organic free cash flow yield and pricing power rather than top-line momentum.",
                "High-quality balance sheets provide both essential downside protection during macroeconomic contractions and explosive compounding capability during subsequent recoveries."
            ])
        ]
    },
    {
        "category": "CRYPTO & DIGITAL ASSETS",
        "badge": "EVERGREEN MACRO",
        "title_template": "Inelastic Supply Economics and the Maturation of Sovereign Digital Reserve Assets",
        "reading_time": "6 min read",
        "summary": "Analyzing the macroeconomic properties of mathematically fixed monetary issuance against expanding global fiat sovereign obligations.",
        "blocks": [
            ("1. Algorithmic Inelasticity in a Expanding Debt Regime", [
                "Unlike sovereign fiat currencies whose supply expands to accommodate sovereign fiscal deficits, algorithmic digital assets enforce absolute mathematical scarcity governed by open cryptographic protocols.",
                "As global sovereign debt ratios reach historical peacetime highs, institutional allocators increasingly view programmatically constrained assets as essential non-sovereign stores of value."
            ]),
            ("2. The Mechanics of Institutional Custodial Absorption", [
                "Regulated spot exchange-traded funds have established high-capacity financial pipes linking traditional brokerage accounts to physical on-chain vaults.",
                "This structural absorption permanently removes liquid circulating supply from secondary market venues, creating compounding upward price sensitivity to incremental liquidity inflows."
            ]),
            ("3. Mantra Labs Strategic Opinion", [
                "Our digital asset research framework views Bitcoin as an emerging sovereign hedge rather than a speculative tech equity proxy.",
                "Allocators should treat spot digital holdings as multi-year strategic treasury reserves, ignoring high-frequency derivative flushes while focusing on long-term monetary debasement trends."
            ])
        ]
    }
]

def clean_text(text: str) -> str:
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", "", text)
    clean = clean.replace("—", "-").replace("–", "-")
    return re.sub(r"\s+", " ", clean).strip()

def slugify(title: str) -> str:
    clean = clean_text(title).lower()
    clean = re.sub(r"[^a-z0-9\s-]", "", clean)
    clean = re.sub(r"[\s-]+", "-", clean).strip("-")
    return clean[:70]

def get_next_pillar_index():
    idx = 0
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                idx = (data.get("last_index", 0) + 1) % len(EVERGREEN_TOPIC_PILLARS)
        except Exception:
            idx = 0
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_index": idx, "updated_at": datetime.now(timezone.utc).isoformat()}, f)
    return idx

def run_evergreen_cron():
    print("=== MANTRA LABS AUTONOMOUS EVERGREEN PUBLISHER ===")
    
    idx = get_next_pillar_index()
    pillar = EVERGREEN_TOPIC_PILLARS[idx]
    
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%B %d, %Y")
    iso_date = now.isoformat()
    
    title = pillar["title_template"]
    slug = slugify(title)
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)
        
    # Check if this exact slug already exists
    if any(a["slug"] == slug for a in articles):
        slug = f"{slug}-{now.strftime('%m%d')}"
        
    from image_pool import get_unique_image
    used_images = {a.get("image_url") for a in articles if a.get("image_url")}
    assigned_image = get_unique_image(pillar["category"], used_images)

    article_dict = {
        "id": str(int(now.timestamp())),
        "slug": slug,
        "category": pillar["category"],
        "badge": pillar["badge"],
        "title": title,
        "date": date_str,
        "iso_date": iso_date,
        "reading_time": pillar["reading_time"],
        "summary": pillar["summary"],
        "image_url": assigned_image,
        "source": "Mantra Labs Institutional Research",
        "source_url": f"https://mantralabs.web.id/articles/{slug}.html",
        "content_blocks": [
            {
                "subheading": sub,
                "paragraphs": paras
            }
            for sub, paras in pillar["blocks"]
        ]
    }
    
    # Prepend to database
    articles.insert(0, article_dict)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)
        
    print(f"Generated Evergreen Article: {title} ({pillar['category']})")
    
    # Rebuild website using existing builder
    builder_script = SITE_ROOT / "scripts" / "build_english_financial_portal.py"
    subprocess.check_call([sys.executable, str(builder_script)])
    
    # Git commit and push
    env_file = Path('C:/Users/dxisa/AppData/Local/hermes/.env')
    token = ''
    token_cf = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    if env_file.exists():
        for eline in env_file.read_text(encoding='utf-8').splitlines():
            if eline.startswith('GITHUB_TOKEN=') and not token:
                token = eline.split('=', 1)[1].strip()
            elif eline.startswith('CLOUDFLARE_API_TOKEN=') and not token_cf:
                token_cf = eline.split('=', 1)[1].strip()

    if not token:
        token_file = Path('C:/Users/dxisa/AppData/Local/hermes/scripts/sync_vault_to_github.py')
        if token_file.exists():
            with open(token_file, 'r', encoding='utf-8') as tf:
                m = re.search(r'TOKEN\s*=\s*"([^"]+)"', tf.read())
                if m:
                    token = m.group(1)

    if token:
        clean_url = 'https://github.com/isafrk/MASASA.git'
        auth_url = f'https://x-access-token:{token}@github.com/isafrk/MASASA.git'
        subprocess.check_call(['git', '-C', str(SITE_ROOT), 'add', '.'])
        status_out = subprocess.check_output(['git', '-C', str(SITE_ROOT), 'status', '--porcelain'], text=True)
        if status_out.strip():
            subprocess.check_call(['git', '-C', str(SITE_ROOT), 'commit', '-m', f'Cron Auto-Publish Evergreen: {title[:50]}...'])
        subprocess.check_call(['git', '-C', str(SITE_ROOT), 'remote', 'set-url', 'origin', auth_url])
        try:
            out = subprocess.check_output(['git', '-C', str(SITE_ROOT), 'push', 'origin', 'main'], text=True)
            print('Git push completed successfully.')
        finally:
            subprocess.check_call(['git', '-C', str(SITE_ROOT), 'remote', 'set-url', 'origin', clean_url])

    # Purge Cloudflare
    if not token_cf:
        token_cf = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    zone_id = "b86d3b08b157ac29256c8e461744f89a"
    if token_cf:
        try:
            req = urllib.request.Request(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache",
                data=json.dumps({"purge_everything": True}).encode(),
                headers={"Authorization": f"Bearer {token_cf}", "Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as r:
                print("Cloudflare cache purged:", json.loads(r.read().decode()).get("success"))
        except Exception as e:
            print("Cloudflare purge error:", e)

if __name__ == "__main__":
    run_evergreen_cron()
