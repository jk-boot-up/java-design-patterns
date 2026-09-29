# Event-Carried State Transfer Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `event-carried-state-transfer-pattern-explained.mp4` | the video, 1920×1080 |
| `event-carried-state-transfer-pattern-explained.m4a` | audio only |
| `event-carried-state-transfer-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Put the changed data itself in the event, so each service that cares can keep its own copy and never has to call the owner back. Event-Carried State Transfer puts the changed data in the event, so listeners keep their own copies and never call the owner back.
