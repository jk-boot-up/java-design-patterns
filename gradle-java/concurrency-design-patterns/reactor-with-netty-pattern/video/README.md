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

> Reactor pattern in Java: one thread waits on many connections at once and
> calls each connection's handler when something happens, like one fast waiter
> covering many tables. Explained with Netty, the open-source networking
> library underneath much of the Java world, whose event loops are reactors.
> Using an online store's tills asking a stock server short questions, we
> serve a hundred tills from one event loop, let the pipeline handle half-sent
> questions, serve everyone at once, and add more event loops. We finish with
> the bill and the one rule you must never break: nothing on the loop may ever
> block.
