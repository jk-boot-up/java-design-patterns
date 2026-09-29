# Query Object Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `query-object-pattern-explained.mp4` | the video, 1920×1080 |
| `query-object-pattern-explained.m4a` | audio only |
| `query-object-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Query Object pattern in Java, explained with an online store search page
> that filters products by category, price and name. A query object holds a
> search as an object made of small criteria that can write itself as safe
> SQL, or run over a plain list in memory for testing, like a library
> request form where the author box is always treated as a name. We watch
> SQL glued together from strings go wrong, build a query object, run the
> same query in memory, and reuse it safely. We finish with what it costs.
> Hold a search as criteria, never as glued-together text.
