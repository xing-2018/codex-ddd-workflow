# Presentation, report, and export guidance

## Fit the figure to its destination

For a slide, reserve room for the title and margins before sizing the diagram. Use a single reading path and remove explanatory prose from nodes into a caption or speaker notes. Start with labels equivalent to at least 18 pt at final slide size, then inspect for viewing distance; this is a practical starting point, not a Mermaid font-size guarantee. [Microsoft's presentation guidance](https://support.microsoft.com/en-us/powerpoint/tips-for-creating-and-delivering-an-effective-presentation) recommends readable fonts, concise text, and avoiding small type.

For a report, use the actual column/page width and its typography rules. Keep caption, numbering, units, abbreviations, and source attribution in the document's convention. Inspect a figure at its final printed size; choose portrait/landscape or split detail before shrinking labels into illegibility. Do not force slide typography into a journal column. If grayscale printing matters, check that categories remain distinguishable without hue.

Judge the final placement, not just export pixel dimensions. For a uniformly scaled SVG, an approximate effective label size in points is `fontSizeInSvgUnits * placedWidthInPoints / viewBoxWidth`; use the actual scale if height is limiting. Increasing PNG scale improves raster sharpness, not the physical size of text in a fixed-width figure.

## Typography, color, and accessibility

Prefer the deck/report's established palette; otherwise use a restrained background, dark readable text, and a limited accent palette. Encode decisions/status with words, shapes, or line styles as well as color. Verify contrast on the actual background, including dark-slide or print use. Avoid decorative gradients, icons, and effects that compete with arrows or imply undocumented semantics.

Choose a font installed in the rendering environment with coverage for the output language. For Chinese, use an available CJK font with a sensible fallback; naming an unavailable font does not embed it in SVG. Inspect missing glyphs and text wrapping after export and insertion.

For supported types, add concise `accTitle` and `accDescr` to describe the meaning. These populate SVG accessibility metadata; they do not replace a visible caption or guarantee accessibility after conversion. Add figure alt text in the destination document/deck when inserting the asset. See [Mermaid accessibility](https://mermaid.js.org/config/accessibility.html).

For custom `themeVariables`, use `theme: base` and hex colors. Mermaid versions and hosts differ in themes, layouts, and configuration support; use the actual renderer's schema and set relevant appearance options explicitly when consistency matters. Prefer per-diagram frontmatter or a local CLI configuration to changing site-wide settings. See [theming](https://mermaid.js.org/config/theming.html) and [configuration](https://mermaid.js.org/config/configuration.html).

## Render and export

Reuse an available project renderer or installed [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli). Inspect `mmdc --version` and `mmdc --help` before choosing flags. Do not auto-install a global package, upgrade locked dependencies, or upload document content to an online editor merely to make a preview. If no renderer exists, identify the missing dependency and continue with source/static checks within the task's permissions.

Export from raw `.mmd` source without Markdown fences. Illustrative commands, after resolving authorized input/output paths and confirming local flag support:

```text
mmdc -i diagram.mmd -o diagram.svg -c mermaid-config.json -b white
mmdc -i diagram.mmd -o diagram.png -c mermaid-config.json -b white -w 1600 -s 2
mmdc -i diagram.mmd -o diagram.pdf -c mermaid-config.json -f
```

The CLI viewport width is not a guarantee of exact output bounds. `-s` changes raster scale; `-f` fits a PDF page to the chart. Verify produced dimensions and margins. A diagram PDF is not the requested complete report.

Choose SVG when the consumer supports it reliably, PNG when image compatibility is the priority, and PDF when requested for a vector page or publishing workflow. Retain editable Mermaid source for each exported figure. SVG is not a promise of editable native PowerPoint shapes; if those are required, reconcile the delivery method explicitly.

SVG consumers may handle HTML `foreignObject` labels differently. When labels disappear or portability matters, try the renderer-supported `htmlLabels: false` configuration and simple text labels, then re-render and check the consumer. Do not disable security controls to fix typography. Explicitly use the intended solid background unless transparency is requested and has been checked against the destination.

## Acceptance at the final size

When rendering and artifact inspection are permitted, inspect the rendered asset and, if insertion is requested, its exported slide/report page. Check:

- All labels/glyphs are present, unclipped, and readable at final size.
- Arrows terminate at the intended nodes; edge labels and crossings are unambiguous.
- Branches, loops, groups, and legends preserve the source's meaning.
- Background, fonts, margins, captions, and alternative text work in the destination.

Repair the source or settings and regenerate; do not hand-edit the generated SVG into a second source of truth. Record renderer/version and non-default settings with delivery evidence, not as a permanently pinned version in this Skill. If only local rendering was checked, distinguish that from Office/PDF insertion validation. Never claim unseen exports or destination layouts passed.
