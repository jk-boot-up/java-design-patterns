# Memoization Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `memoization-pattern-explained.mp4` | the video, 1920×1080 |
| `memoization-pattern-explained.m4a` | audio only |
| `memoization-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> When a function always gives the same answer for the same argument, remember each answer the first time and hand it back after that. Memoization remembers the answer a function gave for each argument and returns it again instead of recomputing, which is correct only when the answer depends on nothing but the argument.
