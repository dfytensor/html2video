# Troubleshooting & Known Issues

Read this file when encountering issues during HTML generation or video export.

---

## Q1: Switching Pages Does Not Re-trigger Animations

**Symptom:** CSS animations play once on first view but do not replay when navigating back.

**Cause:** `animation-fill-mode: forwards` locks the final state. `display: none` also does not reset animation state.

**Solution:** Clone DOM nodes on page switch to force browser re-render.

```javascript
document.querySelectorAll('.slide').forEach(function(s) {
    s.querySelectorAll('.an, .anim-item').forEach(function(item) {
        var clone = item.cloneNode(true);
        item.parentNode.replaceChild(clone, item);
    });
});
```

This is the most **cross-browser reliable** fix.

---

## Q2: AI-Generated HTML Code Volume Insufficient

**Symptom:** Model produces only 200-400 lines of HTML, content is thin.

**Solution:** Explicitly request "1000+ lines of code" in the prompt, or generate in multiple steps and concatenate.

---

## Q3: Flowchart Mode Does Not Generate New Content

**Symptom:** User expects new content in flowchart mode but gets a visual-only restructure.

**Cause:** By design, Mode 2 only re-visualizes existing content from the PPT HTML.

**Solution:** Complete Mode 1 (PPT generation) first, then trigger Mode 2 for visual restructure.

---

## Q4: asyncio + Playwright Conflict

**Symptom:** `RuntimeError` when calling `sync_playwright()` inside an asyncio event loop.

**Solution:** Run Playwright in a thread pool:

```python
loop.run_in_executor(None, functools.partial(screenshot_html_sync, html, path))
```

---

## Q5: moviepy v2 CompositeVideoClip Memory Overflow

**Symptom:** `MemoryError` when creating `CompositeVideoClip(size=(1080, 1920))`.

**Cause:** moviepy allocates float64 full-screen arrays.

**Solution:** Use ffmpeg directly for composition, bypassing moviepy entirely. The `html2video.py` script already handles this.

---

## Q6: Windows Chinese Encoding Issues

**Symptom:** Python crashes on `print()` with Chinese/emoji; ffmpeg UTF-8 output decoded as GBK.

**Cause:** Windows PowerShell defaults to GBK encoding.

**Solution:**
- Use only ASCII characters in `print()` statements
- Set `subprocess.run(cmd, encoding="utf-8", errors="replace")`

---

## Q7: ffmpeg concat Chinese Path Issues

**Symptom:** ffmpeg errors when concat file contains Chinese characters in paths.

**Solution:** Use absolute paths with forward slashes `/` in the concat file.

---

## Q8: TTS Text Too Long

**Symptom:** Edge TTS fails or produces garbled audio for very long slide text.

**Solution:** `html2video.py` auto-truncates TTS text to 200 characters per slide. For longer narration, split content across more slides.

---

## Q9: Blank Screenshots

**Symptom:** Playwright captures blank/white screenshots.

**Cause:** Page has not finished loading CSS/JS resources.

**Solution:** The script injects a 300ms wait after each slide transition. If still blank, increase the wait or check that the HTML file uses relative paths for local assets.

---

## Q10: Font Not Found for Subtitles

**Symptom:** PIL `OSError` when loading subtitle font.

**Solution:** Specify `--font` with an existing font path:
- Windows: `C:/Windows/Fonts/msyh.ttc` (Microsoft YaHei)
- Linux: `/usr/share/fonts/truetype/wqy/wqy-microhei.ttc`
