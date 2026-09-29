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

> Write-Behind Cache pattern in Java, explained with an online store where
> customers change their shopping carts all the time. A write-behind cache
> keeps each change in fast memory and answers straight away, then saves the
> changes to the database a few seconds later in one batch, so a record that
> changed ten times is saved once, like a document that autosaves every few
> minutes. We compare writing every change, write behind, keep working while
> the database is down, and lose changes in a crash before the flush. Answer
> now, save in a moment, and only for what you can afford to lose.
