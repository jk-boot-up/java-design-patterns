# Blue-Green and Canary with Kubernetes Pattern — Teaching Video

A narrated, slide-based video that shows what Kubernetes adds to the Blue-Green and Canary pattern,
and the failures that are its own.

## Output Files

| File | What it is |
| --- | --- |
| `blue-green-and-canary-with-kubernetes-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `blue-green-and-canary-with-kubernetes-pattern-explained.m4a` | Audio-only version. |
| `blue-green-and-canary-with-kubernetes-pattern-explained.srt` | Subtitles. |
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
| 1 | Blue-Green and Canary with Kubernetes | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Line |  |
| 4 | Replace It Where It Stands |  |
| 5 | Blue And Green |  |
| 6 | Going Back |  |
| 7 | A Canary |  |
| 8 | Promote In Steps, With A Gate |  |
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
`python3 ../../docs/make_narration.py --force blue-green-and-canary-with-kubernetes`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `blue-green-and-canary-with-kubernetes-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Blue-Green and Canary release patterns in Java, explained with a real
> Kubernetes cluster. On Kubernetes, blue-green is a change to a service's
> selector between two deployments, and a canary is a change to the replica
> counts of two deployments behind one service. Using an online store's
> checkout, we watch a real cluster fail every request while a release is
> replaced in place, then make a real switch and a real switch back, let the
> cluster itself spread a canary, and halt a bad release at a gate. We
> finish with the bill: running pods for two releases at once.
