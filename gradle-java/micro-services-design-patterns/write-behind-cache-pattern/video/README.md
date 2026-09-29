# Write-Behind Cache Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `write-behind-cache-pattern-explained.mp4` | the video, 1920×1080 |
| `write-behind-cache-pattern-explained.m4a` | audio only |
| `write-behind-cache-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Keep changes in memory and answer at once, then save them to the database in batches, and only for data you can afford to lose if the server dies in between. A write-behind cache answers every change from memory at once and saves the changed records to the database later, in batches, one write per record.
