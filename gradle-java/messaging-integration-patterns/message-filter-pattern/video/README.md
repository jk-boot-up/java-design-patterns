# Message Filter Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `message-filter-pattern-explained.mp4` | the video, 1920×1080 |
| `message-filter-pattern-explained.m4a` | audio only |
| `message-filter-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Put a filter between a channel and a receiver that passes on only the messages matching its rule, so neither the sender nor the receiver has to know about it. A message filter stands between a channel and a receiver and passes on only the messages that match its rule, so the receiver sees only what it wants.
