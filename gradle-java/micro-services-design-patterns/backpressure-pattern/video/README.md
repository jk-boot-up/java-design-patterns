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

> Backpressure pattern in Java: Backpressure lets a slow consumer tell a fast
> producer to slow down, so the work waiting in between stays small instead of
> filling memory, like a kitchen telling front of house to stop seating
> tables. Explained with an online store search indexer reading a supplier's
> product feed that is much faster than the indexer. We watch the waiting pile
> grow without limit, add a bounded buffer, let the consumer ask only for what
> it can handle, and keep only the latest item when that is acceptable. We
> finish with the bill.
