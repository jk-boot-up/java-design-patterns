# Contract Stub with WireMock Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `contract-stub-with-wiremock-pattern-explained.mp4` | the video, 1920×1080 |
| `contract-stub-with-wiremock-pattern-explained.m4a` | audio only |
| `contract-stub-with-wiremock-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Build a real WireMock stub server from a shared contract file for checkout's tests, and replay the same file against the real payment service over HTTP, so the stub and the service can never quietly drift apart. With WireMock, a contract stub is a real HTTP stub server built from a shared contract file that the real service is also checked against.
