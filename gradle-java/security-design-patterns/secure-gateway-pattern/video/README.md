# Secure Gateway Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `secure-gateway-pattern-explained.mp4` | the video, 1920×1080 |
| `secure-gateway-pattern-explained.m4a` | audio only |
| `secure-gateway-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Put a hardened gatekeeper, holding no secrets and no data, between the internet and the trusted services, and let through only requests of an allowed shape. A Secure Gateway is a secret-free gatekeeper that is the only thing the internet can reach, passing on only requests of an allowed shape.
