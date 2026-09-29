# Consumer-Driven Contract with Pact Pattern — Teaching Video

A narrated, slide-based video that shows what Pact adds to the Consumer-Driven Contract pattern,
and the failures that are its own.

## Output Files

| File | What it is |
| --- | --- |
| `consumer-driven-contract-with-pact-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `consumer-driven-contract-with-pact-pattern-explained.m4a` | Audio-only version. |
| `consumer-driven-contract-with-pact-pattern-explained.srt` | Subtitles. |
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
| 1 | Consumer-Driven Contract with Pact | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Line |  |
| 4 | Nobody Told The Consumer |  |
| 5 | The Consumer Writes A Pact |  |
| 6 | The Provider Replays The Pacts |  |
| 7 | The Rename Is Caught |  |
| 8 | Adding Is Safe |  |
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
`python3 ../../docs/make_narration.py --force consumer-driven-contract-with-pact`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `consumer-driven-contract-with-pact-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Consumer-Driven Contract pattern in Java, explained with Pact. A
> consumer's test writes a pact file, and the provider's build replays that
> file against the real service and fails on any difference. With an online
> store's price service and checkout, we watch a field rename break checkout
> in production, let two consumers write real pact files, replay them over
> real HTTP and pass, then catch the rename before release with the consumer
> named. We confirm that adding a field is safe, and finish with what a pact
> cannot catch: a change of meaning.
