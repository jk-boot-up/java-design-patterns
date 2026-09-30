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

> Sharding pattern in Java: data is split across three databases by a key such
> as the customer number, so no single database takes all the load, like a
> library that splits its members across three branches by membership number.
> Explained with real PostgreSQL databases, using an online store's orders on
> Black Friday. We watch one database fall behind, spread the orders over
> three real shards with a jump hash, answer one customer's question from one
> shard, and see a question about everyone hit every shard. We finish with the
> bill: resharding, and databases that each only know their own share.
