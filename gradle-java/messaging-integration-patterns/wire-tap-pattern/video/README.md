# Wire Tap Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `wire-tap-pattern-explained.mp4` | the video, 1920×1080 |
| `wire-tap-pattern-explained.m4a` | audio only |
| `wire-tap-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Wire Tap pattern in Java, explained with an online store checkout that
> sends charges and refunds to the payment service. A wire tap attached to a
> channel sends a copy of every message to a second listener, such as an
> audit log, while the real message carries on untouched, like a call
> recorded for training that pauses when a card number is read out. We see
> why typing logging into services goes wrong, add a wire tap, attach and
> detach it while running, and add a second tap. We finish with the bill:
> watch the traffic from the channel, never from inside the services.
