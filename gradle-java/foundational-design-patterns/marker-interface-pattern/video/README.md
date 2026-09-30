# Marker Interface Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `marker-interface-pattern-explained.mp4` | the video, 1920×1080 |
| `marker-interface-pattern-explained.m4a` | audio only |
| `marker-interface-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Marker Interface pattern in Java: a marker interface has no methods at all;
> its name is the whole message, so a class that implements Perishable is
> saying it must travel cold, and the compiler can check it, like a printed
> keep-cold sticker the chilled van insists on. Explained with an online store
> that ships milk and yoghurt with ice packs, mugs in bubble wrap, and kettles
> with nothing special. We watch free-text tags get misspelt, replace them
> with a marker interface, let the compiler do the checking, and see the mark
> passed on to subclasses. We finish with the bill.
