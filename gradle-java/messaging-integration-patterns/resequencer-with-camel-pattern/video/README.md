# Resequencer with Apache Camel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `resequencer-with-camel-pattern-explained.mp4` | the video, 1920×1080 |
| `resequencer-with-camel-pattern-explained.m4a` | audio only |
| `resequencer-with-camel-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Resequencer pattern in Java with Apache Camel, whose resequencer is built
> in, using an online store order-tracking page and its status updates. A
> resequencer puts out-of-order messages back in order using the number each
> one carries, like a sorting office that either passes pages on as soon as
> the next arrives or waits for the whole bundle. We watch updates applied
> as they arrive, then compare Camel's stream mode and batch mode and what
> each makes the customer see, handle two orders at once, and decide how
> long to wait for a missing message. We finish with the bill.
