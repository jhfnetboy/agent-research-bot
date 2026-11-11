# Agent Research Bot 信息源清单

更新：2026-11-11（Asia/Bangkok UTC+7）。共 50 个来源。可访问性于 2026-11-11 逐个用 curl 检测，状态码见每行最后一列（X 账号用 X API 核验存在）。

优先级：P0 每天必抓；P1 每天抓，入选看相关度；P2 每周扫一遍或按需。

## 模型发布

| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |
| --- | --- | --- | --- | --- | --- | --- |
| OpenAI News | https://openai.com/news/rss.xml | 官方博客 | OpenAI 模型、产品、安全与研究发布 | P0 | RSS | 200 |
| Anthropic News | https://www.anthropic.com/news | 官方博客 | Claude 模型发布、政策、产品 | P0 | HTML 列表页抓取 | 200 |
| Google AI Blog (The Keyword) | https://blog.google/technology/ai/rss/ | 官方博客 | Gemini 产品与大厂 Super Agent（Gemini agent、Antigravity） | P0 | RSS | 200 |
| Meta AI / Meta Superintelligence Labs | https://ai.meta.com/blog/ | 官方博客 | Muse 系列模型、Llama、研究发布 | P1 | HTML 列表页抓取 | 200 |
| xAI News | https://x.ai/news | 官方博客 | Grok 模型与产品更新 | P1 | HTML 列表页抓取 | 200 |
| Mistral AI News | https://mistral.ai/news | 官方博客 | Mistral 模型、Agents API 与企业产品 | P1 | HTML 列表页抓取 | 200 |
| Qwen Blog | https://qwenlm.github.io/blog/index.xml | 官方博客 | Qwen 开源模型发布与技术报告 | P0 | RSS | 200 |
| DeepSeek API News | https://api-docs.deepseek.com/news/news | 官方博客 | DeepSeek 模型与 API 更新 | P0 | HTML 列表页抓取 | 200 |
| X：@OpenAI / @OpenAIDevs | https://x.com/OpenAIDevs | X 账号 | OpenAI 开发者发布 | P0 | X API 用户时间线 | X-API已核验 |
| X：@AnthropicAI / @claudeai / @ClaudeDevs | https://x.com/ClaudeDevs | X 账号 | Claude 发布与开发者公告 | P0 | X API 用户时间线 | X-API已核验 |
| X：@GoogleDeepMind / @GoogleAIStudio | https://x.com/GoogleDeepMind | X 账号 | Gemini 发布 | P0 | X API 用户时间线 | X-API已核验 |
| X：@Alibaba_Qwen / @deepseek_ai / @MistralAI / @AIatMeta | https://x.com/Alibaba_Qwen | X 账号 | 开源与海外模型发布 | P1 | X API 用户时间线 | X-API已核验 |

## 前沿实验室研究

| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |
| --- | --- | --- | --- | --- | --- | --- |
| Google DeepMind Blog | https://deepmind.google/blog/ | 官方博客 | Gemini、AlphaProof 等研究与模型发布 | P0 | HTML 列表页抓取（RSS 当前解析失败） | 200 |
| arXiv API（cs.AI + agent） | https://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+abs:agent&sortBy=submittedDate&max_results=50 | 论文源 | Agent 相关新论文 | P1 | Atom API | 200 |

## RSI

| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |
| --- | --- | --- | --- | --- | --- | --- |
| Hugging Face Daily Papers | https://huggingface.co/api/daily_papers | 论文源 | 社区投票的每日论文，含 RSI、RL、Agent | P0 | JSON API | 200 |
| Import AI（Jack Clark） | https://jack-clark.net/feed/ | Newsletter | 每周研究精选，常涉及 AI 自我改进与安全 | P1 | RSS | 200 |

## 后训练

| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |
| --- | --- | --- | --- | --- | --- | --- |
| Hugging Face Blog | https://huggingface.co/blog/feed.xml | 官方博客 | 开源模型、微调、TRL、数据集 | P1 | RSS | 200 |
| arXiv cs.CL RSS | https://rss.arxiv.org/rss/cs.CL | 论文源 | LLM、RL、RAG 方向每日新论文 | P2 | RSS，按关键词过滤 | 200 |
| TRL Releases | https://github.com/huggingface/trl/releases.atom | GitHub | GRPO、DPO 等 RL 与微调实现 | P1 | Atom | 200 |
| verl Releases | https://github.com/verl-project/verl/releases.atom | GitHub | 大规模 RL 训练框架 | P2 | Atom | 200 |
| Interconnects（Nathan Lambert） | https://www.interconnects.ai/feed | Newsletter | RLHF、RLVR、开源模型后训练分析 | P0 | RSS | 200 |

## RAG 与向量数据库

| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |
| --- | --- | --- | --- | --- | --- | --- |
| LlamaIndex Releases | https://github.com/run-llama/llama_index/releases.atom | GitHub | RAG 框架版本更新 | P2 | Atom | 200 |
| Qdrant Releases | https://github.com/qdrant/qdrant/releases.atom | GitHub | 向量库版本更新 | P2 | Atom | 200 |
| Milvus Releases | https://github.com/milvus-io/milvus/releases.atom | GitHub | 向量库版本更新 | P2 | Atom | 200 |
| Pinecone Blog | https://www.pinecone.io/blog/ | 官方博客 | 检索、RAG 实践与产品 | P2 | HTML 抓取 | 200 |

## Agent 框架

| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |
| --- | --- | --- | --- | --- | --- | --- |
| Anthropic Engineering | https://www.anthropic.com/engineering | 官方博客 | Claude Code、Agent SDK、工具调用的工程实践 | P0 | HTML 列表页抓取 | 200 |
| LangGraph Releases | https://github.com/langchain-ai/langgraph/releases.atom | GitHub | LangGraph 版本更新 | P1 | Atom | 200 |
| LangChain Blog | https://blog.langchain.com/ | 官方博客 | Agent 工程实践、评测、LangSmith | P1 | HTML 抓取（RSS 解析失败） | 200 |
| OpenAI Agents SDK Releases | https://github.com/openai/openai-agents-python/releases.atom | GitHub | OpenAI Agents SDK 版本更新 | P0 | Atom / gh api | 200 |
| Claude Agent SDK Releases | https://github.com/anthropics/claude-agent-sdk-python/releases.atom | GitHub | Claude Agent SDK 版本更新 | P0 | Atom / gh api | 200 |
| Claude Code Releases | https://github.com/anthropics/claude-code/releases.atom | GitHub | Claude Code 版本与新能力 | P1 | Atom / gh api | 200 |
| OpenAI Codex Releases | https://github.com/openai/codex/releases.atom | GitHub | Codex CLI 版本更新 | P1 | Atom / gh api | 200 |
| CrewAI Releases | https://github.com/crewAIInc/crewAI/releases.atom | GitHub | CrewAI 版本更新 | P2 | Atom | 200 |
| AutoGen Releases | https://github.com/microsoft/autogen/releases.atom | GitHub | AutoGen 版本更新 | P2 | Atom | 200 |
| Microsoft Agent Framework Releases | https://github.com/microsoft/agent-framework/releases.atom | GitHub | AutoGen 与 Semantic Kernel 的继任框架 | P1 | Atom | 200 |
| Google ADK Releases | https://github.com/google/adk-python/releases.atom | GitHub | Google Agent Development Kit 版本更新 | P1 | Atom | 200 |
| Simon Willison | https://simonwillison.net/atom/everything/ | Newsletter | LLM 工具、Agent 实践、提示与安全 | P0 | Atom | 200 |

## 大厂 Super Agent

| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |
| --- | --- | --- | --- | --- | --- | --- |
| Cursor Blog | https://cursor.com/blog | 官方博客 | 编码 Agent 产品形态（Projects、多 Agent） | P1 | HTML 列表页抓取 | 200 |

## Agent 协议与工具

| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |
| --- | --- | --- | --- | --- | --- | --- |
| MCP Blog | https://blog.modelcontextprotocol.io/ | 官方博客 | MCP 规范与生态公告 | P0 | HTML 抓取 | 200 |
| MCP 规范 Releases | https://github.com/modelcontextprotocol/modelcontextprotocol/releases.atom | GitHub | MCP 规范版本 | P0 | Atom | 200 |
| A2A Releases | https://github.com/a2aproject/A2A/releases.atom | GitHub | Agent2Agent 协议版本 | P1 | Atom | 200 |

## 评测与基准

| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |
| --- | --- | --- | --- | --- | --- | --- |
| Epoch AI | https://epoch.ai/blog | 论文源 | 算力、能力指数（ECI）、AI 研发自动化（RSI）趋势数据 | P1 | HTML 列表页抓取 | 200 |
| METR | https://metr.org/blog | 官方博客 | Agent 长任务能力、时间跨度评测、模型发布前测试 | P0 | HTML 列表页抓取 | 200 |
| SWE-bench | https://www.swebench.com/ | GitHub | 编码 Agent 主榜单 | P1 | HTML 抓取 | 200 |
| Artificial Analysis | https://artificialanalysis.ai/ | 聚合源 | 独立的智能指数、价格、速度对比 | P0 | HTML 抓取 + X @ArtificialAnlys | 200 |

## 聚合源

| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |
| --- | --- | --- | --- | --- | --- | --- |
| Latent Space + AINews | https://www.latent.space/feed | Newsletter | 每日 AINews（X、Reddit、Discord 汇总）与访谈 | P0 | RSS | 200 |

## 社区

| 名称 | URL / RSS / API | 类型 | 用途 | 优先级 | 抓取方式 | 检测 |
| --- | --- | --- | --- | --- | --- | --- |
| Hacker News（Algolia API） | https://hn.algolia.com/api/v1/search?query=agent&tags=story | 社区 | 按关键词与分数筛选热门讨论 | P0 | JSON API，按 points 和时间过滤 | 200 |
| Reddit r/LocalLLaMA | https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day | 社区 | 开源模型、本地推理、Agent 实测 | P1 | RSS（有频率限制，429 时改用 AINews 的 Reddit 汇总） | 200首次/429限流 |
| Reddit r/ClaudeAI | https://www.reddit.com/r/ClaudeAI/top/.rss?t=day | 社区 | Claude Code 与 Claude 用户反馈 | P2 | RSS（有频率限制） | 200 |
| X：研究者与评测（@karpathy @swyx @simonw @natolambert @omarsar0 @METR_Evals @ArtificialAnlys） | https://x.com/ArtificialAnlys | X 账号 | 第一手评测、实测与观点 | P1 | X API 用户时间线 + 关键词搜索 | X-API已核验 |
