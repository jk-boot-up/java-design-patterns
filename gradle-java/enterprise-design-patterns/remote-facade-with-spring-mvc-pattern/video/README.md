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

> Give the phone app a coarse-grained Spring MVC facade: one GET returns the whole order screen as JSON, one PUT changes the whole delivery all-or-nothing, and a refusal comes back as a standard problem report. With Spring MVC, a remote facade is a thin controller that offers remote callers coarse, screen-sized calls, over fine-grained objects inside.
