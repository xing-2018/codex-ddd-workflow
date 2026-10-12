#!/usr/bin/env python3
"""Audit formal Chinese DOCX reports against an authoritative DOTX template."""

from __future__ import annotations

import argparse
import colorsys
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"w": W, "r": R}
Q = lambda name: f"{{{W}}}{name}"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
REL_Q = lambda name: f"{{{REL_NS}}}{name}"

AUTHORITATIVE_PARTS = (
    "word/styles.xml",
    "word/numbering.xml",
    "word/theme/theme1.xml",
    "word/fontTable.xml",
)
QUICK_STYLES = {
    "A1": "A正文",
    "Af1": "A图表",
    "1": "heading 1",
    "2": "heading 2",
    "3": "heading 3",
    "4": "heading 4",
    "af3": "caption",
}
HEADING_TEXT = {"1": "%1", "2": "%1.%2", "3": "%1.%2.%3", "4": "%1.%2.%3.%4"}
FORBIDDEN_HEADING_STYLES = {"A10", "A20", "A30", "41"}
MANUAL_NUMBER = re.compile(r"^\s*\d+(?:\.\d+){0,3}\.?\s+")
DATE_TEXT = re.compile(r"^\d{4}年\d{1,2}月(?:\d{1,2}日)?$")
CAPTION_FORMAT = re.compile(r"^[图表]\s*\d+(?:[.-]\d+)* {2}\S")
BLACK_VALUES = {"000000", "auto"}
PAGE_NUMBER_SIZE = "21"
REQUIRED_TABLE_BORDERS = ("top", "bottom", "left", "right", "insideH", "insideV")
ON_OFF_PROPERTIES = {"b", "bCs", "i", "iCs", "qFormat", "keepNext", "keepLines", "snapToGrid", "widowControl", "pageBreakBefore", "caps", "smallCaps"}
FORBIDDEN_FIELD_CODE = re.compile(
    r"\b(?:INCLUDETEXT|INCLUDEPICTURE|LINK|DDEAUTO|DDE|DATABASE)\b",
    re.IGNORECASE,
)
LOCAL_PATH = re.compile(
    r'(?:[A-Za-z]:\\[^\s`"<>|]+|/(?:home|Users|mnt)/[^\s`"<>]+|(?:\.\.[/\\]){2,}[^\s`"<>]*)'
)


def read_part(path: Path, name: str) -> bytes:
    with zipfile.ZipFile(path) as package:
        return package.read(name)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def semantic_xml(data: bytes) -> tuple:
    """Compare expanded XML names and values, excluding only editing identities."""
    def editing_marker(name: str) -> bool:
        return (
            name.startswith(f"{{{W}}}rsid")
            or name == "{http://schemas.openxmlformats.org/markup-compatibility/2006}Ignorable"
            or name in {
                "{http://schemas.microsoft.com/office/word/2010/wordml}paraId",
                "{http://schemas.microsoft.com/office/word/2010/wordml}textId",
                "{http://schemas.microsoft.com/office/word/2016/wordml/cid}durableId",
            }
        )

    def signature(node: ET.Element) -> tuple:
        attributes = {key: value for key, value in node.attrib.items() if not editing_marker(key)}
        if node.tag in {Q(name) for name in ON_OFF_PROPERTIES}:
            attributes[Q("val")] = "true" if is_true(node) else "false"
        return (
            node.tag,
            tuple(sorted(attributes.items())),
            (node.text or "").strip(),
            tuple(signature(child) for child in node if not editing_marker(child.tag)),
        )

    return signature(ET.fromstring(data))


def attr(node: ET.Element | None, name: str) -> str | None:
    return None if node is None else node.get(Q(name))


def style_map(styles_xml: bytes) -> dict[str, ET.Element]:
    root = ET.fromstring(styles_xml)
    return {style.get(Q("styleId"), ""): style for style in root.findall("w:style", NS)}


def merge_properties(values: dict[str, str], node: ET.Element | None) -> None:
    if node is None:
        return

    def collect(child: ET.Element, path: str) -> None:
        for key, value in child.attrib.items():
            if child.tag in {Q(name) for name in ON_OFF_PROPERTIES} and key == Q("val"):
                value = "true" if is_true(child) else "false"
            values[f"{path}/{key.rsplit('}', 1)[-1]}"] = value
        if not child.attrib and not len(child):
            values[f"{path}/val"] = "true"
        for item in child:
            collect(item, f"{path}/{item.tag.rsplit('}', 1)[-1]}")

    for child in node:
        name = child.tag.rsplit("}", 1)[-1]
        if name == "tabs":
            values["tabs/definition"] = repr(semantic_xml(ET.tostring(child)))
            continue
        if name == "color":
            for key in list(values):
                if key.startswith("color/"):
                    del values[key]
        if name == "rFonts":
            for face, theme in (("ascii", "asciiTheme"), ("hAnsi", "hAnsiTheme"), ("eastAsia", "eastAsiaTheme"), ("cs", "cstheme")):
                if attr(child, face) is not None:
                    values.pop(f"rFonts/{theme}", None)
                if attr(child, theme) is not None:
                    values.pop(f"rFonts/{face}", None)
        collect(child, name)


def merge_resolved(values: dict[str, str], layer: dict[str, str]) -> None:
    if any(key.startswith("color/") for key in layer):
        for key in list(values):
            if key.startswith("color/"):
                del values[key]
    for face, theme in (("ascii", "asciiTheme"), ("hAnsi", "hAnsiTheme"), ("eastAsia", "eastAsiaTheme"), ("cs", "cstheme")):
        if f"rFonts/{face}" in layer:
            values.pop(f"rFonts/{theme}", None)
        if f"rFonts/{theme}" in layer:
            values.pop(f"rFonts/{face}", None)
    values.update(layer)


class Formatting:
    """Resolve only the inheritance needed by this report's format checks."""
    def __init__(self, styles_xml: bytes, numbering_xml: bytes, theme_xml: bytes):
        self.styles = style_map(styles_xml)
        self.root = ET.fromstring(styles_xml)
        self.numbering = ET.fromstring(numbering_xml)
        self.theme = ET.fromstring(theme_xml)
        self.default_style = next(
            (key for key, style in self.styles.items() if attr(style, "type") == "paragraph" and is_true_attribute(style, "default")),
            "",
        )

    def style_properties(self, style_id: str, kind: str) -> dict[str, str]:
        chain: list[ET.Element] = []
        seen: set[str] = set()
        while style_id:
            if style_id in seen or style_id not in self.styles:
                raise ValueError(f"missing or cyclic style inheritance: {style_id}")
            seen.add(style_id)
            style = self.styles[style_id]
            chain.append(style)
            style_id = attr(style.find("w:basedOn", NS), "val") or ""
        values: dict[str, str] = {}
        for style in reversed(chain):
            merge_properties(values, style.find(f"w:{kind}", NS))
        return values

    def paragraph(self, paragraph: ET.Element, direct: bool = True) -> dict[str, str]:
        values: dict[str, str] = {}
        merge_properties(values, self.root.find("w:docDefaults/w:pPrDefault/w:pPr", NS))
        merge_resolved(values, self.style_properties(paragraph_style(paragraph) or self.default_style, "pPr"))
        numbering_values = dict(values)
        merge_properties(numbering_values, paragraph.find("w:pPr", NS))
        num_id = numbering_values.get("numPr/numId/val", "0")
        level = numbering_values.get("numPr/ilvl/val", "0")
        if num_id != "0":
            num = next((node for node in self.numbering.findall("w:num", NS) if attr(node, "numId") == num_id), None)
            abstract_id = attr(num.find("w:abstractNumId", NS), "val") if num is not None else None
            abstract = next((node for node in self.numbering.findall("w:abstractNum", NS) if attr(node, "abstractNumId") == abstract_id), None)
            lvl = next((node for node in abstract.findall("w:lvl", NS) if attr(node, "ilvl") == level), None) if abstract is not None else None
            if lvl is None:
                raise ValueError(f"missing numbering level: numId={num_id}, ilvl={level}")
            merge_properties(values, lvl.find("w:pPr", NS))
        if direct:
            merge_properties(values, paragraph.find("w:pPr", NS))
        return values

    def run(self, paragraph: ET.Element, run: ET.Element, direct: bool = True) -> dict[str, str]:
        values: dict[str, str] = {}
        merge_properties(values, self.root.find("w:docDefaults/w:rPrDefault/w:rPr", NS))
        merge_resolved(values, self.style_properties(paragraph_style(paragraph) or self.default_style, "rPr"))
        char_style = attr(run.find("w:rPr/w:rStyle", NS), "val")
        if char_style:
            char_values = self.style_properties(char_style, "rPr")
            merge_resolved(values, char_values)
        if direct:
            merge_properties(values, run.find("w:rPr", NS))
        return values

    def font(self, values: dict[str, str], face: str) -> str | None:
        theme_key = "cstheme" if face == "cs" else f"{face}Theme"
        theme_name = values.get(f"rFonts/{theme_key}")
        if not theme_name:
            return values.get(f"rFonts/{face}")
        drawing = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
        family = "majorFont" if theme_name.startswith("major") else "minorFont" if theme_name.startswith("minor") else ""
        if not family:
            return None
        scheme = self.theme.find(f".//{drawing}fontScheme/{drawing}{family}")
        if scheme is None:
            return None
        name = "ea" if face == "eastAsia" else "cs" if face == "cs" else "latin"
        font = scheme.find(f"{drawing}{name}")
        value = font.get("typeface") if font is not None else None
        if not value and face == "eastAsia":
            font = next((node for node in scheme.findall(f"{drawing}font") if node.get("script") == "Hans"), None)
            value = font.get("typeface") if font is not None else None
        if not value and face == "cs":
            language = values.get("lang/bidi", "").split("-")[0].lower()
            script = {"ar": "Arab", "he": "Hebr"}.get(language)
            font = next((node for node in scheme.findall(f"{drawing}font") if node.get("script") == script), None) if script else None
            value = font.get("typeface") if font is not None else None
        return value or None

    def color(self, values: dict[str, str]) -> str:
        value = values.get("color/val", "auto").lower()
        theme_color = values.get("color/themeColor")
        if theme_color:
            drawing = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
            name = {"text1": "dk1", "text2": "dk2", "background1": "lt1", "background2": "lt2"}.get(theme_color, theme_color)
            slot = self.theme.find(f".//{drawing}clrScheme/{drawing}{name}")
            if slot is None or not len(slot):
                return "unresolved-theme-color"
            value = (slot[0].get("val") if slot[0].tag == f"{drawing}srgbClr" else slot[0].get("lastClr") or "").lower()
        if value != "auto" and re.fullmatch(r"[0-9a-f]{6}", value):
            amount = values.get("color/themeTint") or values.get("color/themeShade")
            if amount:
                # Word applies tint before shade when both exist; tint 00 is white.
                # https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oi29500/8229a077-7fc8-4fba-96cc-c77b6a4fc768
                rgb = [int(value[index:index + 2], 16) / 255 for index in (0, 2, 4)]
                hue, luminance, saturation = colorsys.rgb_to_hls(*rgb)
                factor = int(amount, 16) / 255
                luminance = luminance * factor + (1 - factor if values.get("color/themeTint") else 0)
                rgb = colorsys.hls_to_rgb(hue, luminance, saturation)
                value = "".join(f"{round(channel * 255):02x}" for channel in rgb)
        return value


def paragraph_differences(expected: dict[str, str], actual: dict[str, str], allowed: set[str]) -> list[str]:
    monitored = {"spacing", "ind", "jc", "keepNext", "keepLines", "pageBreakBefore", "snapToGrid", "widowControl", "tabs", "outlineLvl"}
    return [
        key for key in expected.keys() | actual.keys()
        if key not in allowed and key.split("/")[0] in monitored and expected.get(key) != actual.get(key)
    ]


def validate_template(template: Path) -> tuple[list[str], str]:
    failures: list[str] = []
    styles = style_map(read_part(template, "word/styles.xml"))
    for style_id, expected_name in QUICK_STYLES.items():
        style = styles.get(style_id)
        if style is None:
            failures.append(f"template missing style {style_id} ({expected_name})")
            continue
        name = attr(style.find("w:name", NS), "val")
        if name != expected_name:
            failures.append(f"template style {style_id} name is {name!r}, expected {expected_name!r}")
        if style.find("w:qFormat", NS) is None:
            failures.append(f"template style {style_id} is not a quick style")

    default_table_styles = [
        style
        for style in styles.values()
        if attr(style, "type") == "table" and is_true_attribute(style, "default")
    ]
    if len(default_table_styles) != 1:
        failures.append(f"template must define exactly one default table style; found {len(default_table_styles)}")
    elif attr(default_table_styles[0], "styleId") != "a3":
        failures.append(
            f"template default table style is {attr(default_table_styles[0], 'styleId')!r}, expected 'a3'"
        )

    numbering = ET.fromstring(read_part(template, "word/numbering.xml"))
    num = next((n for n in numbering.findall("w:num", NS) if attr(n, "numId") == "1"), None)
    abstract_id = attr(num.find("w:abstractNumId", NS), "val") if num is not None else None
    if abstract_id is None:
        failures.append("template numId=1 is missing")
        return failures, ""
    abstract = next(
        (n for n in numbering.findall("w:abstractNum", NS) if attr(n, "abstractNumId") == abstract_id),
        None,
    )
    if abstract is None:
        failures.append(f"template abstractNum {abstract_id} is missing")
        return failures, abstract_id
    for level, (style_id, expected_text) in enumerate(HEADING_TEXT.items()):
        lvl = next((n for n in abstract.findall("w:lvl", NS) if attr(n, "ilvl") == str(level)), None)
        if lvl is None:
            failures.append(f"template heading numbering level {level} is missing")
            continue
        if attr(lvl.find("w:pStyle", NS), "val") != style_id:
            failures.append(f"template numbering level {level} is not linked to style {style_id}")
        if attr(lvl.find("w:lvlText", NS), "val") != expected_text:
            failures.append(f"template numbering level {level} text is not {expected_text}")
    return failures, abstract_id


def section_signature(document_xml: bytes) -> list[dict[str, object]]:
    root = ET.fromstring(document_xml)
    result: list[dict[str, object]] = []
    for section in root.findall(".//w:sectPr", NS):
        size = section.find("w:pgSz", NS)
        margin = section.find("w:pgMar", NS)
        page_num = section.find("w:pgNumType", NS)
        result.append(
            {
                "size": {key: attr(size, key) for key in ("w", "h", "orient")},
                "margin": {
                    key: attr(margin, key)
                    for key in ("top", "right", "bottom", "left", "header", "footer", "gutter")
                },
                "page_num": {key: attr(page_num, key) for key in ("fmt", "start")},
                "different_first_page": section.find("w:titlePg", NS) is not None,
                "header_types": [attr(node, "type") for node in section.findall("w:headerReference", NS)],
                "footer_types": [attr(node, "type") for node in section.findall("w:footerReference", NS)],
                "columns": dict(section.find("w:cols", NS).attrib) if section.find("w:cols", NS) is not None else {},
                "document_grid": dict(section.find("w:docGrid", NS).attrib) if section.find("w:docGrid", NS) is not None else {},
                "section_type": attr(section.find("w:type", NS), "val"),
            }
        )
    return result


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(
        node.text or "" if node.tag == Q("t") else "\t" if node.tag == Q("tab") else "\n"
        for node in paragraph.iter()
        if node.tag in {Q("t"), Q("tab"), Q("br"), Q("cr")}
    )


def paragraph_style(paragraph: ET.Element) -> str:
    return attr(paragraph.find("w:pPr/w:pStyle", NS), "val") or ""


def body_paragraphs(root: ET.Element) -> list[ET.Element]:
    body = root.find(".//w:body", NS)
    return [] if body is None else body.findall(".//w:p", NS)


def document_body_text(root: ET.Element) -> str:
    return "\n".join(paragraph_text(paragraph) for paragraph in body_paragraphs(root))


def body_sections(root: ET.Element) -> list[list[ET.Element]]:
    body = root.find(".//w:body", NS)
    if body is None:
        return []
    sections: list[list[ET.Element]] = [[]]
    for child in list(body):
        sections[-1].append(child)
        if child.find("w:pPr/w:sectPr", NS) is not None:
            sections.append([])
    return sections


def text_runs(paragraph: ET.Element) -> list[ET.Element]:
    runs: list[ET.Element] = []

    def walk(node: ET.Element) -> None:
        if node is not paragraph and node.tag == Q("p"):
            return
        if node.tag == Q("r") and any(item.text for item in node.findall("w:t", NS)):
            runs.append(node)
        for child in node:
            walk(child)

    walk(paragraph)
    return runs


def direct_color_failures(root: ET.Element, part: str) -> list[str]:
    failures: list[str] = []
    for color in root.findall(".//w:color", NS):
        value = (attr(color, "val") or "").lower()
        theme_attrs = [key for key in ("themeColor", "themeTint", "themeShade") if attr(color, key)]
        if value not in BLACK_VALUES or theme_attrs:
            failures.append(f"{part}:{value or '<missing>'}")
    return failures


def default_table_style_id(styles_xml: bytes) -> str:
    styles = ET.fromstring(styles_xml)
    for style in styles.findall("w:style", NS):
        if attr(style, "type") == "table" and is_true_attribute(style, "default"):
            return attr(style, "styleId") or ""
    return ""


def is_true_attribute(node: ET.Element, name: str) -> bool:
    value = attr(node, name)
    return value is not None and value.lower() in {"1", "true", "on", "yes"}


class FieldRecord:
    def __init__(self, code: str = "", simple: bool = False):
        self.code = code
        self.simple = simple
        self.in_result = simple
        self.paragraphs: list[ET.Element] = []


def parse_fields(root: ET.Element) -> tuple[list[FieldRecord], list[str], list[str]]:
    """Keep complex instruction fragments and cached result paragraphs in field scope."""
    records: list[FieldRecord] = []
    stack: list[FieldRecord] = []
    orphan_instructions: list[str] = []
    errors: list[str] = []

    def walk(node: ET.Element, paragraph: ET.Element | None = None) -> None:
        if node.tag == Q("p"):
            paragraph = node
        if node.tag == Q("fldSimple"):
            record = FieldRecord(attr(node, "instr") or "", simple=True)
            records.append(record)
            stack.append(record)
            for child in node:
                walk(child, paragraph)
            if stack and stack[-1] is record:
                stack.pop()
            else:
                errors.append("unclosed complex field inside simple field")
            return
        if node.tag == Q("fldChar"):
            kind = attr(node, "fldCharType")
            if kind == "begin":
                record = FieldRecord()
                records.append(record)
                stack.append(record)
            elif kind in {"separate", "end"}:
                if not stack or stack[-1].simple:
                    errors.append(f"field {kind} without matching begin")
                elif kind == "separate":
                    stack[-1].in_result = True
                else:
                    stack.pop()
            return
        if node.tag == Q("instrText"):
            if stack and not stack[-1].in_result:
                stack[-1].code += node.text or ""
            elif node.text:
                # Retain standalone instructions for conservative external-field scanning.
                orphan_instructions.append(node.text)
        if node.tag == Q("t") and node.text and paragraph is not None:
            for record in stack:
                if record.in_result and paragraph not in record.paragraphs:
                    record.paragraphs.append(paragraph)
        for child in node:
            walk(child, paragraph)

    walk(root)
    if stack:
        errors.append("unclosed field")
    return records, orphan_instructions, errors


def field_codes(root: ET.Element) -> list[str]:
    records, orphan_instructions, _ = parse_fields(root)
    codes = [record.code.strip() for record in records if record.code.strip()]
    if orphan_instructions:
        codes.append("".join(orphan_instructions).strip())
    return codes


def page_number_size_failures(root: ET.Element, part: str) -> tuple[int, list[str]]:
    paragraph_count = 0
    failures: list[str] = []
    for index, paragraph in enumerate(root.findall(".//w:p", NS), start=1):
        if not any(re.search(r"\bPAGE\b", code, re.IGNORECASE) for code in field_codes(paragraph)):
            continue
        paragraph_count += 1
        runs = paragraph.findall(".//w:r", NS)
        if not runs:
            failures.append(f"{part}:paragraph {index}: no runs")
            continue
        for run_index, run in enumerate(runs, start=1):
            size = attr(run.find("w:rPr/w:sz", NS), "val")
            size_cs = attr(run.find("w:rPr/w:szCs", NS), "val")
            if size != PAGE_NUMBER_SIZE or size_cs != PAGE_NUMBER_SIZE:
                failures.append(
                    f"{part}:paragraph {index}:run {run_index}: sz={size or '<missing>'}, "
                    f"szCs={size_cs or '<missing>'}"
                )
    return paragraph_count, failures


def table_border_failures(table: ET.Element, index: int, formatting: Formatting) -> list[str]:
    failures: list[str] = []
    borders = table.find("w:tblPr/w:tblBorders", NS)
    for edge in REQUIRED_TABLE_BORDERS:
        border = borders.find(f"w:{edge}", NS) if borders is not None else None
        value = (attr(border, "val") or "").lower()
        colors = {f"color/{key}": attr(border, key) for key in ("themeColor", "themeTint", "themeShade") if attr(border, key)}
        colors["color/val"] = attr(border, "color") or ""
        color = formatting.color(colors)
        if value != "single" or color not in BLACK_VALUES:
            failures.append(
                f"table {index}:{edge}: val={value or '<missing>'}, color={color or '<missing>'}"
            )
    for border in table.findall(".//w:tcBorders/*", NS) + table.findall(".//w:tblPrEx/w:tblBorders/*", NS):
        colors = {f"color/{key}": attr(border, key) for key in ("themeColor", "themeTint", "themeShade") if attr(border, key)}
        colors["color/val"] = attr(border, "color") or ""
        if attr(border, "val") != "single" or formatting.color(colors) not in BLACK_VALUES:
            failures.append(f"table {index}: cell/row border overrides the black single-line grid")
    return failures


def is_true(node: ET.Element | None) -> bool:
    if node is None:
        return False
    value = attr(node, "val")
    return value is None or value.lower() in {"1", "true", "on", "yes"}


def package_safety(document: Path) -> tuple[bool, list[str], list[dict[str, str]], list[str]]:
    update_fields_on_open = False
    forbidden_field_codes: list[str] = []
    external_relationships: list[dict[str, str]] = []
    unparsed_safety_parts: list[str] = []
    with zipfile.ZipFile(document) as package:
        names = set(package.namelist())
        if "word/settings.xml" in names:
            settings = ET.fromstring(package.read("word/settings.xml"))
            update_fields_on_open = is_true(settings.find("w:updateFields", NS))

        for name in sorted(names):
            if name.startswith("word/") and name.endswith(".xml"):
                try:
                    root = ET.fromstring(package.read(name))
                except ET.ParseError:
                    unparsed_safety_parts.append(name)
                    continue
                _, _, field_errors = parse_fields(root)
                if field_errors:
                    unparsed_safety_parts.append(f"{name}: malformed field structure")
                for code in field_codes(root):
                    for match in FORBIDDEN_FIELD_CODE.finditer(code):
                        forbidden_field_codes.append(f"{name}:{match.group(0).upper()}")

            if name.endswith(".rels"):
                try:
                    rels = ET.fromstring(package.read(name))
                except ET.ParseError:
                    unparsed_safety_parts.append(name)
                    continue
                for rel in rels.findall(REL_Q("Relationship")):
                    if rel.get("TargetMode") != "External":
                        continue
                    relationship = {
                        "part": name,
                        "id": rel.get("Id", ""),
                        "type": rel.get("Type", ""),
                        "target": rel.get("Target", ""),
                    }
                    rel_type = relationship["type"]
                    target = relationship["target"].lower()
                    if not (rel_type.endswith("/hyperlink") and target.startswith(("http://", "https://"))):
                        external_relationships.append(relationship)

    return (
        update_fields_on_open,
        sorted(set(forbidden_field_codes)),
        external_relationships,
        sorted(set(unparsed_safety_parts)),
    )


def audit_document(
    template: Path,
    document: Path,
    forbidden_text: tuple[str, ...] = (),
) -> dict[str, object]:
    failures: list[str] = []
    template_hashes = {part: sha256(read_part(template, part)) for part in AUTHORITATIVE_PARTS}
    document_hashes = {part: sha256(read_part(document, part)) for part in AUTHORITATIVE_PARTS}
    for part in AUTHORITATIVE_PARTS:
        if semantic_xml(read_part(template, part)) != semantic_xml(read_part(document, part)):
            failures.append(f"authoritative part differs: {part}")

    template_sections = section_signature(read_part(template, "word/document.xml"))
    document_xml = read_part(document, "word/document.xml")
    if section_signature(document_xml) != template_sections:
        failures.append("section geometry differs from template")

    root = ET.fromstring(document_xml)
    template_format = Formatting(*(read_part(template, part) for part in AUTHORITATIVE_PARTS[:3]))
    document_format = Formatting(*(read_part(document, part) for part in AUTHORITATIVE_PARTS[:3]))
    document_text = document_body_text(root)
    forbidden_internal_text = [marker for marker in forbidden_text if marker and marker in document_text]
    forbidden_local_paths = sorted(set(LOCAL_PATH.findall(document_text)))
    sections = body_sections(root)
    report_paragraphs = [paragraph for section in sections[2:] for child in section for paragraph in child.iter(Q("p"))]
    body_style_failures: list[str] = []
    for section in sections[2:]:
        for child in section:
            for paragraph in child.iter(Q("p")):
                text = paragraph_text(paragraph).strip()
                if text and paragraph_style(paragraph) not in {"A1", "Af1", "af3", *HEADING_TEXT}:
                    body_style_failures.append(text)
    if body_style_failures:
        failures.append(f"unclassified or incorrect body paragraph styles: {len(body_style_failures)}")
    cover_paragraphs = [
        paragraph
        for paragraph in (sections[0] if sections else [])
        if paragraph.tag == Q("p") and paragraph_text(paragraph).strip()
    ]
    cover_texts = [paragraph_text(paragraph).strip() for paragraph in cover_paragraphs]
    cover_date_size = ""
    if len(cover_paragraphs) != 2:
        failures.append(f"cover must contain exactly report name and date; found {len(cover_paragraphs)} text paragraphs")
    else:
        if paragraph_style(cover_paragraphs[0]) != "a5":
            failures.append("cover report name does not use Title style")
        date_paragraph = cover_paragraphs[1]
        if not DATE_TEXT.fullmatch(cover_texts[1]):
            failures.append(f"cover date is not a standalone Chinese date: {cover_texts[1]!r}")
        date_sizes = {attr(node, "val") or "" for node in date_paragraph.findall(".//w:rPr/w:sz", NS)}
        if date_sizes != {"28"}:
            failures.append(f"cover date must be 14 pt (w:sz=28), found {sorted(date_sizes)}")
        else:
            cover_date_size = "28"

    fields, _, field_errors = parse_fields(root)
    toc_fields = [record for record in fields if re.match(r"\s*TOC\b", record.code, re.IGNORECASE)]
    toc_codes = [record.code.strip() for record in toc_fields]
    failures.extend(field_errors)
    if len(toc_codes) != 1:
        failures.append(f"document must contain exactly one real TOC field; found {len(toc_codes)}")
    if "[[TOC]]" in document_text:
        failures.append("TOC placeholder remains in document")
    toc_result_paragraphs = [
        paragraph
        for paragraph in (toc_fields[0].paragraphs if len(toc_fields) == 1 else [])
        if paragraph_style(paragraph) in {"TOC1", "TOC2", "TOC3"} and paragraph_text(paragraph).strip()
    ]
    if not toc_result_paragraphs or not any(re.search(r"\d+\s*$", paragraph_text(p)) for p in toc_result_paragraphs):
        failures.append("TOC field has no populated cached entries with page numbers")
    toc_identity_failures: list[str] = []
    if toc_fields and not re.search(r'\\o\s+"1-3"', toc_fields[0].code, re.IGNORECASE):
        toc_identity_failures.append("TOC does not request heading levels 1-3")
    toc_headings = [paragraph for paragraph in report_paragraphs if paragraph_style(paragraph) in {"1", "2", "3"}]
    unmatched_headings = list(toc_headings)
    for entry in toc_result_paragraphs:
        text = paragraph_text(entry).strip()
        page = re.search(r"\s+\d+\s*$", text)
        title = text[:page.start()].strip() if page else ""
        anchors = [attr(link, "anchor") for link in entry.findall(".//w:hyperlink", NS) if attr(link, "anchor")]
        level = paragraph_style(entry).removeprefix("TOC")
        matches = []
        for heading in unmatched_headings:
            heading_title = paragraph_text(heading).strip()
            without_number = re.sub(r"^\d+(?:\.\d+){0,3}\.?\s*", "", title)
            if paragraph_style(heading) != level or heading_title not in {title, without_number}:
                continue
            bookmarks = {attr(node, "name") for node in heading.findall(".//w:bookmarkStart", NS)}
            if not anchors or all(anchor in bookmarks for anchor in anchors):
                matches.append(heading)
        if len(matches) != 1:
            toc_identity_failures.append(f"TOC entry does not uniquely match a current heading, level and anchor: {text}")
        else:
            unmatched_headings.remove(matches[0])
    if unmatched_headings:
        toc_identity_failures.append(f"TOC omits {len(unmatched_headings)} current level 1-3 headings")
    failures.extend(toc_identity_failures)

    default_table_style = default_table_style_id(read_part(template, "word/styles.xml"))
    if not default_table_style:
        failures.append("template has no default table style")
    table_style_failures: list[str] = []
    table_border_errors: list[str] = []
    table_cell_style_failures = 0
    table_shading_count = 0
    for index, table in enumerate(root.findall(".//w:body//w:tbl", NS), start=1):
        table_style = attr(table.find("w:tblPr/w:tblStyle", NS), "val") or ""
        if table_style != default_table_style:
            table_style_failures.append(f"table {index}: {table_style or '<none>'}")
        table_border_errors.extend(table_border_failures(table, index, document_format))
        table_shading_count += len(table.findall(".//w:shd", NS))
        for paragraph in table.findall(".//w:p", NS):
            if paragraph_style(paragraph) != "Af1":
                table_cell_style_failures += 1
    if table_style_failures:
        failures.append(
            f"tables do not use template default table style {default_table_style}: {', '.join(table_style_failures)}"
        )
    if table_border_errors:
        failures.append(f"tables do not have complete black single-line borders: {len(table_border_errors)}")
    if table_shading_count:
        failures.append(f"tables contain {table_shading_count} direct shading elements")
    if table_cell_style_failures:
        failures.append(f"{table_cell_style_failures} table-cell paragraphs do not use A图表 (Af1)")

    caption_style_failures: list[str] = []
    caption_separator_failures: list[str] = []
    for paragraph in body_paragraphs(root):
        text = paragraph_text(paragraph).strip()
        has_caption_field = any(
            re.match(r'\s*SEQ\s+"?(?:图|表|Figure|Table)"?(?:\s|$)', code, re.IGNORECASE)
            for code in field_codes(paragraph)
        )
        if paragraph_style(paragraph) == "af3" or has_caption_field:
            if paragraph_style(paragraph) != "af3":
                caption_style_failures.append(text)
            if not CAPTION_FORMAT.match(text):
                caption_separator_failures.append(text)
    if caption_style_failures:
        failures.append(f"caption paragraphs not using 题注 (af3): {len(caption_style_failures)}")
    if caption_separator_failures:
        failures.append(
            f"caption paragraphs do not use exactly two ASCII spaces after the number: "
            f"{len(caption_separator_failures)}"
        )

    non_black_colors: list[str] = []
    non_black_direct_colors: list[str] = []
    header_texts: dict[str, str] = {}
    page_number_paragraph_count = 0
    page_number_font_failures: list[str] = []
    effective_format_failures: list[str] = []
    with zipfile.ZipFile(document) as package:
        for name in sorted(package.namelist()):
            if not (name == "word/document.xml" or name.startswith("word/header") or name.startswith("word/footer")):
                continue
            if not name.endswith(".xml"):
                continue
            try:
                part_root = root if name == "word/document.xml" else ET.fromstring(package.read(name))
            except ET.ParseError:
                continue
            non_black_direct_colors.extend(direct_color_failures(part_root, name))
            for paragraph in part_root.findall(".//w:p", NS):
                page_override = name.startswith("word/footer") and any(re.search(r"\bPAGE\b", code, re.IGNORECASE) for code in field_codes(paragraph))
                date_override = name == "word/document.xml" and len(cover_paragraphs) == 2 and paragraph is cover_paragraphs[1]
                for run in text_runs(paragraph):
                    try:
                        values = document_format.run(paragraph, run)
                        color = document_format.color(values)
                        if color not in BLACK_VALUES:
                            non_black_colors.append(f"{name}:{color}:{paragraph_text(run)}")
                        expected = template_format.run(paragraph, run, direct=False)
                        for face in ("ascii", "hAnsi", "eastAsia", "cs"):
                            expected_font = template_format.font(expected, face)
                            if not expected_font or document_format.font(values, face) != expected_font:
                                effective_format_failures.append(f"{name}: {paragraph_style(paragraph)}: effective {face} font differs or is unresolved")
                        for key in ("sz/val", "szCs/val"):
                            expected_size = "21" if page_override else "28" if date_override and key == "sz/val" else expected.get(key)
                            if values.get(key) != expected_size:
                                effective_format_failures.append(f"{name}: {paragraph_style(paragraph)}: effective {key} differs")
                        if paragraph_style(paragraph) in HEADING_TEXT and paragraph in report_paragraphs:
                            for trait in ("b", "bCs", "i", "iCs", "caps", "smallCaps"):
                                if values.get(f"{trait}/val", "false") != expected.get(f"{trait}/val", "false"):
                                    effective_format_failures.append(f"{name}: heading font trait differs: {trait}")
                    except (ValueError, TypeError) as error:
                        effective_format_failures.append(f"{name}: {error}")
            if name.startswith("word/header"):
                text = paragraph_text(part_root).strip()
                header_texts[name] = text
                if text or part_root.find(".//w:instrText", NS) is not None or part_root.find(".//w:drawing", NS) is not None:
                    failures.append(f"header contains visible content: {name}")
            if name.startswith("word/footer"):
                count, size_failures = page_number_size_failures(part_root, name)
                page_number_paragraph_count += count
                page_number_font_failures.extend(size_failures)
    if non_black_colors:
        failures.append(f"non-black or unresolved effective font colors found: {len(non_black_colors)}")
    if page_number_paragraph_count == 0:
        failures.append("document has no PAGE field in footer parts")
    if page_number_font_failures:
        failures.append(f"page-number runs are not 10.5 pt: {len(page_number_font_failures)}")

    usage: dict[str, int] = {}
    manual_numbered_headings: list[str] = []
    forbidden_usage: list[str] = []
    heading_alignment_failures: list[str] = []
    direct_font_override_paragraphs = 0
    heading_direct_font_overrides = 0
    for paragraph in body_paragraphs(root):
        p_style = paragraph.find("w:pPr/w:pStyle", NS)
        style_id = attr(p_style, "val") or ""
        if style_id:
            usage[style_id] = usage.get(style_id, 0) + 1
        text = paragraph_text(paragraph).strip()
        if style_id in FORBIDDEN_HEADING_STYLES:
            forbidden_usage.append(text)
        if style_id in HEADING_TEXT and MANUAL_NUMBER.match(text):
            manual_numbered_headings.append(text)
        if style_id in HEADING_TEXT and attr(paragraph.find("w:pPr/w:jc", NS), "val") != "both":
            heading_alignment_failures.append(text)
        if style_id in {"A1", "1", "2", "3", "4"}:
            if paragraph.findall(".//w:rPr/w:rFonts", NS) or paragraph.findall(".//w:rPr/w:sz", NS):
                direct_font_override_paragraphs += 1
                if style_id in HEADING_TEXT:
                    heading_direct_font_overrides += 1

    if forbidden_usage:
        failures.append(f"forbidden heading styles used in {len(forbidden_usage)} paragraphs")
    if manual_numbered_headings:
        failures.append(f"manual numbering remains in {len(manual_numbered_headings)} heading paragraphs")
    if heading_alignment_failures:
        failures.append(f"headings not explicitly justified: {len(heading_alignment_failures)}")
    for section in sections[2:]:
        for child in section:
            for paragraph in child.iter(Q("p")):
                if not text_runs(paragraph):
                    continue
                style_id = paragraph_style(paragraph)
                try:
                    expected_paragraph = template_format.paragraph(paragraph, direct=False)
                    actual_paragraph = document_format.paragraph(paragraph)
                    if style_id in HEADING_TEXT:
                        inherited = template_format.style_properties(style_id, "pPr")
                        actual_num = actual_paragraph.get("numPr/numId/val", "0")
                        unnumbered = actual_num == "0" and paragraph_text(paragraph).strip() in {"摘要", "参考文献"}
                        if not unnumbered and (
                            actual_num != inherited.get("numPr/numId/val", "0")
                            or actual_paragraph.get("numPr/ilvl/val", "0") != inherited.get("numPr/ilvl/val", "0")
                        ):
                            effective_format_failures.append(f"{style_id}: heading numbering differs from template")
                    allowed = {"pStyle/val", "numPr/numId/val", "numPr/ilvl/val", "sectPr"}
                    if style_id in HEADING_TEXT:
                        allowed.add("jc/val")
                    if style_id == "Af1":
                        allowed.update({"jc/val", "spacing/before", "spacing/after", "keepNext/val", "keepLines/val", "pageBreakBefore/val"})
                        if actual_paragraph.get("jc/val") not in {"left", "right", "center"}:
                            effective_format_failures.append("table/figure paragraph alignment is not an allowed adaptation")
                    for key in paragraph_differences(expected_paragraph, actual_paragraph, allowed):
                        effective_format_failures.append(f"{style_id}: paragraph property differs: {key}")
                except ValueError as error:
                    effective_format_failures.append(str(error))
    for paragraph in toc_result_paragraphs + cover_paragraphs:
        try:
            expected = template_format.paragraph(paragraph, direct=False)
            actual = document_format.paragraph(paragraph)
            allowed = {"spacing/before", "spacing/after", "jc/val"} if len(cover_paragraphs) == 2 and paragraph is cover_paragraphs[1] else set()
            for key in paragraph_differences(expected, actual, allowed):
                effective_format_failures.append(f"{paragraph_style(paragraph)}: front-matter paragraph property differs: {key}")
        except ValueError as error:
            effective_format_failures.append(str(error))
    if effective_format_failures:
        failures.append(f"effective format differs or cannot be resolved: {len(effective_format_failures)}")
    if usage.get("A1", 0) == 0:
        failures.append("A正文 (A1) is not used")
    if sum(usage.get(style_id, 0) for style_id in HEADING_TEXT) == 0:
        failures.append("numbered heading styles 1-4 are not used")

    (
        update_fields_on_open,
        forbidden_field_codes,
        external_relationships,
        unparsed_safety_parts,
    ) = package_safety(document)
    if update_fields_on_open:
        failures.append("w:updateFields is true; report preference disables field recalculation on open")
    if forbidden_field_codes:
        failures.append(f"external file field codes found: {', '.join(forbidden_field_codes)}")
    if external_relationships:
        failures.append(f"forbidden external relationships found: {len(external_relationships)}")
    if unparsed_safety_parts:
        failures.append(f"safety-relevant package parts could not be parsed: {len(unparsed_safety_parts)}")
    if forbidden_internal_text:
        failures.append(f"forbidden internal text found: {', '.join(forbidden_internal_text)}")

    return {
        "document": str(document),
        "passed": not failures,
        "validation_scope": "structure_only",
        "visual_status": "not_checked",
        "pagination_status": "not_checked",
        "content_preservation_status": "not_checked",
        "required_evidence": ["final field refresh", "all-page visual inspection", "content comparison for format-only"],
        "failures": failures,
        "style_usage": usage,
        "body_style_failures": body_style_failures,
        "manual_numbered_headings": manual_numbered_headings,
        "forbidden_heading_examples": forbidden_usage[:10],
        "heading_alignment_failures": heading_alignment_failures[:10],
        "direct_font_override_paragraphs": direct_font_override_paragraphs,
        "heading_direct_font_overrides": heading_direct_font_overrides,
        "cover_texts": cover_texts,
        "cover_date_size": cover_date_size,
        "toc_codes": toc_codes,
        "toc_cached_entry_count": len(toc_result_paragraphs),
        "toc_identity_failures": toc_identity_failures,
        "header_texts": header_texts,
        "non_black_direct_colors": non_black_direct_colors,
        "non_black_effective_colors": non_black_colors,
        "effective_format_failures": effective_format_failures,
        "default_table_style": default_table_style,
        "table_style_failures": table_style_failures,
        "table_border_failures": table_border_errors,
        "table_shading_count": table_shading_count,
        "table_cell_style_failures": table_cell_style_failures,
        "caption_style_failures": caption_style_failures,
        "caption_separator_failures": caption_separator_failures,
        "page_number_paragraph_count": page_number_paragraph_count,
        "page_number_font_failures": page_number_font_failures,
        "update_fields_on_open": update_fields_on_open,
        "forbidden_field_codes": forbidden_field_codes,
        "forbidden_external_relationships": external_relationships,
        "unparsed_safety_parts": unparsed_safety_parts,
        "forbidden_internal_text": forbidden_internal_text,
        "forbidden_local_paths": forbidden_local_paths,
        "content_review_findings": {"local_paths": forbidden_local_paths},
        "authoritative_part_hashes": document_hashes,
        "template_part_hashes": template_hashes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--documents", type=Path, nargs="+", required=True)
    parser.add_argument(
        "--forbid-text",
        action="append",
        default=[],
        help="Exact internal text that must not appear in a report; repeat for multiple values.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    template_failures, abstract_id = validate_template(args.template)
    forbidden_text = tuple(args.forbid_text)
    results = [audit_document(args.template, document, forbidden_text) for document in args.documents]
    payload = {
        "template": str(args.template),
        "template_passed": not template_failures,
        "template_failures": template_failures,
        "heading_abstract_num_id": abstract_id,
        "documents": results,
        "passed": not template_failures and all(result["passed"] for result in results),
        "validation_scope": "structure_only",
        "visual_status": "not_checked",
        "pagination_status": "not_checked",
        "content_preservation_status": "not_checked",
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"TEMPLATE: {'PASS' if payload['template_passed'] else 'FAIL'}")
        print("SCOPE: structure only; field refresh, all-page visual and format-only content evidence remain required")
        for failure in template_failures:
            print(f"  - {failure}")
        for result in results:
            print(f"DOCUMENT: {'PASS' if result['passed'] else 'FAIL'} {result['document']}")
            for failure in result["failures"]:
                print(f"  - {failure}")
            print(f"  styles: {result['style_usage']}")
            print(f"  cover: {result['cover_texts']}")
            print(f"  TOC cached entries: {result['toc_cached_entry_count']}")
            print(f"  default table style: {result['default_table_style']}")
            print(f"  table border failures: {len(result['table_border_failures'])}")
            print(f"  caption separator failures: {len(result['caption_separator_failures'])}")
            print(f"  PAGE footer paragraphs: {result['page_number_paragraph_count']}")
            print(f"  PAGE font failures: {len(result['page_number_font_failures'])}")
            print(f"  direct font overrides: {result['direct_font_override_paragraphs']}")
            print(f"  heading direct font overrides: {result['heading_direct_font_overrides']}")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
