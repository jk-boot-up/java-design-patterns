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

> Write every price to PostgreSQL and then to a real, shared Redis cache before the write returns, read pages from Redis, and see the one thing the plain version could not: two systems that no transaction spans. With Redis and PostgreSQL, a write-through cache writes every change to the database and then the shared cache before returning, and reads from the cache.
