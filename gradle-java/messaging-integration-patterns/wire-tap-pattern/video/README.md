# Wire Tap Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `wire-tap-pattern-explained.mp4` | the video, 1920×1080 |
| `wire-tap-pattern-explained.m4a` | audio only |
| `wire-tap-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Attach a tap to a channel that sends a copy of every message to a second listener, such as an audit log, while the real message carries on untouched. A wire tap copies every message on a channel to a second listener, while the original is delivered unchanged, so traffic can be observed without touching senders or receivers.
