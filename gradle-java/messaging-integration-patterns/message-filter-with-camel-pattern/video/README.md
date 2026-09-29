# Message Filter with Apache Camel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `message-filter-with-camel-pattern-explained.mp4` | the video, 1920×1080 |
| `message-filter-with-camel-pattern-explained.m4a` | audio only |
| `message-filter-with-camel-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Build the message filter with Apache Camel: a filter() step, written in Camel's Simple expression language, in front of each service, with rules that read their settings as each message passes and a discard channel so nothing vanishes unseen. With Camel, a message filter is a `filter()` step with a Simple rule in front of each receiver, and rejects can be sent to a discard channel.
