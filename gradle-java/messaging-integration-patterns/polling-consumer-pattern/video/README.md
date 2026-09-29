# Polling Consumer Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `polling-consumer-pattern-explained.mp4` | the video, 1920×1080 |
| `polling-consumer-pattern-explained.m4a` | audio only |
| `polling-consumer-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Let the consumer decide when to take messages: each time it is ready, it asks the queue for as many as it can handle, and everything else waits safely in the queue. A polling consumer takes messages from a queue when it is ready, as many as it can handle, so it sets its own pace and can pause without losing anything.
