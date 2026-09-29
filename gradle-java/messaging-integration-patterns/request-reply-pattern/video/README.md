# Request-Reply with Correlation Identifier Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `request-reply-pattern-explained.mp4` | the video, 1920×1080 |
| `request-reply-pattern-explained.m4a` | audio only |
| `request-reply-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Give every request over a queue a unique ID and a return address, and make every reply name the ID it answers, so replies can arrive in any order and still be matched. Request-Reply with a correlation identifier gives each request a unique ID and a return address, and each reply the ID it answers, so replies are matched whatever order they arrive in.
