---
name: femap-control
description: 在Windows通过COM打开、导入和验证Siemens Simcenter Femap模型，调整可见窗口尺寸，或核验Nastran结果流程。用于本机Femap开发验证，不用于服务端AI运行时或Electron产品能力。
---

# Femap控制

模型操作优先使用Femap COM API，窗口尺寸用原生窗口矩形读数核实。入口脚本为[open_femap_model.py](scripts/open_femap_model.py)；执行前核实本机Femap安装及目标模型，并显式传入模型路径。

## 执行前确认

- 从任务取得模型绝对路径、操作范围和所需验收：导入、求解、结果挂接或可见GUI。维护本Skill本身不授权启动Femap；复用会话中已有的目标应用控制授权。
- 检查模型及`femap.exe`存在，Python可导入`pythoncom`和`win32com.client`。缺少pywin32时，按目标项目依赖与运行目录规则使用隔离环境，不默认修改全局Python。
- 脚本会连接已有Femap会话、默认调用`feFileNew`，再导入模型并把窗口置前。先确认现有会话无未保存工作且操作已授权；有多个会话时先明确目标，脚本不能可靠选择指定会话。`--no-new-model`会向当前模型导入，只在明确要求合并时使用。
- 脚本使用`feFileReadNastran`导入BDF/DAT；`.modfem`原生模型应使用目标Femap版本的原生打开API，不能传入此Nastran导入入口。未知API签名查该安装版本的API帮助，不猜测。

## 打开模型并核验窗口

从Skill实际安装位置解析脚本，显式传入模型和程序路径。项目安装示例（替换模型路径和Python解释器）：

```powershell
python '.agents\skills\femap-control\scripts\open_femap_model.py' `
  --model 'D:\models\verification.bdf' `
  --femap-exe 'C:\Program Files\Siemens\Femap 2512\femap.exe' `
  --width 1440 --height 1024
```

检查JSON的`model`、`femap_exe`、`window_pid`及窗口标题是否对应目标；核对`new_model_rc`（如执行）、`import_bdf_rc`和请求的`rect.width`/`rect.height`。Femap成功返回码通常为`-1`，仍以所用API定义为准；进程退出码0不代表导入成功。活动载荷/约束集按输入模型预期核对，不要求所有模型都有非零集合。

窗口矩形只能证明窗口存在和尺寸，不能证明模型渲染正确。验收涉及画面时，用已授权且可用的截图工具查看模型；截图不可用就报告视觉项未验证。用户要求最终可见时保持Femap打开。

## 求解与结果验证

仅在用户要求完整流程且目标项目提供工作流时，读取项目的验证说明与脚本，核实输入、求解器、输出目录、成功返回码和基线后执行。不要因打开模型成功就声称完成求解或结果验证。

使用目标项目自己的工作流、输出位置和期望值；旧项目的fixture或基线不构成当前项目的验收依据。

## 故障与证据

- `ModuleNotFoundError: No module named 'pythoncom'`：在项目允许的隔离Python环境补齐pywin32后再执行。
- `feFileNew`可能表现为整数属性或方法；现有脚本通过`call_or_value`兼容，不能假定均可调用。
- `GetActiveObject('femap.model')`在启动后可能尚未注册。脚本默认等待最多60秒，再尝试`Dispatch`；新自动化会话可能在COM释放后退出。需要可见GUI时先显式启动Femap并连接，核实最终窗口。
- 窗口工具失效时可继续已授权的COM操作；保留失败信息，不能用矩形读数替代图像证据，也不盲发快捷键。
- 交付记录模型、软件版本、实际命令、API回执、窗口与结果证据路径，以及未完成项。求解结果须核实本次输出和数据内容，不能仅凭文件存在或旧基线计数判成功。
