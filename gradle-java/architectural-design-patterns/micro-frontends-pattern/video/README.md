# Micro-Frontends Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `micro-frontends-pattern-explained.mp4` | the video, 1920×1080 |
| `micro-frontends-pattern-explained.m4a` | audio only |
| `micro-frontends-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Micro-Frontends pattern in Java: the page is split into parts, each owned,
> built and released by one team, and assembled with a fallback when a part
> fails, like newspaper desks that each write their own pages. Explained with
> an online store product page built by three teams: the product, a basket
> summary, and recommendations. We watch one front end for everything fail as
> a whole, let each team serve its part, keep a failure inside its slot, and
> release parts independently. We finish with the bill. One part failing never
> takes down the rest.
