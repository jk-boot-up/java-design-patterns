# Space-Based Architecture Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `space-based-pattern-explained.mp4` | the video, 1920×1080 |
| `space-based-pattern-explained.m4a` | audio only |
| `space-based-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Give every copy of the application its own in-memory copy of the data, keep the copies in step through a data grid, and update the database in the background, so no request waits for it. Space-based architecture gives each processing unit an in-memory copy of the data, keeps copies in step through a data grid, and updates the database in the background, so requests never wait for it.
