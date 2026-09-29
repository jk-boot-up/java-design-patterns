# Request-Reply with Correlation Identifier Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `request-reply-pattern-explained.mp4` | the video, 1920×1080 |
| `request-reply-pattern-explained.m4a` | audio only |
| `request-reply-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Request-Reply pattern with a Correlation Identifier in Java, explained
> with an online store checkout that reserves stock by sending requests over
> a queue to an inventory service that works on several at once. Each
> request gets a unique ID and says where the reply should go, and each
> reply quotes that ID, so replies can return in any order and still be
> matched, like numbered cloakroom tickets. We watch replies matched by
> arrival order go wrong, add correlation IDs and return addresses, and keep
> many requests in flight at once. We finish with the bill.
