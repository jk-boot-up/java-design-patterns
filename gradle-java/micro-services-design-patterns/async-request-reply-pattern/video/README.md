# Asynchronous Request-Reply Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `async-request-reply-pattern-explained.mp4` | the video, 1920×1080 |
| `async-request-reply-pattern-explained.m4a` | audio only |
| `async-request-reply-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Asynchronous Request-Reply pattern in Java: when a job takes longer than a
> caller can wait, the server accepts the request at once, hands back a link
> to check on the job, and that link leads to the result when it is ready,
> like a dry cleaner's ticket you bring back on Thursday. Explained with an
> online store where sellers ask for a monthly sales report that takes about
> six seconds to build. We watch a slow report fail behind a normal request
> even when the work succeeds, then accept it at once with 202 Accepted, check
> back and follow a 303 to the result, and stop a double click from doing the
> work twice. We finish with what the pattern costs.
