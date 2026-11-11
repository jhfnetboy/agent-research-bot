# 来源清单的唯一数据源。改这里，然后运行 python3 scripts/make_sources.py 重新生成 sources.json 和 sources.md。
S = [
# 模型发布
("OpenAI News","https://openai.com/news/rss.xml","官方博客","模型发布","OpenAI 模型、产品、安全与研究发布","P0","RSS"),
("Anthropic News","https://www.anthropic.com/news","官方博客","模型发布","Claude 模型发布、政策、产品","P0","HTML 列表页抓取"),
("Anthropic Engineering","https://www.anthropic.com/engineering","官方博客","Agent 框架","Claude Code、Agent SDK、工具调用的工程实践","P0","HTML 列表页抓取"),
("Google DeepMind Blog","https://deepmind.google/blog/","官方博客","前沿实验室研究","Gemini、AlphaProof 等研究与模型发布","P0","HTML 列表页抓取（RSS 当前解析失败）"),
("Google AI Blog (The Keyword)","https://blog.google/technology/ai/rss/","官方博客","模型发布","Gemini 产品与大厂 Super Agent（Gemini agent、Antigravity）","P0","RSS"),
("Meta AI / Meta Superintelligence Labs","https://ai.meta.com/blog/","官方博客","模型发布","Muse 系列模型、Llama、研究发布","P1","HTML 列表页抓取"),
("xAI News","https://x.ai/news","官方博客","模型发布","Grok 模型与产品更新","P1","HTML 列表页抓取"),
("Mistral AI News","https://mistral.ai/news","官方博客","模型发布","Mistral 模型、Agents API 与企业产品","P1","HTML 列表页抓取"),
("Qwen Blog","https://qwenlm.github.io/blog/index.xml","官方博客","模型发布","Qwen 开源模型发布与技术报告","P0","RSS"),
("DeepSeek API News","https://api-docs.deepseek.com/news/news","官方博客","模型发布","DeepSeek 模型与 API 更新","P0","HTML 列表页抓取"),
("Hugging Face Blog","https://huggingface.co/blog/feed.xml","官方博客","后训练","开源模型、微调、TRL、数据集","P1","RSS"),
# 论文
("arXiv API（cs.AI + agent）","https://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+abs:agent&sortBy=submittedDate&max_results=50","论文源","前沿实验室研究","Agent 相关新论文","P1","Atom API"),
("arXiv cs.CL RSS","https://rss.arxiv.org/rss/cs.CL","论文源","后训练","LLM、RL、RAG 方向每日新论文","P2","RSS，按关键词过滤"),
("Hugging Face Daily Papers","https://huggingface.co/api/daily_papers","论文源","RSI","社区投票的每日论文，含 RSI、RL、Agent","P0","JSON API"),
("Epoch AI","https://epoch.ai/blog","论文源","评测与基准","算力、能力指数（ECI）、AI 研发自动化（RSI）趋势数据","P1","HTML 列表页抓取"),
("Import AI（Jack Clark）","https://jack-clark.net/feed/","Newsletter","RSI","每周研究精选，常涉及 AI 自我改进与安全","P1","RSS"),
# 评测
("METR","https://metr.org/blog","官方博客","评测与基准","Agent 长任务能力、时间跨度评测、模型发布前测试","P0","HTML 列表页抓取"),
("SWE-bench","https://www.swebench.com/","GitHub","评测与基准","编码 Agent 主榜单","P1","HTML 抓取"),
("Artificial Analysis","https://artificialanalysis.ai/","聚合源","评测与基准","独立的智能指数、价格、速度对比","P0","HTML 抓取 + X @ArtificialAnlys"),
# Agent 框架
("LangGraph Releases","https://github.com/langchain-ai/langgraph/releases.atom","GitHub","Agent 框架","LangGraph 版本更新","P1","Atom"),
("LangChain Blog","https://blog.langchain.com/","官方博客","Agent 框架","Agent 工程实践、评测、LangSmith","P1","HTML 抓取（RSS 解析失败）"),
("OpenAI Agents SDK Releases","https://github.com/openai/openai-agents-python/releases.atom","GitHub","Agent 框架","OpenAI Agents SDK 版本更新","P0","Atom / gh api"),
("Claude Agent SDK Releases","https://github.com/anthropics/claude-agent-sdk-python/releases.atom","GitHub","Agent 框架","Claude Agent SDK 版本更新","P0","Atom / gh api"),
("Claude Code Releases","https://github.com/anthropics/claude-code/releases.atom","GitHub","Agent 框架","Claude Code 版本与新能力","P1","Atom / gh api"),
("OpenAI Codex Releases","https://github.com/openai/codex/releases.atom","GitHub","Agent 框架","Codex CLI 版本更新","P1","Atom / gh api"),
("CrewAI Releases","https://github.com/crewAIInc/crewAI/releases.atom","GitHub","Agent 框架","CrewAI 版本更新","P2","Atom"),
("AutoGen Releases","https://github.com/microsoft/autogen/releases.atom","GitHub","Agent 框架","AutoGen 版本更新","P2","Atom"),
("Microsoft Agent Framework Releases","https://github.com/microsoft/agent-framework/releases.atom","GitHub","Agent 框架","AutoGen 与 Semantic Kernel 的继任框架","P1","Atom"),
("Google ADK Releases","https://github.com/google/adk-python/releases.atom","GitHub","Agent 框架","Google Agent Development Kit 版本更新","P1","Atom"),
("Cursor Blog","https://cursor.com/blog","官方博客","大厂 Super Agent","编码 Agent 产品形态（Projects、多 Agent）","P1","HTML 列表页抓取"),
# 协议与工具
("MCP Blog","https://blog.modelcontextprotocol.io/","官方博客","Agent 协议与工具","MCP 规范与生态公告","P0","HTML 抓取"),
("MCP 规范 Releases","https://github.com/modelcontextprotocol/modelcontextprotocol/releases.atom","GitHub","Agent 协议与工具","MCP 规范版本","P0","Atom"),
("A2A Releases","https://github.com/a2aproject/A2A/releases.atom","GitHub","Agent 协议与工具","Agent2Agent 协议版本","P1","Atom"),
# RAG 与向量库
("LlamaIndex Releases","https://github.com/run-llama/llama_index/releases.atom","GitHub","RAG 与向量数据库","RAG 框架版本更新","P2","Atom"),
("Qdrant Releases","https://github.com/qdrant/qdrant/releases.atom","GitHub","RAG 与向量数据库","向量库版本更新","P2","Atom"),
("Milvus Releases","https://github.com/milvus-io/milvus/releases.atom","GitHub","RAG 与向量数据库","向量库版本更新","P2","Atom"),
("Pinecone Blog","https://www.pinecone.io/blog/","官方博客","RAG 与向量数据库","检索、RAG 实践与产品","P2","HTML 抓取"),
# 后训练
("TRL Releases","https://github.com/huggingface/trl/releases.atom","GitHub","后训练","GRPO、DPO 等 RL 与微调实现","P1","Atom"),
("verl Releases","https://github.com/verl-project/verl/releases.atom","GitHub","后训练","大规模 RL 训练框架","P2","Atom"),
("Interconnects（Nathan Lambert）","https://www.interconnects.ai/feed","Newsletter","后训练","RLHF、RLVR、开源模型后训练分析","P0","RSS"),
# Newsletter / 聚合
("Latent Space + AINews","https://www.latent.space/feed","Newsletter","聚合源","每日 AINews（X、Reddit、Discord 汇总）与访谈","P0","RSS"),
("Simon Willison","https://simonwillison.net/atom/everything/","Newsletter","Agent 框架","LLM 工具、Agent 实践、提示与安全","P0","Atom"),
# 社区
("Hacker News（Algolia API）","https://hn.algolia.com/api/v1/search?query=agent&tags=story","社区","社区","按关键词与分数筛选热门讨论","P0","JSON API，按 points 和时间过滤"),
("Reddit r/LocalLLaMA","https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day","社区","社区","开源模型、本地推理、Agent 实测","P1","RSS（有频率限制，429 时改用 AINews 的 Reddit 汇总）"),
("Reddit r/ClaudeAI","https://www.reddit.com/r/ClaudeAI/top/.rss?t=day","社区","社区","Claude Code 与 Claude 用户反馈","P2","RSS（有频率限制）"),
("X：@OpenAI / @OpenAIDevs","https://x.com/OpenAIDevs","X 账号","模型发布","OpenAI 开发者发布","P0","X API 用户时间线"),
("X：@AnthropicAI / @claudeai / @ClaudeDevs","https://x.com/ClaudeDevs","X 账号","模型发布","Claude 发布与开发者公告","P0","X API 用户时间线"),
("X：@GoogleDeepMind / @GoogleAIStudio","https://x.com/GoogleDeepMind","X 账号","模型发布","Gemini 发布","P0","X API 用户时间线"),
("X：@Alibaba_Qwen / @deepseek_ai / @MistralAI / @AIatMeta","https://x.com/Alibaba_Qwen","X 账号","模型发布","开源与海外模型发布","P1","X API 用户时间线"),
("X：研究者与评测（@karpathy @swyx @simonw @natolambert @omarsar0 @METR_Evals @ArtificialAnlys）","https://x.com/ArtificialAnlys","X 账号","社区","第一手评测、实测与观点","P1","X API 用户时间线 + 关键词搜索"),
]
