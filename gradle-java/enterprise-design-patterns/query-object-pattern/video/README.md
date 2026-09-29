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

> Represent a search as an object made of criteria, which can write itself as safe SQL with placeholders and can also run over a list in memory. A query object holds a search as a set of criteria that can write themselves as safe SQL with placeholders and can also run over data in memory.
