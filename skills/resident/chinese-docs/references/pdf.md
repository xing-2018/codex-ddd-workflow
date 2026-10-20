# PDF交付

## 适用合同

承接[交付路由](routing.md#交付路由)确定的文档类型与模板合同。直接读取本文件且尚未确定类型时，先按该路由选择；PDF扩展名本身不决定报告版式。

## 共同交付要求

生成和渲染前执行[交付与完成](../SKILL.md#deliver-and-complete)的位置检查：正式PDF位置与临时构建、检查证据位置分别确定。通用转换器、用户模板工具和下述报告脚本均须检查其伴随输出，不能仅凭最终PDF路径推定临时产物位置。

内容变化时使用已审阅的Markdown源；仅格式转换保持已有内容，不新增摘要、结论或改变数据、命令和验收口径。保留文档用途所需的结构与细节。

通用PDF按文档用途和已有结构选择可用生成方式。封面、目录、章节编号及章间分页仅在文档合同需要时采用。用户或项目模板先核对页面、字体、标题编号、题注、页眉页脚和分页要求，再选择转换链。缺少合适工具、字体或渲染能力时报告具体限制，不因报告生成器可用而改变文档类型。

所有类型均须保持中文可读、图片宽高比、公式显示正确、表格和代码不越界，并按下文共同验收检查最终输出。以下正式报告专属流程只在对应路由选中时应用。

## 正式报告专属流程

### 构建

正式中文科技/技术报告无更强模板时默认使用下列命令；脚本与资产路径相对于本Skill目录，输入路径按实际文档位置解析，`<临时工作目录>`替换为按项目规则确定的本次构建目录：

```powershell
python scripts/build_report_pdf.py <report.md> -o <临时工作目录/report.pdf>
```

脚本会在`-o`指定的PDF旁生成同名`.render_check/`目录和`.build.json`摘要；`--no-render-check`也仍会写摘要。因此`-o`须指向临时工作目录，不能直接使用正式文档目录。完成下文验收后，将PDF复制到所需交付位置并核对文件一致，检查图与摘要留在允许的证据位置；不要整目录复制。摘要中的构建输出路径继续指向实际构建位置，在交付记录中另列最终PDF位置。收尾检查实际目录，不以Git忽略代替位置检查，也不因本次修复自动迁移或删除既有资料。

脚本使用 `assets/pandoc-xelatex-report-template.tex`，依赖 Pandoc 和 XeLaTeX。缺少工具、字体或渲染能力时必须明确报告，不能伪造已完成的 PDF 验收。

正式报告 Markdown 可使用 YAML metadata，至少提供 `title` 和 `date`；`version` 未给出时可显示 `V1.0`。`prepared_by`、`checked_by`、`reviewed_by`、`organization` 等字段只在用户明确提供时使用，不为填满封面虚构元数据。

转换时统一规范标题表示：若首个一级标题与YAML `title`完全一致，则把它视为封面文档标题并从正文移除；当其余结构没有其他一级标题时，后续标题整体提升一级，使正文章从一级标题开始。若未提供YAML `title`，但文档以唯一一级标题开头且后续存在二级章节，可将该一级标题转为封面元数据并同样提升章节。已有原生报告式一级章节、与元数据不匹配的真实正文标题或混合层级不得删除或误降级。

### 页面与分页

- A4 页面；封面独占一页。
- 摘要、目录、正文分别从新页开始；新的一级章节从新页开始。
- 一级至三级标题自动编号并进入目录，不混用手写编号与自动编号。
- 正文页码使用阿拉伯数字；目录可按模板使用罗马数字。
- 正文默认不加页眉，只显示页脚页码；用户明确要求时才启用页眉。

### 字体与正文

正文中文优先宋体，标题中文优先黑体，英文/数字优先 Times New Roman；环境缺失时可用思源/Noto CJK 等可读替代字体。不得出现乱码、黑方块或明显缺字。正文保持正式中文报告的段落阅读形态，不用连续空行模拟间距。

### 图表、公式和代码

- 表题在表格上方，图题在图片下方；正式表格必须有表题。
- 默认全文连续编号 `图 1`、`表 1`；只有用户/单位模板明确要求时才使用章节编号。
- 长文本表格优先控制为二至三列；出现逐字换行、严重越界或大面积空白时，应调整源 Markdown 结构而不是只依赖引擎压缩。
- 图片/流程图必须保持宽高比并限制在正文宽度和可用页面高度内，不裁剪；合理的显式尺寸可以保留，但仍须通过页面边界检查。Mermaid/Graphviz/PlantUML 源应先渲染为图片，除非用户明确要求展示源码。
- 公式使用 `$...$` 和 `$$...$$`；数学符号不要用代码样式替代。
- 代码块必须可读且不越界。

### 报告构建摘要

`build_report_pdf.py` may render all pages, but rendering alone is supporting evidence. Keep `visual_inspection_status=pending` and `visually_inspected_page_numbers` empty until actual inspection. Use `complete` only for actual all-page coverage of that final identity; sampled coverage stays `partial` with the true inspected page numbers. Partial visual coverage can satisfy approved sampled acceptance, never an explicit full-page contract or a claim that every page is visually correct. Keep the approved scope in the existing report; do not fabricate summary results.

## 共同验收

Construction success is not acceptance. Render and inspect actual PDF output using [visual inspection](review.md#visual-inspection). Default formal delivery uses structural checks plus risk-based visual sampling; explicit full-page acceptance, unbounded impact or widespread defects still requires all pages. Separate construction, generated images and actual inspected pages; generating all images does not require sending all to the model. Reuse only evidence supported by unchanged content and pagination mappings. The summary records actual coverage as above. Check applicable requirements within the approved scope:

- 中文无乱码/黑方块；
- 现有章节分页正确；合同需要封面、摘要或目录时检查对应页面，不因检查项而新增章节；
- 合同要求的标题编号与目录正确；
- 表格题注、列宽、换行和页面占用合理；
- 图片/流程图不裁剪且文字可读；
- 公式处于数学模式；
- 代码块不越界；
- 页眉/页脚与正文不重叠。

发现问题后在授权范围内修复格式并重新生成，保持仅格式任务的内容边界；不得交付已知存在排版缺陷的PDF。
