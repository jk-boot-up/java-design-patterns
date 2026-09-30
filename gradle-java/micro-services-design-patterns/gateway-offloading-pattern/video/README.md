# Gateway Offloading Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `gateway-offloading-pattern-explained.mp4` | the video, 1920×1080 |
| `gateway-offloading-pattern-explained.m4a` | audio only |
| `gateway-offloading-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Gateway Offloading pattern in Java: chores every service needs on every
> request, such as checking who the caller is, limiting callers who send too
> much, and compressing the answer, move into the gateway in front of them, so
> they are done once and the same way for everyone, like visitors signing in
> at reception instead of at every team's door. Explained with an online store
> running catalog, cart and orders services. We watch three copies of a
> sign-in check drift apart, then check once at the gateway, add rate limiting
> and compression there. We finish with the bill.
