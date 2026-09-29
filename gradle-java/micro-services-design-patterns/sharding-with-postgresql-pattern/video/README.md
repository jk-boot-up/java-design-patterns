# Sharding with PostgreSQL Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `sharding-with-postgresql-pattern-explained.mp4` | the video, 1920×1080 |
| `sharding-with-postgresql-pattern-explained.m4a` | audio only |
| `sharding-with-postgresql-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Split the shop's orders across three real PostgreSQL databases by customer number, route every query to the right one, and see what no single database can do for you any more. With PostgreSQL, sharding splits the data across separate databases by a key, and a router in the application sends each query to the right one.
