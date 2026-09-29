# Authorization Policy Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `authorization-policy-pattern-explained.mp4` | the video, 1920×1080 |
| `authorization-policy-pattern-explained.m4a` | audio only |
| `authorization-policy-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Make every access decision in one policy, written as rules over roles and attributes, deny anything no rule allows, and have every endpoint ask it. An Authorization Policy makes every access decision in one place, from rules over roles and attributes, and denies whatever no rule allows.
