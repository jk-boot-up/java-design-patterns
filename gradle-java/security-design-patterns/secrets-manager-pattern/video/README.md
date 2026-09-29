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

> Secrets Manager pattern in Java, explained with an online store's key for
> its card-payment company. Passwords and keys are kept out of the code in
> one guarded store, each service gets only the secrets it is allowed, every
> read is logged, and a secret can be replaced without rebuilding anything,
> like a hotel key cabinet with a signing-out book. We watch a key hard-
> coded in the source, move it into a manager, rotate it without a rebuild,
> and respond to a leak. We finish with the bill.
