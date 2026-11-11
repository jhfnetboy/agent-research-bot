#!/usr/bin/env bash
# 提交前扫描 token / key 样式的内容。只输出文件名和行号，不输出匹配到的值。
set -uo pipefail
cd "$(dirname "$0")/.."
# 令牌前缀需位于词边界，避免 URL 路径中的 risk-report 被 sk- 误报。
PAT='((?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9]{20,}|(?<![A-Za-z0-9_])github_pat_[A-Za-z0-9_]{20,}|(?<![A-Za-z0-9_])sk-[A-Za-z0-9_-]{20,}|(?<![A-Za-z0-9_])AKIA[0-9A-Z]{16}|(?<![A-Za-z0-9_])xox[abpors]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(CLOUDFLARE_API_TOKEN|CF_API_TOKEN|BAIDU_PUSH_TOKEN|API_KEY|SECRET|PASSWORD)\s*[:=]\s*["'"'"']?[A-Za-z0-9_\-]{12,})'
FILES=$(git ls-files --cached --others --exclude-standard)
hits=0
if [ -n "$FILES" ]; then
  if echo "$FILES" | xargs -d '\n' rg -n -o --pcre2 --no-heading -e "$PAT" -r '<redacted>' 2>/dev/null; then hits=1; fi
  for v in CLOUDFLARE_API_TOKEN BAIDU_PUSH_TOKEN GH_TOKEN GITHUB_TOKEN; do
    val="${!v:-}"
    if [ -n "$val" ] && echo "$FILES" | xargs -d '\n' rg -l -F -- "$val" 2>/dev/null; then
      echo "上面的文件包含环境变量 $v 的值"; hits=1
    fi
  done
fi
if [ "$hits" -ne 0 ]; then echo "发现疑似密钥，停止提交。"; exit 1; fi
echo "密钥扫描通过：未发现 token / key 样式内容。"
