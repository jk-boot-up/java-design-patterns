# Materialized View Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `materialized-view-pattern-explained.mp4` | the video, 1920×1080 |
| `materialized-view-pattern-explained.m4a` | audio only |
| `materialized-view-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> When a page needs data from several services, keep a ready-made copy shaped exactly for that page, and update it from events, instead of asking every service on every visit. A materialized view is a ready-made copy of data from several services, shaped for one page and kept up to date from events, so reading it is one fast lookup that works even when those services are down.
