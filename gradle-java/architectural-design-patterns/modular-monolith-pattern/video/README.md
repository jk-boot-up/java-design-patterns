# Modular Monolith Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `modular-monolith-pattern-explained.mp4` | the video, 1920×1080 |
| `modular-monolith-pattern-explained.m4a` | audio only |
| `modular-monolith-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Modular Monolith pattern in Java, explained with an online store that is
> one program holding a catalogue, orders and payments. It is still built
> and deployed as one piece, but inside it is split into modules that each
> own their data and may only be used through their front door, like
> departments in one store that ask at the counter instead of raiding each
> other's stockrooms. We watch open tables let the shop sell one kettle
> twice, add front doors, check the walls automatically, and move a module
> out into its own service. We finish with the bill.
