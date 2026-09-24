# Claim Check with S3 Pattern — Teaching Video

A narrated, slide-based video that teaches Claim Check on real Amazon S3 and
SQS APIs, played by LocalStack — a PDF the queue genuinely refuses, a ticket
that brings it back, a key stored twice, a delete that deletes nothing, and
two clocks that are not in step — using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `claim-check-with-s3-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `claim-check-with-s3-pattern-explained.m4a` | Audio-only version. |
| `claim-check-with-s3-pattern-explained.srt` | Subtitles. |
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
| 1 | Claim Check with S3 | Title card and the definition |
| 2 | The Scenario | Checkout, an invoice PDF, and the email service |
| 3 | An Invoice Too Big For The Queue | Act one: the real refusal |
| 4 | The Services' Words | Bucket, object, key, message, LocalStack, through a left-luggage office |
| 5 | Why A Smaller PDF Fails Too | Act one, continued: base64 and the real edge |
| 6 | Send The Ticket, Not The Luggage | Act two |
| 7 | Where The Invoice Lives | Four parts, and the order that holds them together |
| 8 | Luggage Nobody Collected | Act three |
| 9 | The Same Key, Twice | Act four: the checksum catches an overwrite |
| 10 | A Delete That Deletes Nothing | Act four, continued: versioning and delete markers |
| 11 | How Long Each One Waits | Act five: lifecycle rule and retention |
| 12 | The Bill | Act six: requests counted |
| 13 | What The Simulation Left Out | The contrast with the plain-Java project |
| 14 | The Verdict | |
| 15 | What Is Real, And When Not | LocalStack 4.14.0 held back, and when a claim check is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, then from the `gradle-java`
directory run `python3 docs/make_narration.py --force claim-check-with-s3`,
then re-run `./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term S3 and SQS introduce before using Amazon's name for it, and never points
at a picture the listener cannot see.

## Publishing Notes

Upload `claim-check-with-s3-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
