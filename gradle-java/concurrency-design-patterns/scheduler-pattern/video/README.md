# Scheduler Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `scheduler-pattern-explained.mp4` | the video, 1920×1080 |
| `scheduler-pattern-explained.m4a` | audio only |
| `scheduler-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> When threads queue for one shared resource, let a scheduler with a replaceable policy decide whose turn is next, instead of whoever happens to grab the lock. A scheduler makes threads ask for their turn at a shared resource and lets a replaceable policy decide whose turn comes next.
