# Recipient List with Apache Camel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `recipient-list-with-camel-pattern-explained.mp4` | the video, 1920×1080 |
| `recipient-list-with-camel-pattern-explained.m4a` | audio only |
| `recipient-list-with-camel-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Build the recipient list with Apache Camel: recipientList() asks a routing table, for each order, which endpoints should get a copy, and sends one to each; the table can change while the routes run. With Camel, a recipient list is one `recipientList()` step that asks a routing table for each message's recipients and sends each a copy.
