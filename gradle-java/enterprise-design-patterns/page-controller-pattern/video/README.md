# Page Controller Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `page-controller-pattern-explained.mp4` | the video, 1920×1080 |
| `page-controller-pattern-explained.m4a` | audio only |
| `page-controller-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Give every page of a web site its own small controller that reads that page's input, decides what to do and sends the reply, instead of one handler for everything. A page controller is a small class for one page or action of a web site that reads that page's input, decides what to do and sends the reply.
