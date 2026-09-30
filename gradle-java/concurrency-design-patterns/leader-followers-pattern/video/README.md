# Leader/Followers Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `leader-followers-pattern-explained.mp4` | the video, 1920×1080 |
| `leader-followers-pattern-explained.m4a` | audio only |
| `leader-followers-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Leader Followers pattern in Java: the threads take turns: one leader waits
> for the next message, hands leadership to another thread, then handles that
> message itself, like the front taxi at a rank driving off as the next one
> moves up. Explained with an online store order service handling a stream of
> order messages with a pool of threads. We compare it with a dispatcher that
> hands work off, walk through receive, promote and handle, and show every
> thread doing useful work. We finish with the bill, including why message
> order is not kept.
