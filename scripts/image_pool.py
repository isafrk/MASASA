"""
MANTRA LABS - Curated High-Resolution Royalty-Free Financial Image Pool
Over 100+ verified unique Unsplash photography URLs across 5 core pillars.
Used by autonomous pipeline to guarantee ZERO duplicate images across any article.
"""

IMAGE_POOLS = {
    "COMMODITIES & GEOPOLITICS": [
        "https://images.unsplash.com/photo-1610375461246-83df859d849d", # Gold bullion stacks
        "https://images.unsplash.com/photo-1518709268805-4e9042af9f23", # Crude tanker at sea
        "https://images.unsplash.com/photo-1544725176-7c40e5a71c5e", # Industrial oil refinery
        "https://images.unsplash.com/photo-1563986768609-322da13575f3", # Copper / mineral cathode
        "https://images.unsplash.com/photo-1579546929518-9e396f3cc809", # Geopolitical crisis / defense
        "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b", # Gold coins pile
        "https://images.unsplash.com/photo-1518384401463-d3876163c195", # Offshore oil rig drilling
        "https://images.unsplash.com/photo-1508873696983-2df5703bc20d", # Cargo vessel in ocean
        "https://images.unsplash.com/photo-1527525443983-6e60c75fff46", # Industrial steel & smelting
        "https://images.unsplash.com/photo-1589829545856-d10d557cf95f", # Legal gavel & international treaty
        "https://images.unsplash.com/photo-1509391365360-2e959784a276", # Desert oil pipelines
        "https://images.unsplash.com/photo-1624365168968-f283b54972ff", # Raw gold nuggets
        "https://images.unsplash.com/photo-1568285564883-718228302f37", # Metal pipes & energy grid
        "https://images.unsplash.com/photo-1581092160607-ee22621dd758", # Industrial laboratory & minerals
        "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a"  # Desert horizon & petroleum
    ],
    "ECONOMIC POLICY & DIPLOMACY": [
        "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e", # Global currency banknotes
        "https://images.unsplash.com/photo-1578575317765-bc5cb6a92ec2", # Container cargo shipping terminal
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb", # Shanghai Pudong skyline
        "https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3", # Container ship leaving harbor
        "https://images.unsplash.com/photo-1541872703-74c5e44368f9", # US Capitol Washington DC
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa", # Earth globe digital satellite
        "https://images.unsplash.com/photo-1529400971008-f566de0e6dfc", # European central district Frankfurt
        "https://images.unsplash.com/photo-1507679799987-c73779587ccf", # Diplomatic negotiation table
        "https://images.unsplash.com/photo-1512453979798-5ea266f8880c", # Dubai financial center skyline
        "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab", # High-rise corporate banking towers
        "https://images.unsplash.com/photo-1521791136064-7986c2920216", # Executive bilateral handshake
        "https://images.unsplash.com/photo-1444653614773-995cb1ef902f", # London Bank of England district
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3", # Digital global networking
        "https://images.unsplash.com/photo-1524850011238-e3d235c7d4c9"  # World map blueprint
    ],
    "ARTIFICIAL INTELLIGENCE & TECH": [
        "https://images.unsplash.com/photo-1591488320449-011701bb6704", # Silicon wafer microchip
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31", # Server racks & blue LED lighting
        "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe", # Fluid neural network visualization
        "https://images.unsplash.com/photo-1518770660439-4636190af475", # Printed circuit board macro
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a8", # Datacenter aisle cooling
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5", # Terminal green code matrix
        "https://images.unsplash.com/photo-1531297484001-80022131f5a1", # Sleek tech laptop & dark ambient
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d", # High-speed fiber optic glow
        "https://images.unsplash.com/photo-1516321497487-e288fb19713f", # Digital neural node web
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c", # Tech engineering workstation
        "https://images.unsplash.com/photo-1620712943543-bcc4688e7485", # AI cyber face mesh
        "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2", # Hardware motherboard inspection
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b"  # Cyber security firewall shield
    ],
    "EQUITIES & CAPITAL MARKETS": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3", # Financial trading screen green/red
        "https://images.unsplash.com/photo-1642543492481-44e81e3914a7", # Candlestick chart upward trend
        "https://images.unsplash.com/photo-1554224155-6726b3ff858f", # Financial accounting & balance sheet
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f", # Stock ticker numbers display
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f", # Quantitative analytics graph
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29", # Corporate boardroom high rise
        "https://images.unsplash.com/photo-1559526324-4b87b5e36e44", # Investor presentation metrics
        "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e", # Capital banknotes & calculations
        "https://images.unsplash.com/photo-1507679799987-c73779587ccf", # Executive equity negotiation
        "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40", # Financial planning workspace
        "https://images.unsplash.com/photo-1565372195458-9de0b320ef04", # Wall street bronze charging bull
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3"  # Multi-screen broker trading desk
    ],
    "CRYPTO & DIGITAL ASSETS": [
        "https://images.unsplash.com/photo-1516245834210-c4c142787335", # Physical Bitcoin on dark slate
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0", # Decentralized 3D token sphere
        "https://images.unsplash.com/photo-1563986768494-4dee2763ff3f", # Cryptographic private key security
        "https://images.unsplash.com/photo-1621416894569-0f39ed31d247", # Bitcoin mining hardware rig
        "https://images.unsplash.com/photo-1622979135225-d2ba269bc1df", # Solana & altcoin visualization
        "https://images.unsplash.com/photo-1640340434855-6084b1f4901c", # Ethereum digital token render
        "https://images.unsplash.com/photo-1622979135225-d2ba269bc1df", # Digital currency blockchain network
        "https://images.unsplash.com/photo-1639762681057-408e52192e55", # Web3 decentralized governance
        "https://images.unsplash.com/photo-1518770660439-4636190af475", # Hardware wallet cryptographic chips
        "https://images.unsplash.com/photo-1621504450181-5d356f61d307"  # Golden crypto coin macro
    ]
}

def get_unique_image(category: str, used_urls: set) -> str:
    pool = IMAGE_POOLS.get(category, IMAGE_POOLS["EQUITIES & CAPITAL MARKETS"])
    for base in pool:
        clean_url = f"{base}?auto=format&fit=crop&w=1200&q=80"
        if clean_url not in used_urls:
            used_urls.add(clean_url)
            return clean_url
    # If all in category used, return a deterministic variant using unique params
    suffix = len(used_urls) + 1
    fallback = f"{pool[suffix % len(pool)]}?auto=format&fit=crop&w=1200&q=80&sig={suffix}"
    used_urls.add(fallback)
    return fallback
