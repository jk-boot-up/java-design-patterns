# Content Enricher Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `content-enricher-pattern-explained.mp4` | the video, 1920×1080 |
| `content-enricher-pattern-explained.m4a` | audio only |
| `content-enricher-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Content Enricher pattern in Java, explained with an online store checkout
> that announces each paid order to a warehouse and an email service with a
> message that is missing details. A content enricher looks the details up
> once, adds them to the message and passes the fuller message on, so
> receivers never look anything up themselves, like a post office clerk
> adding the house number and postcode before the postman sees the letter.
> We watch the thin message force every receiver to do its own lookup, add
> an enricher in the middle, and handle a customer who cannot be found. We
> finish with the bill.
