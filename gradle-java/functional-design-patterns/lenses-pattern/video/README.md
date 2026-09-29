# Lenses for Immutable Updates Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `lenses-pattern-explained.mp4` | the video, 1920×1080 |
| `lenses-pattern-explained.m4a` | audio only |
| `lenses-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Pair a getter and a setter for one part of an immutable object into a lens, then join lenses to read or replace a part deep inside, getting a new whole and leaving the old one untouched. A lens pairs a getter and a setter for one part of an immutable whole, and lenses join to update deep inside, returning a new whole.
