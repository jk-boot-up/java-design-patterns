# Lock-Free Compare-and-Swap Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `compare-and-swap-pattern-explained.mp4` | the video, 1920×1080 |
| `compare-and-swap-pattern-explained.m4a` | audio only |
| `compare-and-swap-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Read a value, work out the new one, and swap it in only if nobody changed it in the meantime; if they did, read again and retry, with no lock at all. Compare-and-swap changes a value only if it still holds what the thread saw, and otherwise retries, giving correct updates to a single value with no locks.
