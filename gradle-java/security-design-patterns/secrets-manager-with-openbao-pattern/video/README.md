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

> Secrets Manager pattern in Java: secrets live in one guarded store, each
> service may read only what its policy allows, and secrets change without a
> rebuild, like safe-deposit boxes that each card opens only its own of.
> Explained with a real OpenBao server, the open-source community fork of
> HashiCorp Vault, using an online store's card-payment key. We move a key out
> of the code, give each service a policy and a token, keep versions and
> rotate the key, and revoke a leaked token at once. We finish with the bill.
