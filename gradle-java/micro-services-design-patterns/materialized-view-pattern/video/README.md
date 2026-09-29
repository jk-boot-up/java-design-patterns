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

> Materialized View pattern in Java, explained with an online store's my-
> orders page, which shows each order, the product name and whether it has
> shipped, from three separate services. A materialized view is a ready-made
> copy of data shaped for one page and kept up to date by listening to
> events, so reading it is one quick lookup, like a railway departures
> board. We watch the page ask three services on every visit, build a ready-
> made view, see it run a moment behind, and rebuild it from the events. We
> finish with the bill.
