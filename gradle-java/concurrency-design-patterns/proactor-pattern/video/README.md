# Proactor Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `proactor-pattern-explained.mp4` | the video, 1920×1080 |
| `proactor-pattern-explained.m4a` | audio only |
| `proactor-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Start slow operations without waiting for them, and give each one a completion handler that the system calls when it finishes, successfully or not. A proactor starts slow operations without waiting and lets the system call a completion handler, or a failure handler, when each finishes.
