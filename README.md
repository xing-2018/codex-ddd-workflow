# codex-ddd-workflow

面向Windows的Codex设计驱动开发（DDD）工作流和按需Skills。先确认需求与设计，再完成获准实施、诊断、审阅和文档交付。

**这是Windows版本。其他平台需要使用者自行修改并验证。**各Skill仍有自己的软件、版本、宿主工具与授权要求，见[环境与限制](docs/环境与限制.md)。

## 让Codex安装

将下面请求发送给本机Codex，把`<本机仓库目录>`替换为希望存放克隆副本的目录：

```text
请获取https://github.com/xing-2018/codex-ddd-workflow到<本机仓库目录>，按其中README.md和docs/安装与更新.md安装全部常驻Skills。
授权在指定目录克隆公开仓库，或对已有干净副本做安全的fast-forward更新；保留本地改动，不切换分支。
先核对仓库版本和本机安装目标，展示差异及备份位置。
来源和目标无冲突且验证通过时，授权按该固定计划完成安装、备份和失败恢复；遇到漂移、未知副本或较新版本时暂停相关写入并报告。
不自动合并、替换或写入我的AGENTS.md，不修改config.toml，不安装非常驻Skills，不删除其他副本，不推送。
报告安装结果、跳过项、冲突及备份位置，并说明如何在新对话中确认Skill可用。
```

默认只安装7项常驻Skills。若同时需要4项子代理角色，将第一句的安装范围改为“全部常驻Skills及仓库全部角色，使用workflow模式”。安装工具对AGENTS.md和config.toml始终只核对是否变化。

根目录[AGENTS.md](AGENTS.md)约束本仓库工作；[AGENTS.global.md](AGENTS.global.md)提供完整全局规则，包含沟通、授权、工作边界及Skill入口，[中文审阅版](AGENTS.global_zh.md)逐条对应。全局规则由用户自行审阅并决定采用内容和范围，安装不会自动合并、替换或写入用户指令。中文副本仅供阅读和审核。

## 使用

```text
使用ddd-flow，为订单列表增加日期筛选，保留现有分页与导出行为。
先给出最小设计；我批准后再完成实现和明确获准的验证。
```

设计、实施、只读诊断和获准修复由ddd-flow路由。独立代码审阅使用ddd-review。更多示例见[使用指南](docs/使用指南.md)。

## 常驻Skills

| Skill | 用途 |
| --- | --- |
| [ddd-flow](skills/resident/ddd-flow/SKILL.md) | 路由项目工作、批准、执行与恢复 |
| [ddd-design](skills/resident/ddd-design/SKILL.md) | 需求、交互、技术设计和实施计划 |
| [ddd-implement](skills/resident/ddd-implement/SKILL.md) | 按设计实施、诊断和修复 |
| [ddd-review](skills/resident/ddd-review/SKILL.md) | 设计一致性及工程质量审阅 |
| [tdd](skills/resident/tdd/SKILL.md) | 有独立预期的测试先行方法 |
| [chinese-docs](skills/resident/chinese-docs/SKILL.md) | 中文文档及按明确请求的其他格式 |
| [writing-for-agents](skills/resident/writing-for-agents/SKILL.md) | AGENTS和Skill指令维护 |

## 按项目选择的Skills

| Skill | 用途与前提 |
| --- | --- |
| [three-js](skills/non-resident/three-js/SKILL.md) | 原生Three.js，先核对目标版本 |
| [threejs-visual-validation](skills/non-resident/threejs-visual-validation/SKILL.md) | 固定视角、时间稳定性及性能验证 |
| [fastapi](skills/non-resident/fastapi/SKILL.md) | FastAPI／Pydantic，适用版本以Skill为准 |
| [playwright-interactive](skills/non-resident/playwright-interactive/SKILL.md) | 本地Web／Electron，需相应宿主工具 |
| [create-chatgpt-local-mcp-plugin](skills/non-resident/create-chatgpt-local-mcp-plugin/SKILL.md) | 显式请求的本机私有MCP插件开发 |
| [femap-control](skills/non-resident/femap-control/SKILL.md) | Windows Femap COM，需本机软件与许可 |
| [demo-video-recording](skills/non-resident/demo-video-recording/SKILL.md) | 经授权的操作演示录制与后期处理 |
| [lsdyna](skills/non-resident/lsdyna/SKILL.md) | 本机LS-DYNA，需求解器及许可 |
| [ship-ice-collision](skills/non-resident/ship-ice-collision/SKILL.md) | 外部案例配置驱动的船冰仿真，配套LS-DYNA |

非常驻Skills只能安装到明确指定的项目。[安装与更新](docs/安装与更新.md)包含可复制请求、冲突处理和恢复方法。

## 许可

原创内容采用[MIT](LICENSE)，第三方内容保留各自许可、署名与[来源声明](THIRD_PARTY_NOTICES.md)。本仓库不分发专用软件、账号、凭据或真实案例数据。
