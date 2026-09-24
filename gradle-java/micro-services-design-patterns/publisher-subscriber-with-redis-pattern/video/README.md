# Publisher-Subscriber with Redis Pattern — Teaching Video

A narrated, slide-based video that teaches Publisher-Subscriber on a real Redis
server — one publish reaching a listener in another process, the count Redis
hands back, nothing kept for a latecomer, and a listener cut off for falling
behind — and argues for when not to use it, using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `publisher-subscriber-with-redis-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `publisher-subscriber-with-redis-pattern-explained.m4a` | Audio-only version. |
| `publisher-subscriber-with-redis-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. |

None of these except `poster.png` is committed; `./build_video.sh` rebuilds them.

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

## Rebuilding

```bash
./build_video.sh
```

### What the script does, step by step

1. **Slides.** `make_slides.py` draws one 1920×1080 PNG per scene into `build/`.
2. **Narration.** Each scene's narration from `scenes.py` is spoken by macOS
   `say` with the `Samantha` voice at 145 words per minute.
3. **Clean-up, per scene.** The speech is resampled to 48 kHz with a long
   filter, a high-pass at 75 Hz removes rumble, and a small lift around 3 kHz
   makes consonants clearer. There is deliberately **no denoiser**: synthesised
   speech has almost no noise floor, and a spectral denoiser subtracts parts of
   the voice instead, leaving it warbling. Each scene gets 0.9 seconds of
   silence at the end, and its audio is padded to a whole number of video
   frames so slides and speech cannot drift apart.
4. **Joining.** Scene audio is kept as lossless WAV and joined losslessly. AAC
   is encoded exactly once, over the whole narration, because separately
   encoded AAC clips each carry priming samples that leave a hole at every join.
5. **Levelling.** Loudness is normalised once, over the whole narration, to
   −16 LUFS with a true peak of −1.5 dB, in two passes: the first measures,
   the second applies one constant gain. Levelling per scene would pump the
   volume at every cut.
6. **Checks.** Subtitles are timed from the encoded scene clips, and the script
   reads every audio packet of the finished video and prints
   `audio timeline continuous: N packets, no gaps`. If that line is missing or
   reports a gap, the build has failed even if an mp4 exists.

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

The video itself needs no container runtime; only the demo does.

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Publisher-Subscriber with Redis | Title card and the definition |
| 2 | The Scenario | One order, four services that care |
| 3 | The Order Service Calls Each One | Act one |
| 4 | Redis's Words | Publish, channel, subscribe, through live radio |
| 5 | Publish Once, Redis Fans It Out | Act two, with a listener in a second Java process |
| 6 | The Publisher Gets A Number | What `PUBLISH` answers |
| 7 | A Subscriber That Arrives Late | Act three |
| 8 | Each Takes What It Wants | Act four: exact names and a star |
| 9 | A Pile For Every Listener | The output buffer and its limit, through a kitchen |
| 10 | A Subscriber That Cannot Keep Up | Act five: the cut-off |
| 11 | Why Redis Cuts It Off | The two worse choices |
| 12 | The Bill | Act six |
| 13 | What The Simulation Left Out | The contrast with the partner project |
| 14 | The Verdict | |
| 15 | What Is Real, And When Not | Redis 8.10.2 in a container the demo owns |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, regenerate `narration.md` with the
shared narration generator, then re-run `./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term Redis introduces before using Redis's name for it, and never points at a
picture the listener cannot see. Every figure comes from `./gradlew run`.

## Publishing Notes

Upload `publisher-subscriber-with-redis-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in `../docs/youtube.md`.
