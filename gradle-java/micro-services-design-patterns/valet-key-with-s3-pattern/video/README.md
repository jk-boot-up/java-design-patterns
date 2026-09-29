# Valet Key with Amazon S3 Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `valet-key-with-s3-pattern-explained.mp4` | the video, 1920×1080 |
| `valet-key-with-s3-pattern-explained.m4a` | audio only |
| `valet-key-with-s3-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Let customers upload review photos straight to object storage with S3 presigned URLs, signed by the shop with the AWS SDK: one object, an exact size, a few minutes, and nothing else. With S3, a valet key is a presigned URL: a signed, expiring permission for one request, checked by the storage service.
