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

> Token Authentication pattern in Java: after signing in you carry a signed
> token saying who you are and until when, and Spring Security checks it on
> every request without looking anything up, like a festival wristband any
> steward can trust. Explained with Spring Security, using an online store
> website running as two server instances. We watch sessions on one server
> fail, issue a token from Spring Security, reject forged and expired tokens,
> and handle signing out early. We finish with the bill: sign in once, carry
> signed proof, and let the framework check it.
