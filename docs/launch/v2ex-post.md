# V2EX Post

Board: `分享创造`

Title:

```text
做了一个 Codex 插件：让 skill/plugin 更容易命中正确能力
```

Body:

````md
最近我在用 Codex 的时候遇到一个问题：skill 和插件越装越多，但真正做任务时，不一定能稳定命中正确能力。

比如：

- 用户问“为什么 pdf skill 没有命中”，这其实应该进入 routing 诊断，而不是直接进入 PDF 处理。
- “把 PDF 整理成 PPT”，最终交付物是 PPT，主能力应该是 Presentations，PDF 只是输入上下文。
- 本地项目调试时，默认应该走本地文件/测试/浏览器验证，而不是优先考虑外部 connector。

于是我做了一个小插件：Skill Routing Kit。

仓库：
https://github.com/juew/Skill-Routing-Kit

它做的事情比较克制：

- 在 AGENTS.md 里加入一个很短的 routing guard，让 Codex 在非简单任务前做静默路由判断。
- 用本地 JSON registry 记录 skill/plugin 的 use_when、avoid_when、分类和来源。
- 提供 route_request.py，可以手动诊断一个请求应该命中哪个 skill/plugin。
- 默认本地优先，不联网，不读 Gmail/Slack/Notion/Drive 里的真实内容，不后台扫描。

一个例子：

```bash
python3 scripts/route_request.py "为什么 pdf skill 没有命中这个请求"
```

输出会推荐：

```text
Recommended skill/plugin:
- Skill Router (skill-router)

Helper skills/plugins:
- PDF (pdf)
```

另一个例子：

```bash
python3 scripts/route_request.py "把这个 PDF 整理成一份 PPT"
```

主能力会是 Presentations，PDF 只是 helper。

我自己的理解是，提高 AI skill 命中率不只是“描述写长一点”，而是要有四件事：

1. 说明什么时候用
2. 分层路由：process/source/artifact/domain/risk
3. 说明什么时候不用
4. 先召回，再按最终交付物、来源、动作和权限风险重排

现在还是 v0.1.0，比较朴素，用的是保守关键词和分类匹配，还没上 embedding/reranker。

想听听大家有没有类似的 missed skill/plugin trigger 场景。尤其是用了很多 Codex skill、MCP、connector 之后，大家怎么管理“什么时候该调用哪个能力”？
````
