# Immutable Object Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `immutable-object-pattern-explained.mp4` | the video, 1920×1080 |
| `immutable-object-pattern-explained.m4a` | audio only |
| `immutable-object-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Immutable Object pattern in Java, explained with an online store that
> passes addresses and price lists everywhere, where orders keep a shipping
> address and checkout reads the prices. An immutable object can never
> change after it is made; to change something you make a new object, and
> everyone holding the old one still sees it exactly as it was, like a
> printed till receipt rather than a café whiteboard. We watch a shared
> address change under an order, a price list change while being read, and
> an object get lost in a set, then fix all three with immutable objects. We
> finish with the bill.
