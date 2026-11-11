import os
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import subprocess

SITE_ROOT = Path(r"D:\PORTFOLIO_NEO_BRUTALISM")
ARTICLES_DIR = SITE_ROOT / "articles"
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
DB_FILE = SITE_ROOT / "data" / "financial_articles.json"

ARTICLES_DATA = [
    {
        "id": "1",
        "slug": "korelasi-emas-dan-minyak-saat-eskalasi-perang-timur-tengah",
        "category": "KOMODITAS & GEOPOLITIK",
        "badge": "ANALISIS UTAMA",
        "title": "Minyak, Emas, dan Eskalasi Perang Timur Tengah: Mekanisme Transmisi Risiko ke Pasar Global",
        "date": "11 November 2026",
        "iso_date": "2026-11-11T02:00:00Z",
        "reading_time": "7 menit baca",
        "summary": "Ketika ketegangan militer di Selat Hormuz meningkat, minyak mentah dan emas bereaksi melalui dua saluran transmisi yang berbeda: disrupsi pasokan fisik dan perlindungan nilai aset likuid.",
        "content_blocks": [
            {
                "subheading": "1. Disrupsi Fisik Jalur Energi: Mengapa Selat Hormuz Menjadi Titik Krusial",
                "paragraphs": [
                    "Kenaikan harga minyak mentah saat perang pecah bukan sekadar reaksi spekulatif trader harian. Selat Hormuz dilalui oleh lebih dari 20 persen konsumsi cairan minyak bumi dunia setiap hari. Ketika ancaman penutupan jalur maritim atau serangan terhadap infrastruktur kilang terjadi, premi risiko geopolitik langsung diperhitungkan ke dalam harga kontrak berjangka Brent dan WTI.",
                    "Disrupsi pasokan energi secara otomatis memicu kenaikan biaya pengapalan, lonjakan premi asuransi kapal tanker, dan eskalasi biaya logistik global. Hasil akhirnya adalah tekanan inflasi impor (imported inflation) bagi negara-negara konsumen utama energi di Asia dan Eropa."
                ]
            },
            {
                "subheading": "2. Emas Sebagai Instrumen Moneter Terakhir Tanpa Risiko Pihak Ketiga",
                "paragraphs": [
                    "Berbeda dengan minyak yang merupakan komoditas konsumsi dan input manufaktur, emas berperan sebagai instrumen pelindung nilai (safe haven). Di tengah konflik berskala besar, risiko sanksi ekonomi, pembekuan cadangan devisa, dan penurunan nilai mata uang fiat mendorong bank sentral serta investor institusi untuk mengakumulasi emas fisik.",
                    "Emas tidak memiliki counterparty risk atau risiko gagal bayar dari negara penerbit. Oleh sebab itu, lonjakan harga emas sering kali mencerminkan penurunan kepercayaan pasar terhadap stabilitas sistem moneter global dan ancaman stagflasi berkepanjangan."
                ]
            },
            {
                "subheading": "3. Dampak Ganda Terhadap Neraca Pembayaran Negara Berkembang",
                "paragraphs": [
                    "Bagi negara net-importer minyak seperti Indonesia, kombinasi kenaikan harga minyak dunia dan penguatan nilai tukar Dolar AS akibat sentimen risk-off menciptakan beban ganda. Subsidi energi domestik membengkak, defisit transaksi berjalan melebar, dan bank sentral dipaksa mempertahankan suku bunga acuan tinggi untuk menopang stabilitas mata uang.",
                    "Investor yang memahami relasi ini cenderung mengalokasikan modal ke instrumen berbasis komoditas keras dan instrumen lindung nilai moneter sebelum dampak transmisi makro merembes ke pasar saham domestik."
                ]
            }
        ]
    },
    {
        "id": "2",
        "slug": "dinamika-bilateral-as-china-dan-pergeseran-petrodollar",
        "category": "KEBIJAKAN EKONOMI",
        "badge": "MAKRO STRATEGIS",
        "title": "Dinamika Bilateral AS - China dan Erosi Dominasi Petrodollar di Jalur Perdagangan Energi",
        "date": "11 November 2026",
        "iso_date": "2026-11-11T01:30:00Z",
        "reading_time": "8 menit baca",
        "summary": "Hubungan bilateral antara Amerika Serikat dan China kini memasuki babak baru di mana penyelesaian transaksi perdagangan minyak internasional mulai beralih menggunakan mata uang lokal.",
        "content_blocks": [
            {
                "subheading": "1. Kerangka Petrodollar 1974 dan Transformasi Hubungan Bilateral",
                "paragraphs": [
                    "Sistem petrodollar yang dibangun pada dekade 1970-an mewajibkan negara produsen minyak utama menjual minyak mentah dalam denominasi Dolar AS, yang kemudian diinvestasikan kembali ke dalam obligasi pemerintah AS (US Treasuries). Struktur ini memberikan keistimewaan likuiditas permanen bagi perekonomian Amerika Serikat.",
                    "Namun, dengan berjalannya revolusi energi shale yang membuat AS mandiri secara energi, arah aliran minyak mentah Timur Tengah bergeser drastis. Lebih dari 80 persen ekspor energi Teluk kini mengalir ke pasar Asia, dengan China sebagai importir terbesar di dunia."
                ]
            },
            {
                "subheading": "2. Eskalasi Transaksi Bilateral Berbasis Yuan (Petroyuan)",
                "paragraphs": [
                    "Dalam beberapa tahun terakhir, porsi penyelesaian transaksi minyak antara China dan mitra dagangnya di Timur Tengah yang menggunakan mata uang Renminbi melonjak hingga melampaui Euro. Penggunaan platform mBridge, sistem pembayaran CIPS, dan perjanjian swap mata uang bilateral menjadi fondasi teknis yang memungkinkan perdagangan berjalan tanpa melewati sistem kliring perbankan Barat.",
                    "Langkah ini bukan bertujuan menghancurkan Dolar AS dalam semalam, melainkan menciptakan sistem penyelesaian alternatif yang kebal terhadap sanksi pembekuan aset unilateral."
                ]
            },
            {
                "subheading": "3. Reorganisasi Rantai Pasok Global dan Pengaruh Terhadap Pasar Finansial",
                "paragraphs": [
                    "Diversifikasi mata uang cadangan global menyebabkan bank sentral dunia mengurangi kepemilikan obligasi AS dan secara aktif menambah cadangan emas batangan. Fragmentasi blok perdagangan ini memicu volatilitas nilai tukar valuta asing dan menuntut korporasi multinasional memperketat strategi mitigasi risiko valas dalam neraca keuangan mereka."
                ]
            }
        ]
    },
    {
        "id": "3",
        "slug": "proyeksi-kebijakan-suku-bunga-the-fed-dan-dampaknya-ke-ihsg",
        "category": "SAHAM & BURSA",
        "badge": "PASAR MODAL",
        "title": "Arah Suku Bunga The Fed dan Dampak Arus Modal Asing Terhadap Valuasi Saham IHSG",
        "date": "11 November 2026",
        "iso_date": "2026-11-11T01:00:00Z",
        "reading_time": "6 menit baca",
        "summary": "Ketidakpastian penurunan suku bunga Federal Reserve menahan laju ekspansi valuasi saham perbankan dan emiten berkapitalisasi besar di Bursa Efek Indonesia.",
        "content_blocks": [
            {
                "subheading": "1. Paradigma Suku Bunga Tinggi Lebih Lama (Higher for Longer)",
                "paragraphs": [
                    "Rilis data inflasi tenaga kerja dan indeks harga konsumen AS yang masih bertahan di atas target 2 persen membuat komite kebijakan Federal Reserve bersikap sangat berhati-hati dalam memangkas Federal Funds Rate. Imbal hasil obligasi US Treasury tenor 10 tahun yang bertahan di atas 4.3 persen memberikan daya tarik investasi tanpa risiko yang sangat kompetitif.",
                    "Kondisi ini membatasi aliran dana investor institusi global menuju pasar negara berkembang (emerging markets) karena selisih imbal hasil (yield spread) yang belum cukup lebar untuk mengkompensasi risiko nilai tukar."
                ]
            },
            {
                "subheading": "2. Ketahanan Sektor Perbankan dan Konsumsi Domestik di IHSG",
                "paragraphs": [
                    "Meskipun arus modal keluar jangka pendek terjadi pada saham-saham perbankan lapis satu (seperti BBCA dan BBRI), fundamental laba bersih perbankan nasional tetap kokoh berkat margin bunga bersih (NIM) yang terjaga dan kualitas aset kredit yang sehat.",
                    "Sektor konsumsi primer dan telekomunikasi juga menjadi penopang indeks karena permintaan domestik yang relatif stabil dan tidak terlalu terpapar utang valuta asing."
                ]
            },
            {
                "subheading": "3. Titik Balik Likuiditas dan Strategi Akumulasi Bertahap",
                "paragraphs": [
                    "Bagi investor institusi lokal dan manajer investasi, periode konsolidasi indeks saham saat ini menjadi jendela akumulasi saham-saham berfundamental kuat dengan valuasi terdiskon, menjelang dimulainya siklus pelonggaran likuiditas global."
                ]
            }
        ]
    },
    {
        "id": "4",
        "slug": "likuiditas-kripto-etf-institusional-dan-siklus-halving-bitcoin",
        "category": "CRYPTO & ASET DIGITAL",
        "badge": "ASET DIGITAL",
        "title": "Adopsi ETF Spot dan Dinamika Likuiditas Bitcoin Pasca-Halving di Tengah Sentimen Makro",
        "date": "11 November 2026",
        "iso_date": "2026-11-11T00:30:00Z",
        "reading_time": "6 menit baca",
        "summary": "Perjalanan aset kripto kini terikat erat dengan siklus likuiditas global dan arus masuk modal institusional melalui instrumen ETF berizin resmi.",
        "content_blocks": [
            {
                "subheading": "1. Institusionalisasi Bitcoin: Dari Aset Ritel ke Portofolio Makro",
                "paragraphs": [
                    "Persetujuan ETF spot oleh otoritas bursa Amerika Serikat mengubah lanskap kepemilikan aset kripto secara permanen. Pengelola dana pensiun, sovereign wealth fund, dan hedge fund kini dapat mengekspos portofolio mereka ke Bitcoin tanpa harus mengelola private key secara langsung.",
                    "Dampaknya, pergerakan harga Bitcoin semakin sensitif terhadap kalender rilis data ekonomi makro AS, angka inflasi CPI, dan proyeksi suku bunga bank sentral."
                ]
            },
            {
                "subheading": "2. Tekanan Pasokan Pasca-Halving Menghadapi Permintaan Konsisten",
                "paragraphs": [
                    "Pemotongan imbalan penambang (block reward) mengurangi pasokan harian koin baru yang masuk ke pasar hingga separuhnya. Ketika pasokan baru menyusut sementara emiten ETF menyerap volume signifikan setiap hari bursa, ketidakseimbangan pasokan dan permintaan ini menjadi pendorong struktural apresiasi harga jangka panjang.",
                    "Fase konsolidasi saat ini merefleksikan proses perpindahan koin dari penambang yang membutuhkan modal operasional ke tangan investor institusi berjangka waktu panjang."
                ]
            }
        ]
    },
    {
        "id": "5",
        "slug": "fragmentasi-geopolitik-dan-kebijakan-proteksionisme-tarif-dagang",
        "category": "MAKRO GLOBAL",
        "badge": "TREN GLOBAL",
        "title": "Proteksionisme Tarif Dagang dan Restrukturisasi Rantai Pasok Manufaktur Dunia",
        "date": "11 November 2026",
        "iso_date": "2026-11-10T23:30:00Z",
        "reading_time": "7 menit baca",
        "summary": "Penerapan tarif dagang unilateral dan kebijakan pembatasan ekspor teknologi strategis mendorong relokasi rantai pasok ke kawasan Asia Tenggara.",
        "content_blocks": [
            {
                "subheading": "1. Berakhirnya Era Efisiensi Biaya Absolut (Cost-Driven Globalization)",
                "paragraphs": [
                    "Selama tiga dekade, globalisasi didorong oleh pencarian lokasi manufaktur dengan upah tenaga kerja terendah. Namun, ketegangan geopolitik dan kekhawatiran atas ketahanan rantai pasok telah mengubah prioritas para pemimpin industri dari 'just-in-time' menjadi 'just-in-case'.",
                    "Kebijakan friend-shoring dan near-shoring kini diutamakan untuk memastikan kelangsungan pasokan komponen semikonduktor, mineral baterai kendaraan listrik, dan perangkat telekomunikasi penting."
                ]
            },
            {
                "subheading": "2. Posisi Strategis Indonesia dan ASEAN Sebagai Hub Manufaktur Baru",
                "paragraphs": [
                    "Kawasan ASEAN, khususnya Indonesia, Vietnam, dan Malaysia, menjadi penerima manfaat utama dari diversifikasi pabrik global (strategi China+1). Kebijakan hilirisasi nikel dan bauksit di Indonesia memberikan daya tawar tinggi dalam menarik investasi pabrik baterai dan ekosistem industri hijau internasional.",
                    "Tantangan utamanya terletak pada kepastian hukum regulasi investasi dan standarisasi kepatuhan lingkungan hidup (ESG) yang diwajibkan oleh pasar ekspor Barat."
                ]
            }
        ]
    }
]

# Write DB
with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(ARTICLES_DATA, f, indent=2)

print(f"Saved {len(ARTICLES_DATA)} structured editorial articles to {DB_FILE}")
