# Railway-Oriented Programming Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `railway-oriented-pattern-explained.mp4` | the video, 1920×1080 |
| `railway-oriented-pattern-explained.m4a` | audio only |
| `railway-oriented-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Railway-Oriented Programming in Java: picture two tracks, one for success
> and one for failure: every step runs on the success track, and the first
> failure switches the train to the failure track so every later step is
> skipped, like a rejected bag sent down an airport side belt. Explained with
> an online store checkout of four steps. We watch an exception nobody caught
> become an error page, then return results that keep the steps in a straight
> line, switch tracks on failure, reuse plain functions, and find a way back.
> We finish with the bill.
