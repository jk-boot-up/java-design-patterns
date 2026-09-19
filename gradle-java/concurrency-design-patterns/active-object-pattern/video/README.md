# Active Object Pattern — Teaching Video

A narrated, slide-based video that teaches Active Object using this
project's code, assembling four earlier projects.

## Output Files

| File | What it is |
| --- | --- |
| `active-object-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `active-object-pattern-explained.m4a` | Audio-only version. |
| `active-object-pattern-explained.srt` | Subtitles. |
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
| 1 | Active Object | Title card and the definition |
| 2 | The Scenario | Inventory updates from several places |
| 3 | A Monitor — The Caller Waits | A checkout behind a slow import |
| 4 | The Pattern — A Thread And A Mailbox | Calls become messages |
| 5 | The Call Returns At Once | A future, answered later, in order |
| 6 | No Lock At All | One thread owns the state |
| 7 | What It Is Made Of | Four earlier projects, assembled |
| 8 | Cost One — The Mailbox Backs Up | Ten thousand waiting |
| 9 | Cost Two — Errors Arrive Later | The worker's stack, not the caller's |
| 10 | Cost Three — One Worker Is A Ceiling | The same rate for one caller or four |
| 11 | How The Demo Forces It | A gate, a latch, and real work |
| 12 | What The Scheduler Really Does | The honesty rule |
| 13 | Where This Leads, And When It Is Too Much | Actors and event loops |
| 14 | Thanks for Watching | The bounded-mailbox exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force active-object`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `active-object-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
