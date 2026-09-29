# Process Manager Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `process-manager-pattern-explained.mp4` | the video, 1920×1080 |
| `process-manager-pattern-explained.m4a` | audio only |
| `process-manager-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Put one component in charge of a multi-step process: it keeps each instance's state, sends it to the next step, and decides what happens after every reply, including the unhappy paths. A process manager keeps each instance of a multi-step process, sends it to the next step, and decides what to do after every reply, including undoing work when a step fails.
