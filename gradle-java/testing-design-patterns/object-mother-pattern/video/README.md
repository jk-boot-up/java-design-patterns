# Object Mother / Test Data Builder Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `object-mother-pattern-explained.mp4` | the video, 1920×1080 |
| `object-mother-pattern-explained.m4a` | audio only |
| `object-mother-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Object Mother and Test Data Builder patterns in Java, explained with an
> online store's tests. Both help tests create the objects they need: an
> Object Mother is a class of ready-made objects with clear names, and a
> Test Data Builder starts from sensible defaults so each test changes only
> what it cares about, like a chef's shelf of ready-made sauces and a cook
> making the usual without onions. We watch test data built by hand bury the
> point, add an Object Mother, see it multiply, and switch to a builder. We
> finish with the bill: a test should only show the details it depends on.
