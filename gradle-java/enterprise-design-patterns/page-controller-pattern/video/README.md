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

> Page Controller pattern in Java, explained with an online store web site
> that has a product page, a basket and a checkout, served by a real web
> server. A page controller is a small class for one page: it reads that
> page's input, decides what to do, and sends the reply, like separate desks
> in a department store that each know only their own job. We watch one
> handler for every page let changes leak between pages, give each page its
> own controller, keep errors on their own page, and add a new page. We
> finish with the bill: a check every page needs is easy to forget.
