# Claim Check Pattern — Teaching Video

A narrated, slide-based video that teaches Claim Check, and argues for when not to use it,
using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `claim-check-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `claim-check-pattern-explained.m4a` | Audio-only version. |
| `claim-check-pattern-explained.srt` | Subtitles. |
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
| 1 | Claim Check | Title card and the definition |
| 2 | The Scenario | The scenario |
| 3 | A Message That Is Too Big |  |
| 4 | The Pattern |  |
| 5 | Send The Ticket, Not The Luggage |  |
| 6 | What The Broker Carries |  |
| 7 | Luggage Nobody Collected |  |
| 8 | Is It The Same Luggage? |  |
| 9 | The Bill |  |
| 10 | How To Recognise It |  |
| 11 | The Verdict |  |
| 12 | What Is Real Here |  |
| 13 | When This Is Too Much |  |
| 14 | Thanks for Watching | The exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force claim-check`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `claim-check-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Claim Check pattern in Java: a claim check stores a large payload somewhere
> cheap and sends only a small ticket through the message broker, and the
> receiver redeems the ticket for the payload, the way you collect a coat from
> a cloakroom. Explained with an online store that must send an invoice PDF to
> another service. We watch a broker refuse a big message, send a ticket
> instead and see how little the broker carries, find luggage nobody
> collected, and catch a changed payload with a checksum. The bill is extra
> steps, and a ticket that must be hard to guess.
