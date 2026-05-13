# Template Selection Guide

Read this file when entering **Step 3 (Mode 1 - PPT restructure)** or **Step 1 (Mode 2 - Animation/Flowchart)**.

---

## PPT Template Selection (Mode 1, Step 3)

**AI must read `assets/templates/PPT Template-level2/SUMMARY.md` for full details.**

### Quick Selection

| Content Type | Recommended | Reason |
|---|---|---|
| Two-sided comparison/debate | 8-1, 8-3, 5-3, 6-2 | Rich VS cards (8-1: 12 groups, 8-3: 30 groups) |
| Steps / process / engineering | 3-2, 6-1, 6-3, 6-4, 9-3 | SVG flowcharts + step animations |
| Concept / definition | 1, 2, 3-1, 3-3 | Clean layout + gradient text |
| Case / experiment analysis | 4-2, 4-3, 5-1~5-4 | Data charts + code animations |
| Warning / danger / failure | 5-4, 6-4, 7-3 | 15-16 animation types, warning style |
| Simple / lightweight | 3-1, 3-3, 4-1, 9-2 | Few animations, small code, fast load |
| Maximum visual impact | 2, 5-4, 6-2, 7-2 | 10+ animation types, rich particles |

### Size Spectrum

| Metric | Template | Value |
|---|---|---|
| Smallest | 3-3.html | 331 lines, 7 pages, 0 animations |
| Largest | 6-2.html | 1576 lines, 8 pages, 15 animations |
| Most animations | 7-2.html | 17 animation types |
| Most pages | 5-4.html | 13 pages |
| Fewest pages | 9-3.html | 5 pages |

### Selection Criteria

1. **Read `assets/templates/PPT Template-level2/SUMMARY.md`** first
2. Match content type to template theme
3. Consider page count vs content volume
4. Prefer templates with more animations for dense content
5. Fall back to `assets/templates/PPT/` if no Level2 match

---

## Animation Template Selection (Mode 2)

**AI must read `assets/templates/Animation/SUMMARY.md` for full details.**

### Quick Selection

| Content Type | Recommended | Reason |
|---|---|---|
| RNN / LSTM / recurrent networks | RNN-3 (default) > RNN-4 > RNN-2 | Deep green theme, RNN series |
| Gradient vanishing / exploding | RNN-6 > RNN-7 | explode + shake animations |
| Architecture / system / multi-module | Comprehension > Cross-modal | Architecture cards + connections |
| Word2Vec / word vectors | word2vec-1 | Semantic ID card |
| One-hot encoding | onehot > onehot-drawback | Sparse vector visualization |
| GPU / compute hardware | GPU | Compute node connections |
| DNN / deep learning flaws | The fatal flaw of DNN | Purple warning style |
| General concept / steps | LSTM-1 | Three-stage flow |

### Special Animation Index

| Animation | Templates | Effect |
|---|---|---|
| explode | RNN-6, RNN-7 | Explosion effect |
| shake | RNN-6, RNN-7 | Shake/tremor |
| heartbeat | RNN-5, RNN-6, RNN-7 | Heartbeat pulse |
| typewriter | RNN-4 | Typewriter text |
| arrowFlow / arrowPulse | RNN-4, RNN-5, RNN-6, RNN-7 | Arrow flow pulse |
| gradientShift | Cross-modal | Gradient displacement |
| drawLine | RNN-3/4/5/6/7, Cross-modal | Line drawing animation |

**Default template:** `assets/templates/Animation/RNN-3.html`
