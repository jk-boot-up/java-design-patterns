# Money Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `money-pattern-explained.mp4` | the video, 1920×1080 |
| `money-pattern-explained.m4a` | audio only |
| `money-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> A price is not a number. It is an amount of the smallest coin, plus a currency, and it should never round without being asked. Money keeps a price as a whole number of the smallest coin plus its currency, so arithmetic is exact, currencies cannot be mixed, and rounding only happens when someone decides it should.
