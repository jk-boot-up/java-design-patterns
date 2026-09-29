# Service Stub Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `service-stub-pattern-explained.mp4` | the video, 1920×1080 |
| `service-stub-pattern-explained.m4a` | audio only |
| `service-stub-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Service Stub pattern in Java, explained with an online store checkout that
> turns a postcode into an address using a paid outside service. A service
> stub is a small, free stand-in behind the same interface that answers like
> the real service while you develop and test, like a flight simulator that
> can fail an engine on demand but is checked against the real plane. We
> hear what developing against the real service costs, swap in a stub,
> produce awkward cases on demand, and keep the stub honest with a contract
> check. We finish with the bill.
