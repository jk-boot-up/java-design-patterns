# Half-Sync/Half-Async Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `half-sync-half-async-pattern-explained.mp4` | the video, 1920×1080 |
| `half-sync-half-async-pattern-explained.m4a` | audio only |
| `half-sync-half-async-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Split the work in two: a fast asynchronous half that only accepts events and queues them, and a synchronous half of plain threads that take from the queue and do the slow, blocking work. Half-Sync/Half-Async splits a system into a non-blocking half that accepts and queues events and a blocking half of plain workers that process them, joined by a bounded queue.
