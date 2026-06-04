# Skill Routing Kit

Skill Routing Kit 是一个本地优先的 Codex 插件，用来提升 skill 和插件的命中率，同时避免引入缓慢、强侵入的运行时路由层。

它提供：

- 一段可放入 `AGENTS.md` 的强制静默路由规则
- 一个本地 skill/plugin 分层能力索引
- 一个手动路由诊断命令
- 显式 registry 更新和健康检查命令
- 明确的剥离和恢复步骤

这个插件适合主要项目都在本地仓库、本地文件里的用户。外部连接器只有在用户明确点名、数据源明显位于该应用、或用户确认后才升权。

## 插件简介

这个插件解决的问题是：Codex 有很多 skill 和插件，但实际任务中不一定能稳定命中正确能力。

Skill Routing Kit 的目标不是接管 Codex，而是让 Codex 在每个非简单任务前做一次很轻的静默路由判断：

```text
任务类型是什么？
素材在哪里？
最终交付物是什么？
需要哪个 process skill？
需要哪个 artifact skill？
是否涉及外部 connector？
```

普通任务不展示路由报告；复杂任务才展示简短 routing check。

## 设计原理与实现逻辑

系统分三层：

```text
Always-on Routing Guard
  放在 AGENTS.md 的极短规则，负责日常静默路由判断。

Registry
  本地 JSON 分层能力索引，按 process/source/artifact/domain/risk 分类。

Diagnostic Plugin
  显式调用的诊断工具，用于排查为什么没命中、更新索引、改进 skill 描述。
```

提高命中率的方法论：

1. **描述何时用**  
   每个 skill/plugin 都要能回答“什么任务、什么输入、什么最终交付物出现时应该用我”。这对应 registry card 里的 `use_when`、`inputs`、`outputs`，也对应 skill 描述里的触发条件。

2. **分层路由设计**  
   先按 `process/source/artifact/domain/risk` 分类，再决定主能力和辅助能力。比如“把 PDF 做成 PPT”里，最终交付物决定主能力是 Presentations，PDF 只作为输入处理能力参与。

3. **增加负样本描述**  
   每张 card 必须说明 `avoid_when`，也就是“什么时候不要用”。负样本用来减少误触发，例如 connector 未被明确点名时不主动访问外部数据，或 PDF 只是输入时不把 PDF skill 当主能力。

4. **召回加重排**  
   路由先宽召回候选能力，再按最终交付物、素材来源、任务动作、风险/权限要求重排。v1 使用保守关键词和分类匹配；registry 的结构是为了以后替换成 embedding 或更强 reranker 时不用重写文档和能力卡。

这四点分别落在：

- `SKILL.md` 描述：让模型知道何时该考虑某个 skill。
- `registry/*.json`：保存可检索的 `use_when/categories/avoid_when`。
- `scripts/route_request.py`：执行召回、打分、重排和诊断。
- `AGENTS.md` 片段：把路由判断变成日常默认动作。

核心原则：

1. **强制路由判断，但不强制展示报告**  
   每个非简单任务都应该内部做 routing micro-check，但普通任务不打扰用户。

2. **本地优先**  
   默认使用本地文件、本地仓库、本地浏览器验证和本地构建/测试。外部连接器必须明确触发或确认。

3. **快速检索，不每轮扫描**  
   registry 是本地 JSON 索引。新增或修改 skill/plugin 后手动刷新，不在每次对话中动态扫描。

4. **连接器保守处理**  
   registry 不读取 Gmail、Slack、Notion、Drive 等真实内容，也不判断授权状态。连接器只表示“可能相关”，不代表可用。

5. **可剥离**  
   插件不安装 hooks、不做 telemetry、不后台扫描、不接管 runtime path。删除 AGENTS 片段、registry 和插件目录后即可回到 Codex 原生行为。

## 安装方式

### 推荐：直接让 Codex 安装

如果你不熟悉命令行、目录结构或插件安装流程，直接把下面这句话复制给 Codex：

```text
请从 https://github.com/juew/Skill-Routing-Kit 安装 Skill Routing Kit 插件。插件源请全局安装到 ~/plugins/skill-routing-kit，注册到 ~/.agents/plugins/marketplace.json，执行 codex plugin add skill-routing-kit@personal，并默认把路由规则启用到 ~/.codex/AGENTS.md，让所有项目都能受益。不要把插件安装到当前项目目录。不要让我手动创建目录；请使用仓库里的安装脚本完成安装，并在安装后验证插件。
```

Codex 应该替你完成这些事：

- 下载或克隆仓库
- 创建需要的本地目录
- 安装插件文件
- 注册个人 marketplace
- 通过 `codex plugin add skill-routing-kit@personal` 启用插件
- 默认写入全局 `~/.codex/AGENTS.md` 路由规则
- 运行插件校验和基础测试

你不需要手动创建 `.codex-plugin`、`skills`、`registry` 这些目录。

### 一行命令安装

如果你愿意在终端里执行一条命令：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents --codex-add
```

默认安装到：

```text
~/plugins/skill-routing-kit
```

并注册到：

```text
~/.agents/plugins/marketplace.json
```

并把路由规则写入：

```text
~/.codex/AGENTS.md
```

默认作用域：

- 插件源：全局，`~/plugins/skill-routing-kit`
- marketplace：个人，`~/.agents/plugins/marketplace.json`
- 路由规则：全局，`~/.codex/AGENTS.md`
- 项目级路由：高级选项，通过 `--agents /path/to/project/AGENTS.md` 指定

如果你只想安装插件、不自动写入 `AGENTS.md`：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --codex-add
```

如果你想把路由规则写入某个项目的 `AGENTS.md`：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents --agents "/path/to/project/AGENTS.md" --codex-add
```

安装后如果 Codex 没有立刻识别新插件，请重启 Codex 或重新加载插件。

## 更新方式

### 推荐：直接让 Codex 更新

如果你不熟悉命令行，直接把下面这句话复制给 Codex：

```text
请从 https://github.com/juew/Skill-Routing-Kit 更新 Skill Routing Kit 插件。插件源继续安装在全局目录 ~/plugins/skill-routing-kit，继续注册到 ~/.agents/plugins/marketplace.json，执行 codex plugin add skill-routing-kit@personal，路由规则继续全局启用在 ~/.codex/AGENTS.md。请备份旧版本、覆盖安装新版本、刷新 registry、验证插件，不要让我手动创建或复制目录。
```

Codex 应该替你完成这些事：

- 拉取 GitHub 上的最新版本
- 备份当前本地版本
- 覆盖安装到 `~/plugins/skill-routing-kit`
- 更新 `~/.agents/plugins/marketplace.json`
- 重新执行 `codex plugin add skill-routing-kit@personal`
- 更新 `~/.codex/AGENTS.md` 中 `BEGIN/END Skill Routing Kit` 之间的路由规则
- 刷新 registry
- 运行插件校验和基础测试

### 一行命令更新

安装器也可以直接作为更新器使用：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents --codex-add
```

已有版本会自动备份到：

```text
~/plugins/.backups/
```

更新后如果 Codex 没有立刻识别新版本，请重启 Codex 或重新加载插件。

### 高级用户：手动安装

插件目录结构如下，供发布者或高级用户排查使用：

```text
skill-routing-kit/
├── .codex-plugin/plugin.json
├── skills/skill-router/SKILL.md
├── scripts/
├── registry/
├── examples/
└── assets/
```

日常静默路由规则位于：

```text
assets/agents-routing-snippet.md
```

片段带有明确标记，方便以后安全删除：

```text
BEGIN Skill Routing Kit
END Skill Routing Kit
```

## 日常使用方式

大多数时候，你不需要说“调用 router”。正常向 Codex 提需求即可。

`AGENTS.md` 片段会让 Codex 静默判断：

- 任务类型
- 素材位置
- 最终交付物
- 是否需要 process skill
- 是否涉及连接器

普通任务不展示路由报告。

复杂、模糊、多交付物或长任务时，Codex 可以展示简短 routing check：

```text
主 skill: ...
辅助 skill: ...
数据源: ...
验证路径: ...
```

## 手动诊断路由

当你想明确查看某个请求会命中什么能力时：

```bash
python3 scripts/route_request.py "把这个 PDF 整理成一份 PPT"
```

调试模式：

```bash
python3 scripts/route_request.py --debug "修复这个前端报错"
```

检查 registry 健康状态：

```bash
python3 scripts/route_request.py --check-registry
```

刷新 registry 后再诊断：

```bash
python3 scripts/route_request.py --refresh "分析这个 CSV 并生成 Excel 报告"
```

## 更新 Registry 的方式

在安装、删除或修改 skill/plugin 后刷新 registry：

```bash
python3 scripts/build_registry.py --yes
```

只看扫描摘要，不写入：

```bash
python3 scripts/build_registry.py --dry-run
```

指定输出路径：

```bash
python3 scripts/build_registry.py --output registry/capabilities.generated.json --yes
```

扫描器遵守这些限制：

- 只读本地 metadata 文件
- 不联网
- 不读取连接器真实内容
- 不判断连接器授权状态
- 只写 registry 输出文件

每张 capability card 都带来源路径和时间戳，方便追踪错误索引。

## Registry 健康检查

`route_request.py` 会在以下情况提醒：

- registry 不存在
- registry 超过 7 天
- `schema_version` 不匹配
- 来源路径已经不存在

查看详细来源：

```bash
python3 scripts/route_request.py --check-registry --debug
```

## 剥离与恢复

如果你不再需要 Skill Routing Kit：

1. 删除 `AGENTS.md` 中以下标记之间的内容：

```text
BEGIN Skill Routing Kit
END Skill Routing Kit
```

2. 删除生成的 registry 文件：

```bash
rm registry/capabilities.generated.json
```

3. 通过正常 Codex 插件流程卸载插件，或删除插件目录。

插件没有 hooks、telemetry、后台扫描或 runtime path 接管，所以删除后会回到 Codex 原生 skill discovery。

## 限制

- registry 是辅助索引，不是真相源。
- connector card 不代表已授权或可访问数据。
- v1 使用保守关键词和分类匹配，不使用 embedding。
- 自动扫描、registry diff、连接器可用性探测、深度冲突诊断放到 v2。

## 验收方式

运行：

```bash
python3 -m unittest discover -s tests
python3 scripts/route_request.py --check-registry
python3 scripts/build_registry.py --dry-run
```
