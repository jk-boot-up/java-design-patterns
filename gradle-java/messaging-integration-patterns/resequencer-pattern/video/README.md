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

> When numbered messages can arrive out of order, hold the early ones and release each sequence strictly in order, with a limit so a lost message cannot block everything for ever. A resequencer holds messages that arrive early and releases each sequence strictly in order, giving up on a gap after a limit.
