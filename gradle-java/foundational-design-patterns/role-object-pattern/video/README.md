# Role Object Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `role-object-pattern-explained.mp4` | the video, 1920×1080 |
| `role-object-pattern-explained.m4a` | audio only |
| `role-object-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Keep one core object for the identity, and model each thing it does for a while (buying, selling, referring) as a separate role object that can be added and removed. A role object keeps one core object for an identity and models each activity it performs for a while as a separate object that can be added and removed.
