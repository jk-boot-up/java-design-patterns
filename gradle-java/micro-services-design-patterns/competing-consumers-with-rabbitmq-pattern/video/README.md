# Competing Consumers with RabbitMQ Pattern — Teaching Video

A narrated, slide-based video that teaches Competing Consumers on a real
RabbitMQ broker — how many orders one picker may hold, what the broker hands
back when a picker dies half-way through, and what is lost when nobody says
done — and argues for when not to use it, using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `competing-consumers-with-rabbitmq-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `competing-consumers-with-rabbitmq-pattern-explained.m4a` | Audio-only version. |
| `competing-consumers-with-rabbitmq-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. Not the thumbnail. |

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

## Rebuilding

```bash
./build_video.sh
```

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

The video itself needs no container runtime; only the demo does.

## How the audio is made

Everything below happens inside `build_video.sh`; nothing is read from any
other project.

1. **Slides.** `make_slides.py` draws one 1920×1080 PNG per scene into `build/`.
2. **Voice.** Each scene's narration from `scenes.py` is spoken by macOS `say`
   with the `Samantha` voice at 145 words per minute. The `[[slnc N]]` markers
   in the text are pauses of N milliseconds for `say`; they are not words and
   never reach the subtitles.
3. **Clean-up, per scene.** The voice is resampled to 48 kHz with a long filter
   so the upsampling adds no grit, a high-pass at 75 Hz removes rumble, and a
   small lift around 3 kHz makes consonants clearer. There is deliberately no
   denoiser: synthesised speech has almost no noise floor, and a denoiser ends
   up removing parts of the voice and making it warble.
4. **Frame-exact scenes.** Each scene's audio gets a short tail of silence and
   is padded to a whole number of video frames, so the slide changes cannot
   drift away from the voice over sixteen scenes. Audio stays as lossless WAV
   at this stage.
5. **One join, one encode.** All the WAV files are joined losslessly, and the
   whole narration is encoded to AAC exactly once. Encoding each scene
   separately and joining the results would leave a tiny gap at every scene
   change, because each AAC clip carries padding at its start and end.
6. **Loudness, once, over the whole video.** The joined narration is measured
   first, and then brought to −16 LUFS, the level YouTube plays at, as one
   constant gain (`loudnorm` in two passes, with `linear=true`). Levelling
   each scene on its own would make quiet scenes jump up to match loud ones.
7. **The continuity check.** At the end the script reads every audio packet
   timestamp in the finished mp4 and fails the build if there is any gap. A
   good build prints `audio timeline continuous: N packets, no gaps`.
8. **Subtitles** are timed from the finished scene clips by
   `make_subtitles.py`, so they cannot drift either.

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Competing Consumers with RabbitMQ | Title card and the definition |
| 2 | The Scenario | Orders faster than one picker; a broker that hands work out |
| 3 | One Picker, Then Three | Act one, and the split described as a range |
| 4 | The Broker's Words | Queue, consumer, acknowledgement, through a kitchen ticket rail |
| 5 | No Limit: One Takes Everything | Act two: prefetch, and its default of no limit |
| 6 | Prefetch: How Many To Hold | Act three: prefetch 10 and prefetch 1 |
| 7 | Where An Order Can Be | Waiting, held, or said done |
| 8 | A Picker Dies Mid-Work | Act four: all three held orders back, marked seen before |
| 9 | No Saying Done | Act five: automatic acknowledgement, three lost |
| 10 | Two Settings, Two Lines | `basicQos` and the acknowledgement flag |
| 11 | The Bill | Act six: the poison order, and the costs |
| 12 | What The Simulation Left Out | The contrast with the plain-Java version |
| 13 | The Verdict | |
| 14 | What Is Real Here | RabbitMQ 4.3.6 in a container the demo owns |
| 15 | When This Is Too Much | |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 docs/make_narration.py --force competing-consumers-with-rabbitmq`
from the `gradle-java` directory, then re-run `./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term RabbitMQ introduces before using the broker's name for it, and never
points at a picture the listener cannot see.

## Publishing Notes

Upload `competing-consumers-with-rabbitmq-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Competing Consumers pattern in Java, explained with a real RabbitMQ
> broker. Several workers read one shared queue, each job goes to exactly
> one of them, and adding a worker adds capacity without anyone else
> changing. In our online store every order becomes a pick order, and
> several warehouse pickers share the queue while the broker decides who
> gets which. We watch one picker handed the whole queue while another
> stands idle, fix it with prefetch, see a picker die holding five orders
> and hand back three, and lose three orders for good by never saying done.
> Two settings decide it all.
