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

> Run the whole system as several complete, independent copies called cells, each serving its own share of customers, so a failure or a bad release only ever reaches one cell. Cell-based architecture runs several complete, independent copies of a system, each serving a fixed share of customers behind a thin router, so failures and releases only reach one cell at a time.
