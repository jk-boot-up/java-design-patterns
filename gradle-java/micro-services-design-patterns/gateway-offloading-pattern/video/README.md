# Gateway Offloading Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `gateway-offloading-pattern-explained.mp4` | the video, 1920×1080 |
| `gateway-offloading-pattern-explained.m4a` | audio only |
| `gateway-offloading-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Move the chores every service needs, such as sign-in checks, rate limiting and compression, out of the services and into the gateway in front of them, so they are done once and the same way. Gateway Offloading moves the chores every service needs into the gateway in front of them, so they are done once and the same way.
