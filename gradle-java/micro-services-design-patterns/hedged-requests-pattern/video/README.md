# Hedged Requests Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `hedged-requests-pattern-explained.mp4` | the video, 1920×1080 |
| `hedged-requests-pattern-explained.m4a` | audio only |
| `hedged-requests-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> If a call has not answered within a short delay, send the same call to a second replica, use whichever answers first, and cancel the other. Hedged Requests sends a second copy of a slow call to another replica after a short delay, and uses whichever answer arrives first.
