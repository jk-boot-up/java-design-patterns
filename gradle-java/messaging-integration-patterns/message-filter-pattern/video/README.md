# Message Filter Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `message-filter-pattern-explained.mp4` | the video, 1920×1080 |
| `message-filter-pattern-explained.m4a` | audio only |
| `message-filter-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Message Filter pattern in Java: a filter sits between the channel and one
> receiver and passes on only the messages that match its rule, without sender
> or receiver knowing, like an email spam filter. Explained with an online
> store that publishes every order on one channel while a gift-wrap service
> and a loyalty service each care about only some of them. We watch everything
> go to everyone, put a filter in front of each receiver, chain filters
> together, and change a rule. We finish with the bill: never lose track of
> what a filter drops.
