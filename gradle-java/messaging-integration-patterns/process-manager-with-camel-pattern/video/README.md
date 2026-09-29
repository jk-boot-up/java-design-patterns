# Process Manager with Apache Camel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `process-manager-with-camel-pattern-explained.mp4` | the video, 1920×1080 |
| `process-manager-with-camel-pattern-explained.m4a` | audio only |
| `process-manager-with-camel-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Process Manager pattern in Java with Apache Camel's saga step, using
> online store orders that reserve stock, take payment and ship. A process
> manager runs a journey of several steps from one place and makes sure
> every journey ends in a known state; Camel's saga undoes earlier steps
> when a later one fails, like a travel agent cancelling the hotel and
> flight when the car hire falls through. We watch steps that hand on to
> each other lose track, run the journey as a saga, add a branch, and let
> Camel run the undo steps. We finish with the bill.
