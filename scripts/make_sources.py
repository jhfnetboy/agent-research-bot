#!/usr/bin/env python3
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from sources_data import S
root = Path(__file__).resolve().parent.parent
keys = ["name","url","type","area","purpose","priority","fetch"]
rows = [dict(zip(keys, r)) for r in S]
verify = {}
vf = root / "scripts" / "sources_check.txt"
if vf.exists():
    for l in vf.read_text().splitlines():
        c, u = l.split(" ", 1); verify[u] = c
for r in rows:
    r["http_status_2026_11_11"] = verify.get(r["url"], "未检测")
(root / "sources.json").write_text(json.dumps({"updated": "2026-11-11", "count": len(rows), "sources": rows}, ensure_ascii=False, indent=2) + "\n")
order = ["模型发布","前沿实验室研究","RSI","后训练","RAG 与向量数据库","Agent 框架","大厂 Super Agent","Agent 协议与工具","评测与基准","聚合源","社区"]
md = ["# Agent Research Bot 信息源清单", "", f"更新：2026-11-11（Asia/Bangkok UTC+7）。共 {len(rows)} 个来源。可访问性于 2026-11-11 逐个用 curl 检测，状态码见每行最后一列（X 账号用 X API 核验存在）。", "", "优先级：P0 每天必抓；P1 每天抓，入选看相关度；P2 每周扫一遍或按需。", ""]
for a in order:
    sub = [r for r in rows if r["area"] == a]
    if not sub: continue
    md += [f"## {a}", "", "| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in sub:
        md.append(f"| {r['name']} | {r['url']} | {r['type']} | {r['purpose']} | {r['priority']} | {r['fetch']} | {r['http_status_2026_11_11']} |")
    md.append("")
(root / "sources.md").write_text("\n".join(md))
print(len(rows), "sources")
