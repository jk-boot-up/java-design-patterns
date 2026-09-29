# Secrets Manager Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `secrets-manager-pattern-explained.mp4` | the video, 1920×1080 |
| `secrets-manager-pattern-explained.m4a` | audio only |
| `secrets-manager-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Keep passwords and keys out of code and builds, in one guarded store that hands each service only the secrets it is allowed, logs every read, and lets a secret be rotated without a rebuild. A Secrets Manager keeps secrets in one guarded store, grants each service only what it needs, logs every read, and rotates secrets without rebuilds.
