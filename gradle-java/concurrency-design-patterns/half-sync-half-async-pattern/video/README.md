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

> Half-Sync, Half-Async pattern in Java: the work is split into two halves
> joined by a queue: a fast half only accepts and queues events, and a slow
> half of ordinary worker threads does the blocking work, like a restaurant
> host pinning tickets for the cooks. Explained with an online store where
> orders arrive in bursts and each needs slow work: save it, charge the card,
> send an email. We watch blocking work stall the event thread, then build the
> async half and the sync half, and let the queue absorb a burst. We finish
> with the bill, including a full queue.
