# Secure Gateway with NGINX Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `secure-gateway-with-nginx-pattern-explained.mp4` | the video, 1920×1080 |
| `secure-gateway-with-nginx-pattern-explained.m4a` | audio only |
| `secure-gateway-with-nginx-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Put a real NGINX in front of the shop's order service as the gatekeeper: an allow-list of locations, limit_except for methods, client_max_body_size for size, and proxy_set_header to strip internal headers, with no secrets on the gate. With NGINX, a secure gateway is a secret-free reverse proxy whose configuration allow-lists locations and methods, limits size and strips internal headers.
