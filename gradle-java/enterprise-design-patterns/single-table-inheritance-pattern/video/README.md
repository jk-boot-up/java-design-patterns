# Single Table Inheritance Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `single-table-inheritance-pattern-explained.mp4` | the video, 1920×1080 |
| `single-table-inheritance-pattern-explained.m4a` | audio only |
| `single-table-inheritance-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Store every subclass in one table, with a type column that says which class each row becomes, and leave the columns another type needs empty. Single table inheritance stores every subclass in one table with a type column and a column for every field, leaving unused columns empty.
