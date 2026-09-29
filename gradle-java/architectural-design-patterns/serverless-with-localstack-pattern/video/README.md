# Serverless with LocalStack Pattern — Teaching Video

A narrated, slide-based video that shows what LocalStack and AWS Lambda adds to the Serverless pattern,
and the failures that are its own.

## Output Files

| File | What it is |
| --- | --- |
| `serverless-with-localstack-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `serverless-with-localstack-pattern-explained.m4a` | Audio-only version. |
| `serverless-with-localstack-pattern-explained.srt` | Subtitles. |
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
| 1 | Serverless with LocalStack | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Line |  |
| 4 | A Machine That Is Always On |  |
| 5 | A Function Per Event |  |
| 6 | Scale Out, And Back To Zero |  |
| 7 | The Cold Start |  |
| 8 | No Memory Between Calls |  |
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
`python3 ../../docs/make_narration.py --force serverless-with-localstack`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `serverless-with-localstack-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Learn the Serverless pattern in Java with AWS Lambda running on
> LocalStack, using the same online store. We upload a real function once,
> send five orders at the same time and watch five real containers start,
> then watch them disappear when the platform goes quiet, like taxis pulling
> in for a crowd and driving away afterwards. We hear a real cold start, a
> function that forgets what it knew between calls, and a job stopped at its
> time limit. We finish with the honest price of all three.
