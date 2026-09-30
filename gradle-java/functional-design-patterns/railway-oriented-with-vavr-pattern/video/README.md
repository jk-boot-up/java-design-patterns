# Railway-Oriented Programming with Vavr Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `railway-oriented-with-vavr-pattern-explained.mp4` | the video, 1920×1080 |
| `railway-oriented-with-vavr-pattern-explained.m4a` | audio only |
| `railway-oriented-with-vavr-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Railway-Oriented Programming in Java: each step runs on the success track
> and a failure switches to the other track so every later step is skipped.
> Explained with Vavr, an open-source functional library that provides the two
> tracks, using an online store checkout. We wrap a throwing library, chain
> the steps with Vavr's Either, skip on failure and catch exceptions with Try,
> recover with map and orElse, and use Validation to report every problem in a
> form at once. Keep failures on their own track, and when checking a form,
> collect them all.
