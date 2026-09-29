# Event-Carried State Transfer Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `event-carried-state-transfer-pattern-explained.mp4` | the video, 1920×1080 |
| `event-carried-state-transfer-pattern-explained.m4a` | audio only |
| `event-carried-state-transfer-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Event-Carried State Transfer pattern in Java, explained with an online
> store where a customer service owns the addresses and a shipping service
> prints delivery labels. When data changes, the new data travels in the
> event itself, so every service that cares keeps its own copy and never
> calls the owner back, like a change-of-address card with the address on
> it. We watch a thin event force a call back, put the address in the event,
> see the copy lag behind, and handle events out of order. We finish with
> the bill: send the new data, not just the news.
