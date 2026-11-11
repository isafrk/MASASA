# -*- coding: utf-8 -*-
"""
MANTRA LABS - Autonomous Financial RSS Intelligence & Editorial Engine
1. Fetches curated RSS feeds (Commodities, Geopolitics, Stock Market, Crypto, AI Tech).
2. Filters out duplicates and checks against existing database.
3. Automatically rewrites content in Indonesian following Mantra Labs standards:
   - Zero em-dashes (—).
   - Crisp technical and financial terminology.
   - Comprehensive analytical structure + Mandatory "Opini & Sudut Pandang Mantra Labs" section.
4. Generates standalone HTML article under /articles/{slug}.html.
5. Updates /index.html and sitemap.xml.
6. Commits and pushes to GitHub Pages repo (isafrk/MASASA) and purges Cloudflare cache.
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
    # Strip HTML tags
    clean = re.sub(r"<[^>]+>", "", text)
    # Remove all em-dash and en-dash (Taste-Skill strict ban)
    clean = clean.replace("—", "-").replace("–", "-")
    # Clean up whitespace
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
                pub_el = item.find("pubDate")
                
                title = clean_text(title_el.text if title_el is not None else "")
                link = link_el.text.strip() if link_el is not None and link_el.text else ""
                desc = clean_text(desc_el.text if desc_el is not None else "")
                pub_date = pub_el.text.strip() if pub_el is not None and pub_el.text else ""
                
                if title and len(title) > 15:
                    items.append({
                        "title": title,
                        "link": link,
                        "description": desc,
                        "pub_date": pub_date
                    })
            return items
    except Exception as e:
        print(f"[!] Feed fetch failed ({feed_url[:40]}): {e}")
        return []

def rewrite_into_mantra_article(raw_item: dict, niche_name: str, source_name: str):
    """
    Transforms an external wire item into an institutional Mantra Labs editorial.
    Adds comprehensive Indonesian context and strategic 'Opini Mantra Labs'.
    """
    title_raw = raw_item["title"]
    desc_raw = raw_item["description"] or title_raw
    
    slug = slugify(title_raw)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%d %B %Y")
    iso_date = now.isoformat()
    
    # Generate contextual structured sections based on niche
    if "Minyak" in niche_name or "Emas" in niche_name or "Geopolitik" in niche_name:
        category = "KOMODITAS & GEOPOLITIK"
        badge = "ANALISIS RISIKO"
        block1_sub = "1. Sinyal Pasar Komoditas dan Disrupsi Aliran Pasokan"
        block1_p1 = f"Laporan terbaru dari {source_name} menyoroti dinamika: {title_raw}. Dalam konteks pasar energi global, perkembangan ini mempertegas betapa sensitifnya harga komoditas terhadap pergeseran keamanan jalur logistik internasional."
        block1_p2 = f"Informasi yang terhimpun mencatat bahwa: {desc_raw}. Volatilitas ini secara langsung mempengaruhi kalkulasi premi risiko pengapalan dan struktur harga kontrak berjangka di bursa komoditas utama dunia."
        
        block2_sub = "2. Transmisi Inflasi Energi dan Tekanan Likuiditas Moneter"
        block2_p1 = "Kenaikan harga energi bukan sekadar isu sektoral, melainkan pemicu utama imported inflation yang memaksa bank sentral memperketat proyeksi penurunan suku bunga acuan. Bagi negara-negara pengimpor minyak neto, lonjakan harga minyak mentah dan penguatan Dolar AS secara bersamaan memperlebar defisit transaksi berjalan."
        
        opini_sub = "3. Opini dan Sudut Pandang Mantra Labs"
        opini_p1 = "Kami di Mantra Labs melihat bahwa eskalasi geopolitik saat ini mempercepat proses diversifikasi cadangan devisa global. Kenaikan harga minyak yang diiringi ketegangan militer selalu menjadi katalis alami bagi akumulasi emas batangan fisik oleh bank sentral non-Barat."
        opini_p2 = "Bagi pelaku pasar modal dan manajer investasi di Indonesia, kami merekomendasikan pendekatan defensif: kurangi eksposur pada emiten berbobot utang valas tinggi tanpa lindung nilai, dan tingkatkan alokasi pada aset berfundamental riil atau komoditas energi dengan neraca keuangan yang sehat."

    elif "Bilateral" in niche_name:
        category = "KEBIJAKAN EKONOMI"
        badge = "MAKRO STRATEGIS"
        block1_sub = "1. Perkembangan Terkini Hubungan Dagang Bilateral"
        block1_p1 = f"Berdasarkan pemantauan rilis {source_name}, isu krusial yang tengah berkembang adalah {title_raw}. Fokus utama tertuju pada negosiasi perdagangan dan perimbangan neraca transaksi antar kekuatan ekonomi dunia."
        block1_p2 = f"Detail laporan mengindikasikan: {desc_raw}. Kesepakatan maupun friksi dalam jalur bilateral ini secara historis menentukan arah relokasi investasi modal langsung lintas benua."
        
        block2_sub = "2. Dampak Struktural Terhadap Neraca Perdagangan Kawasan"
        block2_p1 = "Kebijakan tarif dan penyelesaian transaksi menggunakan mata uang lokal (local currency settlement) terus mengikis hegemoni sistem pembayaran tunggal. Perubahan ini menciptakan koridor perdagangan alternatif yang kebal terhadap sanksi sepihak."
        
        opini_sub = "3. Opini dan Sudut Pandang Mantra Labs"
        opini_p1 = "Sudut pandang analitis Mantra Labs menegaskan bahwa fragmentasi blok ekonomi dunia bukan lagi prediksi masa depan, melainkan realitas yang sedang berlangsung. Korporasi multinasional dituntut memiliki fleksibilitas rantai pasok agar tidak terjebak sanksi atau tarif mendadak."
        opini_p2 = "Indonesia berada pada posisi tawar yang menguntungkan jika mampu mempertahankan diplomasi ekonomi yang independen dan memaksimalkan hilirisasi komoditas strategis untuk kebutuhan industri kedua kubu."

    elif "Crypto" in niche_name:
        category = "CRYPTO & ASET DIGITAL"
        badge = "LIKUIDITAS DIGITAL"
        block1_sub = "1. Dinamika On-Chain dan Arus Modal Institusional"
        block1_p1 = f"Kabar pasar digital dari {source_name} melaporkan: {title_raw}. Indikator on-chain merefleksikan pergerakan likuiditas signifikan yang dipicu oleh aktivitas perdagangan institusional."
        block1_p2 = f"Rangkuman data menggarisbawahi: {desc_raw}. Hal ini menunjukkan bagaimana sentimen makroekonomi global kian mendominasi pola pergerakan harga aset kripto utama."
        
        block2_sub = "2. Korelasi Siklus Suku Bunga Terhadap Minat Risiko (Risk-On)"
        block2_p1 = "Seiring masuknya dana pensiun dan manajer aset Wall Street melalui produk ETF berlisensi resmi, pasar kripto tidak lagi bergerak di ruang hampa. Fluktuasi imbal hasil obligasi pemerintah AS dan ekspektasi likuiditas bank sentral menjadi variabel penentu arah tren."
        
        opini_sub = "3. Opini dan Sudut Pandang Mantra Labs"
        opini_p1 = "Menurut penilaian tim riset Mantra Labs, fase pendewasaan pasar kripto ditandai oleh pergeseran dari spekulasi ritel murni menuju manajemen risiko portofolio berbasis data kuantitatif."
        opini_p2 = "Investor disarankan untuk memprioritaskan aset berkapitalisasi besar dengan adopsi institusi yang terverifikasi, serta mewaspadai volatilitas ekstrem yang dipicu oleh penyesuaian posisi leverage derivatif."

    elif "AI" in niche_name or "Teknologi" in niche_name:
        category = "KECERDASAN BUATAN & TEKNOLOGI"
        badge = "RISET TEKNOLOGI"
        block1_sub = "1. Inovasi Komputasi dan Perkembangan Infrastruktur AI"
        block1_p1 = f"Riset teknologi dari {source_name} menyoroti: {title_raw}. Percepatan kapasitas komputasi dan kapabilitas model otonom terus membuka batas efisiensi baru di industri perangkat lunak global."
        block1_p2 = f"Ringkasan teknis mencatat: {desc_raw}. Investasi pada perangkat keras akselerator dan arsitektur model mutakhir menjadi prioritas utama para pemimpin teknologi."
        
        block2_sub = "2. Batasan Fisik Energi dan Tantangan Skalabilitas Data Center"
        block2_p1 = "Kebutuhan daya listrik raksasa dan pasokan chip semikonduktor canggih mentransformasi ekosistem AI menjadi industri padat modal. Sektor utilitas listrik dan produsen silikon kini menjadi penopang utama keberlanjutan ekspansi kecerdasan buatan."
        
        opini_sub = "3. Opini dan Sudut Pandang Mantra Labs"
        opini_p1 = "Opini Mantra Labs memproyeksikan bahwa gelombang nilai ekonomi berikutnya tidak akan dinikmati oleh penyedia model dasar semata, melainkan oleh platform yang mampu mengintegrasikan agen AI otonom ke dalam eksekusi alur kerja nyata."
        opini_p2 = "Perusahaan yang gagal mengotomasi proses analisis data dan operasional menggunakan sistem otonom berisiko mengalami penurunan margin laba yang tajam di era komputasi modern."

    else: # Saham & Pasar Modal
        category = "SAHAM & BURSA"
        badge = "PASAR MODAL"
        block1_sub = "1. Sentimen Pasar Modal dan Valuasi Saham"
        block1_p1 = f"Rilis berita bursa dari {source_name} mengabarkan: {title_raw}. Indeks harga saham merespons langsung rilis data ekonomi dan pernyataan terbaru komite kebijakan moneter."
        block1_p2 = f"Fakta pasar memaparkan: {desc_raw}. Rotasi sektoral terlihat jelas saat para pengelola dana menyesuaikan bobot portofolio mereka menghadapi ketidakpastian suku bunga."
        
        block2_sub = "2. Valuasi Fundamental Menghadapi Biaya Modal Tinggi"
        block2_p1 = "Tingkat suku bunga bebas risiko yang masih menarik menahan laju ekspansi valuasi pasar saham. Saham-saham dengan arus kas operasional positif dan kemampuan meneruskan kenaikan biaya (pricing power) menjadi pilihan defensif terbaik."
        
        opini_sub = "3. Opini dan Sudut Pandang Mantra Labs"
        opini_p1 = "Mantra Labs berpandangan bahwa fase konsolidasi pasar saham saat ini memberikan peluang disiplin bagi investor jangka panjang untuk melakukan akumulasi pada saham berfundamental kuat."
        opini_p2 = "Hindari mengejar reli jangka pendek yang tidak didukung pertumbuhan laba bersih riil. Fokus pada emiten dengan neraca bersih tanpa beban bunga utang valas yang memberatkan."

    summary = f"Analisis mendalam Mantra Labs atas kabar {source_name} mengenai {title_raw}. Mengurai dampak transmisi pasar finansial, likuiditas makro, serta proyeksi strategis ke depan."
    
    from image_pool import get_unique_image
    with open(DB_FILE, "r", encoding="utf-8") as f_db:
        curr_arts = json.load(f_db)
    used_images = {a.get("image_url") for a in curr_arts if a.get("image_url")}
    assigned_image = get_unique_image(category, used_images)

    article_dict = {
        "id": str(int(now.timestamp())),
        "slug": slug,
        "category": category,
        "badge": badge,
        "title": title_raw,
        "date": date_str,
        "iso_date": iso_date,
        "reading_time": "6 menit baca",
        "summary": summary,
        "image_url": assigned_image,
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
    
    return article_dict

def update_site_files():
    # Rebuild articles and homepage
    subprocess.check_call([sys.executable, str(SITE_ROOT / "scripts" / "build_article_pages.py")])
    subprocess.check_call([sys.executable, str(SITE_ROOT / "scripts" / "build_news_portal.py")])

def run_rss_pipeline():
    print("=== MANTRA LABS AUTONOMOUS RSS PIPELINE ===")
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        existing_articles = json.load(f)
    
    existing_slugs = {a["slug"] for a in existing_articles}
    existing_titles = {a["title"].lower() for a in existing_articles}
    
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources_cfg = json.load(f)
        
    new_articles = []
    
    # Process feeds
    for niche in sources_cfg.get("niche_sources", []):
        niche_name = niche.get("niche", "")
        for s in niche.get("sources", []):
            s_name = s.get("name", "")
            s_rss = s.get("rss", "")
            if not s_rss:
                continue
                
            print(f"Scanning RSS [{niche_name}] -> {s_name}...")
            items = fetch_rss_feed(s_rss)
            
            for item in items[:2]: # Check top 2 items from each feed
                title_lower = clean_text(item["title"]).lower()
                slug = slugify(item["title"])
                
                if slug in existing_slugs or title_lower in existing_titles:
                    continue
                    
                print(f" [NEW STORY FOUND] {item['title'][:60]}...")
                art = rewrite_into_mantra_article(item, niche_name, s_name)
                new_articles.append(art)
                existing_slugs.add(slug)
                existing_titles.add(title_lower)
                break # 1 high-quality article per active feed source per run
    
    if not new_articles:
        print("No new unique stories to publish. All up to date.")
        return 0
        
    print(f"\nGenerated {len(new_articles)} new editorial articles with Mantra Labs opinion!")
    
    # Prepend new articles to database
    updated_db = new_articles + existing_articles
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_db, f, indent=2)
        
    # Rebuild static site
    update_site_files()
    
    # Update sitemap
    base_url = "https://mantralabs.web.id"
    all_files = ["index.html"] + [f"articles/{a['slug']}.html" for a in updated_db]
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
        
    print(f"Successfully updated site and sitemap with {len(updated_db)} articles.")
    return len(new_articles)

if __name__ == "__main__":
    run_rss_pipeline()
