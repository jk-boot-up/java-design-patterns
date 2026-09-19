# Sidecar on Kubernetes Pattern — Teaching Video

A narrated, slide-based video that shows what a Kubernetes Pod guarantees a sidecar,
using a plain-Java model. It never depends on a cluster.

## Output Files

| File | What it is |
| --- | --- |
| `sidecar-on-kubernetes-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `sidecar-on-kubernetes-pattern-explained.m4a` | Audio-only version. |
| `sidecar-on-kubernetes-pattern-explained.srt` | Subtitles. |
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
| 1 | Sidecar on Kubernetes | Title card, and the two earlier projects |
| 2 | Read The First Video First |  |
| 3 | Before Any Command: What Kubernetes Is |  |
| 4 | Two Ways To Share |  |
| 5 | Shared By Definition |  |
| 6 | One Lifecycle |  |
| 7 | But Restarts Are Per Container |  |
| 8 | Injection |  |
| 9 | READY 2/2 |  |
| 10 | The Bill, And The Honest Question |  |
| 11 | What The Model Does Not Show |  |
| 12 | Where You Have Met This |  |
| 13 | What Is Real Here |  |
| 14 | When This Is Too Much |  |
| 15 | Thanks for Watching | The second-sidecar exercise |

Scene 15 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force sidecar-on-kubernetes`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `sidecar-on-kubernetes-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
