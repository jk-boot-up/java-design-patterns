# Table-Driven State Machine Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `table-driven-state-machine-pattern-explained.mp4` | the video, 1920×1080 |
| `table-driven-state-machine-pattern-explained.m4a` | audio only |
| `table-driven-state-machine-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Write down every allowed move as a row in one table, from this status on this action to that status, and refuse anything that is not in it. A table-driven state machine keeps every allowed move, from a status on an action to a new status, in one table, and refuses every move that is not in it.
