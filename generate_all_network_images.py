# -*- coding: utf-8 -*-
"""
GENERATE 100% UNIQUE AI IMAGES ACROSS ALL 3 WEBSITES VIA 9ROUTER
1. Gomora Game (Indonesian Potato PC & Game Gratis Guides)
2. Game on Radar (English Global PC Giveaways & Industry Analysis)
3. Mantra Labs (English Financial & Global Macro Wire)
"""

import os
import json
import base64
import urllib.request
import time
from pathlib import Path

ROUTER_URL = "http://localhost:20128/v1/images/generations"

def get_9router_key():
    env_file = r"C:\Users\dxisa\AppData\Local\hermes\.env"
    if os.path.exists(env_file):
        for line in open(env_file, "r", encoding="utf-8"):
            if line.startswith("HERMES_CUSTOM_9ROUTER_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""

API_KEY = get_9router_key()
OUT_DIR_GAMING = Path(r"D:\PORTFOLIO_NEO_BRUTALISM\assets\gaming")
OUT_DIR_GAMING.mkdir(parents=True, exist_ok=True)
OUT_DIR_MANTRA = Path(r"D:\PORTFOLIO_NEO_BRUTALISM\articles\images")
OUT_DIR_MANTRA.mkdir(parents=True, exist_ok=True)

def generate_image(prompt, out_path):
    if out_path.exists() and out_path.stat().st_size > 50000:
        print(f"[=] Already exists: {out_path.name}")
        return True

    payload = {
        "model": "ag/gemini-3.1-flash-image",
        "prompt": prompt,
        "size": "1024x1024"
    }
    req = urllib.request.Request(
        ROUTER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    )
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                if resp.status == 200:
                    res = json.loads(resp.read().decode())
                    b64_data = res["data"][0]["b64_json"]
                    raw_bytes = base64.b64decode(b64_data)
                    with open(out_path, "wb") as f:
                        f.write(raw_bytes)
                    print(f"[✓] Generated: {out_path.name} ({len(raw_bytes)} bytes)")
                    return True
        except Exception as e:
            print(f"[-] Attempt {attempt+1} error for {out_path.name}: {e}")
            time.sleep(2)
    return False

# Target 1: Gomora Game Indonesian Articles
GOMORA_TARGETS = [
    ("cara-setting-laptop-kentang-ram-4gb-lancar-game-60fps", "Cinematic realistic photography of an open budget laptop running a vibrant video game with FPS counter on screen, glowing keyboard, warm cozy dim room lighting, shallow depth of field, photorealistic, 8k"),
    ("5-game-steam-gratis-terbaik-enteng-spek-intel-hd", "Artistic clean setup of a lightweight gaming laptop playing a colorful multiplayer action platformer game, crisp screen display, minimalist desk, 8k"),
    ("panduan-lengkap-klaim-game-epic-games-store-gratis", "Cinematic dark room desk setup displaying a digital game store launcher on monitor showing 100% free claim promotion, glowing ambient RGB, 8k"),
    ("cara-menghindari-penipuan-steam-key-dan-phishing-akun", "Moody cyber security visual, glowing padlock icon hovering over gaming keyboard, matrix telemetry backdrop, digital safety concept, 8k"),
    ("rekomendasi-game-open-world-ringan-under-10gb", "Vibrant fantasy open world landscape view on gaming monitor, lush mountains and castle, desktop setup, atmospheric lighting, 8k"),
    ("cara-mengatasi-lag-stuttering-game-pc-windows-11", "Close up of modern PC hardware components, glowing cooling fan and graphics card inside tempered glass case, tech optimization visual, 8k"),
    ("mengenal-game-drm-free-dan-cara-backup-offline", "Vintage classic game CD jewel case and USB flash drive resting on wooden desk, digital preservation nostalgia, soft natural lighting, 8k"),
    ("panduan-beli-game-steam-pakai-dana-gopay-qris", "Smartphone displaying modern digital wallet QR payment screen next to sleek gaming keyboard, modern fintech gaming lifestyle, 8k")
]

# Target 2: Game on Radar English Articles
GAMEONRADAR_TARGETS = [
    ("how-to-get-free-steam-games-legally-complete-guide", "Cinematic wide shot of modern PC gaming battle station, dual monitors displaying Steam library grid of games, high-end desk setup, 8k"),
    ("how-to-safely-optimize-windows-11-for-maximum-gaming-fps", "Sleek PC desktop screen showing advanced hardware telemetry performance charts and graphs, dark mode interface, 8k"),
    ("the-ultimate-guide-to-gog-and-drm-free-pc-game-preservation", "Collection of retro physical PC big box games and DRM-free collector boxes arranged on wooden shelf, nostalgic warm lighting, 8k"),
    ("epic-games-weekly-giveaways-history-economics-and-publisher-compensation", "Dramatic editorial visual of game publishing studio boardroom with digital revenue graphs and game art concepts on screen, 8k"),
    ("best-free-steam-games-you-can-play-on-4gb-ram-low-end-laptops", "Close-up of hands gaming on a slim compact laptop in coffee shop, vibrant pixel art indie game on screen, authentic lifestyle, 8k"),
    ("the-complete-guide-to-prime-gaming-and-twitch-drops-in-2026", "Streaming studio microphone and headset in foreground, background showing vibrant game stream, purple and teal cinematic neon, 8k"),
    ("why-video-game-physical-media-is-dying-and-what-players-lose-forever", "Artistic top-down view of retro game cartridges and modern digital download cards fading away, bittersweet nostalgia concept, 8k"),
    ("how-to-identify-fake-free-steam-key-scams-phishing-bots-and-malware", "Dark room cybersecurity command center screen displaying phishing bot analysis, red warning telemetry, hacker defense aesthetic, 8k"),
    ("steam-deck-performance-tuning-40-fps-sweet-spot-vs-60-fps-battery-drain", "Ergonomic handheld gaming PC held in hands outdoors during golden hour, crisp screen displaying adventure game, photorealistic, 8k"),
    ("the-rise-of-micro-transactions-in-single-player-aaa-games-an-industry-autopsy", "Dark conceptual sculpture of a golden virtual loot crate glowing with credit card chips, critique of modern gaming monetization, 8k"),
    ("how-to-legally-emulate-classic-retro-games-on-modern-pc-without-piracy", "Retro arcade CRT television monitor displaying nostalgic 16-bit platformer next to a modern keyboard, retro-futurism aesthetic, 8k"),
    ("indie-games-vs-aaa-bloat-why-smaller-studios-are-winning-critical-acclaim", "Independent indie game development workspace, dual screens with code and hand-drawn 2D animation sprites, creative passion, 8k"),
    ("the-hidden-cost-of-game-pass-and-subscription-fatigue-do-gamers-actually-own-anything", "Minimalist living room TV display with endless scrolling digital game subscription catalog, moody evening lighting, 8k"),
    ("mount-chiliad-to-valentine-5-unsolved-gaming-mysteries-that-still-haunt-players", "Atmospheric mystical foggy mountain peak at dusk, mysterious mural glyphs illuminated on stone, cinematic gaming mystery, 8k")
]

def main():
    print("=== STARTING BATCH AI IMAGE GENERATION FOR ALL WEBSITES ===")
    
    # 1. Gomora Game
    print("\n--- Generating Gomora Game Images ---")
    for slug, prompt in GOMORA_TARGETS:
        out_file = OUT_DIR_GAMING / f"{slug}.jpg"
        generate_image(prompt, out_file)
        time.sleep(1)

    # 2. Game on Radar
    print("\n--- Generating Game on Radar Images ---")
    for slug, prompt in GAMEONRADAR_TARGETS:
        out_file = OUT_DIR_GAMING / f"{slug}.jpg"
        generate_image(prompt, out_file)
        time.sleep(1)

    print("\n=== FINISHED GENERATION FOR ALL SITES! ===")

if __name__ == "__main__":
    main()
