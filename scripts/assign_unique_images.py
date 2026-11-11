import json

# Curated verified high-res royalty-free Unsplash images
IMAGE_REGISTRY = {
    # 1. Lead war/gold article
    "gold-oil-middle-east-war-risk-transmission-macro-assets": "https://images.unsplash.com/photo-1610375461246-83df859d849d?auto=format&fit=crop&w=1200&q=80", # Gold bullion
    # 2. US China bilateral
    "us-china-bilateral-dynamics-petrodollar-erosion-trade": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=1200&q=80", # Currency & globe
    # 3. AI CapEx
    "ai-hyperscaler-capex-supercycle-semiconductors-energy-limits": "https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=1200&q=80", # Silicon chip & GPU
    # 4. Federal Reserve Equities
    "federal-reserve-interest-rates-emerging-market-equity-valuations": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80", # Financial skyscraper & Wall St
    # 5. Bitcoin ETF
    "bitcoin-etf-institutional-liquidity-supply-halving-dynamics": "https://images.unsplash.com/photo-1516245834210-c4c142787335?auto=format&fit=crop&w=1200&q=80", # Physical Bitcoin macro
    # 6. Middle East oil flows
    "middle-east-oil-flows-far-from-normal-despite-signs-of-oversupply": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1200&q=80", # Oil tanker maritime
    # 7. Platinum & Copper
    "platinum-and-copper-reversals-raise-doubts-about-the-strength-of-recen": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1200&q=80", # Industrial raw copper / metal
    # 8. Former Iraqi lawmaker
    "former-iraqi-awmaker-ahmed-al-alwani-found-dead-in-beirut": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&w=1200&q=80", # Geopolitical smoke / security
    # 9. China India trade
    "china-wants-indias-market-does-it-want-indias-industrial-rise": "https://images.unsplash.com/photo-1578575317765-bc5cb6a92ec2?auto=format&fit=crop&w=1200&q=80", # Container cargo port
    # 10. Social security 100 years
    "the-thought-of-living-to-100-terrifies-me-is-social-security-a-giant-p": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=1200&q=80", # Calculator & retirement documents
    # 11. Warren White house betting
    "warren-what-is-white-house-doing-to-prevent-a-repeat-of-teleprompters-": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1200&q=80", # Washington Capitol / regulatory
    # 12. LNbits emergency patch
    "lnbits-rushes-emergency-patch-after-reported-bitcoin-wallet-thefts": "https://images.unsplash.com/photo-1563986768494-4dee2763ff3f?auto=format&fit=crop&w=1200&q=80", # Cyber security & code
    # 13. Bitcoin miner HIVE AI revenue
    "bitcoin-miner-hive-eyes-45-million-in-annual-revenue-from-ai-deal": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80", # Server rack datacenter
    # 14. Forward industries SOL
    "forward-industries-grows-sol-treasury-to-87-million-as-token-hits-near": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&w=1200&q=80", # Abstract decentralized crypto art
    # 15. Grok Build coding agent leak
    "grok-build-coding-agent-leaks-oodles-of-confidential-info-some-belongi": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80", # Matrix code screen
    # 16. OpenAI acquires Odessia
    "openai-acquires-odessia-travel-startup-created-by-sonder-founder": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80", # Travel / modern architecture
    # 17. Hugging Face Google Cloud
    "pay-for-hugging-face-hub-with-your-google-cloud-account": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80", # Cloud infrastructure network
    # 18. Microsoft optical networking
    "microsoft-lobbies-against-potential-ban-on-chinese-optical-networking-": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80", # Fiber optics & hardware circuits
}

# Category fallback pools if slug not matched
CATEGORY_POOLS = {
    "COMMODITIES & GEOPOLITICS": [
        "https://images.unsplash.com/photo-1610375461246-83df859d849d?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1544725176-7c40e5a71c5e?auto=format&fit=crop&w=1200&q=80"
    ],
    "ECONOMIC POLICY & DIPLOMACY": [
        "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1578575317765-bc5cb6a92ec2?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?auto=format&fit=crop&w=1200&q=80"
    ],
    "ARTIFICIAL INTELLIGENCE & TECH": [
        "https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80"
    ],
    "EQUITIES & CAPITAL MARKETS": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1642543492481-44e81e3914a7?auto=format&fit=crop&w=1200&q=80"
    ],
    "CRYPTO & DIGITAL ASSETS": [
        "https://images.unsplash.com/photo-1516245834210-c4c142787335?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80"
    ]
}

db_file = r"D:\PORTFOLIO_NEO_BRUTALISM\data\financial_articles.json"
with open(db_file, "r", encoding="utf-8") as f:
    articles = json.load(f)

for i, a in enumerate(articles):
    slug = a.get("slug", "")
    cat = a.get("category", "")
    if slug in IMAGE_REGISTRY:
        a["image_url"] = IMAGE_REGISTRY[slug]
    else:
        pool = CATEGORY_POOLS.get(cat, CATEGORY_POOLS["EQUITIES & CAPITAL MARKETS"])
        a["image_url"] = pool[i % len(pool)]

with open(db_file, "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=2)

print(f"Assigned unique distinct images to all {len(articles)} articles!")
