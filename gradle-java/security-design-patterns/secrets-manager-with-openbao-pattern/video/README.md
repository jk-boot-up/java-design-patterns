# Secrets Manager with OpenBao Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `secrets-manager-with-openbao-pattern-explained.mp4` | the video, 1920×1080 |
| `secrets-manager-with-openbao-pattern-explained.m4a` | audio only |
| `secrets-manager-with-openbao-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Keep the payment key in a real OpenBao server, the open-source fork of HashiCorp Vault: a policy decides which service may read it, each service has its own token, the key is versioned for rotation, and a leaked token is revoked at once. With OpenBao, secrets live at paths, policies decide who may read them, each service holds a revocable token, and every change is a new version.
