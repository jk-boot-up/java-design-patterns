# Test Double Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `test-double-pattern-explained.mp4` | the video, 1920×1080 |
| `test-double-pattern-explained.m4a` | audio only |
| `test-double-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> A test double stands in for something your code depends on, so a test can run fast, offline, without real money, and ask exactly the question it needs. A test double takes the place of something your code depends on, so a test can run fast and offline and ask one precise question: a dummy for "unused", a stub for "what if", a spy for "what was called", a mock for "never anything else", and a fake for "the whole journey".
