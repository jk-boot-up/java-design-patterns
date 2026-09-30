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

> Secure Gateway pattern in Java: the services with secrets never face the
> internet; NGINX does, holding no secrets and letting through only a few
> allowed kinds of request, like a bank teller with no vault key. Explained
> with NGINX as the gatekeeper, using an online store order service that holds
> the database password. We watch two tricks export every order, put an NGINX
> gatekeeper in front with a short configuration, allow-list its locations,
> and enforce size and shape limits. We finish with the bill: write the gate's
> rules as an allow-list.
