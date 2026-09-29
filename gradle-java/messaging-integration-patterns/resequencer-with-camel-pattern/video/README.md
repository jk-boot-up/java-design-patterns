# Resequencer with Apache Camel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `resequencer-with-camel-pattern-explained.mp4` | the video, 1920×1080 |
| `resequencer-with-camel-pattern-explained.m4a` | audio only |
| `resequencer-with-camel-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Build the resequencer with Apache Camel: resequence() puts order-status updates back in order, either as a stream that releases each update as soon as it can, or as batches that are sorted and released together, with a timeout for updates that never arrive. With Camel, a resequencer is one `resequence()` step that restores order by sequence number, either as a stream with a gap timeout or in sorted batches.
