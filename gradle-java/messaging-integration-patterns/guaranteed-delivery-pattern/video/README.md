# Guaranteed Delivery Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `guaranteed-delivery-pattern-explained.mp4` | the video, 1920×1080 |
| `guaranteed-delivery-pattern-explained.m4a` | audio only |
| `guaranteed-delivery-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Guaranteed Delivery pattern in Java: every message is written to disk before
> it is accepted, marked done only after it is delivered, and everything not
> marked done is sent again after a crash, like recorded delivery with a
> ledger and a signature. Explained with an online store that sends an order
> confirmation email for every order through a queue in front of a slow email
> provider. We watch messages kept only in memory disappear, write them to
> disk first, add acknowledgements, and accept that this means at-least-once
> delivery. We finish with the bill.
