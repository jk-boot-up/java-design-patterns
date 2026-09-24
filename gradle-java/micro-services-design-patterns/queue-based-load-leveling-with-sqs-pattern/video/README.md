# Queue-Based Load Leveling with SQS Pattern — Teaching Video

A narrated, slide-based video that teaches Queue-Based Load Leveling on the
real Amazon SQS API, played by LocalStack — the depth a burst of 100 orders
really builds, an order that is taken but only hidden, a slow packer that packs
one order twice, a packer that stops and loses nothing, and a queue with no
limit to set — using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `queue-based-load-leveling-with-sqs-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `queue-based-load-leveling-with-sqs-pattern-explained.m4a` | Audio-only version. |
| `queue-based-load-leveling-with-sqs-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. |

None of these is committed except `poster.png`.

## Rebuilding

```bash
./build_video.sh
```

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

The video itself needs no container runtime; only the demo does.

## How the audio is made

The script does five things in order, and each is there for a reason.

1. **Slides.** `make_slides.py` draws one 1920×1080 picture per scene into `build/`.
2. **Voice.** Each scene's narration is spoken by the macOS voice `Samantha` at 145 words per minute, the pace educational videos settle on.
3. **Cleanup, per scene.** The voice is resampled to 48 kHz with a long filter, a high-pass at 75 Hz removes rumble, and a small lift around 3 kHz makes consonants clearer. There is deliberately no denoiser: synthetic speech has almost no noise floor, and a denoiser ends up removing parts of the voice and leaving it warbling. Each scene gets a short silence at the end, and is padded to a whole number of video frames so the slides and voice never drift apart.
4. **One join, one encode.** Every scene's audio stays lossless until all of them are joined into one track, and only then is it encoded to AAC, once. Encoding each scene separately and joining the results leaves a tiny gap at every join, because each AAC clip carries padding at its start and end.
5. **Levelling, once.** The loudness is measured over the whole narration and then corrected to −16 LUFS, YouTube's target, as one constant gain (`loudnorm`, two passes, linear). Levelling each scene separately would make the volume step at every cut.

At the end the script checks that the audio timeline has no gaps and prints
`audio timeline continuous: N packets, no gaps`. If that line is missing, the
build failed even if an mp4 was produced.

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Queue-Based Load Leveling with SQS | Title card and the definition, through a post office on a busy day |
| 2 | The Scenario | A sale's burst of 100 orders, and a packer that does 10 a round |
| 3 | A Burst Lands On The Queue | Act one: 10 to a request, and the depth SQS reports |
| 4 | The Service's Words | Waiting, depth, in flight, visibility timeout, LocalStack |
| 5 | The Packer Keeps Its Own Pace | Act two: 90 waiting and 10 in flight, and the depth falling by 10 |
| 6 | Where The Orders Live | Four parts, and the order that holds them together |
| 7 | Taken Is Not Removed | Act three: an order handed out a second time |
| 8 | Why Hide, And Not Remove? | The coat-check analogy, and the price of it |
| 9 | A Slow Packer | Act four: one order packed twice |
| 10 | Still Working | Act four, continued: changing visibility, and long polling |
| 11 | The Packer Stops Half Way | Act five: 7 in flight come back, 0 lost |
| 12 | The Bill | Act six: no limit to set, a growing backlog, requests counted |
| 13 | What The Simulation Left Out | The contrast with the plain-Java project |
| 14 | The Verdict | |
| 15 | What Is Real, And When Not | LocalStack 4.14.0 held back, and when a queue is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, then from the `gradle-java`
directory run `python3 docs/make_narration.py --force queue-based-load-leveling-with-sqs`,
then re-run `./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term SQS introduces before using Amazon's name for it, and never points
at a picture the listener cannot see.

## Publishing Notes

Upload `queue-based-load-leveling-with-sqs-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
