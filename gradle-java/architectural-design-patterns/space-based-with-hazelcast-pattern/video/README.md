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

> Space-Based Architecture pattern in Java: the busy data lives in the memory
> of the processing units themselves, and the database is written later in the
> background, like market stalls sharing one stock with a partner keeping a
> backup note. Explained with Hazelcast, an open-source in-memory data grid,
> using an online store's kettle flash sale. We see why the database was the
> bottleneck, hold the stock in a real grid as one copy rather than three,
> sell the last kettle exactly once by changing it where it lives, write the
> database behind, and watch what happens when a unit crashes.
