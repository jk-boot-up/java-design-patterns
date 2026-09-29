# Space-Based Architecture with Hazelcast Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `space-based-with-hazelcast-pattern-explained.mp4` | the video, 1920×1080 |
| `space-based-with-hazelcast-pattern-explained.m4a` | audio only |
| `space-based-with-hazelcast-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Keep the shop's stock in a real Hazelcast data grid spread across three processing units, sell with an entry processor that runs on the key's owner, write the database behind the scenes, and survive a unit crashing. With Hazelcast, a space-based design keeps data in a partitioned in-memory grid with backups, runs changes on each key's owner, and writes the database behind.
