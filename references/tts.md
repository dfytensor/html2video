# Text-to-Speech (Edge TTS)

Read this file when generating narration or voiceover for video export.

---

## Voice Selection

Match voice to content. Default is `zh-CN-YunxiNeural` (male, Chinese).

### Chinese Voices (Primary)

| Voice | Gender | Style | Best for |
|---|---|---|---|
| `zh-CN-YunxiNeural` | Male | Warm, natural | Default — most educational content |
| `zh-CN-XiaoxiaoNeural` | Female | Clear, professional | Tutorials, corporate |
| `zh-CN-YunjianNeural` | Male | Authoritative | Narration, serious content |
| `zh-CN-XiaoyiNeural` | Female | Expressive | Storytelling, emotional |
| `zh-CN-YunyangNeural` | Male | News anchor | Formal presentations |

### English Voices

| Voice | Gender | Style | Best for |
|---|---|---|---|
| `en-US-GuyNeural` | Male | Deep, authoritative | Narration, documentaries |
| `en-US-JennyNeural` | Female | Warm, conversational | Tutorials, explainers |
| `en-US-AriaNeural` | Female | Professional | Corporate, presentations |
| `en-GB-SoniaNeural` | Female | British, clear | Academic, formal |

### Other Languages

| Language | Voice | Notes |
|---|---|---|
| Japanese | `ja-JP-NanamiNeural` | Female, natural |
| Korean | `ko-KR-SunHiNeural` | Female, clear |
| French | `fr-FR-DeniseNeural` | Female, standard |
| German | `de-DE-KatjaNeural` | Female, standard |
| Spanish | `es-ES-ElviraNeural` | Female, standard |

Run `edge-tts --list-voices` to see all available voices.

---

## Speed Tuning

| Rate | Use for |
|---|---|
| `-10%` to `+0%` | Tutorial, complex content, Chinese text |
| `+0%` to `+10%` | Natural pace (default) |
| `+10%` to `+20%` | Intros, upbeat content |
| `+20%` to `+30%` | Fast narration, social media |
| `+30%+` | Rarely appropriate — hard to follow |

Chinese text naturally reads slower than English. Use `+0%` or `-5%` for educational Chinese content.

---

## Usage

### Via html2video.py (Recommended)

The video pipeline handles TTS automatically:

```bash
python scripts/html2video.py input.html --voice zh-CN-YunxiNeural --rate +10%
```

See `references/video-pipeline.md` for full parameters.

### Standalone Edge TTS

```bash
# Generate speech from text
edge-tts --voice zh-CN-YunxiNeural --rate "+10%" --text "Hello world" --write-media output.mp3

# Generate speech from file
edge-tts --voice zh-CN-YunxiNeural --rate "+0%" --file script.txt --write-media output.mp3

# Export script only (no audio)
python scripts/html2video.py input.html --export-script --script-output narration.txt
```

---

## Multilingual Content

For mixed Chinese/English content:

1. Use a Chinese voice (e.g., `zh-CN-YunxiNeural`) — it handles English words embedded in Chinese text reasonably well
2. If English sections are long (>1 paragraph), consider splitting into separate audio files and merging with ffmpeg
3. Adjust rate to `-5%` for mixed content to improve English pronunciation clarity

---

## Script Writing Guidelines

- **Short sentences.** TTS handles short sentences better than long ones. Break complex sentences at natural pauses.
- **Spell out abbreviations.** "AI" → "A I", "HTTP" → "H T T P". TTS sometimes mispronounces abbreviations.
- **Numbers:** Write out important numbers ("twenty-three" instead of "23") for better pronunciation.
- **Punctuation matters.** Commas add pauses. Periods add longer pauses. Question marks change intonation.
- **Test with `--export-script` first.** Review the generated narration text before generating audio.

---

## TTS + Captions Workflow

```bash
# 1. Export the narration script
python scripts/html2video.py input.html --export-script --script-output script.txt

# 2. Generate audio (automatic in the pipeline)
python scripts/html2video.py input.html --voice zh-CN-YunxiNeural

# 3. For advanced captions, transcribe the generated audio
# See transcript-guide.md for transcription options
```

---

## Requirements

```bash
pip install edge-tts
```

Edge TTS uses Microsoft's cloud service — requires internet connection. No local model downloads needed.
