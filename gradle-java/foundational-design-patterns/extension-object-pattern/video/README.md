# Extension Object Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `extension-object-pattern-explained.mp4` | the video, 1920×1080 |
| `extension-object-pattern-explained.m4a` | audio only |
| `extension-object-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Keep the core class small, let other code attach extra roles to individual objects, and let clients ask whether an object has the role they need. An extension object lets code attach extra roles to individual objects and lets clients ask for a role by type, so a core class stays small while new abilities keep arriving.
