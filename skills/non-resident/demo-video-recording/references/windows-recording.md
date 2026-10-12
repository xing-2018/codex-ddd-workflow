# Windows录制工作流

本参考用于Windows上的本地Web、Electron和桌面应用录制。先遵循目标项目的运行入口与权限规则，再选择下列工具和参数。

## 工具盘点

PowerShell中优先使用`Get-Command`检查命令行工具，并从卸载项确认GUI软件。不要为盘点启动录制器或读取可能包含推流密钥的用户配置。

```powershell
Get-Command ffmpeg, ffprobe, node, npm -ErrorAction SilentlyContinue

Get-ItemProperty `
  'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*', `
  'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*', `
  'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*' `
  -ErrorAction SilentlyContinue |
  Where-Object DisplayName -Match '^OBS Studio$|Clipchamp|VLC|ScreenToGif|ShareX'
```

FFmpeg能力用静态列表确认，不开始采集：

```powershell
ffmpeg -hide_banner -devices
ffmpeg -hide_banner -encoders
```

关注`gdigrab`、`dshow`、`h264_nvenc`和`libx264`是否存在。硬件编码器出现在列表中只证明构建支持；正式录制前仍需短片验证驱动和负载。

## OBS窗口录制

创建任务专属场景并添加“窗口采集”，只选择目标应用窗口。除非演示确实跨越多个程序、系统对话框或文件选择器，否则不使用“显示器采集”。关闭无关摄像头、桌面音频和通知来源；需要旁白时单独检查麦克风电平。

通用起点为：

- 画布与输出分辨率`1920×1080`；
- `30 fps`；
- 优先使用可用的硬件H.264编码器，否则使用x264；
- 原始录制保存为`MKV`，交付前重新封装为`MP4`；
- 需要音频时交付使用AAC。

三维渲染、视频播放或高刷新动画应先录制约30秒样片。若目标应用明显卡顿，降低录制输出负载或使用更合适的编码器；不要修改产品渲染逻辑来掩盖录制环境问题。

## Web与Electron操作回放

项目已有Playwright时优先复用锁定版本和现有测试入口。Electron应用如果通过项目入口开放任务专属Chrome DevTools Protocol（CDP）端口，可连接真实renderer执行DOM操作；不要把开发调试端口写入正式配置。

回放脚本应做到：

- 只连接本任务启动或用户明确指定的目标；
- 使用角色、标签、测试标识或稳定DOM关系定位元素；
- 为启动、导航、加载和结果设置有界等待；
- 失败时停止后续步骤并输出脱敏错误；
- 不激活、置前、移动或缩放窗口，不使用系统级键鼠注入；
- 按项目入口停止本任务启动的应用，不关闭既有会话。

Playwright的页面视频适合纯浏览器内容，但可能不包含Electron边框、系统对话框或其他应用。交付需要完整桌面上下文时仍使用窗口或显示器录制。

## 重新封装与压缩

保留原始录像，通过OBS“重新封装录像”或FFmpeg把`MKV`无损转换为`MP4`：

```powershell
ffmpeg -hide_banner -i '<input>.mkv' -c copy '<output>.mp4'
```

需要压缩且机器已验证NVENC可用时，可生成独立汇报版：

```powershell
ffmpeg -hide_banner -i '<input>.mp4' `
  -c:v h264_nvenc -preset p6 -cq 21 `
  -c:a aac -b:a 192k `
  '<output>-presentation.mp4'
```

没有硬件编码时使用目标机器FFmpeg实际支持的软件H.264编码器。不要覆盖唯一原始文件，命令中的占位路径必须替换为任务路径。

## 技术检查与人工观看

使用FFprobe输出必要参数：

```powershell
ffprobe -v error `
  -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate `
  -of json `
  '<video>.mp4'
```

随后在交付播放器中从头到尾观看。确认文件可以打开、拖动和播放至结尾，画面连贯、文字可读、音画同步、关键结果停留充分，并检查画面、声音、字幕及文件名是否泄露敏感信息。PPT中嵌入视频时仍保留独立MP4副本，并在目标汇报电脑的离线状态下试播。
