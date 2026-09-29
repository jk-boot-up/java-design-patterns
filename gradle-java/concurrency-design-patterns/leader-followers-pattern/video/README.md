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

> Let a pool of threads take turns: one leader waits for the next message, hands leadership to a follower as soon as it gets one, and then handles that message itself. Leader/Followers lets a pool of threads take turns: the leader waits for a message, promotes a follower, and handles the message itself, with no dispatcher and no hand-off.
