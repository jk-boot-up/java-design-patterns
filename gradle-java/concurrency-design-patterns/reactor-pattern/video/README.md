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

> Reactor pattern in Java: one thread waits for events on many connections at
> once and hands each event to a short handler, so no connection needs a
> thread of its own, like one waiter watching a whole restaurant for raised
> hands. Explained with an online store warehouse stock server that has a
> hundred shop tills connected all day asking short questions. We watch a
> thread per connection waste threads, replace them with one reactor thread,
> write a handler per event, and serve every till from one thread. We finish
> with the bill and the one rule you must never break: every handler must be
> quick.
