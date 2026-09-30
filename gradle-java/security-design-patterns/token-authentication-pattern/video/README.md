# Token Authentication Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `token-authentication-pattern-explained.mp4` | the video, 1920×1080 |
| `token-authentication-pattern-explained.m4a` | audio only |
| `token-authentication-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Token Authentication pattern in Java: after you sign in, the server gives
> you a token that says who you are and when it expires, signed with a secret
> key so any server holding the key can trust it without looking anything up,
> like a festival wristband checked once at the gate. Explained with an online
> store website running on two servers. We watch sessions on one server fail
> on the other, switch to a signed token, reject forged and expired tokens,
> and deal with signing out early. We finish with the bill.
