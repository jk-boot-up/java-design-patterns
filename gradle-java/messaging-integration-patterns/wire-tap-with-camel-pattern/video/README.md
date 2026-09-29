# Wire Tap with Apache Camel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `wire-tap-with-camel-pattern-explained.mp4` | the video, 1920×1080 |
| `wire-tap-with-camel-pattern-explained.m4a` | audio only |
| `wire-tap-with-camel-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Wire Tap pattern in Java with Apache Camel, using an online store's
> payments and the auditors who want a copy of each one. A wire tap sends a
> copy of every message to a side channel while sender and receiver carry on
> as if nothing were listening, like a camera over a shop till that must
> only ever see a copy of the receipt. We tap every payment with one Camel
> step, discover that masking the card number in the tap also changed the
> real payment because it was not a copy after all, fix it with onPrepare,
> and watch the audit stop. We finish with the bill.
