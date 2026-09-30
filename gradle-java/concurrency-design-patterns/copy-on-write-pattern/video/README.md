# Copy-on-Write Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `copy-on-write-pattern-explained.mp4` | the video, 1920×1080 |
| `copy-on-write-pattern-explained.m4a` | audio only |
| `copy-on-write-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Copy-on-Write pattern in Java: readers use the current version with no locks
> at all, and a writer copies, changes the copy and swaps it in, like a
> restaurant reprinting its menus while diners finish the old ones. Explained
> with an online store that tells a list of listeners about every price
> change: the web page cache, the loyalty service and the phone app. We watch
> a plain list crash when it changes while being read, switch to a
> copy-on-write list, show that readers never lock and see snapshots. We
> finish with what every write costs.
