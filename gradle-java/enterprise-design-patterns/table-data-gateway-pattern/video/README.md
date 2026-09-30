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

> Table Data Gateway pattern in Java: a table data gateway is one class per
> table that holds all of that table's SQL, and the rest of the program asks
> it plain questions, like bank customers who ask at the counter and never
> enter the vault. Explained with an online store products table holding a
> code, a name, a price and the stock. We watch SQL spread through every
> caller break on a rename, move it into one gateway, fix the rename in one
> place, and decide where the SQL should live. We finish with the bill.
