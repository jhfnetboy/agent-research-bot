# Agent Research Bot

AI Agent 开发每日研究日报，以及它的 Cloudflare Pages 卡片站。结构借鉴 Ethereum Research Bot 的站点（build.py 由其复制后修改）。

- 线上页面：https://agent-research-bot.pages.dev/
- 时区：Asia/Bangkok（UTC+7），每天 10:00 前更新

## 目录

- `sources.md` / `sources.json`：信息源清单（由 `scripts/sources_data.py` 生成，改来源只改这个文件）
- `preferences.md`：用户偏好（选题、长度、屏蔽话题等）
- `digests/YYYY-MM-DD.md`：当天日报全文
- `digests/YYYY-MM-DD.json`：当天结构化数据，站点从这里生成
- `weekly/YYYY-Www.md` / `weekly/YYYY-Www.json`：按自然周汇总的周报；总览文件为 `weekly/2026-W43_W46-overview.md` 与对应 JSON
- `scripts/weekly_data.py` 与 `scripts/build_weekly.py`：周报数据与生成脚本
- `site/build.py`：读取 `digests/*.json` 和 `weekly/*.json`，生成 `site/dist/` 纯静态页面（零依赖，Python 3）
- `site/assets/`：从真实新闻来源下载的配图，JSON 里记录出处
- `site/wrangler.toml`：Pages 项目配置（项目名 `agent-research-bot`）
- `scripts/fetch_feeds.py`：抓取 RSS / Atom / HN 最近 48 小时候选，写到 `work/`（不提交）
- `scripts/fetch_image.py`：按 `image.source_url` 抓 og:image 存到 `site/assets/`
- `scripts/scan_secrets.sh`：提交前扫描 token / key 样式内容
- `scripts/daily.sh`：每日流程（生成站点 + 扫描 + git commit/push + wrangler 部署）

## 页面结构

- 首页：最新一周的卡片（每天一张：日期、关键词、关键信息、配图），按时间倒序；上一周 / 下一周导航
- `weeks/YYYY-Www/`：日报首页按 ISO 周翻页（周一至周日）
- `days/YYYY-MM-DD/`：当天详情页，按 topic 分组列出每条的标题、概述、链接和日期
- `weekly/`：周报栏目首页，最新一周在前；`weekly/YYYY-Www/` 为当周详情，条目含标题、概述和带来源日期的链接；`weekly/2026-W43_W46-overview/` 为四周总览
- `archive/`：按月归档；`about/`：关于与完整来源

## JSON 格式

```json
{
  "date": "2026-11-11",
  "keywords": ["关键词一", "关键词二"],
  "summary": "两三句关键信息，显示在卡片上。",
  "image": {"local_path": "assets/2026-11-11.jpg", "source_url": "https://原文", "credit": "来源"},
  "items": [
    {"topic": "话题", "title": "标题", "summary": "一两句概述", "url": "https://原文", "date": "2026-11-11", "keywords": ["..."]}
  ]
}
```

## 每日用法

```bash
python3 scripts/fetch_feeds.py --hours 48      # 收集候选
# 阅读原文，写 digests/DATE.md 和 digests/DATE.json
bash scripts/daily.sh 2026-11-12               # 生成、提交、推送、部署
```

部署需要环境变量 `CLOUDFLARE_API_TOKEN`（Cloudflare Pages 编辑权限，可选 `CLOUDFLARE_ACCOUNT_ID`）。仓库是公开的，任何凭证都不得写入文件；`.gitignore` 排除了 `.env` 等文件，`daily.sh` 每次提交前都会运行 `scan_secrets.sh`。

本地预览：`python3 site/build.py && python3 -m http.server 8765 --directory site/dist`
