# Active Record Pattern — Teaching Video

A narrated, slide-based video that teaches Active Record, and argues for when not to use it,
using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `active-record-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `active-record-pattern-explained.m4a` | Audio-only version. |
| `active-record-pattern-explained.srt` | Subtitles. |
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
| 1 | Active Record | Title card and the definition |
| 2 | The Scenario | The scenario |
| 3 | A Record That Saves Itself |  |
| 4 | The Pattern |  |
| 5 | Finders On The Class |  |
| 6 | The Rules Are On The Record |  |
| 7 | The Bill: A Rule That Needs The Table |  |
| 8 | The Bill: The Class Is The Table |  |
| 9 | The Bill: Queries You Cannot See |  |
| 10 | How To Recognise It |  |
| 11 | The Verdict |  |
| 12 | What Is Real Here |  |
| 13 | When This Is Too Much |  |
| 14 | Thanks for Watching | The exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force active-record`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `active-record-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Active Record pattern in Java: an active record wraps one database row,
> carries the rules about that row, and knows how to find, save and change
> itself, like a paper form that files itself but must know how the filing
> cabinet works. Explained with an online store order that saves itself. We
> find and save an order in three lines with its rules beside its data, then
> hear three costs: a rule you cannot test without the table, a class that is
> the table, and database queries you cannot see. It is the quickest way to
> get data in and out, and the price is that the class and the table become
> one thing.
