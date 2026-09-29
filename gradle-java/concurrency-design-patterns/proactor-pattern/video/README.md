# Proactor Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `proactor-pattern-explained.mp4` | the video, 1920×1080 |
| `proactor-pattern-explained.m4a` | audio only |
| `proactor-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Proactor pattern in Java, explained with an online store warehouse that
> asks five suppliers for today's kettle price, each taking a fifth of a
> second to answer. You start slow operations without waiting, hand each a
> completion handler for success and failure, and the system does the
> waiting and calls you back, like buzzers at a food court. We watch asking
> one after another add up, start everything at once, handle results in
> completion handlers, and treat a failure as just another completion. We
> finish with the bill.
