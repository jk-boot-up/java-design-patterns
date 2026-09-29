# Backpressure with Project Reactor Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `backpressure-with-reactor-pattern-explained.mp4` | the video, 1920×1080 |
| `backpressure-with-reactor-pattern-explained.m4a` | audio only |
| `backpressure-with-reactor-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Handle a fast supplier feed and a slow search indexer with Project Reactor, where every subscriber states its demand: Reactor refuses a source that ignores it, limitRate() asks in batches, and onBackpressureLatest() keeps only the newest stock level. With Reactor, backpressure is built in: subscribers state their demand, and sources that cannot honour it must buffer, drop or keep the latest.
