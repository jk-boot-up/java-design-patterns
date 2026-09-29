# Template Method with Spring Pattern — Teaching Video

A narrated, slide-based video that shows what Spring Boot adds to the Template Method pattern,
and the failures that are its own.

## Output Files

| File | What it is |
| --- | --- |
| `template-method-with-spring-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `template-method-with-spring-pattern-explained.m4a` | Audio-only version. |
| `template-method-with-spring-pattern-explained.srt` | Subtitles. |
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
| 1 | Template Method with Spring | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Line |  |
| 4 | Plain JDBC Leaks |  |
| 5 | The Template Closes On Every Path |  |
| 6 | What Is Ours |  |
| 7 | Exceptions, Translated |  |
| 8 | What The Template Decides |  |
| 9 | A Transaction Is A Template Too |  |
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
`python3 ../../docs/make_narration.py --force template-method-with-spring`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `template-method-with-spring-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Learn the Template Method pattern in Java with Spring Boot, in the same
> online shop. A template owns the fixed steps of a task and leaves one step
> for you to fill in, like a car wash that always soaps, rinses and dries
> while you only pick the extras. We hear plain database code leak a
> connection, then run the same query through Spring's JDBC template, which
> closes it on every path and translates the exceptions. Then a transaction
> template undoes a half-finished checkout. A Spring template owns the fixed
> steps, and quietly makes some decisions for you.
