# README 路由

README 的目标是让目标读者尽快理解项目并完成首次成功，而不是覆盖仓库中的每个事实。

## 1. 选择策略

独立判断：

- operation：`greenfield`（新建）、`refactor`（保留正确内容并重构）、`partial`（只改指定章节）；
- density：`minimal`、`standard`、`extended`；
- audience：正常仓库使用，可叠加 `release` 对外发布润色。

用户明确要求精简时直接采用 `refactor + minimal`。README 语言优先级：用户明确选择 → 现有 README → 项目主要文档 → 对话语言。即使当前 Skill 以中文文档为主，也不要擅自把稳定的英文开源 README 改成中文。

## 2. 建立仓库证据图

先读取 `evidence.md`，再只检查与 README 声明相关的文件：

1. 适用 instruction 与现有 README；
2. package/project metadata、权威 lockfile、入口与公开接口；
3. 已提交配置示例、CI、release metadata、license、contribution docs；
4. 能证明使用路径的测试和示例。

必须先解决冲突的包管理器、运行命令、项目名、配置项和 URL。不得虚构发布状态、registry 安装命令、badge、主页、demo、API 地址、截图、基准指标或支持渠道。

## 3. 按首次成功组织

默认顺序如下，可省略无证据或无必要章节：

1. 项目名和一句话价值；
2. 2–4 个能力/使用场景；
3. 最短正确 Quick Start；
4. 使用方法和必要配置；
5. 项目特有参考信息；
6. 帮助、贡献、License（有依据时）。

GitHub README 默认不手写目录，除非用户要求或目标渲染器/篇幅确实需要。

项目类型侧重点：

- CLI：安装、命令、常见示例、flags/config；
- Library/SDK：安装/import、最小示例、公开 API、兼容性；
- Backend/API：前置条件、配置名、本地运行、路由/集成面；
- Frontend component：安装/import、使用、props/API、真实预览链接；
- Full-stack/desktop/mobile：能力摘要、依赖服务、本地设置、平台约束；
- DevOps/infrastructure：问题、环境假设、自动化与 CI；
- Data/ML/research：数据来源、环境、可复现运行、输出、限制；
- Monorepo：仓库入口、workspace 命令、包映射和子文档链接。

中文 greenfield README 可使用 `../assets/templates/README.zh-CN.md` 作为脚手架，未使用的占位符和章节必须删除。

## 4. 验证

静态验证至少包括：

- 命令与项目 scripts / package manager 匹配；
- 示例与公开代码、CLI help、路由或测试匹配；
- 相对链接和图片目标存在；
- 配置只写名称和安全示例，不泄露秘密；
- 删除无证据的 badge、发布路径、指标和营销性断言。

只有在安全、相关且授权时才运行最窄现有检查。不要仅为验证 README 安装依赖、启动持久服务、执行迁移或联网。无法执行时在交付说明写 `not run`，不要把静态检查冒充运行验证。

## 5. 写入边界

用户要求 create/update/rewrite/simplify README 时可以修改权威 README；明确要求更新某个章节时，只修改该授权章节。只要求 draft/review/plan，或仅提供某章节草稿时保持只读。保护无关用户改动，优先最小有价值改写。
