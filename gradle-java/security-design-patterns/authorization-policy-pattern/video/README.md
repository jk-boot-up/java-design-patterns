# Authorization Policy Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `authorization-policy-pattern-explained.mp4` | the video, 1920×1080 |
| `authorization-policy-pattern-explained.m4a` | audio only |
| `authorization-policy-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Authorization Policy pattern in Java: signing in proves who you are;
> authorization decides what you may do, and a policy makes every one of those
> decisions in one place, from rules about roles and about details such as who
> owns what, refusing anything no rule allows, like a hotel key-card system.
> Explained with an online store that has customers, support staff and an
> admin. We watch checks scattered through every endpoint, see roles alone
> fall short, add rules on attributes, and deny by default. We finish with the
> bill: one place decides, and the answer starts as no.
