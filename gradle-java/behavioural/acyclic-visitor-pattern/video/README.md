# Acyclic Visitor Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `acyclic-visitor-pattern-explained.mp4` | the video, 1920×1080 |
| `acyclic-visitor-pattern-explained.m4a` | audio only |
| `acyclic-visitor-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Give every product type its own tiny visitor interface, so each visitor handles only the types it cares about and a new type changes nothing that already exists. An acyclic visitor gives each type its own one-method visitor interface and an empty root, so each visitor handles only the types it chooses and new types change nothing existing.
