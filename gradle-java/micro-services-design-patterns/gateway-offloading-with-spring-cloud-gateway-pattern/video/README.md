# Gateway Offloading with Spring Cloud Gateway Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `gateway-offloading-with-spring-cloud-gateway-pattern-explained.mp4` | the video, 1920×1080 |
| `gateway-offloading-with-spring-cloud-gateway-pattern-explained.m4a` | audio only |
| `gateway-offloading-with-spring-cloud-gateway-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Put a real Spring Cloud Gateway in front of the shop's catalog, cart and orders services, and move the shared chores into it: the sign-in check, a per-customer rate limit, response compression, and stripping a caller's claim to be someone else. With Spring Cloud Gateway, offloading puts the shared chores in a global filter and server settings, so every service behind gets them for free.
