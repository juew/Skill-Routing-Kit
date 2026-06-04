# Juejin Post

Title:

```text
我做了一个 Codex 插件，用来提高 AI skill/plugin 的命中率
```

Body:

````md
## 背景

Codex 的 skill 和插件越来越多之后，一个很现实的问题会出现：能力是装上了，但不一定会在正确时机被调用。

这个问题不显眼，但很影响体验。你会发现模型知道很多能力，却在某些任务里没有选对：

- 问“为什么 pdf skill 没命中”，它可能直接进入 PDF 任务，而不是做 routing 诊断。
- 让它“把 PDF 做成 PPT”，它可能过度关注 PDF，而不是把最终交付物识别为 presentation。
- 明明是本地项目调试，却可能考虑外部 connector。

我把这个问题抽象成 skill/plugin routing hit rate，于是做了一个本地优先的小插件：Skill Routing Kit。

GitHub:
https://github.com/juew/Skill-Routing-Kit

## 它是什么

Skill Routing Kit 是一个 Codex 插件，目标不是接管 Codex，而是让 Codex 更容易在正确时机调用正确能力。

它提供：

- 一个 `skill-router` skill，用于路由诊断
- 一个本地 capability registry
- 一段可放进 `AGENTS.md` 的静默 routing guard
- `route_request.py` 诊断脚本
- `build_registry.py` registry 刷新脚本

它默认不联网、不读取 connector 内容、不做后台扫描。

## 一个例子

```bash
python3 scripts/route_request.py "为什么 pdf skill 没有命中这个请求"
```

输出：

```text
Recommended skill/plugin:
- Skill Router (skill-router)

Helper skills/plugins:
- PDF (pdf)
```

这里 `pdf` 是被提到的上下文，但主任务是“诊断为什么没命中”，所以主能力应该是 `skill-router`。

再看一个：

```bash
python3 scripts/route_request.py "把这个 PDF 整理成一份 PPT"
```

主能力应该是 `Presentations`，因为最终交付物是 PPT。PDF 只是输入。

## 方法论

我现在比较确定，提高 skill/plugin 命中率至少需要四层设计：

1. when to use：明确什么时候应该用
2. layered routing：按 process/source/artifact/domain/risk 分层
3. when not to use：写负样本，说明什么时候不要用
4. recall + rerank：先宽召回，再按最终交付物、素材来源、任务动作和权限风险重排

Skill Routing Kit v0.1.0 还是很朴素的版本，用关键词和分类匹配。但 registry 的结构已经为后续 embedding/reranker 预留了位置。

## 为什么本地优先

我不希望路由层变成另一个黑箱，也不希望它一上来就读 Slack、Gmail、Notion 或 Drive 内容。

所以这个插件：

- 只读本地 `SKILL.md`、`plugin.json` 和 registry metadata
- 不判断 connector 是否授权
- 不读取 connector 内容
- 不安装 daemon 或后台 scanner
- 可以通过删除 AGENTS block 和插件目录恢复原状

## 安装

让 Codex 安装：

```text
请从 https://github.com/juew/Skill-Routing-Kit 安装 Skill Routing Kit 插件。插件源请全局安装到 ~/plugins/skill-routing-kit，注册到 ~/.agents/plugins/marketplace.json，执行 codex plugin add skill-routing-kit@personal，并默认把路由规则启用到 ~/.codex/AGENTS.md。不要把插件安装到当前项目目录。不要让我手动创建目录；请使用仓库里的安装脚本完成安装，并在安装后验证插件。
```

或者一行命令：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents --codex-add
```

## 想收集反馈

如果你也在维护 Codex skills、MCP 或 agent workflow，欢迎分享你遇到的 missed trigger 场景。

我最想收集的是：

- 哪类请求最容易选错 skill？
- 负样本应该怎么写才有用？
- connector 什么时候应该默认保守，什么时候应该主动进入？
````
