# Process Manager with Apache Camel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `process-manager-with-camel-pattern-explained.mp4` | the video, 1920×1080 |
| `process-manager-with-camel-pattern-explained.m4a` | audio only |
| `process-manager-with-camel-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Build the process manager with Apache Camel's Saga step: one route owns each order's journey, each step names how to undo itself, and Camel runs the undo steps and a final completion or cancellation route for you. With Camel, a process manager can be a saga: one route runs the journey, each step names its undo, and Camel calls the undo steps and a final completion or cancellation route.
