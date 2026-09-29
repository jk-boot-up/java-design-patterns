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

> Keep all the product table's SQL in one gateway class built on Spring's JdbcTemplate, which borrows and returns connections, maps rows to records, and turns database errors into meaningful exceptions. With JdbcTemplate, a table data gateway keeps one table's SQL in one class while Spring handles connections, row mapping and error translation.
