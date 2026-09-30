# Hedged Requests Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `hedged-requests-pattern-explained.mp4` | the video, 1920×1080 |
| `hedged-requests-pattern-explained.m4a` | audio only |
| `hedged-requests-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Hedged Requests pattern in Java: if a call has not answered after a short
> wait, the same call goes to a second replica, the first answer wins and the
> other is cancelled, like ringing a shop's other branch when nobody picks up.
> Explained with an online store product page that asks a price service,
> running as several replicas, for each price. We see why the average hides
> slow calls, hedge after fifty milliseconds, hedge at once, and run a real
> race. We finish with the bill: extra load, and requests that must be safe to
> send twice.
