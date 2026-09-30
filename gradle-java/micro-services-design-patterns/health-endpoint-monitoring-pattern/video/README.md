# Health Endpoint Monitoring Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `health-endpoint-monitoring-pattern-explained.mp4` | the video, 1920×1080 |
| `health-endpoint-monitoring-pattern-explained.m4a` | audio only |
| `health-endpoint-monitoring-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Health Endpoint Monitoring pattern in Java: each copy answers a small web
> address with two answers: am I alive, and if not restart me; and am I ready,
> and if not stop sending me work, like a restaurant host who sends a fainted
> waiter home but only stops giving tables to one whose kitchen has run out of
> gas. Explained with an online store checkout service running as three
> copies. We watch an open port lie about health, add liveness and readiness
> checks, and see a liveness check that is too deep restart copies for
> nothing. Alive is not the same as ready.
