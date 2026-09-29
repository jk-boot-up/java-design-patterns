# Write-Through Cache Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `write-through-cache-pattern-explained.mp4` | the video, 1920×1080 |
| `write-through-cache-pattern-explained.m4a` | audio only |
| `write-through-cache-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Send every write through the cache, which writes the database first and then itself before returning, so reads from the cache always match the database. A write-through cache takes every write, writes the database, then updates itself before returning, so reads from it always match the database.
