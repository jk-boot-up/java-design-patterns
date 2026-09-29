# Reactor Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `reactor-pattern-explained.mp4` | the video, 1920×1080 |
| `reactor-pattern-explained.m4a` | audio only |
| `reactor-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Let one thread wait for events on every connection at once, and hand each event to a short handler, instead of giving every connection a thread that mostly waits. A reactor uses one thread to wait for events on many connections at once and dispatches each event to a short handler.
