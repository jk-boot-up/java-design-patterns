# Table-Driven State Machine Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `table-driven-state-machine-pattern-explained.mp4` | the video, 1920×1080 |
| `table-driven-state-machine-pattern-explained.m4a` | audio only |
| `table-driven-state-machine-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Table-Driven State Machine pattern in Java: every allowed move is one row in
> a table, from this status on this action to that status, and anything not in
> the table is refused, like an airport's chart of check-in, security and
> gate. Explained with online store orders that move from placed to paid,
> shipped and delivered, and can be cancelled or refunded. We watch scattered
> if statements hide missing rules, replace them with one table, refuse wrong
> moves, and add a rule in two lines. We finish with what the table does not
> do for you.
