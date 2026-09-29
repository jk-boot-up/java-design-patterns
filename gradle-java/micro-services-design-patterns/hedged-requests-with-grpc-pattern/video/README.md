# Hedged Requests with gRPC Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `hedged-requests-with-grpc-pattern-explained.mp4` | the video, 1920×1080 |
| `hedged-requests-with-grpc-pattern-explained.m4a` | audio only |
| `hedged-requests-with-grpc-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Cut the slow tail of price lookups with gRPC's built-in hedging policy: a second attempt after 50 ms, set in the channel's service config, with the losing attempt cancelled by gRPC itself. With gRPC, hedging is a service-config policy: send another attempt after a delay, take the first answer, and cancel the rest.
