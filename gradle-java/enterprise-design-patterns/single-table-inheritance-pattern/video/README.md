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

> Single Table Inheritance pattern in Java: several related classes are stored
> in one database table, a type column says which class each row is, and each
> row leaves the other types' columns empty, like one expenses form with a
> section for every kind of trip. Explained with an online store that sells
> books, food and electronics, each with a code, a name, a price and one field
> of its own. We see why a table per type makes simple questions slow, move to
> one table, turn each row back into its own class, and add a new type. We
> finish with the bill.
