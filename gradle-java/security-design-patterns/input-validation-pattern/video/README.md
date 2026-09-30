# Input Validation Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `input-validation-pattern-explained.mp4` | the video, 1920×1080 |
| `input-validation-pattern-explained.m4a` | audio only |
| `input-validation-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Input Validation pattern in Java: nothing that arrives from outside can be
> trusted, so every field is checked where it enters the program, against
> rules for what is allowed, before anything else uses it, like a post room
> that checks every parcel once at the door. Explained with an online store
> checkout form and its product reviews. We watch trusting the form go wrong,
> check at the boundary, use types that cannot hold a wrong value, and encode
> data on the way out. We finish with the bill: check everything that comes
> in, and encode everything that goes out.
