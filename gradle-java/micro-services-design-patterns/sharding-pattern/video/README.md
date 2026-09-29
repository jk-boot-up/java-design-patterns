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

> Split one large table across several databases by a key, such as the customer number, so each database holds and serves only its share. Sharding splits one large table across several databases by a key, so each holds and serves only its share, with a router that picks the shard from the key.
