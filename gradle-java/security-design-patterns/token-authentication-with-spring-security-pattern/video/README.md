# Token Authentication with Spring Security Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `token-authentication-with-spring-security-pattern-explained.mp4` | the video, 1920×1080 |
| `token-authentication-with-spring-security-pattern-explained.m4a` | audio only |
| `token-authentication-with-spring-security-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Issue a signed JSON Web Token when a customer signs in, and let Spring Security's resource-server support check it on every instance of the shop: signature, expiry and a revoked list, with no session store. With Spring Security, token authentication is a resource-server filter that checks every request's JWT, and an encoder that issues them at sign-in.
