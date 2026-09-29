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

> After sign-in, give the client a signed token that says who they are and when it expires, so any server holding the key can check it without a shared session store. Token Authentication gives the client a signed statement of who it is and until when, which any server with the key can check on its own.
