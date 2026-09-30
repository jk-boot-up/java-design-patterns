# Resequencer Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `resequencer-pattern-explained.mp4` | the video, 1920×1080 |
| `resequencer-pattern-explained.m4a` | audio only |
| `resequencer-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Resequencer pattern in Java: when numbered messages arrive out of order, a
> resequencer holds the early ones, releases each sequence strictly in order,
> and has a limit so a lost message cannot block everything forever, like
> reading a letter sent in five muddled envelopes. Explained with an online
> store order page that shows status updates: placed, paid, packed, shipped
> and delivered. We watch updates applied as they arrive go wrong, hold and
> release them in order, and keep one sequence per order. We finish with the
> bill.
