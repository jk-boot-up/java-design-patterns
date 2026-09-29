# Page Object Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `page-object-pattern-explained.mp4` | the video, 1920×1080 |
| `page-object-pattern-explained.m4a` | audio only |
| `page-object-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Wrap each page of a web interface in a class that knows its selectors and its timing, so browser tests speak in the shop's words and a page change is fixed in one place. A Page Object wraps a page in a class that knows its selectors and timing, so tests speak in the shop's words.
