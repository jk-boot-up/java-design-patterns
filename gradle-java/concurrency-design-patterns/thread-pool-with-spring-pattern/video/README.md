# Thread Pool with Spring Pattern — Teaching Video

A narrated, slide-based video that shows what Spring Boot adds to the Thread Pool pattern,
and the failures that are its own.

## Output Files

| File | What it is |
| --- | --- |
| `thread-pool-with-spring-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `thread-pool-with-spring-pattern-explained.m4a` | Audio-only version. |
| `thread-pool-with-spring-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. Not the thumbnail. |

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

## Rebuilding

```bash
./build_video.sh
```

The audio chain is identical across every project in this repository; see
[`../../../architectural-design-patterns/layered-architecture-pattern/video/README.md`](../../../architectural-design-patterns/layered-architecture-pattern/video/README.md)
for the full explanation.

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Thread Pool with Spring | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Line |  |
| 4 | What You Get By Default |  |
| 5 | @Async Moves The Work |  |
| 6 | The Unbounded Queue |  |
| 7 | Bound It |  |
| 8 | The Annotation That Does Nothing |  |
| 9 | Pool Starvation |  |
| 10 | The Verdict |  |
| 11 | How To Recognise It |  |
| 12 | Where You Have Met This |  |
| 13 | What Was Used |  |
| 14 | What Is Real Here |  |
| 15 | When This Is Too Much |  |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force thread-pool-with-spring`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `thread-pool-with-spring-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Learn the Thread Pool pattern in Java with Spring Boot, using the same
> order packing. A pool runs work on a few threads that are created once and
> reused, so a burst of work cannot create a burst of threads, like a
> restaurant that does not hire new waiters in a rush. We hear the pool
> Spring Boot gives you when you configure nothing, watch its queue grow
> without limit, then bound it and hear a real refusal. We also meet two
> failures that belong to Spring: an @Async annotation that silently does
> nothing, and a pool that starves itself. A thread pool you did not
> configure has a queue that never says no.
