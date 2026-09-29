# Feature Toggle with flagd Pattern — Teaching Video

A narrated, slide-based video that shows what flagd and OpenFeature adds to the Feature Toggle pattern,
and the failures that are its own.

## Output Files

| File | What it is |
| --- | --- |
| `feature-toggle-with-flagd-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `feature-toggle-with-flagd-pattern-explained.m4a` | Audio-only version. |
| `feature-toggle-with-flagd-pattern-explained.srt` | Subtitles. |
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
| 1 | Feature Toggle with flagd | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Line |  |
| 4 | Deploying Is Releasing |  |
| 5 | Deploy Dark, Switch Later |  |
| 6 | Switch On For Some |  |
| 7 | The Kill Switch |  |
| 8 | When flagd Cannot Be Reached |  |
| 9 | The Bill |  |
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
`python3 ../../docs/make_narration.py --force feature-toggle-with-flagd`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `feature-toggle-with-flagd-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Learn the Feature Toggle pattern in Java with flagd and OpenFeature. With
> flagd, a flag is an entry in a file that a daemon watches, and the
> application asks the daemon whether a flag is on for a given customer.
> Using an online store's gift-wrap feature, we watch a real flag daemon
> serve a flag that is off, edit the file and see the daemon notice by
> itself, roll out to a share of customers and to named testers, pull a kill
> switch, and fall back safely when the daemon is stopped. We finish with
> the bill.
