# Backpressure Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `backpressure-pattern-explained.mp4` | the video, 1920×1080 |
| `backpressure-pattern-explained.m4a` | audio only |
| `backpressure-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Let a slow consumer push back on a fast producer, by bounding what waits, asking for work in batches, or dropping stale updates, instead of buffering until memory runs out. Backpressure lets a slow consumer control how fast a producer sends, so waiting work stays bounded instead of filling memory.
