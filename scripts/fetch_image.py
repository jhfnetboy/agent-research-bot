#!/usr/bin/env python3
"""给 digests/DATE.json 下载配图：读取 image.source_url 页面的 og:image，存到 site/assets/DATE.ext。
找不到就跳过，绝不生成或编造图片。用法：python3 scripts/fetch_image.py 2026-11-11"""
import json, re, sys, urllib.request
from pathlib import Path
root = Path(__file__).resolve().parent.parent
date = sys.argv[1]
p = root / "digests" / f"{date}.json"
day = json.loads(p.read_text(encoding="utf-8"))
img = day.get("image") or {}
if img.get("local_path") and (root / "site" / img["local_path"]).is_file():
    print("image exists:", img["local_path"]); sys.exit(0)
src = img.get("source_url") or next((i["url"] for i in day.get("items", []) if i.get("url")), "")
if not src:
    print("no source url, skip"); sys.exit(0)
UA = {"User-Agent": "Mozilla/5.0 (agent-research-bot)"}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25).read()
try:
    page = get(src).decode("utf-8", "ignore")
    m = re.search(r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\'][^>]+content=["\']([^"\']+)', page) or \
        re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\'](?:og:image|twitter:image)', page)
    if not m:
        print("no og:image, skip"); sys.exit(0)
    url = m.group(1).replace("&amp;", "&")
    if url.startswith("//"): url = "https:" + url
    data = get(url)
    ext = ".png" if data[:4] == b"\x89PNG" else ".webp" if data[8:12] == b"WEBP" else ".jpg"
    dest = root / "site" / "assets" / f"{date}{ext}"
    dest.write_bytes(data)
    img.update({"local_path": f"assets/{date}{ext}", "source_url": src, "credit": img.get("credit") or re.sub(r"^https?://(www\.)?([^/]+).*", r"\2", src)})
    day["image"] = img
    p.write_text(json.dumps(day, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("saved", dest)
except Exception as e:
    print("image fetch failed, skip:", e)
