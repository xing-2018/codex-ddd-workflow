# 可选生命周期适配器

> 对应[英文执行规则](lifecycle-hooks.md)，仅供中文审阅，不作为额外执行指令。

[workflow_hooks.py](../scripts/workflow_hooks.py)只接管确定的查找与结构检查，不选择任务阶段、不授予权限、不更新记录或运行产品测试。注册、信任、安装及配置变更分别需要授权；交付Skill不启用hook，也不附带hook配置文件。

## 恢复

`session-start`从stdin读取Codex的SessionStart事件，仅对`resume`或`compact`查找。startup、clear及明确子代理标记静默退出。查找最近具有`.planning`的祖先目录，读取schema2项目入口及对话索引，仅选择`owner_thread`与`session_id`完全相同的唯一安全record.md。无绑定静默退出；多绑定、不安全路径、未知schema或不可读文件给出短提示，回到既有人工恢复路径。

返回项目／记录指针、记录SHA-256及白名单内的声明状态，不注入记录正文、批准回复、对话日志或新记忆。主会话只补读缺失摘要及相关权威，再判断事实是否适用；不扫描历史记录、不选择最新指针。

启用前须在实际宿主核实身份对应与事件覆盖。子代理可能共享父session_id；适配器忽略明确子代理标记，但缺少标记不证明根身份。不注册到SubagentStart／SubagentStop，也不据source检查认证所有宿主。

人工恢复调用同一查找，无需启用hook：

```text
python -B <ddd-flow>/scripts/workflow_hooks.py recover --project <root> --thread <observed-id>
```

本对话有多条索引时，增加`--change`明确选择变更目录或记录。schema1继续由Skill的单指针恢复及workflow_check.py支持；适配器不编造归属或迁移记录。

## 记录检查

`post-tool-use`读取PostToolUse事件，只识别apply_patch命令的明确文件路径（含移动／删除），及Write／Edit的file_path。其他工具和任意shell命令不触发；脚本／shell写入使用人工校验。只有明确写到唯一选中活动record.md时，才在同一进程调用现有校验器。

成功静默，问题只返回有界问题代码及记录指针作为事实反馈。不阻断、不续跑、不作权限或输入重写决定，也不能撤销写入。校验器仍会读取项目、索引及声明的本地依赖，结论只覆盖结构。多步写入中间态可能不完整；主会话按授权维护或报告缺口，适配器不自动修复或改变语义状态。

完整写入后、宣称结构有效前，复用可辨认且对应准确输入的hook／检查证据，否则使用既有命令：

```text
python -B <ddd-flow>/scripts/workflow_check.py --project <root> --change <change-directory> --thread <observed-id>
```

静默不证明hook已配置、受信或运行。有效结果不因阶段结束重查；输入变化及项目必需检查仍需处理。hook缺失、关闭或未受信时沿同一人工方法，不建立第二套校验政策。

## 运行与交付边界

解析实际Python及Skill绝对路径；以上只是未注册入口，不是安装指令。适配器仅用标准库，禁止本地导入字节缓存、不启动子进程、不读取transcript_path；读取及上下文有界，无关调用不读取工作流文件，不建立持久缓存或第二状态库。

后续获准启用时，仅注册上述事件，使用短显式超时及正数上下文上限，在真实宿主核实加载、根身份、路径覆盖、中间态及失败反馈。不启用Stop续跑，不自动批准工具。宿主信任及工具覆盖限制保持；见[官方文档](https://learn.chatgpt.com/docs/hooks)。

源码静态检查不证明事件执行、模型行为或token／耗时收益。完整路径含hook输出的比较须另获评测授权；等价行为确立前保留人工路径，不删去政策或语义保护。
