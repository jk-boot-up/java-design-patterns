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

> Hedged Requests pattern in Java: if a call has not answered after a short
> wait, the same call is sent again, the first answer is used and the other is
> cancelled, like ringing a second branch and hanging up on the first.
> Explained with gRPC, which can hedge for you as a setting, using an online
> store product page asking a price service for each price. We cut the slow
> tail with one hedging policy, watch gRPC cancel the loser, hedge at once,
> and see why placing an order must never be hedged. Only hedge questions that
> are safe to ask twice.
