# Guaranteed Delivery Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `guaranteed-delivery-pattern-explained.mp4` | the video, 1920×1080 |
| `guaranteed-delivery-pattern-explained.m4a` | audio only |
| `guaranteed-delivery-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Store every message safely on disk before accepting it, acknowledge it only after it is delivered, and after a crash deliver everything that was never acknowledged. Guaranteed delivery stores each message durably before accepting it and acknowledges it after delivery, so after a crash every unacknowledged message is delivered again.
