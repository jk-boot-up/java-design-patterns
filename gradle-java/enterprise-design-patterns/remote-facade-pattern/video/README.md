# Remote Facade Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `remote-facade-pattern-explained.mp4` | the video, 1920×1080 |
| `remote-facade-pattern-explained.m4a` | audio only |
| `remote-facade-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Remote Facade pattern in Java, explained with an online store phone app
> whose order screen shows the customer, items, total, address and delivery
> slot. A remote facade gives callers across a network one call that returns
> everything a screen needs and one call that makes a whole change, all or
> nothing, while the objects inside stay small, like posting one letter with
> every question instead of five. We hear why many small remote calls are
> slow, replace them with one facade call, make a change in one call, and
> keep the fine-grained objects inside. We finish with the bill.
