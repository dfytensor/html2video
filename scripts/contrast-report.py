#!/usr/bin/env python3
"""
contrast-report.py — WCAG Contrast Ratio Audit for HTML Presentations

Walks the DOM of an HTML file rendered in headless Chromium, finds text elements,
samples background pixels, computes WCAG contrast ratios, and reports failures.

Usage:
    python scripts/contrast-report.py input.html
    python scripts/contrast-report.py input.html -o report.json
    python scripts/contrast-report.py input.html --width 1080 --height 1920

Requirements:
    pip install playwright pillow
    python -m playwright install chromium
"""

import argparse
import json
import math
import os
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Error: playwright not installed. Run: pip install playwright && python -m playwright install chromium")


INJECT_JS = """
() => {
    const textElements = [];
    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_ELEMENT,
        {
            acceptNode: (node) => {
                const style = window.getComputedStyle(node);
                if (style.display === 'none' || style.visibility === 'hidden') {
                    return NodeFilter.FILTER_REJECT;
                }
                const tag = node.tagName.toLowerCase();
                if (['script', 'style', 'svg', 'canvas', 'img', 'video', 'audio', 'i'].includes(tag)) {
                    return NodeFilter.FILTER_REJECT;
                }
                if (node.childNodes.length === 0 && !node.textContent.trim()) {
                    return NodeFilter.FILTER_REJECT;
                }
                return NodeFilter.FILTER_ACCEPT;
            }
        }
    );

    while (walker.nextNode()) {
        const node = walker.currentNode;
        const text = node.textContent.trim();
        if (!text || text.length < 1) continue;

        const style = window.getComputedStyle(node);
        const fontSize = parseFloat(style.fontSize);
        if (fontSize < 8) continue;

        const rect = node.getBoundingClientRect();
        if (rect.width < 1 || rect.height < 1) continue;

        textElements.push({
            tag: node.tagName,
            text: text.substring(0, 80),
            fontSize: fontSize,
            fontWeight: style.fontWeight,
            color: style.color,
            backgroundColor: style.backgroundColor,
            x: Math.round(rect.x),
            y: Math.round(rect.y),
            width: Math.round(rect.width),
            height: Math.round(rect.height),
            parentBg: ''
        });
    }

    // Walk up to find parent background
    textElements.forEach(el => {
        const elements = document.elementsFromPoint(el.x + el.width / 2, el.y + el.height / 2);
        for (const elem of elements) {
            const bg = window.getComputedStyle(elem).backgroundColor;
            if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') {
                el.parentBg = bg;
                break;
            }
        }
    });

    return textElements;
}
"""


def parse_color(color_str):
    if not color_str or color_str == 'transparent':
        return None

    color_str = color_str.strip()

    if color_str.startswith('rgba(') or color_str.startswith('rgb('):
        parts = color_str.replace('rgba(', '').replace('rgb(', '').replace(')', '').split(',')
        try:
            r, g, b = int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip())
            a = float(parts[3].strip()) if len(parts) > 3 else 1.0
            return (r, g, b, a)
        except (ValueError, IndexError):
            return None

    if color_str.startswith('#'):
        hex_str = color_str.lstrip('#')
        if len(hex_str) == 6:
            return (int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16), 1.0)
        elif len(hex_str) == 3:
            return (int(hex_str[0]*2, 16), int(hex_str[1]*2, 16), int(hex_str[2]*2, 16), 1.0)

    return None


def relative_luminance(r, g, b):
    def linearize(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(color1, color2):
    l1 = relative_luminance(*color1[:3])
    l2 = relative_luminance(*color2[:3])
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def blend_colors(fg, bg):
    if fg[3] >= 1.0:
        return fg[:3]
    if bg is None:
        return fg[:3]
    a = fg[3]
    return (
        int(fg[0] * a + bg[0] * (1 - a)),
        int(fg[1] * a + bg[1] * (1 - a)),
        int(fg[2] * a + bg[2] * (1 - a))
    )


def analyze_contrast(html_path, width=1080, height=1920):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height})

        abs_path = os.path.abspath(html_path)
        page.goto("file:///" + abs_path.replace("\\", "/"))
        page.wait_for_timeout(1000)

        elements = page.evaluate(INJECT_JS)
        browser.close()

    results = []
    for el in elements:
        fg_color = parse_color(el.get('color', ''))
        bg_color = parse_color(el.get('backgroundColor', ''))
        parent_bg = parse_color(el.get('parentBg', ''))

        if fg_color is None:
            continue

        if bg_color is None or (bg_color[0] == 0 and bg_color[1] == 0 and bg_color[2] == 0 and bg_color[3] == 0):
            bg_for_calc = parent_bg if parent_bg else (255, 255, 255, 1.0)
        else:
            bg_for_calc = bg_color

        text_color = blend_colors(fg_color, bg_for_calc)
        bg_final = bg_for_calc[:3]

        ratio = contrast_ratio(text_color, bg_final)

        font_size = el.get('fontSize', 16)
        is_large_text = font_size >= 24 or (font_size >= 18.667 and int(el.get('fontWeight', 400)) >= 700)

        aa_threshold = 3.0 if is_large_text else 4.5
        aaa_threshold = 4.5 if is_large_text else 7.0

        results.append({
            "tag": el.get("tag", ""),
            "text": el.get("text", ""),
            "fontSize": font_size,
            "fontWeight": el.get("fontWeight", ""),
            "textColor": el.get("color", ""),
            "bgColor": el.get("parentBg", "") or el.get("backgroundColor", ""),
            "contrastRatio": round(ratio, 2),
            "wcagAA": "PASS" if ratio >= aa_threshold else "FAIL",
            "wcagAAA": "PASS" if ratio >= aaa_threshold else "FAIL",
            "isLargeText": is_large_text
        })

    return results


def generate_report(results):
    total = len(results)
    aa_fails = [r for r in results if r["wcagAA"] == "FAIL"]
    aaa_fails = [r for r in results if r["wcagAAA"] == "FAIL"]

    lines = []
    lines.append("=" * 60)
    lines.append("CONTRAST REPORT")
    lines.append("=" * 60)
    lines.append(f"Elements checked: {total}")
    lines.append(f"WCAG AA failures: {len(aa_fails)}")
    lines.append(f"WCAG AAA failures: {len(aaa_fails)}")
    lines.append("")

    if aa_fails:
        lines.append("WCAG AA FAILURES (contrast < 4.5 for normal, < 3.0 for large):")
        lines.append("-" * 60)
        for fail in aa_fails[:20]:
            lines.append(f"  [{fail['tag']}] \"{fail['text'][:40]}\"")
            lines.append(f"    Size: {fail['fontSize']}px | Weight: {fail['fontWeight']} | Ratio: {fail['contrastRatio']}:1")
            lines.append(f"    Text: {fail['textColor']} | BG: {fail['bgColor']}")
            lines.append("")

    if len(aa_fails) > 20:
        lines.append(f"  ... and {len(aa_fails) - 20} more failures")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="WCAG contrast ratio audit for HTML presentations")
    parser.add_argument("input", help="Input HTML file path")
    parser.add_argument("-o", "--output", help="Output JSON report path (default: <input>_contrast-report.json)")
    parser.add_argument("--width", type=int, default=1080, help="Viewport width (default: 1080)")
    parser.add_argument("--height", type=int, default=1920, help="Viewport height (default: 1920)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit(f"Error: {args.input} not found")

    results = analyze_contrast(args.input, args.width, args.height)

    output_path = args.output
    if not output_path:
        base = os.path.splitext(args.input)[0]
        output_path = base + "_contrast-report.json"

    report_data = {
        "totalElements": len(results),
        "aaFailures": len([r for r in results if r["wcagAA"] == "FAIL"]),
        "aaaFailures": len([r for r in results if r["wcagAAA"] == "FAIL"]),
        "elements": results
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    ascii_report = generate_report(results)
    print(ascii_report)
    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
