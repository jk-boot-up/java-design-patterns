# Dead Letter Channel with RabbitMQ Pattern — Teaching Video

A narrated, slide-based video that shows what a real RabbitMQ broker adds to the Dead Letter Channel
pattern: the broker decides when a message is dead, and writes down its own reason.

## Output Files

| File | What it is |
| --- | --- |
| `dead-letter-channel-with-rabbitmq-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `dead-letter-channel-with-rabbitmq-pattern-explained.m4a` | Audio-only version. |
| `dead-letter-channel-with-rabbitmq-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. Also used as the YouTube thumbnail. |

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
| 1 | Dead Letter Channel with RabbitMQ | Title card, the pattern in plain words, and the sorting-office analogy |
| 2 | The Partner Video | The hand-built project this one pairs with |
| 3 | Three Words First | Queue, exchange, and refusing a message |
| 4 | An Order That Can Never Succeed | Act one: asking for it back for ever |
| 5 | A Rule Written On The Queue | Act two: the broker does the moving |
| 6 | The Broker Writes Down Why | Act three: the note, and reason `rejected` |
| 7 | Deaths Nobody Chose | Act four: `expired` and `maxlen` |
| 8 | Fix It, And Put It Back | Act five: replay, and what it does not restore |
| 9 | The Bill: Nobody Is Looking | Act six: twenty parked orders and a healthy dashboard |
| 10 | The Three Reasons | The three words in one place |
| 11 | The Verdict |  |
| 12 | How To Recognise It |  |
| 13 | What Was Used | Pinned versions |
| 14 | What Is Real Here | Real broker, real queues, bounded polls |
| 15 | When This Is Too Much |  |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force dead-letter-channel-with-rabbitmq`, then
re-run `./build_video.sh`.

Same discipline as the rest of the repository: every narration line names
the actors, says what each one decides, and speaks counts and outcomes in
words, rather than pointing at a picture the listener cannot see. Every
number spoken is the real output of `./gradlew run`.

## Publishing Notes

Upload `dead-letter-channel-with-rabbitmq-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Dead Letter Channel pattern in Java: a dead letter channel takes a message
> that can never be handled off the belt and shelves it with a note, so the
> belt keeps moving and a person can look later. Explained with RabbitMQ,
> using an online store queue of orders where one order's address can never be
> read. What is new with a real broker is who decides: the application writes
> a rule on the queue, and RabbitMQ takes the message off and writes down its
> own reason. We hear deaths nobody chose, fix and put a message back, and
> learn the three reasons a message dies. The bill is the same: someone has to
> look.
