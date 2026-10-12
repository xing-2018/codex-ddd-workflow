#!/usr/bin/env python3
"""Build a Chinese technical report PDF from Markdown using the packaged Pandoc/XeLaTeX template."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def render_page_indices(page_count: int, render_limit: int | None) -> list[int]:
    """Return all formal-delivery pages unless an explicit preview limit is set."""
    if render_limit is None:
        return list(range(page_count))
    return list(range(min(page_count, render_limit)))


def page_count_from_pdfinfo(pdf: Path) -> int:
    proc = run(["pdfinfo", str(pdf)])
    if proc.returncode != 0:
        raise RuntimeError(f"pdfinfo failed: {proc.stdout[-1000:]}")
    match = re.search(r"^Pages:\s+(\d+)\s*$", proc.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError("pdfinfo did not report a page count")
    return int(match.group(1))


def render_with_poppler(
    pdf: Path, render_dir: Path, pages_to_render: list[int]
) -> None:
    for index in pages_to_render:
        prefix = render_dir / f"page-{index + 1:02d}"
        proc = run(
            [
                "pdftoppm",
                "-png",
                "-r",
                "108",
                "-f",
                str(index + 1),
                "-l",
                str(index + 1),
                "-singlefile",
                str(pdf),
                str(prefix),
            ]
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"pdftoppm failed for page {index + 1}: {proc.stdout[-1000:]}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Chinese technical report PDF from Markdown.")
    parser.add_argument("markdown", type=Path, help="Input Markdown file")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output PDF file")
    parser.add_argument("--toc-depth", default="3", help="TOC depth, default 3")
    parser.add_argument("--no-render-check", action="store_true", help="Skip PyMuPDF render check")
    parser.add_argument(
        "--render-limit",
        type=int,
        help="Preview only: render at most this many leading pages; never use as formal-delivery acceptance.",
    )
    args = parser.parse_args()
    if args.render_limit is not None and args.render_limit <= 0:
        parser.error("--render-limit must be positive")
    if args.no_render_check and args.render_limit is not None:
        parser.error("--render-limit cannot be combined with --no-render-check")

    skill_root = Path(__file__).resolve().parents[1]
    template = skill_root / "assets" / "pandoc-xelatex-report-template.tex"
    heading_filter = skill_root / "scripts" / "normalize_report_headings.lua"
    md = args.markdown.resolve()
    out_pdf = args.output.resolve()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    summary = {
        "markdown": str(md),
        "output_pdf": str(out_pdf),
        "template": str(template),
        "heading_filter": str(heading_filter),
        "build_status": "pending",
        "render_status": "pending",
        "visual_inspection_status": "pending",
        "visually_inspected_page_numbers": [],
        "checks": [],
        "errors": [],
    }

    for tool in ["pandoc", "xelatex"]:
        path = shutil.which(tool)
        summary["checks"].append({"tool": tool, "path": path})
        if path is None:
            summary["errors"].append(f"Missing required tool: {tool}")

    if not md.exists():
        summary["errors"].append(f"Markdown file not found: {md}")
    if not template.exists():
        summary["errors"].append(f"Template file not found: {template}")
    if not heading_filter.exists():
        summary["errors"].append(f"Heading filter not found: {heading_filter}")

    if summary["errors"]:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 2

    cmd = [
        "pandoc", str(md),
        "--from", "markdown+tex_math_dollars+pipe_tables+fenced_code_blocks+yaml_metadata_block+implicit_figures",
        "--output", str(out_pdf),
        "--resource-path", str(md.parent),
        "--pdf-engine=xelatex",
        "--pdf-engine-opt=-interaction=nonstopmode",
        "--pdf-engine-opt=-halt-on-error",
        "--template", str(template),
        "--lua-filter", str(heading_filter),
        "--toc", "--toc-depth", str(args.toc_depth),
        "--number-sections", "--listings",
    ]
    proc = run(cmd, cwd=md.parent)
    summary["pandoc_returncode"] = proc.returncode
    summary["pandoc_output_tail"] = proc.stdout[-4000:]

    if proc.returncode != 0 or not out_pdf.exists():
        summary["build_status"] = "failed"
        summary["errors"].append("Pandoc/XeLaTeX build failed")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 3

    summary["pdf_size_bytes"] = out_pdf.stat().st_size
    summary["build_status"] = "completed"

    if args.no_render_check:
        summary["render_status"] = "skipped"
        summary["rendered_page_numbers"] = []
    else:
        try:
            render_dir = out_pdf.with_suffix(".render_check")
            render_dir.mkdir(parents=True, exist_ok=True)
            for stale_page in render_dir.glob("page-*.png"):
                stale_page.unlink()
            try:
                import fitz  # type: ignore
            except ImportError:
                if shutil.which("pdfinfo") is None or shutil.which("pdftoppm") is None:
                    raise RuntimeError(
                        "render check requires PyMuPDF or both pdfinfo and pdftoppm"
                    )
                page_count = page_count_from_pdfinfo(out_pdf)
                pages_to_render = render_page_indices(page_count, args.render_limit)
                render_with_poppler(out_pdf, render_dir, pages_to_render)
                summary["render_engine"] = "poppler"
            else:
                doc = fitz.open(out_pdf)
                page_count = doc.page_count
                pages_to_render = render_page_indices(page_count, args.render_limit)
                for i in pages_to_render:
                    page = doc.load_page(i)
                    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
                    png = render_dir / f"page-{i+1:02d}.png"
                    pix.save(png)
                doc.close()
                summary["render_engine"] = "pymupdf"
            summary["page_count"] = page_count
            summary["render_check_dir"] = str(render_dir)
            summary["rendered_pages"] = len(pages_to_render)
            summary["rendered_page_numbers"] = [index + 1 for index in pages_to_render]
            summary["render_status"] = (
                "complete" if len(pages_to_render) == page_count else "preview"
            )
        except Exception as exc:  # pragma: no cover
            summary["render_status"] = "failed"
            summary["errors"].append(f"Render check failed: {exc}")

    summary_path = out_pdf.with_suffix(".build.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not summary["errors"] else 4


if __name__ == "__main__":
    raise SystemExit(main())
