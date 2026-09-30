# Page Object Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `page-object-pattern-explained.mp4` | the video, 1920×1080 |
| `page-object-pattern-explained.m4a` | audio only |
| `page-object-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Page Object pattern in Java: a page object is a class for one page that
> knows how to find its boxes and buttons and how long it takes to update, so
> the tests only say what a shopper does, like a hotel concierge who knows the
> taxi firm's number. Explained with an online store checkout page and the
> automated browser tests that check it. We watch tests full of selectors
> break when one button is renamed, move them into a page object, and return
> the next page from each action. We finish with the bill.
