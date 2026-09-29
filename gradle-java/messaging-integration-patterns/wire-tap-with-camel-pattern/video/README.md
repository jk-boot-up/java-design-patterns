# Wire Tap with Apache Camel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `wire-tap-with-camel-pattern-explained.mp4` | the video, 1920×1080 |
| `wire-tap-with-camel-pattern-explained.m4a` | audio only |
| `wire-tap-with-camel-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Build the wire tap with Apache Camel: wireTap() sends a copy of every payment to an audit route on its own thread, and onPrepare() makes sure the copy is truly a copy. With Camel, a wire tap is one `wireTap()` step that copies each message to a side route on its own thread; `onPrepare()` makes the copy independent.
