# Page Controller with Spring MVC Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `page-controller-with-spring-mvc-pattern-explained.mp4` | the video, 1920×1080 |
| `page-controller-with-spring-mvc-pattern-explained.m4a` | audio only |
| `page-controller-with-spring-mvc-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Give each page of the shop its own Spring MVC controller, let Spring convert and check each page's input, add pages without opening the others, and keep checks every page needs in one HandlerInterceptor. With Spring MVC, a page controller is a @RestController per page, found by annotation, with shared checks in a HandlerInterceptor.
