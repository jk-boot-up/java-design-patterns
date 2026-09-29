# Cell-Based Architecture Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `cell-based-pattern-explained.mp4` | the video, 1920×1080 |
| `cell-based-pattern-explained.m4a` | audio only |
| `cell-based-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Cell-Based Architecture pattern in Java, explained with an online store
> where thirty customers check out. The whole back end runs as several
> complete, independent copies called cells, each serving its own share of
> customers, so a failure or a bad release only ever reaches one cell, like
> branches of a restaurant chain with their own kitchens. We watch one
> shared stack fail everyone at once, split it into cells, see the blast
> radius shrink, and grow by adding a cell. We finish with what all those
> copies cost. Run small, complete copies, so any problem stays small.
