# Extension Object Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `extension-object-pattern-explained.mp4` | the video, 1920×1080 |
| `extension-object-pattern-explained.m4a` | audio only |
| `extension-object-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Extension Object pattern in Java, explained with an online store that
> sells downloadable e-books, kettles with a warranty, plain mugs, and later
> coffee subscriptions. The core class stays small, other code attaches
> extra roles to individual objects, and code that needs a role asks whether
> the object has it, like visas added to a passport that a border guard
> checks without the passport ever being reprinted. We watch one product
> class grow a field for everything, shrink it to a core with roles, ask for
> a role safely, and add a new role without touching the core. We finish
> with the bill.
