# Reactor with Netty Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `reactor-with-netty-pattern-explained.mp4` | the video, 1920×1080 |
| `reactor-with-netty-pattern-explained.m4a` | audio only |
| `reactor-with-netty-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Serve a hundred shop tills from one Netty event loop, let the channel pipeline turn bytes into whole questions, spread connections over several event loops, and move slow work off the loop. With Netty, the reactor is an event loop: one thread waiting on many connections, running a pipeline of handlers for each.
