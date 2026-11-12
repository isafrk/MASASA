import re, os
from pathlib import Path

path = Path("D:/PORTFOLIO_NEO_BRUTALISM/scripts/cron_evergreen_publisher.py")
content = path.read_text(encoding="utf-8")

old_pattern = r"    # Git commit and push[\s\S]*?print\(\"Git push completed successfully\.\"\)\s*"

new_block = """    # Git commit and push
    env_file = Path("C:/Users/dxisa/AppData/Local/hermes/.env")
    token = ""
    token_cf = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("GITHUB_TOKEN=") and not token:
                token = line.split("=", 1)[1].strip()
            elif line.startswith("CLOUDFLARE_API_TOKEN=") and not token_cf:
                token_cf = line.split("=", 1)[1].strip()

    if not token:
        token_file = Path("C:/Users/dxisa/AppData/Local/hermes/scripts/sync_vault_to_github.py")
        if token_file.exists():
            with open(token_file, "r", encoding="utf-8") as tf:
                m = re.search(r'TOKEN\s*=\s*"([^"]+)"', tf.read())
                if m:
                    token = m.group(1)

    if token:
        clean_url = "https://github.com/isafrk/MASASA.git"
        auth_url = f"https://x-access-token:{token}@github.com/isafrk/MASASA.git"
        subprocess.check_call(["git", "-C", str(SITE_ROOT), "add", "."])
        status_out = subprocess.check_output(["git", "-C", str(SITE_ROOT), "status", "--porcelain"], text=True)
        if status_out.strip():
            subprocess.check_call(["git", "-C", str(SITE_ROOT), "commit", "-m", f"Cron Auto-Publish Evergreen: {title[:50]}..."])
        subprocess.check_call(["git", "-C", str(SITE_ROOT), "remote", "set-url", "origin", auth_url])
        try:
            out = subprocess.check_output(["git", "-C", str(SITE_ROOT), "push", "origin", "main"], text=True)
            print("Git push completed successfully.")
        finally:
            subprocess.check_call(["git", "-C", str(SITE_ROOT), "remote", "set-url", "origin", clean_url])
"""

if re.search(old_pattern, content):
    new_content = re.sub(old_pattern, new_block + "\n", content, count=1)
    path.write_text(new_content, encoding="utf-8")
    print("Successfully replaced git push block.")
else:
    print("Could not match old pattern!")
