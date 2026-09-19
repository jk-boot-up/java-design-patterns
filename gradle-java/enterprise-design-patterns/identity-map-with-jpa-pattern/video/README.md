# Identity Map with JPA Pattern — Teaching Video

A narrated, slide-based video that teaches the persistence context as an identity map,
using the hand-built Identity Map project's customer and order over real JPA.

## Output Files

| File | What it is |
| --- | --- |
| `identity-map-with-jpa-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `identity-map-with-jpa-pattern-explained.m4a` | Audio-only version. |
| `identity-map-with-jpa-pattern-explained.srt` | Subtitles. |
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
| 1 | Identity Map with JPA | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Annotation |  |
| 4 | Two Annotations |  |
| 5 | One Persistence Context |  |
| 6 | The Order's Customer |  |
| 7 | Both Changes Are Kept |  |
| 8 | The Failure Of Its Own: Two Contexts |  |
| 9 | A Detached Change Is Not Saved |  |
| 10 | Cost: The Context Is A Cache |  |
| 11 | Cost: It Holds References |  |
| 12 | Where You Have Met This |  |
| 13 | What Was Used |  |
| 14 | What Is Real Here |  |
| 15 | When This Is Too Much |  |
| 16 | Thanks for Watching | The merge exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force identity-map-with-jpa`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `identity-map-with-jpa-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
