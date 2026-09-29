# Single Table Inheritance with JPA Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `single-table-inheritance-with-jpa-pattern-explained.mp4` | the video, 1920×1080 |
| `single-table-inheritance-with-jpa-pattern-explained.m4a` | audio only |
| `single-table-inheritance-with-jpa-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Map the shop's product classes to one table with JPA's @Inheritance(SINGLE_TABLE), let Hibernate write the SQL and pick each row's class from a type column, and compare the SQL with a table per class. With JPA, single table inheritance is @Inheritance(SINGLE_TABLE): one table, a type column, and Hibernate building the right class for each row.
