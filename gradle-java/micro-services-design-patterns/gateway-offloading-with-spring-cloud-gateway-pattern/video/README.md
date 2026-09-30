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

> Gateway Offloading pattern in Java: checking the caller, limiting how often
> they call and compressing the answer move into the gateway in front of the
> services, like an office reception where the teams upstairs trust that
> everyone in the corridor was checked. Explained with Spring Cloud Gateway,
> using an online store's catalog, cart and orders services. We watch three
> copies of a check drift apart, check once at the gateway, add a token-bucket
> rate limit and compression, and learn that every other door must then be
> locked. We finish with the bill.
