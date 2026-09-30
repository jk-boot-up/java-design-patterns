# Domain Service Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `domain-service-pattern-explained.mp4` | the video, 1920×1080 |
| `domain-service-pattern-explained.m4a` | audio only |
| `domain-service-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Domain Service pattern from domain-driven design in Java: some rules involve
> several objects and belong to none of them, so a domain service holds the
> rule, keeps no data of its own, and is named in the business's words, like a
> referee applying the rules to two players. Explained with an online store
> where gold customers get ten percent off, a coupon takes five pounds off
> baskets over forty, and the two must not simply add up. We watch copies of
> the rule drift apart, move it into one service that explains itself, and use
> it for every case. We finish with how services can empty your objects.
