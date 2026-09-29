# Copy-on-Write Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `copy-on-write-pattern-explained.mp4` | the video, 1920×1080 |
| `copy-on-write-pattern-explained.m4a` | audio only |
| `copy-on-write-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Let readers use the current copy with no locks at all, and make every writer copy the whole thing, change the copy, and swap it in. Copy-on-write lets readers use the current version with no locks and makes every writer copy it, change the copy and swap it in.
