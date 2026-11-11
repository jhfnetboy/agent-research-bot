#!/usr/bin/env bash
# 每日流程：生成站点 -> 密钥扫描 -> git commit/push -> wrangler 部署到 Cloudflare Pages。
# 前提：digests/DATE.md 和 digests/DATE.json 已写好（先运行 scripts/fetch_feeds.py 收集候选，再撰写日报）。
# 用法：bash scripts/daily.sh [YYYY-MM-DD]   （默认今天，Asia/Bangkok）
# 需要：环境变量 CLOUDFLARE_API_TOKEN（Pages 编辑权限）；可选 CLOUDFLARE_ACCOUNT_ID；gh 已登录可 push。
# 可选：SKIP_DEPLOY=1 只生成和提交不部署；SKIP_PUSH=1 不 push。
set -euo pipefail
cd "$(dirname "$0")/.."
DATE="${1:-$(TZ=Asia/Bangkok date +%F)}"
PROJECT="${CF_PAGES_PROJECT:-agent-research-bot}"
[ -f "digests/$DATE.json" ] || { echo "缺少 digests/$DATE.json，先写日报"; exit 1; }
python3 -c "import json,sys; d=json.load(open('digests/$DATE.json')); assert d['date']=='$DATE' and d['items'], 'JSON 无效'; assert all(i.get('url') and i.get('date') for i in d['items']), '有条目缺链接或日期'"
python3 scripts/make_sources.py
python3 scripts/fetch_image.py "$DATE" || true
python3 site/build.py
bash scripts/scan_secrets.sh
git add -A
if git diff --cached --quiet; then echo "没有新改动可提交"; else git commit -q -m "digest: $DATE"; fi
[ "${SKIP_PUSH:-0}" = 1 ] || git push -q origin main
if [ "${SKIP_DEPLOY:-0}" != 1 ]; then
  [ -n "${CLOUDFLARE_API_TOKEN:-}" ] || { echo "缺少 CLOUDFLARE_API_TOKEN，跳过部署"; exit 2; }
  cd site
  WR=$(command -v wrangler || echo "npx --yes wrangler")
  $WR pages deploy dist --project-name "$PROJECT" --branch main --commit-dirty=true
  echo "线上地址：https://$PROJECT.pages.dev/"
fi
