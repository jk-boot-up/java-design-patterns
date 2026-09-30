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

> Contract Stub pattern in Java: the stub is built from a written contract,
> and the real service is checked against the same contract, so the two cannot
> drift apart, like a fire drill run from a floor plan the builders must keep
> current. Explained with WireMock, a stub server that answers real web
> requests, using an online store checkout calling another team's payment
> service. We watch a stub drift, build the WireMock stub from the contract,
> verify the provider against it, and make the stub strict about what it
> accepts. We finish with the bill.
