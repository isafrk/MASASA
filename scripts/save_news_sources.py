import json

SOURCES_CONFIG = {
    "niche_sources": [
        {
            "niche": "Emas, Minyak, & Geopolitik Perang",
            "description": "Fokus pada harga komoditas energi, logam mulia safe haven, dan eskalasi konflik militer maritim.",
            "sources": [
                {
                    "name": "OilPrice.com",
                    "url": "https://oilprice.com",
                    "rss": "https://oilprice.com/rss/main",
                    "focus": "Energi mentah, dinamika OPEC+, dan disrupsi pipa/kilang minyak global."
                },
                {
                    "name": "Investing.com Commodities",
                    "url": "https://www.investing.com/commodities",
                    "rss": "https://www.investing.com/rss/commodities.rss",
                    "focus": "Live update harga emas spot, perak, gas alam, dan minyak WTI/Brent."
                },
                {
                    "name": "Al Jazeera Economy & Geopolitics",
                    "url": "https://www.aljazeera.com/economy",
                    "rss": "https://www.aljazeera.com/xml/rss/all.xml",
                    "focus": "Perspektif konflik Timur Tengah, rute Selat Hormuz, dan sanksi militer."
                },
                {
                    "name": "SMM (Shanghai Metals Market)",
                    "url": "https://news.metal.com",
                    "rss": "https://news.metal.com/rss",
                    "focus": "Permintaan komoditas logam industri, cadangan emas fisik China, dan transaksi bullion."
                }
            ]
        },
        {
            "niche": "Hubungan Bilateral Negara & Makroekonomi Global",
            "description": "Fokus pada dedolarisasi, pergeseran petrodollar, perang tarif, dan perdagangan antar negara besar.",
            "sources": [
                {
                    "name": "The Diplomat",
                    "url": "https://thediplomat.com",
                    "rss": "https://thediplomat.com/feed/",
                    "focus": "Analisis geopolitik dan aliansi dagang Asia-Pasifik, China, dan Timur Tengah."
                },
                {
                    "name": "Financial Times Macro",
                    "url": "https://www.ft.com",
                    "rss": "https://news.google.com/rss/search?q=when:24h+allinurl:ft.com+economy&hl=en-US&gl=US&ceid=US:en",
                    "focus": "Kebijakan perbankan sentral, arus modal global, dan proteksionisme dagang."
                },
                {
                    "name": "ThinkChina (Lianhe Zaobao)",
                    "url": "https://www.thinkchina.sg",
                    "rss": "https://www.thinkchina.sg/rss",
                    "focus": "Internasionalisasi Renminbi (petroyuan), inisiatif mBridge, dan diplomasi Teluk."
                },
                {
                    "name": "SUERF - The European Money and Finance Forum",
                    "url": "https://www.suerf.org",
                    "rss": "https://www.suerf.org/feed/",
                    "focus": "Riset akademis sistem moneter internasional, cadangan devisa, dan hegemoni Dolar AS."
                }
            ]
        },
        {
            "niche": "Pasar Saham & Bursa Finansial",
            "description": "Fokus pada Wall Street, Bursa Efek Indonesia (IHSG), suku bunga The Fed, dan earnings emiten.",
            "sources": [
                {
                    "name": "MarketWatch",
                    "url": "https://www.marketwatch.com",
                    "rss": "https://feeds.content.dowjones.io/public/rss/mw_topstories",
                    "focus": "S&P 500, Dow Jones, yield obligasi US Treasury, dan sentimen harian Wall Street."
                },
                {
                    "name": "CNBC Markets",
                    "url": "https://www.cnbc.com/markets/",
                    "rss": "https://search.cnbc.com/rs/search/view.html?partnerId=2000&keywords=market&sort=date&type=all&output=rss",
                    "focus": "Pidato pejabat The Fed, pergerakan indeks bursa, dan laporan keuangan kuartalan."
                },
                {
                    "name": "Bloomberg Markets Wire",
                    "url": "https://www.bloomberg.com/markets",
                    "rss": "https://news.google.com/rss/search?q=when:24h+allinurl:bloomberg.com+markets&hl=en-US&gl=US&ceid=US:en",
                    "focus": "Laporan intelijen pasar primer, order flow institusi, dan valas."
                },
                {
                    "name": "Kontan Investasi",
                    "url": "https://investasi.kontan.co.id",
                    "rss": "https://www.kontan.co.id/rss/investasi",
                    "focus": "Pergerakan saham IHSG, aksi korporasi emiten domestik, dan kebijakan Bank Indonesia."
                }
            ]
        },
        {
            "niche": "Crypto & Aset Digital",
            "description": "Fokus pada dinamika on-chain, ETF spot Bitcoin/Ethereum, regulasi SEC, dan likuiditas DeFi.",
            "sources": [
                {
                    "name": "CoinDesk",
                    "url": "https://www.coindesk.com",
                    "rss": "https://www.coindesk.com/arc/outboundfeeds/rss/",
                    "focus": "Arus dana ETF spot, kebijakan regulasi SEC, dan riset ekonomi kripto."
                },
                {
                    "name": "CoinTelegraph",
                    "url": "https://cointelegraph.com",
                    "rss": "https://cointelegraph.com/rss",
                    "focus": "Berita pasar Bitcoin harian, adopsi institusional, dan likuiditas altcoin."
                },
                {
                    "name": "Decrypt",
                    "url": "https://decrypt.co",
                    "rss": "https://decrypt.co/feed",
                    "focus": "Perkembangan web3, ekosistem layer 2, dan irisan AI dengan aset kripto."
                },
                {
                    "name": "The Block",
                    "url": "https://www.theblock.co",
                    "rss": "https://www.theblock.co/rss.xml",
                    "focus": "Data analitik volume perdagangan, pendanaan venture capital Web3, dan derivatif."
                }
            ]
        },
        {
            "niche": "Kecerdasan Buatan (AI) & Teknologi",
            "description": "Fokus pada siklus super CapEx AI Big Tech, chip akselerator semikonduktor, dan agen otonom.",
            "sources": [
                {
                    "name": "Ars Technica (AI & Tech Lab)",
                    "url": "https://arstechnica.com",
                    "rss": "https://feeds.arstechnica.com/arstechnica/technology-lab",
                    "focus": "Analisis mendalam arsitektur model AI, semikonduktor, dan kebijakan komputasi."
                },
                {
                    "name": "TechCrunch AI",
                    "url": "https://techcrunch.com/category/artificial-intelligence/",
                    "rss": "https://techcrunch.com/category/artificial-intelligence/feed/",
                    "focus": "Investasi modal ventura AI, rilis produk OpenAI/Anthropic/Google, dan startup LLM."
                },
                {
                    "name": "Hugging Face Daily Papers",
                    "url": "https://huggingface.co/papers",
                    "rss": "https://huggingface.co/blog/feed.xml",
                    "focus": "Riset frontier open-weights, teknik inferensi efisien, dan model multimodal."
                },
                {
                    "name": "Tom's Hardware / SemiAnalysis",
                    "url": "https://www.tomshardware.com",
                    "rss": "https://www.tomshardware.com/feeds/all",
                    "focus": "Spesifikasi GPU Nvidia/AMD, fabrikasi wafer TSMC, dan konsumsi daya data center."
                }
            ]
        }
    ]
}

with open(r"D:\PORTFOLIO_NEO_BRUTALISM\data\20_trusted_news_sources.json", "w", encoding="utf-8") as f:
    json.dump(SOURCES_CONFIG, f, indent=2)

print("Saved 20 curated web news sources to D:\\PORTFOLIO_NEO_BRUTALISM\\data\\20_trusted_news_sources.json")
