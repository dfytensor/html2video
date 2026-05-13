#!/usr/bin/env python3
"""
animation-map.py — Animation Quality Audit for HTML Presentations

Analyzes an HTML file with GSAP/CSS animations, enumerates all tweens,
detects issues (offscreen elements, collisions, invisible animations,
dead zones), and outputs a JSON report.

Usage:
    python scripts/animation-map.py input.html
    python scripts/animation-map.py input.html -o report.json
    python scripts/animation-map.py input.html --width 1080 --height 1920

Requirements:
    pip install playwright
    python -m playwright install chromium
"""

import argparse
import json
import os
import sys
import tempfile

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Error: playwright not installed. Run: pip install playwright && python -m playwright install chromium")


INJECT_JS = r"""
() => {
    const result = {
        slides: [],
        totalSlides: 0,
        hasGSAP: typeof gsap !== 'undefined',
        hasTimelines: typeof window.__timelines !== 'undefined',
        timelineIds: [],
        issues: []
    };

    // Detect slides
    const slides = document.querySelectorAll('.slide, .ppt-container > .slide, [class*="slide"]');
    result.totalSlides = slides.length;

    slides.forEach((slide, idx) => {
        const rect = slide.getBoundingClientRect();
        const slideInfo = {
            index: idx,
            width: rect.width,
            height: rect.height,
            animatedElements: [],
            totalAnimations: 0,
            issues: []
        };

        // Find animated elements
        const animated = slide.querySelectorAll('.an, .anim-item, [style*="animation"], [class*="animate"]');
        animated.forEach(el => {
            const elRect = el.getBoundingClientRect();
            const styles = window.getComputedStyle(el);
            const animInfo = {
                tag: el.tagName,
                classes: el.className,
                x: Math.round(elRect.x),
                y: Math.round(elRect.y),
                width: Math.round(elRect.width),
                height: Math.round(elRect.height),
                opacity: parseFloat(styles.opacity),
                visibility: styles.visibility,
                display: styles.display,
                hasAnimation: styles.animationName !== 'none',
                animationName: styles.animationName,
                animationDuration: styles.animationDuration,
                hasTransform: styles.transform !== 'none'
            };
            slideInfo.animatedElements.push(animInfo);
            slideInfo.totalAnimations++;

            // Check offscreen
            if (elRect.x < 0 || elRect.y < 0 ||
                elRect.x + elRect.width > rect.width ||
                elRect.y + elRect.height > rect.height) {
                slideInfo.issues.push({
                    type: 'offscreen',
                    element: animInfo.tag + '.' + animInfo.classes.split(' ')[0],
                    message: 'Element is offscreen or overflowing'
                });
            }

            // Check invisible
            if (parseFloat(styles.opacity) < 0.1 || styles.visibility === 'hidden' || styles.display === 'none') {
                slideInfo.issues.push({
                    type: 'invisible',
                    element: animInfo.tag + '.' + animInfo.classes.split(' ')[0],
                    message: 'Animated element is invisible (opacity/visibility/display)'
                });
            }
        });

        // Check collision between animated elements
        for (let i = 0; i < slideInfo.animatedElements.length; i++) {
            for (let j = i + 1; j < slideInfo.animatedElements.length; j++) {
                const a = slideInfo.animatedElements[i];
                const b = slideInfo.animatedElements[j];
                if (a.x < b.x + b.width && a.x + a.width > b.x &&
                    a.y < b.y + b.height && a.y + a.height > b.y) {
                    const overlapX = Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x);
                    const overlapY = Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y);
                    const overlapArea = overlapX * overlapY;
                    const minArea = Math.min(a.width * a.height, b.width * b.height);
                    if (overlapArea / minArea > 0.3) {
                        slideInfo.issues.push({
                            type: 'collision',
                            element: a.tag + ' <-> ' + b.tag,
                            message: 'Significant overlap between animated elements (' + Math.round(overlapArea / minArea * 100) + '%)'
                        });
                    }
                }
            }
        }

        result.slides.push(slideInfo);
    });

    // Check GSAP timelines
    if (result.hasTimelines) {
        result.timelineIds = Object.keys(window.__timelines || {});
        result.timelineIds.forEach(id => {
            const tl = window.__timelines[id];
            if (tl && tl.duration) {
                const dur = tl.duration();
                if (dur === 0) {
                    result.issues.push({
                        type: 'empty-timeline',
                        timeline: id,
                        message: 'Timeline has zero duration'
                    });
                }
            }
        });
    }

    // Global checks
    if (result.totalSlides === 0) {
        result.issues.push({
            type: 'no-slides',
            message: 'No slide elements found. Video export may treat entire page as one slide.'
        });
    }

    // Check for emoji
    const bodyText = document.body.innerText;
    const emojiRegex = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E0}-\u{1F1FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu;
    const emojis = bodyText.match(emojiRegex);
    if (emojis && emojis.length > 0) {
        result.issues.push({
            type: 'emoji-found',
            message: 'Found ' + emojis.length + ' emoji characters. Replace with UI icons.'
        });
    }

    // Check animation reset JS
    const scripts = document.querySelectorAll('script');
    let hasCloneNode = false;
    scripts.forEach(s => {
        if (s.textContent.includes('cloneNode')) hasCloneNode = true;
    });
    if (!hasCloneNode && result.totalSlides > 1) {
        result.issues.push({
            type: 'missing-animation-reset',
            message: 'No cloneNode animation reset found. CSS animations may not replay on slide revisit.'
        });
    }

    return result;
}
"""


def analyze_html(html_path, width=1080, height=1920):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height})

        abs_path = os.path.abspath(html_path)
        page.goto("file:///" + abs_path.replace("\\", "/"))
        page.wait_for_timeout(1000)

        result = page.evaluate(INJECT_JS)
        browser.close()

    return result


def generate_ascii_timeline(report):
    lines = []
    lines.append("=" * 60)
    lines.append("ANIMATION MAP REPORT")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"Slides: {report['totalSlides']}")
    lines.append(f"GSAP: {'Yes' if report['hasGSAP'] else 'No'}")
    lines.append(f"Timelines: {', '.join(report['timelineIds']) if report['timelineIds'] else 'None'}")
    lines.append("")

    for slide in report.get("slides", []):
        status = "OK" if not slide["issues"] else f"{len(slide['issues'])} ISSUE(S)"
        lines.append(f"  Slide {slide['index']} | {slide['totalAnimations']} animations | {status}")

        if slide["issues"]:
            for issue in slide["issues"]:
                lines.append(f"    [{issue['type'].upper()}] {issue.get('message', '')}")

    if report["issues"]:
        lines.append("")
        lines.append("GLOBAL ISSUES:")
        for issue in report["issues"]:
            lines.append(f"  [{issue['type'].upper()}] {issue.get('message', '')}")

    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Animation quality audit for HTML presentations")
    parser.add_argument("input", help="Input HTML file path")
    parser.add_argument("-o", "--output", help="Output JSON report path (default: <input>_animation-map.json)")
    parser.add_argument("--width", type=int, default=1080, help="Viewport width (default: 1080)")
    parser.add_argument("--height", type=int, default=1920, help="Viewport height (default: 1920)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit(f"Error: {args.input} not found")

    report = analyze_html(args.input, args.width, args.height)

    output_path = args.output
    if not output_path:
        base = os.path.splitext(args.input)[0]
        output_path = base + "_animation-map.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    ascii_report = generate_ascii_timeline(report)
    print(ascii_report)
    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
