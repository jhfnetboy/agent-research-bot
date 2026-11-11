import json,sys,os
sys.path.insert(0,os.path.dirname(__file__))
from weekly_data import WEEKS,TRENDS,GAPS
OUT=os.path.join(os.path.dirname(__file__),'..','weekly')
def lk(l):
    n=f"，{l['note']}" if l.get('note') else ''
    return f"[{l['label']}]({l['url']})（{l['date']}{n}）"
def item_json(it,kind):
    return {"kind":kind,"topic":it["topic"],"title":it["title"],
            "summary": (it["what"]+" "+it["why"]) if kind=="major" else it["summary"],
            "what":it.get("what"),"why":it.get("why"),
            "links":it["links"],"date":min(l["date"] for l in it["links"]),
            "keywords":it["keywords"],
            "second_hand_parts": any(l.get("note")=="二手汇总" for l in it["links"]) or "二手" in (it.get("what","")+it.get("why","")+it.get("summary",""))}
for w in WEEKS:
    md=[f"# AI 重大技术变化周报 {w['week']}",f"",f"覆盖：{w['range']}（Asia/Bangkok UTC+7）" + ("" if w['complete'] else "。本周尚未结束，内容不完整。"),"",
        f"**本周主线**：{w['theme']}","","## 重大变化",""]
    for i,it in enumerate(w['major'],1):
        md+= [f"### {i}. {it['title']}",f"",f"- **发生了什么**：{it['what']}",f"- **为什么重要**：{it['why']}",f"- **来源**：" + "；".join(lk(l) for l in it['links']),""]
    md+=["## 其他值得一提",""]
    for it in w['others']:
        md.append(f"- **{it['title']}**：{it['summary']}（" + "；".join(lk(l) for l in it['links'])+"）")
    md+=["","---","注：标“二手”的内容转引自 Latent Space AINews 汇总，非原始发布。OpenAI 链接对 curl 返回 403，已用官方 RSS 核实存在和日期。",""]
    open(f"{OUT}/{w['week']}.md","w").write("\n".join(md))
    js={"week":w['week'],"range":w['range'],"timezone":"Asia/Bangkok (UTC+7)","complete":w['complete'],"theme":w['theme'],
        "items":[item_json(i,"major") for i in w['major']]+[item_json(i,"other") for i in w['others']]}
    json.dump(js,open(f"{OUT}/{w['week']}.json","w"),ensure_ascii=False,indent=2)
# overview
ov=["# AI 重大技术变化：2026-W43 至 W46 总览","","覆盖 2026-10-19 至 2026-11-11（Asia/Bangkok UTC+7），W46 为本周至今。每周详情见同目录 2026-W4x.md。",""]
for w in WEEKS:
    ov+=[f"## {w['week']}（{w['range']}）","",f"**主线**：{w['theme']}",""]
    for it in w['major']:
        ov.append(f"- **{it['title']}**：" + "；".join(lk(l) for l in it['links'][:2]))
    ov.append("")
ov+=["## 四周趋势",""]
for i,t in enumerate(TRENDS,1): ov.append(f"{i}. **{t['title']}**：{t['text']}")
ov+=["","## 覆盖不足与说明",""]+[f"- {g}" for g in GAPS]+[""]
open(f"{OUT}/2026-W43_W46-overview.md","w").write("\n".join(ov))
ov_js={
    "id":"2026-W43_W46-overview",
    "title":"AI 重大技术变化：2026-W43 至 W46 总览",
    "range":"2026-10-19 至 2026-11-11",
    "timezone":"Asia/Bangkok (UTC+7)",
    "note":"W46 为本周至今。",
    "weeks":[{"week":w["week"],"range":w["range"],"theme":w["theme"],"complete":w["complete"],
              "majors":[{"title":it["title"],"links":it["links"]} for it in w["major"]]}
             for w in WEEKS],
    "trends":TRENDS,
    "gaps":GAPS,
}
json.dump(ov_js,open(f"{OUT}/2026-W43_W46-overview.json","w"),ensure_ascii=False,indent=2)
print("done")
