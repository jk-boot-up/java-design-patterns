# Asynchronous Request-Reply Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `async-request-reply-pattern-explained.mp4` | the video, 1920×1080 |
| `async-request-reply-pattern-explained.m4a` | audio only |
| `async-request-reply-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> When work takes longer than a caller can wait, accept the request at once, hand back a link to check, and let the caller come back for the result. Asynchronous Request-Reply accepts slow work at once with 202 and a status link, lets the caller check back when told, and sends it on to the result when the work is done.
