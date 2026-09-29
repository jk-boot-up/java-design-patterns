# Servant Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `servant-pattern-explained.mp4` | the video, 1920×1080 |
| `servant-pattern-explained.m4a` | audio only |
| `servant-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Put behaviour that many unrelated classes need into one separate helper, the servant, which works on anything that offers a small interface. A servant is a separate class that performs one job for many unrelated classes, each of which only offers a small interface with the facts the job needs.
