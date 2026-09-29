# Contract Stub Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `contract-stub-pattern-explained.mp4` | the video, 1920×1080 |
| `contract-stub-pattern-explained.m4a` | audio only |
| `contract-stub-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Make the stub your tests use from the same written contract that the real service is checked against, so the stub and the real service can never quietly drift apart. A Contract Stub is a test stub made from a shared contract that the real service is also checked against, so the two cannot drift apart.
