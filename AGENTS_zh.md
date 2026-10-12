# codex-ddd-workflow中文审阅版

本文件对应[AGENTS.md](AGENTS.md)，仅供审阅，不作为额外执行指令。

## 范围与指令来源

- 本版本面向Windows；其他平台由使用者自行适配。使用用户的语言，从其电脑解析工具和路径。
- AGENTS.global.md是可选的全局指令源，不额外加载为项目规则。采用时由用户决定准确内容和作用范围，不自动合并、替换或写入用户AGENTS.md，不修改config.toml。
- 英文AGENTS及Skill文件为执行源。AGENTS_zh.md、AGENTS.global_zh.md及Skill中文副本仅供审阅，不额外加载。阅读Skill不授权安装或调用它。
- 保护已有指令、配置和无关文件。缺少工具或依赖只阻塞相关动作，不未经授权安装或修改设置。

## 安装与更新

- 遵循README.md和docs/安装与更新.md，获取仓库固定版本，使用scripts/install_public_distribution.py核对来源和目标。
- 默认安装全部常驻Skills；用户选择workflow模式时才增加角色。非常驻Skills仅安装到明确指定的项目。
- 展示固定版本、真实目标、差异、冲突及备份位置。只有明确授权的安装才执行；无漂移的同一计划复用批准，来源或目标漂移时停止相关写入。
- 更新前，本机安装记录须与旧副本完整内容相同。保留未知、较新和本地修改的目标。备份放在Skill与角色发现目录之外，核验所有复制文件，报告恢复失败及保留位置。
- 安装计划和日志放在本checkout的.local-artifacts/<task>/中；其中包含本机路径，不提交或分享。
- 安装后在新Codex对话中检查Skill和角色是否可用；实际任务遵循docs/使用指南.md及所选Skill的要求。
