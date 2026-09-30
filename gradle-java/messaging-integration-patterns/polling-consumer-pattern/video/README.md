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

> Polling Consumer pattern in Java: a polling consumer decides when to take
> messages, asking the queue for as many as it can handle each time it is
> ready while the rest wait safely, like collecting letters from a post office
> box instead of answering the doorbell. Explained with an online store
> warehouse whose label printer can only print so fast while orders arrive in
> bursts. We watch orders pushed at the printer overwhelm it, switch to
> polling, pause safely, and decide how often to poll. We finish with the
> bill.
