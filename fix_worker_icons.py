import os, json, base64, urllib.request, re

with open("D:/PORTFOLIO_NEO_BRUTALISM/icon.png", "rb") as f:
    png_b64 = base64.b64encode(f.read()).decode("ascii")

with open("D:/PORTFOLIO_NEO_BRUTALISM/favicon.ico", "rb") as f:
    ico_b64 = base64.b64encode(f.read()).decode("ascii")

with open("D:/PORTFOLIO_NEO_BRUTALISM/icon.svg", "r", encoding="utf-8") as f:
    svg_content = f.read()

with open("D:/Blog/deploy_mantralabs_pdf_edge.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add variable declarations right after const PDFS = {json.dumps(PDF_B64)};
DECLARATIONS = f"""const PDFS = {{json.dumps(PDF_B64)}};
const MANTRA_FAVICON_ICO_B64 = "{ico_b64}";
const MANTRA_ICON_PNG_B64 = "{png_b64}";
const MANTRA_ICON_SVG = {{json.dumps(svg_content)}};
"""

if 'const MANTRA_FAVICON_ICO_B64 = "' not in code:
    code = code.replace("const PDFS = {json.dumps(PDF_B64)};", DECLARATIONS)

# 2. Use base64ToArrayBuffer for ICO and PNG
old_fav_route = """  // ROUTE: Favicon & App Icons
  if (path === '/favicon.ico') {{
    return new Response(b64ToUint8(MANTRA_FAVICON_ICO_B64), {{
      headers: {{
        'Content-Type': 'image/x-icon',
        'Cache-Control': 'public, max-age=2592000, immutable'
      }}
    }});
  }}

  if (path === '/icon.png' || path === '/apple-touch-icon.png' || path === '/favicon.png') {{
    return new Response(b64ToUint8(MANTRA_ICON_PNG_B64), {{
      headers: {{
        'Content-Type': 'image/png',
        'Cache-Control': 'public, max-age=2592000, immutable'
      }}
    }});
  }}"""

new_fav_route = """  // ROUTE: Favicon & App Icons
  if (path === '/favicon.ico') {{
    const buf = base64ToArrayBuffer(MANTRA_FAVICON_ICO_B64);
    return new Response(buf, {{
      headers: {{
        'Content-Type': 'image/x-icon',
        'Cache-Control': 'public, max-age=2592000, immutable'
      }}
    }});
  }}

  if (path === '/icon.png' || path === '/apple-touch-icon.png' || path === '/favicon.png') {{
    const buf = base64ToArrayBuffer(MANTRA_ICON_PNG_B64);
    return new Response(buf, {{
      headers: {{
        'Content-Type': 'image/png',
        'Cache-Control': 'public, max-age=2592000, immutable'
      }}
    }});
  }}"""

if "base64ToArrayBuffer(MANTRA_FAVICON_ICO_B64)" not in code:
    code = code.replace(old_fav_route, new_fav_route)

with open("D:/Blog/deploy_mantralabs_pdf_edge.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated D:/Blog/deploy_mantralabs_pdf_edge.py cleanly!")
