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

> Single Table Inheritance pattern in Java: several related classes live in
> one database table with a type column saying which class each row is, like
> one stock book with a word at the start of each line naming the kind of
> item. Explained with JPA and Hibernate, using an online store's books,
> electronics and food. We read the SQL Hibernate writes for a table per class
> and for one table, watch each row come back as its own class, and add a new
> type. We finish with the bill: a rule the database can no longer keep.
> Always look at the SQL.
