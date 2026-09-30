# Process Manager Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `process-manager-pattern-explained.mp4` | the video, 1920×1080 |
| `process-manager-pattern-explained.m4a` | audio only |
| `process-manager-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Process Manager pattern in Java: a process manager takes charge of a
> multi-step process: it tracks where each case is, sends it to the next step,
> and decides what happens after every reply, including when something goes
> wrong, like a wedding planner who calls a backup florist. Explained with an
> online store where each order must be reserved, paid for and shipped. We
> watch a simple chain of steps lose track, let a process manager run each
> order, add a branch, and handle the unhappy path. We finish with the bill.
