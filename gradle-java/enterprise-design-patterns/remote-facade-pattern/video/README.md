# Remote Facade Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `remote-facade-pattern-explained.mp4` | the video, 1920×1080 |
| `remote-facade-pattern-explained.m4a` | audio only |
| `remote-facade-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Keep objects fine-grained inside the server, but give remote callers a coarse-grained front that answers a whole screen or makes a whole change in one call. A remote facade gives remote callers coarse-grained calls, a whole screen or a whole change at once, over fine-grained objects that stay unchanged inside.
