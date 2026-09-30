# Write-Through Cache Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `write-through-cache-pattern-explained.mp4` | the video, 1920×1080 |
| `write-through-cache-pattern-explained.m4a` | audio only |
| `write-through-cache-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Write-Through Cache pattern in Java: every write goes through the cache,
> which writes the database and then its own copy before saying the write is
> done, so cache reads always match the database, like a supermarket that
> changes the shelf label the moment it changes the till price. Explained with
> an online store product page that reads prices from a cache while a nightly
> job changes them. We watch a write that goes round the cache leave a stale
> price, switch to write-through, enjoy fast reads, and handle a refused
> write. We finish with the bill.
