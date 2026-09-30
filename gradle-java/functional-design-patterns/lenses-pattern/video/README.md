# Lenses for Immutable Updates Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `lenses-pattern-explained.mp4` | the video, 1920×1080 |
| `lenses-pattern-explained.m4a` | audio only |
| `lenses-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Lenses in Java: a lens is a pair of functions for one part of an immutable
> object: one reads the part and the other returns a new object with that part
> replaced, and lenses join to reach deep inside, like a tool for replacing
> the smallest of a set of glued nesting dolls. Explained with an online store
> order that holds a customer who holds a delivery address, all immutable. We
> watch rebuilding by hand go wrong, write one lens, join lenses together, and
> change a value with a function. We finish with what lenses cost.
