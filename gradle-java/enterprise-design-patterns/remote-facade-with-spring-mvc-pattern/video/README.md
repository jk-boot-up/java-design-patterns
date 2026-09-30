# Remote Facade with Spring MVC Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `remote-facade-with-spring-mvc-pattern-explained.mp4` | the video, 1920×1080 |
| `remote-facade-with-spring-mvc-pattern-explained.m4a` | audio only |
| `remote-facade-with-spring-mvc-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Remote Facade pattern in Java: a remote facade gives callers across a
> network a few coarse calls that each do a lot, instead of many small calls
> that each pay for a trip, like giving a waiter your whole order in one
> visit. Explained with Spring MVC, using an online store phone app that shows
> and changes an order. We hear what five round trips cost, return the whole
> screen as JSON in one call, make a change all or nothing, and keep the
> fine-grained objects inside. We finish with what the facade costs.
