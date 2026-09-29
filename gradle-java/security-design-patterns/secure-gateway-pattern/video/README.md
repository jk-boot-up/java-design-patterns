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

> Secure Gateway pattern in Java, also called the Gatekeeper, explained with
> an online store order service that holds the database password. The
> services holding secrets never face the internet; a separate gatekeeper
> does, holding no secrets and letting through only requests of a few
> allowed shapes, like a bank teller with no key to the vault. We watch two
> tricks export every order from a service facing the internet, put a
> gatekeeper in front, write an allow-list, and add size and shape limits.
> We finish with the bill: let only a gate with nothing to steal face the
> internet.
