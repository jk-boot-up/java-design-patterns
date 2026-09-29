# Table Data Gateway Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `table-data-gateway-pattern-explained.mp4` | the video, 1920×1080 |
| `table-data-gateway-pattern-explained.m4a` | audio only |
| `table-data-gateway-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Give each database table one class that holds all of its SQL, so the rest of the program asks plain questions and never writes SQL itself. A table data gateway is one class per table that holds all of that table's SQL, so the rest of the program asks plain questions and gets plain records back.
