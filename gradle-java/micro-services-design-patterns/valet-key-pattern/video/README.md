# Valet Key Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `valet-key-pattern-explained.mp4` | the video, 1920×1080 |
| `valet-key-pattern-explained.m4a` | audio only |
| `valet-key-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Instead of carrying every upload yourself, give the client a signed key that lets it do one specific thing directly with the storage service, for a few minutes. A valet key is a signed, narrow, short-lived permission that lets a client do one specific thing directly with a storage service, so the application does not carry the data itself.
