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

> Put a broker between clients and services: services register by name, clients call by name, and the broker finds the service and forwards the call. A broker sits between clients and services, lets services register by name and forwards clients' calls by name, so neither side needs the other's address.
