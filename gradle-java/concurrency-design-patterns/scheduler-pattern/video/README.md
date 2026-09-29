# Scheduler Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `scheduler-pattern-explained.mp4` | the video, 1920×1080 |
| `scheduler-pattern-explained.m4a` | audio only |
| `scheduler-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Scheduler pattern in Java, explained with an online store warehouse where
> six packing stations share one label printer and express orders must catch
> the afternoon van. When many threads wait for one shared resource, a
> scheduler decides whose turn is next by a policy that can be swapped
> without touching anything else, like a triage nurse deciding by urgency.
> We see why a fair lock serves the wrong job first, put express orders
> first, make the policy replaceable, and make sure nobody waits forever. We
> finish with the bill.
