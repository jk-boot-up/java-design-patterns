# Table Data Gateway with JdbcTemplate Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `table-data-gateway-with-jdbc-template-pattern-explained.mp4` | the video, 1920×1080 |
| `table-data-gateway-with-jdbc-template-pattern-explained.m4a` | audio only |
| `table-data-gateway-with-jdbc-template-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Table Data Gateway pattern in Java: one class holds all the SQL for one
> table and everyone else asks it, while JdbcTemplate takes care of the
> database plumbing, like a library desk that fetches and returns books the
> same careful way every time. Explained with Spring's JdbcTemplate, using an
> online store's product table. We watch hand-written JDBC leak connections,
> rebuild the gateway on JdbcTemplate, turn errors into exceptions that mean
> something, and update stock in one statement. We finish with the bill.
