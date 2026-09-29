# Authorization Policy with Spring Security Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `authorization-policy-with-spring-security-pattern-explained.mp4` | the video, 1920×1080 |
| `authorization-policy-with-spring-security-pattern-explained.m4a` | audio only |
| `authorization-policy-with-spring-security-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Let Spring Security make every access decision in the shop: URL rules first, @PreAuthorize rules beside each endpoint for ownership and refund limits, denyAll() for anything nobody wrote a rule for, and an event for every refusal. With Spring Security, an authorization policy is URL rules that deny by default plus @PreAuthorize rules beside each endpoint, with refusals published as events.
