# Write-Through Cache with Redis Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `write-through-cache-with-redis-pattern-explained.mp4` | the video, 1920×1080 |
| `write-through-cache-with-redis-pattern-explained.m4a` | audio only |
| `write-through-cache-with-redis-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Write-Through Cache pattern in Java: every write goes to the database and
> then to the cache before it is finished, so the cache never shows something
> the database does not have, like updating the back-office price list and
> then the shelf tag. Explained with a real Redis cache and a real PostgreSQL
> database, using an online store's prices. We watch a write round the cache
> go stale, write through instead, serve reads from Redis, and handle the
> moment when one of the two refuses a write. We finish with the bill: put a
> limit on how long they can disagree.
