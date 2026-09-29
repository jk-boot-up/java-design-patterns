# Routing Slip with Apache Camel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `routing-slip-with-camel-pattern-explained.mp4` | the video, 1920×1080 |
| `routing-slip-with-camel-pattern-explained.m4a` | audio only |
| `routing-slip-with-camel-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Build the routing slip with Apache Camel: each order's list of steps is written once into a header, routingSlip() follows it, and dynamicRouter() shows what to use when the next step must be decided on the way. With Camel, a routing slip is a header listing each order's steps, and `routingSlip()` sends the order through them in turn.
