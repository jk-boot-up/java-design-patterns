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

> Backpressure pattern in Java with Project Reactor, where every stream
> carries demand from consumer to producer, using an online store search
> indexer reading a supplier's product feed. A slow consumer tells a fast
> producer how much it can take, so work does not pile up in between, like a
> chef calling for exactly two more tickets. We watch what Reactor does with
> a source that ignores demand, produce only what is asked, use limitRate,
> and keep only the latest item. We finish with the bill: decide on purpose
> what happens when a source cannot wait.
