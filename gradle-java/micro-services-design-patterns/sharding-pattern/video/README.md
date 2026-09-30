# Sharding Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `sharding-pattern-explained.mp4` | the video, 1920×1080 |
| `sharding-pattern-explained.m4a` | audio only |
| `sharding-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Sharding pattern in Java: Sharding splits one large set of data across
> several databases called shards, each row going to a shard chosen from a key
> such as the customer number, like splitting patient records into A to H, I
> to P and Q to Z cabinets. Explained with an online store on Black Friday,
> when orders arrive faster than one database can take them. We watch one
> database fall behind, split it into three shards, keep one customer on one
> shard, and see a question about everyone hit every shard. We finish with the
> bill, including the refiling a fourth shard needs.
