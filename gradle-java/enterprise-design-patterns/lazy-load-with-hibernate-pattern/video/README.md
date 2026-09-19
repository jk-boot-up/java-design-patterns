# Lazy Load with Hibernate Pattern — Teaching Video

A narrated, slide-based video that explains LazyInitializationException from its mechanism,
using the hand-built Lazy Load project's store over real Hibernate.

## Output Files

| File | What it is |
| --- | --- |
| `lazy-load-with-hibernate-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `lazy-load-with-hibernate-pattern-explained.m4a` | Audio-only version. |
| `lazy-load-with-hibernate-pattern-explained.srt` | Subtitles. |
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
| 1 | Lazy Load with Hibernate | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Annotation |  |
| 4 | One Word Makes It Lazy |  |
| 5 | The Exception |  |
| 6 | What Is In The Field |  |
| 7 | Fix One: Keep The Session Open |  |
| 8 | Fix Two: Fetch It In The Same Query |  |
| 9 | Fix Three: Ask For What You Need |  |
| 10 | The Fix Not On The List |  |
| 11 | Where You Have Met This |  |
| 12 | What Was Used |  |
| 13 | What Is Real Here |  |
| 14 | When This Is Too Much |  |
| 15 | Thanks for Watching | The batch-size exercise |

Scene 15 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force lazy-load-with-hibernate`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `lazy-load-with-hibernate-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
