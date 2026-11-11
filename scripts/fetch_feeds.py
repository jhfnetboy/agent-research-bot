#!/usr/bin/env python3
"""每日候选抓取：读取 sources.json 里的 RSS / Atom 源和 HN Algolia，输出最近 N 小时的条目到 work/candidates-DATE.tsv。
它只收集候选，日报正文仍需人工或 Agent 阅读原文后撰写，每条保留原文链接和日期。
用法：python3 scripts/fetch_feeds.py [--hours 48]"""
import argparse, json, re, time, urllib.parse, urllib.request, concurrent.futures as cf
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
root = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser(); ap.add_argument("--hours", type=int, default=48); a = ap.parse_args()
cut = datetime.now(timezone.utc) - timedelta(hours=a.hours)
UA = {"User-Agent": "Mozilla/5.0 (agent-research-bot)"}
src = json.loads((root / "sources.json").read_text(encoding="utf-8"))["sources"]
feeds = [s for s in src if re.search(r"(rss|atom|feed|\.xml|export\.arxiv)", s["url"]) and "reddit.com" not in s["url"]]
def pd(s):
    s = (s or "").strip()
    for f in (parsedate_to_datetime, lambda x: datetime.fromisoformat(x.replace("Z", "+00:00"))):
        try:
            d = f(s); return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except Exception: pass
def run(s):
    out = []
    try: rootel = ET.fromstring(urllib.request.urlopen(urllib.request.Request(s["url"], headers=UA), timeout=25).read())
    except Exception as e: return [(s["name"], "ERR", str(e)[:80], "")]
    for el in rootel.iter():
        if el.tag.split("}")[-1] not in ("item", "entry"): continue
        d = {c.tag.split("}")[-1]: c for c in el}
        title = (d["title"].text if "title" in d and d["title"].text else "").strip()
        link = (d["link"].text or d["link"].get("href", "")) if "link" in d else ""
        ds = next((pd(d[k].text) for k in ("pubDate", "published", "updated", "date") if k in d and d[k].text), None)
        if ds and ds >= cut: out.append((s["name"], ds.astimezone(timezone(timedelta(hours=7))).strftime("%Y-%m-%d %H:%M"), title, link.strip()))
    return out
rows = []
with cf.ThreadPoolExecutor(12) as ex:
    for r in ex.map(run, feeds): rows += r
for q in ["agent", "LLM", "Claude", "OpenAI", "Gemini", "MCP"]:
    u = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode({"query": q, "tags": "story", "numericFilters": f"created_at_i>{int(cut.timestamp())},points>60", "hitsPerPage": 20})
    try:
        for h in json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20))["hits"]:
            t = datetime.fromtimestamp(h["created_at_i"], timezone(timedelta(hours=7))).strftime("%Y-%m-%d %H:%M")
            rows.append(("HN", t, f'{h["title"]} [{h["points"]} 分 / {h["num_comments"]} 评论] {h.get("url") or ""}', f'https://news.ycombinator.com/item?id={h["objectID"]}'))
    except Exception as e: rows.append(("HN", "ERR", str(e)[:80], ""))
rows = list(dict.fromkeys(rows))
(root / "work").mkdir(exist_ok=True)
date = datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d")
out = root / "work" / f"candidates-{date}.tsv"
out.write_text("\n".join("\t".join(r) for r in sorted(rows, key=lambda r: r[1], reverse=True)) + "\n", encoding="utf-8")
print(f"{len(rows)} candidates -> {out}")
