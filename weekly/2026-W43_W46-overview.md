# AI 重大技术变化：2026-W43 至 W46 总览

覆盖 2026-10-19 至 2026-11-11（Asia/Bangkok UTC+7），W46 为本周至今。每周详情见同目录 2026-W4x.md。

## 2026-W43（2026-10-19 至 2026-10-25）

**主线**：AI 找漏洞的能力集中兑现，防守方开始用 AI 做形式化证明；开源推理栈和开源大模型同时向前沿逼近。

- **PHP2Shell 与 AI 漏洞披露潮，LiteLLM 被投毒**：[PHP 安全公告](https://www.php.net/archive/2026.php#2026-10-21-5)（2026-10-21）；[OpenAI: Patch the Planet](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities)（2026-10-21）
- **Anthropic 用 Claude 做大规模形式化验证**：[Anthropic Research](https://www.anthropic.com/research/formal-verification)（2026-10-22）
- **DeepSeek 开源生产推理框架 DeepInfer**：[GitHub: deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer)（2026-10-20）；[HN 讨论（2355 分）](https://news.ycombinator.com/item?id=50163277)（2026-10-20）
- **Kimi K3.1 Pro：开源权重逼近 Fable 级**：[Kimi 官方博客](https://www.kimi.ai/blog/kimi-k3-1-pro)（2026-10-23）；[HN 讨论](https://news.ycombinator.com/item?id=50212065)（2026-10-23）
- **Claude Duet 主动式 Agent，Agent Skills 捐给 AAIF**：[Claude: Claude Duet](https://claude.com/resources/articles/claude-duet)（2026-10-21）；[Anthropic: 捐赠 Agent Skills](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation)（2026-10-22）

## 2026-W44（2026-10-26 至 2026-11-01）

**主线**：前沿模型与评测体系同时换代，Agent 群体做数学证明成为新的能力展示方式，训练期监控和 Agent 供应链安全跟进。

- **Gemini 4 Carbon 发布，先给网络防御者**：[DeepMind Blog](https://deepmind.google/blog/gemini-4-carbon-our-next-frontier-model/)（2026-10-28）；[Google Blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/)（2026-10-28）
- **Agent 群体做数学：CFSG 完成 Lean 形式化，OpenAI 公布 ETH 等结果**：[OpenAI](https://openai.com/index/building-scientific-understanding-with-academic-communities)（2026-10-26）；[Axiom on X](https://x.com/axiommathai/status/2115089794867040584)（2026-10-27）
- **评测换代：AA Index v5 与 FrontierCode 2.0**：[Artificial Analysis on X](https://x.com/ArtificialAnlys/status/2115265133467635877)（2026-10-28）；[Cognition on X](https://x.com/cognition/status/2115132488775524793)（2026-10-28）
- **Mistral Large 4 开放权重**：[Mistral](https://mistral.ai/news/mistral-large-4-oss/)（2026-10-29）；[Hugging Face Blog](https://huggingface.co/blog/mistral-large4)（2026-10-29）
- **训练期监控上线，Agent 分发渠道出现后门**：[OpenAI](https://openai.com/index/how-we-detect-frontier-model-misalignment)（2026-10-29）；[Phorion](https://phorion.io/blog/offical-claude-code-vsx-compromise/)（2026-10-30）

## 2026-W45（2026-11-02 至 2026-11-08）

**主线**：RSI 从讨论变成可测量的数字：模型能直接改权重，METR 估计 Anthropic 的能力进步速度约翻倍；AI 网络攻防进入千漏洞量级。

- **Weight-Space Programming：模型直接读写神经网络权重**：[原文](https://rikiyat.github.io/blog/weight-space-programming/)（2026-11-02）；[Simon Willison 复现](https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights/)（2026-11-03）
- **METR：AI 正在把 Anthropic 的能力进步速度提高约一倍**：[METR 评估报告](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/)（2026-11-05）；[METR 风险报告评审](https://metr.org/blog/2026-11-05-rd-section-anthropic-risk-report-august-2026-review/)（2026-11-05）
- **OpenAI 自治流水线修复 948 个 Linux 内核提权漏洞，发布 GPT-6 Cyber**：[OpenAI: A thousand fewer paths to root](https://openai.com/index/a-thousand-fewer-paths-to-root)（2026-11-04）；[OpenAI: GPT-6 Cyber](https://openai.com/index/introducing-gpt-6-cyber)（2026-11-05）
- **开源权重集中发布：Kimi K3.1 Pro、Inkling 2 Small、Axion 1.0**：[Hugging Face: Kimi-K3.1-Pro](https://huggingface.co/moonshotai/Kimi-K3.1-Pro)（2026-11-04）；[Thinking Machines: Inkling 2 Small](https://thinkingmachines.ai/news/inkling-2-small/)（2026-11-05）

## 2026-W46（2026-11-09 至 2026-11-11（本周至今，未完））

**主线**：多 Agent 编排成为旗舰模型的官方卖点，Anthropic 首次公开在训练中压低 RSI 相关能力。

- **Claude Fable 5.2 / Mythos 5.2**：[Anthropic](https://www.anthropic.com/news/claude-fable-and-mythos-5-2)（2026-11-09）；[AINews: Fable 5.2](https://latent.space/p/ainews-fable-5-2-retakes-world-1-llm-spot-as-ant-ipo-roadshow-begins/)（2026-11-10，二手汇总）
- **Gemini 4 Carbon 全面可用，Antigravity 推出 /swarm**：[DeepMind Blog](https://deepmind.google/blog/gemini-4-carbon-is-now-available/)（2026-11-10）；[AINews](https://latent.space/p/ainews-mercor-750m-series-d-at-20b-valuation-3b-run-rate/)（2026-11-11，二手汇总）
- **AlphaProof Code：用 Agent 形式化验证真实软件**：[DeepMind Blog](https://deepmind.google/blog/introducing-alphaproof-code/)（2026-11-10）
- **紧急停止、权重后门、推理商数据保留**：[OpenAI: Control Room](https://openai.com/index/control-room)（2026-11-09）；[Microsoft Research: Lazarus](https://www.microsoft.com/en-us/research/blog/lazare-veni-foras-reprogramming-dormant-neurons-to-backdoor-ai-agents/)（2026-11-10）

## 四周趋势

1. **多 Agent 编排从实验走向产品默认形态**：Kimi Hosted Agents（W43），Axiom 用 Agent 群体完成 CFSG、DeepSeek 开源 Super-agent harness（W44），Meta 收购 Conductor、s3 用 RL 学分工（W45），Fable 5.2 千 Agent 案例和 Antigravity /swarm（W46）。四周里“协调者加多个执行者加验证者”从研究演示变成官方推荐用法和产品功能。
2. **可机器检查的证明成为长时程 Agent 的验收标准**：Anthropic 用 Claude 写出约 1.8 亿行 Rocq 证明（W43），CFSG 的 5000 万行 Lean（W44），AlphaProof Code 验证 Signal 实现、CPython Lean 形式化（W46）。Lean、Rocq 这类环境让 Agent 的长任务可以自动判对错，也是 RL 和群体协作最好用的训练场。
3. **RSI 从讨论变成测量和主动限制**：Weight-Space Programming 展示模型直接改权重（W45），METR 估计 Anthropic 能力进步速度约为过去两倍（W45），Fable 5.2 发布时写明在训练中压低了 AI 研发相关能力（W46）。实验室开始把 RSI 当作需要度量和设闸的具体能力。
4. **网络安全同时是能力主战场和最大风险面**：PHP2Shell（W43），Carbon 先给防御者（W44），948 个 Linux 漏洞和 GPT-6 Cyber（W45），Mythos 5.2 只给审核机构（W46）。同时 Agent 自身的供应链接连出事：LiteLLM 投毒（W43）、Claude Code 扩展后门（W44）、Lazarus 权重后门和 Fireworks 数据保留（W46）。
5. **评测转向私有集和单任务成本，开源权重持续逼近**：AA Index v5 与 FrontierCode 2.0（W44）、GDPx（W45）都把私有任务和每任务成本放到核心位置；Fable 5.2 单价降而每任务成本升（W46）。开源侧 Kimi K3.1 Pro、Mistral Large 4、Inkling 2 Small 四周内接连放出权重，后训练工具链首日即可支持。

## 覆盖不足与说明

- RAG 与向量数据库的重大变化较少，只在 W43 收录了 Qdrant v1.20 和 Cohere Rerank 5，W45 收录了 Anthropic 的 Agent 记忆文章；其他周没有找到够得上“重大”的检索类发布。
- OpenAI 官网对 curl 返回 403（反爬），OpenAI 条目的存在和日期以官方 RSS（openai.com/news/rss.xml）核实。Microsoft Research 对 curl 返回 403，Lazarus 页面已用另一种抓取方式打开核实（2026-11-10 发布）。
- 部分条目（Axiom CFSG、AA Index v5、FrontierCode 2.0、GDPx、DeepSeek harness、Cohere Rerank 5）官方首发在 X，所以链接用 X 帖子，日期按帖子 ID 换算为 UTC+7。
- 参数、跑分、成本等细节有一部分来自 Latent Space AINews 汇总，文中已标注“二手”或“据 AINews 转述”。Reddit 没有直接抓取。
- W46 只覆盖到 11-11，本周还没结束。
- 未收录：腾讯 Hy4（官方页面返回 567 无法核验）、Recursive Flint 和 Google Harness²（发布日期在 W42）、Anthropic S-1 等纯商业事件。
