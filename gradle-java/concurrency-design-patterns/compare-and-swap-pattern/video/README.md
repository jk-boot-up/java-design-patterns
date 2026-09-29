# Lock-Free Compare-and-Swap Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `compare-and-swap-pattern-explained.mp4` | the video, 1920×1080 |
| `compare-and-swap-pattern-explained.m4a` | audio only |
| `compare-and-swap-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Lock-Free Compare-and-Swap pattern in Java, explained with an online store
> flash sale: a hundred kettles and eight buyer threads racing for them.
> Compare-and-swap changes a shared value only if it still holds what you
> saw, and if someone changed it first you read it again and retry, with
> nobody waiting on a lock, like booking a concert seat that might just have
> been taken. We watch the shop sell more kettles than it has, fix it slowly
> with a lock, then without one using compare-and-swap, and fold the retry
> loop into one call. We finish with its limits.
