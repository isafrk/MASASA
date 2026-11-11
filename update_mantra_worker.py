import os, json, base64, urllib.request

TOKEN = ""
with open(r"C:\Users\dxisa\AppData\Local\hermes\.env") as f:
    for line in f:
        if line.startswith("CLOUDFLARE_API_TOKEN="):
            TOKEN = line.split("=", 1)[1].strip()

ACCOUNT_ID = "6e3bc73e59772cd41b333b1a5a66d271"
ZONE_ID = "b86d3b08b157ac29256c8e461744f89a"
SCRIPT_NAME = "mantralabs-seo-edge"

# 1. Read Icon assets
with open("D:/PORTFOLIO_NEO_BRUTALISM/icon.png", "rb") as f:
    png_b64 = base64.b64encode(f.read()).decode("ascii")

with open("D:/PORTFOLIO_NEO_BRUTALISM/favicon.ico", "rb") as f:
    ico_b64 = base64.b64encode(f.read()).decode("ascii")

with open("D:/PORTFOLIO_NEO_BRUTALISM/icon.svg", "r", encoding="utf-8") as f:
    svg_content = f.read()

# 2. Read deploy_mantralabs_pdf_edge.py
with open("D:/Blog/deploy_mantralabs_pdf_edge.py", "r", encoding="utf-8") as f:
    script_text = f.read()

# Locate WORKER_SCRIPT in deploy_mantralabs_pdf_edge.py
icon_constants = f"""
const MANTRA_FAVICON_ICO_B64 = "{ico_b64}";
const MANTRA_ICON_PNG_B64 = "{png_b64}";
const MANTRA_ICON_SVG = {json.dumps(svg_content)};

function b64ToUint8(b64) {{
  const bin = atob(b64);
  const len = bin.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) bytes[i] = bin.charCodeAt(i);
  return bytes;
}}
"""

icon_routes = """
  // ROUTE: Favicon & App Icons
  if (path === '/favicon.ico') {
    return new Response(b64ToUint8(MANTRA_FAVICON_ICO_B64), {
      headers: {
        'Content-Type': 'image/x-icon',
        'Cache-Control': 'public, max-age=2592000, immutable'
      }
    });
  }

  if (path === '/icon.png' || path === '/apple-touch-icon.png' || path === '/favicon.png') {
    return new Response(b64ToUint8(MANTRA_ICON_PNG_B64), {
      headers: {
        'Content-Type': 'image/png',
        'Cache-Control': 'public, max-age=2592000, immutable'
      }
    });
  }

  if (path === '/icon.svg') {
    return new Response(MANTRA_ICON_SVG, {
      headers: {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'public, max-age=2592000, immutable'
      }
    });
  }
"""

# Inject before addEventListener or export default
if "MANTRA_FAVICON_ICO_B64" not in script_text:
    script_text = script_text.replace("const WORKER_SCRIPT = f\"\"\"", "const WORKER_SCRIPT = f\"\"\"" + icon_constants)
    script_text = script_text.replace("  if (path === '/sitemap.xml')", icon_routes + "\n  if (path === '/sitemap.xml')")
    with open("D:/Blog/deploy_mantralabs_pdf_edge.py", "w", encoding="utf-8") as f:
        f.write(script_text)
    print("Injected icon handling into deploy_mantralabs_pdf_edge.py!")

print("Deploying updated mantralabs-seo-edge worker...")
