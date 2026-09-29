# Broker Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `broker-pattern-explained.mp4` | the video, 1920×1080 |
| `broker-pattern-explained.m4a` | audio only |
| `broker-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Broker pattern in Java, explained with an online store checkout that calls
> a stock service and a price service running as small web servers. A broker
> sits between clients and services: services register with it by name,
> clients call it by name, and the broker finds the service, forwards the
> call and returns the answer, like an old hotel switchboard operator. We
> watch hard-coded addresses break, route calls through a broker, move a
> service without touching the checkout, and spread calls across several
> copies. We finish with the bill. Call services by name, and let the broker
> know where they live.
