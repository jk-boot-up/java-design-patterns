# Private Class Data Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `private-class-data-pattern-explained.mp4` | the video, 1920×1080 |
| `private-class-data-pattern-explained.m4a` | audio only |
| `private-class-data-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Private Class Data pattern in Java, explained with an online store that
> prints invoices, sometimes with a staff discount shown. The values a class
> must never change move into a separate private data object that cannot be
> changed, so not even the class's own methods can overwrite them, like a
> museum exhibit in a glass case that even the staff cannot alter. We watch
> a method quietly change its own invoice figures, protect them with private
> class data so nothing can write to them, and keep working state beside the
> data where it may change. We finish with the bill and when this is just an
> immutable object.
