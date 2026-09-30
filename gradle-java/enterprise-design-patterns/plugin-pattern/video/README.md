# Plugin Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `plugin-pattern-explained.mp4` | the video, 1920×1080 |
| `plugin-pattern-explained.m4a` | audio only |
| `plugin-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Plugin pattern in Java: the code asks for what it needs by interface, a
> configuration file per environment names the class that plays each part, and
> one factory creates it, like a theatre cast sheet that names tonight's
> actors without changing the script. Explained with an online store that runs
> in development, staging and production, where only production may charge
> real cards or send real emails. We watch scattered environment choices go
> wrong, load plugins from configuration, add an environment with no code, and
> catch mistakes at startup. We finish with what you give up.
