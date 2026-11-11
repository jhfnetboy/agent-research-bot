#!/usr/bin/env python3
"""Build a static card site from data/*.json into dist/.

Default links are relative, so the same dist/ works at the site root
or under a subpath. Blog domain forwarding is handled by the user and
is out of scope for this project.

Optional: python3 build.py --base-path /ethereum
  writes root-absolute links prefixed with /ethereum, for the case
  where files themselves live under that path and no prefix is stripped.
"""

from __future__ import annotations

import argparse
import math
import html
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WEEK_RE = re.compile(r"^\d{4}-W\d{2}$")
REPO_URL = "https://github.com/jhfnetboy/agent-research-bot"
SITE_TITLE = "Agent 开发日报"
SITE_EYEBROW = "Agent Research Digest"
SITE_LEDE = "按日收录 AI Agent 开发相关的模型、框架、协议、评测与社区动态。"
SITE_INTRO = (
    "本页每天早上根据当天日报自动生成。系统从日报中提取关键词、要点、配图和每条来源链接，"
    "建成卡片并部署到 Cloudflare Pages。每天一张卡片，首页每页一周，点开卡片是当天的详情页，"
    "按话题列出每条信息的标题、概述和链接。重点话题深入写，其他动态简要说明。"
    "周报和日报卡片按时间顺序列在同一条时间线里，周报卡片标有“周报”。也可以从导航进入周报栏目。"
    "内容覆盖自上一期以来的变化，每条都附来源和日期，不编造数据。"
)
SITE_INTRO_SUGGEST_TEXT = "想建议增加来源，请在 GitHub 仓库提 issue："


def load_site_sources() -> list[str]:
    """Read source names from ../sources.json so the about page stays in sync."""
    path = Path(__file__).resolve().parent.parent / "sources.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return [f"{s['name']}（{s['priority']}）" for s in data.get("sources", [])]
    except Exception:
        return []


SITE_SOURCES = load_site_sources()


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def format_cn_date(iso: str) -> str:
    dt = datetime.strptime(iso, "%Y-%m-%d")
    return f"{dt.year}年{dt.month}月{dt.day}日"


def format_cn_month(ym: str) -> str:
    dt = datetime.strptime(ym, "%Y-%m")
    return f"{dt.year}年{dt.month}月"


def normalize_base_path(raw: str) -> str:
    path = (raw or "").strip()
    if not path or path == "/":
        return ""
    if not path.startswith("/"):
        path = "/" + path
    return path.rstrip("/")


def root_for(base: str, depth: int) -> str:
    """Prefix that points at the site root from a page `depth` directories deep.

    With a base path every link is root-absolute (/ethereum/...). Without one,
    links stay relative so the same dist/ works anywhere. depth < 0 means
    "served from an unknown path" (404.html) and uses root-absolute links.
    """
    if base:
        return f"{base}/"
    if depth < 0:
        return "/"
    return "./" if depth == 0 else "../" * depth


def load_days(data_dir: Path) -> list[dict]:
    days = []
    if not data_dir.exists():
        return days
    for path in sorted(data_dir.glob("*.json")):
        if path.name.startswith("_"):
            continue
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"skip {path.name}: invalid JSON ({exc})", file=sys.stderr)
            continue
        if not isinstance(raw, dict) or not DATE_RE.match(str(raw.get("date") or "")):
            print(f"skip {path.name}: missing or invalid date", file=sys.stderr)
            continue
        raw["_file"] = path.name
        days.append(raw)
    days.sort(key=lambda d: d["date"], reverse=True)
    return days


def item_groups(items: list) -> list[tuple[str, list]]:
    groups: list[tuple[str, list]] = []
    index: dict[str, list] = {}
    for item in items or []:
        if not isinstance(item, dict):
            continue
        topic = (item.get("topic") or "其他").strip() or "其他"
        if topic not in index:
            bucket: list = []
            index[topic] = bucket
            groups.append((topic, bucket))
        index[topic].append(item)
    return groups


def image_name(day: dict) -> str:
    image = day.get("image")
    if not isinstance(image, dict):
        return ""
    local = (image.get("local_path") or "").replace("\\", "/").lstrip("/")
    return Path(local).name if local else ""


def week_key(iso: str) -> str:
    y, w, _ = datetime.strptime(iso, "%Y-%m-%d").isocalendar()
    return f"{y}-W{w:02d}"


def week_range_label(key: str) -> str:
    y, w = key.split("-W")
    monday = datetime.fromisocalendar(int(y), int(w), 1)
    sunday = datetime.fromisocalendar(int(y), int(w), 7)
    return f"{format_cn_date(monday.strftime('%Y-%m-%d'))} 至 {format_cn_date(sunday.strftime('%Y-%m-%d'))}"


def week_href(root: str, weeks: list[str], key: str) -> str:
    """Latest week lives at the site root; older weeks under weeks/YYYY-Www/."""
    return root if key == weeks[0] else f"{root}weeks/{key}/"


def nav_html(root: str, current: str) -> str:
    links = [("home", "目录", root), ("weekly", "周报", f"{root}weekly/"), ("archive", "归档", f"{root}archive/"), ("about", "关于", f"{root}about/")]
    parts = []
    for key, label, href in links:
        cls = ' class="current"' if key == current else ""
        parts.append(f'<a href="{esc(href)}"{cls}>{label}</a>')
    return f'<nav class="site-nav" aria-label="站点导航">{"".join(parts)}</nav>'


def suggest_html() -> str:
    repo = esc(REPO_URL)
    return (
        f'<p class="suggest">{esc(SITE_INTRO_SUGGEST_TEXT)}'
        f'<a href="{repo}/issues">{repo}</a></p>'
    )


def intro_block_html(include_sources: bool, about_url: str = "") -> str:
    sources = ""
    if include_sources:
        items = "".join(f"<li>{esc(s)}</li>" for s in SITE_SOURCES)
        sources = f'<h3 id="sources">研究来源</h3><ul class="source-list">{items}</ul>'
    elif about_url:
        sources = (
            f'<p class="sources-link-note">完整研究来源见'
            f'<a href="{esc(about_url)}">关于页</a>。</p>'
        )
    return (
        f'<section class="about-intro">'
        f"<h2>关于本页</h2>"
        f"<p>{esc(SITE_INTRO)}</p>"
        f"{sources}"
        f"{suggest_html()}"
        f"</section>"
    )


def footer_html(root: str) -> str:
    repo = esc(REPO_URL)
    return (
        f'<footer class="site-footer">'
        f"<p>{esc(SITE_TITLE)}"
        f' · <a href="{esc(root)}">目录</a>'
        f' · <a href="{esc(root)}weekly/">周报</a>'
        f' · <a href="{esc(root)}archive/">归档</a>'
        f' · <a href="{esc(root)}about/">关于</a>'
        f' · <a href="{repo}">GitHub</a></p>'
        f"</footer>"
    )


def head_html(root: str, title: str, description: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="stylesheet" href="{esc(root)}styles.css">
</head>"""


def media_block(day: dict, root: str, img_exists: bool, eager: bool = False) -> tuple[str, str, str]:
    name = image_name(day) if img_exists else ""
    image = day.get("image") if isinstance(day.get("image"), dict) else {}
    credit = (image.get("credit") or "").strip()
    source_url = (image.get("source_url") or "").strip()
    alt = f"{format_cn_date(day['date'])} 配图"
    if name:
        loading = "eager" if eager else "lazy"
        fig = (
            f'<div class="media"><img src="{esc(root)}assets/{esc(name)}" alt="{esc(alt)}" '
            f'width="1200" height="675" loading="{loading}" decoding="async"></div>'
        )
    else:
        fig = (
            f'<div class="media placeholder" aria-hidden="true">'
            f'<div class="placeholder-mark"></div>'
            f'<div class="placeholder-date">{esc(format_cn_date(day["date"]))}</div>'
            f"</div>"
        )
    return fig, credit, source_url


def render_card(day: dict, root: str, img_exists: bool, eager: bool) -> str:
    fig, _, _ = media_block(day, root, img_exists, eager)
    keywords = [str(k).strip() for k in (day.get("keywords") or []) if str(k).strip()][:5]
    tags = "".join(f"<li>{esc(k)}</li>" for k in keywords)
    badge = '<p class="badge">示例</p>' if day.get("example") else ""
    href = f"{root}days/{day['date']}/"
    summary = (day.get("summary") or "").strip()
    return f"""
<article class="card">
  <a class="card-link" href="{esc(href)}">
    {fig}
    <div class="card-body">
      {badge}
      <time datetime="{esc(day["date"])}">{esc(format_cn_date(day["date"]))}</time>
      <ul class="tags">{tags}</ul>
      <p class="summary">{esc(summary)}</p>
    </div>
  </a>
</article>
"""


def pager_html(root: str, weeks: list[str], key: str) -> str:
    i = weeks.index(key)
    older = weeks[i + 1] if i + 1 < len(weeks) else None
    newer = weeks[i - 1] if i > 0 else None
    left = (
        f'<a class="prev" rel="prev" href="{esc(week_href(root, weeks, older))}">← 上一周</a>'
        if older else '<span class="prev disabled">← 上一周</span>'
    )
    right = (
        f'<a class="next" rel="next" href="{esc(week_href(root, weeks, newer))}">下一周 →</a>'
        if newer else '<span class="next disabled">下一周 →</span>'
    )
    mid = f'<span class="current" aria-current="page">{esc(key)}</span>'
    return f'<nav class="pager" aria-label="按周翻页">{left}{mid}{right}</nav>'


def render_index_page(entries: list[dict], weeks: list[str], key: str, root: str, total_days: int) -> str:
    latest = key == weeks[0]
    if entries:
        main = f'<section class="card-list" aria-label="本周卡片">{"".join(e["html"] for e in entries)}</section>'
    else:
        main = (
            '<section class="empty">'
            "<h2>暂无内容</h2>"
            "<p>把日报放到 digests 目录、或把周报放到 weekly 目录后重新构建即可。</p>"
            "</section>"
        )
    n_days = sum(1 for e in entries if e.get("kind") == "daily")
    n_weekly = sum(1 for e in entries if e.get("kind") != "daily")
    status = (
        f'<p class="page-status">{esc(key)} · {esc(week_range_label(key))} · 本周 {n_days} 天日报'
    )
    if n_weekly:
        status += f'、{n_weekly} 篇周报'
    status += (
        f' · 共 {total_days} 天、{len(weeks)} 周，更早的见“上一周”或<a href="{esc(root)}archive/">按月归档</a>。</p>'
    )
    if latest:
        intro = intro_block_html(include_sources=False, about_url=f"{root}about/")
        title = SITE_TITLE
    else:
        intro = ""
        title = f"{key} · {SITE_TITLE}"
    return f"""{head_html(root, title, SITE_LEDE)}
<body>
  <header class="site-header">
    {nav_html(root, "home")}
    <p class="eyebrow">{esc(SITE_EYEBROW)}</p>
    <h1>{esc(SITE_TITLE)}</h1>
    <p class="lede">{esc(SITE_LEDE)}</p>
  </header>
  {intro}
  <main>
    {status}
    {pager_html(root, weeks, key)}
    {main}
    {pager_html(root, weeks, key)}
  </main>
  {footer_html(root)}
</body>
</html>
"""


def render_archive(days: list[dict], root: str) -> str:
    months: dict[str, list[dict]] = {}
    for d in days:
        months.setdefault(d["date"][:7], []).append(d)
    sections = []
    for ym in sorted(months, reverse=True):
        rows = []
        for d in months[ym]:
            kws = "、".join(str(k).strip() for k in (d.get("keywords") or [])[:5] if str(k).strip())
            rows.append(
                f'<li><a class="day" href="{esc(root)}days/{esc(d["date"])}/">{esc(format_cn_date(d["date"]))}</a>'
                f'<span class="kw">{esc(kws)}</span></li>'
            )
        sections.append(
            f'<section class="archive-month" id="m{esc(ym)}"><h2>{esc(format_cn_month(ym))}'
            f'<span class="count">{len(months[ym])} 天</span></h2>'
            f'<ul class="archive-list">{"".join(rows)}</ul></section>'
        )
    body = "".join(sections) or "<p>暂无日报。</p>"
    return f"""{head_html(root, f"归档 · {SITE_TITLE}", "按月浏览全部日报。")}
<body>
  <header class="site-header">
    {nav_html(root, "archive")}
    <p class="eyebrow">{esc(SITE_EYEBROW)}</p>
    <h1>按月归档</h1>
    <p class="lede">共 {len(days)} 天日报，按月份倒序排列。</p>
  </header>
  <main class="archive-main">
    {body}
  </main>
  {footer_html(root)}
</body>
</html>
"""


def render_day(day: dict, root: str, img_exists: bool, newer: dict | None, older: dict | None) -> str:
    fig, credit, source_url = media_block(day, root, img_exists, eager=True)
    keywords = [str(k).strip() for k in (day.get("keywords") or []) if str(k).strip()][:5]
    tags = "".join(f"<li>{esc(k)}</li>" for k in keywords)
    badge = '<p class="badge">示例</p>' if day.get("example") else ""
    summary = (day.get("summary") or "").strip()
    groups_html = []
    for topic, items in item_groups(day.get("items") or []):
        entries = []
        for item in items:
            title = (item.get("title") or "").strip() or "未命名条目"
            note = (item.get("summary") or item.get("note") or "").strip()
            url = (item.get("url") or "").strip()
            item_date = (item.get("date") or day["date"]).strip()
            title_html = (
                f'<h3><a href="{esc(url)}" rel="noopener noreferrer">{esc(title)}</a></h3>'
                if url
                else f"<h3>{esc(title)}</h3>"
            )
            note_html = f"<p class=\"note\">{esc(note)}</p>" if note else ""
            meta_bits = []
            if url:
                meta_bits.append(
                    f'<a class="source" href="{esc(url)}" rel="noopener noreferrer">{esc(url)}</a>'
                )
            if item_date:
                meta_bits.append(f'<time datetime="{esc(item_date)}">{esc(item_date)}</time>')
            meta_html = f'<p class="meta">{" ".join(meta_bits)}</p>' if meta_bits else ""
            entries.append(f'<article class="item">{title_html}{note_html}{meta_html}</article>')
        groups_html.append(
            f'<section class="topic"><h2>{esc(topic)}</h2>{"".join(entries)}</section>'
        )
    topics = "".join(groups_html) or '<p class="empty-items">这一天还没有收录条目。</p>'
    credit_html = ""
    if credit or source_url:
        label = esc(credit or "配图来源")
        if source_url:
            credit_html = (
                f'<p class="credit">配图来源：'
                f'<a href="{esc(source_url)}" rel="noopener noreferrer">{label}</a></p>'
            )
        else:
            credit_html = f'<p class="credit">配图来源：{label}</p>'
    left = (
        f'<a rel="prev" href="{esc(root)}days/{esc(older["date"])}/">← {esc(format_cn_date(older["date"]))}</a>'
        if older else "<span></span>"
    )
    right = (
        f'<a rel="next" href="{esc(root)}days/{esc(newer["date"])}/">{esc(format_cn_date(newer["date"]))} →</a>'
        if newer else "<span></span>"
    )
    day_nav = f'<nav class="day-nav" aria-label="前后日报">{left}{right}</nav>'
    title = f"{format_cn_date(day['date'])} · {SITE_TITLE}"
    return f"""{head_html(root, title, summary or SITE_LEDE)}
<body>
  <header class="day-header">
    {nav_html(root, "day")}
    <a class="back" href="{esc(root)}">返回目录</a>
    {badge}
    <p class="eyebrow">{esc(SITE_EYEBROW)}</p>
    <time datetime="{esc(day["date"])}">{esc(format_cn_date(day["date"]))}</time>
    <h1>{esc(SITE_TITLE)}</h1>
    <ul class="tags">{tags}</ul>
    <p class="lede">{esc(summary)}</p>
  </header>
  <figure class="hero">
    {fig}
    {credit_html}
  </figure>
  <main class="day-main">
    {topics}
    {day_nav}
  </main>
  {footer_html(root)}
</body>
</html>
"""


def render_404(root: str) -> str:
    return f"""{head_html(root, f"页面不存在 · {SITE_TITLE}", SITE_LEDE)}
<body>
  <main class="empty">
    {nav_html(root, "")}
    <h1>页面不存在</h1>
    <p>这条地址没有对应的日报。</p>
    <p><a href="{esc(root)}">回到首页</a> · <a href="{esc(root)}weekly/">周报</a> · <a href="{esc(root)}archive/">归档</a> · <a href="{esc(root)}about/">关于</a></p>
  </main>
</body>
</html>
"""


def render_about(root: str) -> str:
    intro = intro_block_html(include_sources=True)
    return f"""{head_html(root, f"关于 · {SITE_TITLE}", SITE_INTRO)}
<body>
  <header class="site-header">
    {nav_html(root, "about")}
    <p class="eyebrow">{esc(SITE_EYEBROW)}</p>
    <h1>关于本页</h1>
    <p class="lede">{esc(SITE_LEDE)}</p>
  </header>
  <main class="about-page">
    {intro}
  </main>
  {footer_html(root)}
</body>
</html>
"""



def load_weeklies(data_dir: Path) -> list[dict]:
    weeks: list[dict] = []
    if not data_dir.exists():
        return weeks
    for path in sorted(data_dir.glob("*.json")):
        if "overview" in path.name:
            continue
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"skip {path.name}: invalid JSON ({exc})", file=sys.stderr)
            continue
        if not isinstance(raw, dict) or not WEEK_RE.match(str(raw.get("week") or "")):
            print(f"skip {path.name}: missing or invalid week", file=sys.stderr)
            continue
        raw["_file"] = path.name
        weeks.append(raw)
    weeks.sort(key=lambda w: w["week"], reverse=True)
    return weeks


def load_overviews(data_dir: Path) -> list[dict]:
    overviews: list[dict] = []
    if not data_dir.exists():
        return overviews
    for path in sorted(data_dir.glob("*overview*.json"), reverse=True):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"skip {path.name}: invalid JSON ({exc})", file=sys.stderr)
            continue
        if not isinstance(raw, dict):
            continue
        raw["_file"] = path.name
        raw["_slug"] = path.stem
        overviews.append(raw)
    return overviews


def range_end_date(text: str) -> str:
    """Last YYYY-MM-DD in a coverage string, used as the card's sort date."""
    found = re.findall(r"\d{4}-\d{2}-\d{2}", text or "")
    return found[-1] if found else ""


def weekly_sort_date(week: dict) -> str:
    end = range_end_date(week.get("range") or "")
    if end:
        return end
    key = week.get("week") or ""
    if WEEK_RE.match(str(key)):
        try:
            year, num = str(key).split("-W")
            return datetime.fromisocalendar(int(year), int(num), 7).strftime("%Y-%m-%d")
        except Exception:
            return ""
    return ""


def overview_sort_date(overview: dict) -> str:
    return range_end_date(overview.get("range") or "")


def stream_sort_key(entry: dict) -> tuple:
    # Newest date first; on the same date, overview then weekly report then daily.
    rank = {"overview": 0, "weekly": 1, "daily": 2}
    return (entry.get("date") or "", -rank.get(entry.get("kind") or "", 9))


def sort_stream(entries: list[dict]) -> list[dict]:
    return sorted(entries, key=stream_sort_key, reverse=True)


def weekly_stream_entries(weeklies: list[dict], overviews: list[dict]) -> list[dict]:
    entries: list[dict] = []
    for ov in overviews:
        date = overview_sort_date(ov)
        slug = ov.get("_slug") or "overview"
        title = ov.get("title") or "四周总览"
        summary_bits = []
        if ov.get("range"):
            summary_bits.append(f"覆盖 {ov['range']}")
        if ov.get("note"):
            summary_bits.append(ov["note"])
        summary = "，".join(summary_bits)
        if summary and not summary.endswith("。"):
            summary += "。"
        entries.append(
            {
                "kind": "overview",
                "date": date,
                "week": week_key(date) if date else "",
                "card": {
                    "title": "四周总览",
                    "slug_href": f"weekly/{slug}/",
                    "summary": summary or title,
                    "tags": [],
                    "badges": ["周报", "总览"],
                    "placeholder": "四周总览",
                    "datetime_value": date,
                },
            }
        )
    for week in weeklies:
        key = week["week"]
        date = weekly_sort_date(week)
        theme = (week.get("theme") or "").strip()
        coverage = (week.get("range") or "").strip()
        n = len(week.get("items") or [])
        summary = theme
        if coverage:
            extra = f"覆盖 {coverage}，共 {n} 条。"
            summary = f"{theme} {extra}" if theme else extra
        badges = ["周报"]
        if not week.get("complete", True):
            badges.append("进行中")
        entries.append(
            {
                "kind": "weekly",
                "date": date,
                "week": key,
                "card": {
                    "title": key,
                    "slug_href": f"weekly/{key}/",
                    "summary": summary,
                    "tags": week_keywords(week),
                    "badges": badges,
                    "placeholder": key,
                    "datetime_value": date,
                },
            }
        )
    return entries


def daily_stream_entries(days: list[dict]) -> list[dict]:
    return [
        {"kind": "daily", "date": day["date"], "week": week_key(day["date"]), "day": day}
        for day in days
    ]


def render_stream_card(entry: dict, root: str, existing: set[str], eager: bool = False) -> str:
    if entry.get("kind") == "daily":
        day = entry["day"]
        return render_card(day, root, image_name(day) in existing, eager)
    card = entry["card"]
    return render_weekly_card(
        title=card["title"],
        href=f"{root}{card['slug_href']}",
        summary=card["summary"],
        tags=card["tags"],
        badges=card["badges"],
        placeholder=card["placeholder"],
        datetime_value=card.get("datetime_value") or "",
    )


def render_stream_entries(entries: list[dict], root: str, existing: set[str], eager_first_daily: bool = False) -> list[dict]:
    out = []
    saw_daily = False
    for entry in entries:
        eager = False
        if eager_first_daily and entry.get("kind") == "daily" and not saw_daily:
            eager = True
            saw_daily = True
        item = dict(entry)
        item["html"] = render_stream_card(entry, root, existing, eager)
        out.append(item)
    return out


def week_start_iso(key: str) -> str:
    try:
        year, week = key.split("-W")
        return datetime.fromisocalendar(int(year), int(week), 1).strftime("%Y-%m-%d")
    except Exception:
        return ""


def item_sources_html(links: list) -> str:
    rows = []
    for link in links or []:
        if not isinstance(link, dict):
            continue
        url = (link.get("url") or "").strip()
        label = (link.get("label") or url or "来源").strip()
        date = (link.get("date") or "").strip()
        note = (link.get("note") or "").strip()
        if url:
            label_html = f'<a class="source" href="{esc(url)}" rel="noopener noreferrer">{esc(label)}</a>'
        else:
            label_html = esc(label)
        date_html = f'<time datetime="{esc(date)}">{esc(date)}</time>' if date else ""
        note_html = f"（{esc(note)}）" if note else ""
        rows.append(f'<p class="meta">{label_html}{date_html}{note_html}</p>')
    return "".join(rows)


def render_weekly_item(item: dict) -> str:
    title = (item.get("title") or "").strip() or "未命名条目"
    topic = (item.get("topic") or "").strip()
    topic_html = f'<ul class="tags"><li>{esc(topic)}</li></ul>' if topic else ""
    first_url = ""
    for link in item.get("links") or []:
        if isinstance(link, dict) and (link.get("url") or "").strip():
            first_url = link["url"].strip()
            break
    if not first_url:
        first_url = (item.get("url") or "").strip()
    title_html = (
        f'<h3><a href="{esc(first_url)}" rel="noopener noreferrer">{esc(title)}</a></h3>'
        if first_url
        else f"<h3>{esc(title)}</h3>"
    )
    what = (item.get("what") or "").strip()
    why = (item.get("why") or "").strip()
    summary = (item.get("summary") or "").strip()
    notes = []
    if what or why:
        if what:
            notes.append(f'<p class="note"><strong>发生了什么：</strong>{esc(what)}</p>')
        if why:
            notes.append(f'<p class="note"><strong>为什么重要：</strong>{esc(why)}</p>')
    elif summary:
        notes.append(f'<p class="note">{esc(summary)}</p>')
    links = item.get("links") or []
    if not links and item.get("url"):
        links = [{"label": "来源", "url": item.get("url"), "date": item.get("date") or ""}]
    return f'<article class="item">{topic_html}{title_html}{"".join(notes)}{item_sources_html(links)}</article>'


def weekly_report_pager_html(root: str, weeks: list[str], key: str) -> str:
    i = weeks.index(key)
    older = weeks[i + 1] if i + 1 < len(weeks) else None
    newer = weeks[i - 1] if i > 0 else None
    left = (
        f'<a class="prev" rel="prev" href="{esc(root)}weekly/{esc(older)}/">← {esc(older)}</a>'
        if older else '<span class="prev disabled">← 更早一周</span>'
    )
    right = (
        f'<a class="next" rel="next" href="{esc(root)}weekly/{esc(newer)}/">{esc(newer)} →</a>'
        if newer else '<span class="next disabled">更新一周 →</span>'
    )
    mid = f'<span class="current" aria-current="page">{esc(key)}</span>'
    return f'<nav class="pager" aria-label="周报翻页">{left}{mid}{right}</nav>'


def week_keywords(week: dict) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in week.get("items") or []:
        if not isinstance(item, dict):
            continue
        for raw in item.get("keywords") or []:
            key = str(raw).strip()
            if key and key not in seen:
                seen.add(key)
                out.append(key)
            if len(out) >= 5:
                return out
    return out


def placeholder_media(label: str) -> str:
    return (
        f'<div class="media placeholder" aria-hidden="true">'
        f'<div class="placeholder-mark"></div>'
        f'<div class="placeholder-date">{esc(label)}</div>'
        f"</div>"
    )


def render_weekly_card(title: str, href: str, summary: str, tags: list[str], placeholder: str, datetime_value: str = "", badges: list[str] | None = None, badge: str = "") -> str:
    tag_html = "".join(f"<li>{esc(k)}</li>" for k in tags if str(k).strip())
    tags_block = f'<ul class="tags">{tag_html}</ul>' if tag_html else ""
    labels = [str(b).strip() for b in (badges or []) if str(b).strip()]
    if badge and badge.strip() and badge.strip() not in labels:
        labels.append(badge.strip())
    if labels:
        pills = "".join(f'<p class="badge">{esc(b)}</p>' for b in labels)
        badge_html = f'<div class="badges">{pills}</div>'
    else:
        badge_html = ""
    dt_attr = f' datetime="{esc(datetime_value)}"' if datetime_value else ""
    return f"""
<article class="card">
  <a class="card-link" href="{esc(href)}">
    {placeholder_media(placeholder)}
    <div class="card-body">
      {badge_html}
      <time{dt_attr}>{esc(title)}</time>
      {tags_block}
      <p class="summary">{esc(summary)}</p>
    </div>
  </a>
</article>
"""


def render_weekly_report(week: dict, root: str, week_keys: list[str], overviews: list[dict]) -> str:
    key = week["week"]
    items = [i for i in (week.get("items") or []) if isinstance(i, dict)]
    majors = [i for i in items if i.get("kind") == "major"]
    others = [i for i in items if i.get("kind") != "major"]
    if not majors and not others:
        body = '<p class="empty-items">这一周还没有收录条目。</p>'
    else:
        sections = []
        if majors:
            sections.append(
                '<section class="topic"><h2>重大变化</h2>'
                + "".join(render_weekly_item(i) for i in majors)
                + "</section>"
            )
        if others:
            sections.append(
                '<section class="topic"><h2>其他值得一提</h2>'
                + "".join(render_weekly_item(i) for i in others)
                + "</section>"
            )
        body = "".join(sections)
    keywords = week_keywords(week)
    tags = "".join(f"<li>{esc(k)}</li>" for k in keywords)
    tags_html = f'<ul class="tags">{tags}</ul>' if tags else ""
    badge = '<p class="badge">进行中</p>' if not week.get("complete", True) else ""
    theme = (week.get("theme") or "").strip()
    coverage = (week.get("range") or "").strip()
    tz = (week.get("timezone") or "Asia/Bangkok (UTC+7)").strip()
    status = f"覆盖 {coverage}，时区 {tz}，共 {len(items)} 条。"
    ov_html = ""
    if overviews:
        ov = overviews[0]
        ov_html = (
            f'<p>也可阅读<a href="{esc(root)}weekly/{esc(ov["_slug"])}/">'
            f'{esc(ov.get("title") or "四周总览")}</a>。</p>'
        )
    monday = week_start_iso(key)
    time_attr = f' datetime="{esc(monday)}"' if monday else ""
    title = f"{key} 周报 · {SITE_TITLE}"
    return f"""{head_html(root, title, theme or status)}
<body>
  <header class="day-header">
    {nav_html(root, "weekly")}
    <a class="back" href="{esc(root)}weekly/">返回周报</a>
    {badge}
    <p class="eyebrow">Weekly Report</p>
    <time{time_attr}>{esc(key)}</time>
    <h1>AI 重大技术变化周报</h1>
    {tags_html}
    <p class="lede">{esc(status)}</p>
    <p class="lede">{esc(theme)}</p>
  </header>
  <main class="day-main">
    {body}
    {ov_html}
    {weekly_report_pager_html(root, week_keys, key)}
  </main>
  {footer_html(root)}
</body>
</html>
"""


def overview_week_block(entry: dict, root: str) -> str:
    week = (entry.get("week") or "").strip()
    heading = week
    if entry.get("range"):
        heading = f"{week}（{entry['range']}）" if week else str(entry["range"])
    if week:
        heading_html = f'<h2><a href="{esc(root)}weekly/{esc(week)}/">{esc(heading)}</a></h2>'
    else:
        heading_html = f"<h2>{esc(heading)}</h2>"
    theme = (entry.get("theme") or "").strip()
    theme_html = f'<p class="note"><strong>主线：</strong>{esc(theme)}</p>' if theme else ""
    rows = []
    for major in entry.get("majors") or []:
        if not isinstance(major, dict):
            continue
        title = (major.get("title") or "").strip() or "未命名条目"
        first_url = ""
        for link in major.get("links") or []:
            if isinstance(link, dict) and (link.get("url") or "").strip():
                first_url = link["url"].strip()
                break
        title_html = (
            f'<h3><a href="{esc(first_url)}" rel="noopener noreferrer">{esc(title)}</a></h3>'
            if first_url
            else f"<h3>{esc(title)}</h3>"
        )
        rows.append(f'<article class="item">{title_html}{item_sources_html(major.get("links") or [])}</article>')
    return f'<section class="topic">{heading_html}{theme_html}{"".join(rows)}</section>'


def render_overview(overview: dict, root: str) -> str:
    title = (overview.get("title") or "四周总览").strip()
    coverage = (overview.get("range") or "").strip()
    note = (overview.get("note") or "").strip()
    tz = (overview.get("timezone") or "Asia/Bangkok (UTC+7)").strip()
    lede_bits = []
    if coverage:
        lede_bits.append(f"覆盖 {coverage}")
    if tz:
        lede_bits.append(f"时区 {tz}")
    if note:
        lede_bits.append(note)
    lede = "，".join(lede_bits) + ("。" if lede_bits else "")
    week_blocks = "".join(overview_week_block(w, root) for w in (overview.get("weeks") or []) if isinstance(w, dict))
    trends = []
    for i, trend in enumerate(overview.get("trends") or [], 1):
        if not isinstance(trend, dict):
            continue
        trends.append(
            f'<article class="item"><h3>{i}. {esc(trend.get("title") or "")}</h3>'
            f'<p class="note">{esc(trend.get("text") or "")}</p></article>'
        )
    trends_html = (
        f'<section class="topic"><h2>四周趋势</h2>{"".join(trends)}</section>' if trends else ""
    )
    gaps = [f"<li>{esc(g)}</li>" for g in (overview.get("gaps") or []) if str(g).strip()]
    gaps_html = (
        f'<section class="topic"><h2>覆盖不足与说明</h2><ul class="source-list">{"".join(gaps)}</ul></section>'
        if gaps
        else ""
    )
    start = ""
    if coverage:
        maybe = coverage.split("至")[0].strip()
        if len(maybe) >= 10 and maybe[:10].count("-") == 2:
            start = maybe[:10]
    time_attr = f' datetime="{esc(start)}"' if start else ""
    return f"""{head_html(root, f"{title} · {SITE_TITLE}", lede or title)}
<body>
  <header class="day-header">
    {nav_html(root, "weekly")}
    <a class="back" href="{esc(root)}weekly/">返回周报</a>
    <p class="eyebrow">Weekly Report</p>
    <time{time_attr}>四周总览</time>
    <h1>{esc(title)}</h1>
    <p class="lede">{esc(lede)}</p>
  </header>
  <main class="day-main">
    {week_blocks}
    {trends_html}
    {gaps_html}
  </main>
  {footer_html(root)}
</body>
</html>
"""


def render_weekly_index(weeklies: list[dict], overviews: list[dict], root: str) -> str:
    cards = [
        render_stream_card(entry, root, set())
        for entry in sort_stream(weekly_stream_entries(weeklies, overviews))
    ]
    if cards:
        main = f'<section class="card-list" aria-label="周报列表">{"".join(cards)}</section>'
    else:
        main = (
            '<section class="empty">'
            "<h2>暂无周报</h2>"
            "<p>把当周的数据文件放进 weekly 目录后重新构建即可。</p>"
            "</section>"
        )
    status = f'<p class="page-status">共 {len(weeklies)} 期周报' + (
        f'、{len(overviews)} 篇总览。</p>' if overviews else "。</p>"
    )
    return f"""{head_html(root, f"周报 · {SITE_TITLE}", "按自然周汇总 AI 相关的重大技术变化。")}
<body>
  <header class="site-header">
    {nav_html(root, "weekly")}
    <p class="eyebrow">Weekly Report</p>
    <h1>周报</h1>
    <p class="lede">按自然周汇总 AI 相关的重大技术变化，最新一周在前。每条都有标题、概述和带来源日期的链接。</p>
  </header>
  <main>
    {status}
    {main}
  </main>
  {footer_html(root)}
</body>
</html>
"""


STYLES = """
:root {
  --bg: #f1eee6;
  --bg-deep: #e7e2d6;
  --paper: #fffcf6;
  --ink: #1c1915;
  --muted: #5c564d;
  --line: #d8d1c4;
  --accent: #143f33;
  --accent-soft: #d9ece4;
  --tag: #ece7dc;
  --tag-ink: #2a3d35;
  --shadow: 0 16px 40px rgba(40, 32, 18, 0.08);
  --radius: 18px;
  --sans: "Noto Sans CJK SC", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", ui-sans-serif, system-ui, sans-serif;
  --serif: "Noto Serif CJK SC", "Songti SC", "STSong", "SimSun", "Times New Roman", serif;
}
* { box-sizing: border-box; }
html { color-scheme: light; }
body {
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(1200px 500px at 10% -10%, #fbf8f0 0%, transparent 60%),
    linear-gradient(180deg, var(--bg) 0%, var(--bg-deep) 100%);
  color: var(--ink);
  font-family: var(--sans);
  font-size: 16px;
  line-height: 1.7;
}
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 0.18em; }
a:hover { color: #0b2b22; }
img { max-width: 100%; display: block; }
.site-header, .day-header, .day-main, .site-footer, .empty, .card-list, .about-intro, .about-page, .page-status, .archive-main {
  width: min(1080px, calc(100% - 2rem));
  margin-left: auto;
  margin-right: auto;
}
.site-nav {
  display: flex;
  gap: 1.1rem;
  margin: 0 0 1.2rem;
  font-size: 0.92rem;
}
.site-nav a { color: var(--muted); text-decoration: none; }
.site-nav a:hover, .site-nav a.current { color: var(--accent); }
.site-nav a.current { font-weight: 600; }
.about-intro {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.25rem 1.4rem 1.35rem;
  margin-bottom: 1.8rem;
}
.about-page .about-intro { margin-top: 0; box-shadow: none; background: transparent; border: 0; padding: 0 0 2.5rem; }
.about-intro h2 { font-family: var(--serif); font-size: 1.3rem; margin: 0 0 0.7rem; }
.about-page .about-intro h2 { display: none; }
.about-intro h3 { font-size: 1rem; margin: 1rem 0 0.45rem; }
.about-intro p { margin: 0; max-width: 46rem; }
.about-intro .sources-link-note, .about-intro .suggest { margin-top: 0.85rem; }
.source-list {
  margin: 0;
  padding-left: 1.15rem;
  max-width: 40rem;
}
.source-list li { margin: 0.2rem 0; }
.site-header, .day-header { padding: 2.6rem 0 1.4rem; }
.eyebrow {
  margin: 0 0 0.6rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 0.72rem;
  color: var(--muted);
}
.site-header h1, .day-header h1, .day-header time {
  font-family: var(--serif);
  font-weight: 650;
  letter-spacing: 0.02em;
  line-height: 1.25;
  margin: 0;
}
.site-header h1 { font-size: clamp(2rem, 5vw, 3.1rem); }
.day-header time {
  display: block;
  font-size: clamp(2rem, 5vw, 3rem);
  margin: 0.2rem 0 0.4rem;
}
.day-header h1 {
  font-size: 1rem;
  font-family: var(--sans);
  font-weight: 600;
  color: var(--muted);
}
.lede, .summary {
  color: var(--ink);
  max-width: 40rem;
}
.lede { margin: 0.85rem 0 0; font-size: 1.05rem; }
.card-list {
  display: grid;
  gap: 1.4rem;
  padding: 0.4rem 0 3rem;
}
.card {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}
.card-link {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.15fr);
  color: inherit;
  text-decoration: none;
  min-height: 240px;
}
.card-link:hover { color: inherit; }
.card-link:hover .summary { color: var(--accent); }
.media {
  min-height: 220px;
  background: #d9e3dc;
  overflow: hidden;
}
.media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  aspect-ratio: 16 / 9;
}
.placeholder {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 0.8rem;
  padding: 1.2rem;
  background:
    linear-gradient(160deg, #1c3f35 0%, #31574b 42%, #c9b498 100%);
  color: #f6f1e8;
}
.placeholder-mark {
  width: 42px;
  height: 42px;
  border: 2px solid rgba(255, 252, 246, 0.75);
  border-radius: 10px;
  transform: rotate(12deg);
  position: relative;
}
.placeholder-mark::after {
  content: "";
  position: absolute;
  inset: 8px;
  border: 2px solid rgba(255, 252, 246, 0.55);
}
.placeholder-date {
  font-family: var(--serif);
  font-size: 1.25rem;
}
.card-body { padding: 1.25rem 1.35rem 1.4rem; display: flex; flex-direction: column; gap: 0.7rem; }
.card-body time {
  font-family: var(--serif);
  font-size: 1.55rem;
  line-height: 1.2;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  list-style: none;
  padding: 0;
  margin: 0;
}
.tags li {
  background: var(--tag);
  color: var(--tag-ink);
  border-radius: 999px;
  padding: 0.15rem 0.7rem;
  font-size: 0.82rem;
}
.summary { margin: 0; color: var(--muted); }
.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  align-self: flex-start;
}
.badge {
  align-self: flex-start;
  margin: 0;
  background: var(--accent-soft);
  color: var(--accent);
  font-size: 0.75rem;
  padding: 0.1rem 0.55rem;
  border-radius: 999px;
}
.day-header .back {
  display: inline-block;
  margin-bottom: 1rem;
  color: var(--muted);
}
.hero {
  width: min(1080px, calc(100% - 2rem));
  margin: 0 auto 2rem;
}
.hero .media, .hero img {
  border-radius: 18px;
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}
.hero .placeholder { min-height: 240px; border-radius: 18px; }
.credit { margin: 0.6rem 0 0; color: var(--muted); font-size: 0.88rem; }
.day-main { padding-bottom: 3rem; display: grid; gap: 2rem; }
.topic h2 {
  font-family: var(--serif);
  font-size: 1.5rem;
  margin: 0 0 0.9rem;
  padding-bottom: 0.45rem;
  border-bottom: 1px solid var(--line);
}
.item + .item { margin-top: 1.15rem; }
.item h3 { margin: 0 0 0.3rem; font-size: 1.08rem; }
.item .note { margin: 0 0 0.35rem; color: var(--ink); }
.item .meta { margin: 0; color: var(--muted); font-size: 0.88rem; word-break: break-all; }
.item .meta time { margin-left: 0.8rem; }
.empty { padding: 3rem 0 5rem; }
.empty h1, .empty h2 { font-family: var(--serif); margin-bottom: 0.6rem; }
.site-footer {
  padding: 0 0 2.5rem;
  color: var(--muted);
  font-size: 0.9rem;
}
@media (max-width: 800px) {
  .card-link { grid-template-columns: 1fr; min-height: 0; }
  .media img, .hero img, .hero .media { aspect-ratio: 16 / 9; min-height: 0; }
  .card-body time { font-size: 1.35rem; }
}
@media (prefers-reduced-motion: reduce) {
  * { scroll-behavior: auto !important; }
}

.site-nav a + a { margin-left: 0.2rem; }
.page-status { margin: 0 auto 1rem; color: var(--muted); font-size: 0.95rem; }
.pager {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  padding: 0 0 3rem;
}
.pager a, .pager span {
  display: inline-block;
  min-width: 2.3rem;
  text-align: center;
  padding: 0.35rem 0.75rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: var(--paper);
  color: var(--ink);
  text-decoration: none;
  font-size: 0.92rem;
}
.pager a:hover { border-color: var(--accent); color: var(--accent); }
.pager .current { background: var(--accent); border-color: var(--accent); color: #fffcf6; }
.pager .disabled { color: var(--line); }
.pager .gap { border: 0; background: transparent; min-width: 0; padding: 0.35rem 0.2rem; }
.archive-main { padding-bottom: 3rem; display: grid; gap: 2rem; }
.archive-month h2 {
  font-family: var(--serif);
  font-size: 1.45rem;
  margin: 0 0 0.8rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--line);
}
.archive-month h2 .count { font-family: var(--sans); font-size: 0.9rem; color: var(--muted); margin-left: 0.6rem; font-weight: 400; }
.archive-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.7rem; }
.archive-list li { display: grid; grid-template-columns: 7.5rem minmax(0, 1fr); gap: 0.8rem; align-items: baseline; }
.archive-list a.day { font-family: var(--serif); font-weight: 600; }
.archive-list .kw { color: var(--muted); font-size: 0.92rem; }
.day-nav { display: flex; justify-content: space-between; gap: 1rem; padding: 0 0 2rem; font-size: 0.95rem; }
@media (max-width: 600px) { .archive-list li { grid-template-columns: 1fr; gap: 0.1rem; } }

"""


def copy_images(days: list[dict], site_root: Path, dist_assets: Path) -> set[str]:
    dist_assets.mkdir(parents=True, exist_ok=True)
    present: set[str] = set()
    for day in days:
        image = day.get("image") if isinstance(day.get("image"), dict) else None
        if not image:
            continue
        local = (image.get("local_path") or "").replace("\\", "/").lstrip("/")
        if not local:
            continue
        src = site_root / local
        if not src.is_file():
            alt = site_root / "assets" / Path(local).name
            src = alt if alt.is_file() else src
        if not src.is_file():
            print(f"warning: image not found for {day['date']}: {local}", file=sys.stderr)
            continue
        dest = dist_assets / src.name
        shutil.copyfile(src, dest)
        present.add(src.name)
    return present


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Build the Agent daily digest static site.")
    parser.add_argument("--data-dir", default=str(here.parent / "digests"))
    parser.add_argument("--out-dir", default=str(here / "dist"))
    parser.add_argument(
        "--base-path",
        default="",
        help="Optional root-absolute prefix such as /ethereum. Leave empty (default) to use relative links.",
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    base = normalize_base_path(args.base_path)

    days = load_days(data_dir)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    existing = copy_images(days, here, out_dir / "assets")
    write(out_dir / "styles.css", STYLES.strip() + "\n")

    weekly_dir = here.parent / "weekly"
    weeklies = load_weeklies(weekly_dir)
    overviews = load_overviews(weekly_dir)

    raw_entries = daily_stream_entries(days) + weekly_stream_entries(weeklies, overviews)
    by_week: dict[str, list[dict]] = {}
    for entry in raw_entries:
        key = entry.get("week") or (week_key(entry["date"]) if entry.get("date") else "")
        if not key:
            print(f"skip stream entry without week: {entry.get('kind')}", file=sys.stderr)
            continue
        by_week.setdefault(key, []).append(entry)
    weeks = sorted(by_week, reverse=True) or [week_key(datetime.now().strftime("%Y-%m-%d"))]
    for key in weeks:
        chunk = sort_stream(by_week.get(key, []))
        if key == weeks[0]:
            write(
                out_dir / "index.html",
                render_index_page(
                    render_stream_entries(chunk, root_for(base, 0), existing, eager_first_daily=True),
                    weeks,
                    key,
                    root_for(base, 0),
                    len(days),
                ),
            )
        write(
            out_dir / "weeks" / key / "index.html",
            render_index_page(
                render_stream_entries(chunk, root_for(base, 2), existing),
                weeks,
                key,
                root_for(base, 2),
                len(days),
            ),
        )
    total_pages = len(weeks)
    write(out_dir / "archive" / "index.html", render_archive(days, root_for(base, 1)))
    write(out_dir / "about" / "index.html", render_about(root_for(base, 1)))
    write(out_dir / "404.html", render_404(root_for(base, -1)))
    write(out_dir / "_redirects", f"/weeks/{weeks[0]} / 302\n/weeks/{weeks[0]}/ / 302\n")
    for i, day in enumerate(days):
        newer = days[i - 1] if i > 0 else None
        older = days[i + 1] if i + 1 < len(days) else None
        write(
            out_dir / "days" / day["date"] / "index.html",
            render_day(day, root_for(base, 2), image_name(day) in existing, newer, older),
        )

    write(out_dir / "weekly" / "index.html", render_weekly_index(weeklies, overviews, root_for(base, 1)))
    week_keys = [w["week"] for w in weeklies]
    for week in weeklies:
        write(
            out_dir / "weekly" / week["week"] / "index.html",
            render_weekly_report(week, root_for(base, 2), week_keys, overviews),
        )
    for overview in overviews:
        write(
            out_dir / "weekly" / overview["_slug"] / "index.html",
            render_overview(overview, root_for(base, 2)),
        )

    files = sum(1 for p in out_dir.rglob("*") if p.is_file())
    size = sum(p.stat().st_size for p in out_dir.rglob("*") if p.is_file())
    print(
        f"built {len(days)} day(s), {total_pages} week page(s), "
        f"{len(weeklies)} weekly report(s), {len(overviews)} overview(s), "
        f"{files} file(s), {size / 1024:.0f} KiB -> {out_dir}"
    )
    print(f"base path: {base or 'relative links'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
