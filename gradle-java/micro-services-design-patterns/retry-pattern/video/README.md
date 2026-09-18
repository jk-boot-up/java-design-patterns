# Retry with Backoff Pattern — Teaching Video

A narrated, slide-based video that teaches the Retry with Backoff pattern using this
project's code. Aimed at beginners with no prior microservices knowledge, and
written so that it still works for somebody who is only listening.

## Output Files

| File | What it is |
| --- | --- |
| `retry-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `retry-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `retry-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The video's opening frame, 1920×1080. Not the thumbnail — see the publishing notes below. |

**Runtime:** approximately sixteen minutes.
**Narration:** female voice (macOS `Samantha`, US English).

The `.mp4`, `.m4a` and `.srt` are build output and are not committed — run
`./build_video.sh` to produce them. `poster.png` *is* committed, so the title
card is available without a build.

## Source Files

| File | Purpose |
| --- | --- |
| `narration.md` | The full spoken script, scene by scene — read this to review the wording. It is generated from `scenes.py` by `../../docs/make_narration.py`, so edit the scenes, not the script. |
| `scenes.py` | Slide content *and* narration text, kept together so they cannot drift apart. |
| `make_slides.py` | Renders one 1920×1080 PNG per scene. |
| `make_subtitles.py` | Generates the SRT, timed from the encoded scene clips. |
| `build_video.sh` | The whole pipeline: slides → narration → per-scene clips → final video → subtitles. |
| `build/` | Generated slide images (regenerated on every build). |

## Rebuilding

```bash
./build_video.sh
```

The script will:

1. render the slides,
2. narrate each scene with the `say` command,
3. pair every slide with its narration into a clip,
4. concatenate the clips, export the audio-only version and lift out `poster.png`,
5. generate the SRT subtitles, then clean up the intermediates.

### Why audio and video are kept apart until the last step

This is the part of the pipeline most worth understanding before changing
anything, because getting it wrong produces a file that looks fine and
sounds broken.

AAC is a lapped format: every separately encoded clip carries priming
samples at its head and padding at its tail. Concatenating such clips with
`-c copy` cannot strip either, so each join leaves a hole in the timeline —
the voice cuts out for a moment at every scene change, and over a full
video the gaps add up to tens of seconds of missing narration. So each
scene's narration is written as lossless WAV, and the whole narration is
encoded to AAC exactly once, at the mux. One encode, one set of priming
samples, no internal joins.

Loudness normalisation is run in two passes for a related reason. Left to
itself `loudnorm` works dynamically, riding the level as it goes, and on
some narrations that makes it emit a timestamp discontinuity partway
through — the same audible hole, in the middle of a sentence, with nothing
wrong anywhere upstream. Measuring the narration first and handing the
numbers back with `linear=true` reduces it to one constant gain, which
cannot do that, and which also stops it pumping between quiet and loud
lines.

The build checks itself for both: after the mux it reads every audio packet
timestamp and fails if any two are more than one AAC frame apart. If you
change the ffmpeg calls, that check is what will tell you.

Scene lengths are rounded up to a whole number of video frames and the
audio padded to match, so a scene's picture and its narration are exactly
the same length. Slide changes therefore cannot drift away from the voice,
however many scenes the video grows to.

The final mux is deliberate, not incidental: the file is written with
`+faststart` so the index sits at the front and the poster paints the moment
the file is opened, and the AAC priming edit list is dropped so the video
track starts at 0.000 alongside the audio rather than 21 ms late. Without
either, players show black at 0:00. If you change the ffmpeg calls, check
with `ffprobe -show_entries stream=start_time` that both streams still start
at zero.

The narration is cleaned up before it is encoded, and that matters more than
it sounds. Every voice macOS ships by default is the compact 22 kHz tier, and
resampling it straight to the 48 kHz the AAC track needs leaves an audible
hiss. The `CLEANUP` filter chain in `build_video.sh` resamples with a long
filter so the upsampling adds no grit of its own, drops the rumble below the
voice, and lifts the consonant range slightly.

There is deliberately no denoiser in that chain. An earlier version ran
`afftdn` over the narration, and by the numbers it worked — about 15 dB off
the noise floor. It also made the voice noticeably worse. A spectral
denoiser assumes a real, roughly stationary noise floor to subtract;
synthesised speech has almost none, so `afftdn` ends up subtracting parts of
the speech instead and leaves it warbling. The faint hiss is much the lesser
problem, so it stays.

Levelling is deliberately not part of that chain either — run per scene it
re-measures on every clip, so a quiet scene gets pushed up to match a loud
one and the level audibly steps at each join. It happens once instead, over
the whole narration, at YouTube's -16 LUFS target.

An Enhanced or Premium voice would sound better still — those sample at
44.1 kHz — but they are a manual download: **System Settings → Accessibility
→ Spoken Content → System Voice → Manage Voices**. Once one is installed,
just re-run the build.

Set `KEEP_INTERMEDIATE=1` to retain the per-scene narration and clips for
inspection.

### Options

Both are environment variables:

```bash
VOICE=Ava RATE=155 ./build_video.sh
```

| Variable | Default | Meaning |
| --- | --- | --- |
| `VOICE` | `Samantha` | Any voice from `say -v '?'` |
| `RATE` | `145` | Speaking rate in words per minute — the pace educational YouTube converges on for technical material |

### Requirements

- **macOS** — the narration uses the built-in `say` command
- **ffmpeg** — `brew install ffmpeg`
- **Python 3** with `pillow` and `matplotlib`
  (`matplotlib` is used only for its bundled DejaVu fonts)

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Retry with Backoff | Title card, author credit, the plain-language definition of the pattern, and then the same idea in the online store |
| 2 | The Scenario | One espresso machine at £449.99, a payment gateway across the internet, and one call in five failing for reasons that have nothing to do with the payment |
| 3 | The Obvious Answer — Just Try Again | The four-line loop everybody writes first: it rescues checkouts, throws nothing, and every test written against it passes |
| 4 | Act One — A Timeout That Recovers | The demo's real output: a timeout, a 103ms wait, a charge on attempt two — card charged **1 time**, £449.99, at a cost of 203ms instead of 50ms |
| 5 | Wait Longer Each Time — And Not All The Same | Backoff as room for a struggling service rather than politeness, and jitter as the thing that stops a thousand callers returning as one wave |
| 6 | Not Every Failure Is Worth Another Go | `worthRetrying` — one line, written as a whitelist, and why the opposite rule eventually retries a `NullPointerException` four hundred times |
| 7 | Act Two — A Declined Card | The demo's real output: one attempt, 50ms, a permanent answer reported at once — against a plain loop's three attempts and two waits for the same "no" |
| 8 | The Pieces, And What Each One Decides | `CheckoutService`, `Retrier`, `RetryPolicy` and `PaymentGateway`, the three ways the gateway can fail, and why a `Supplier` cannot know what it is retrying |
| 9 | The Failure You Cannot See | The card **is** charged and the reply is lost on the way home — and from the caller's side that is byte-for-byte the same timeout as act one |
| 10 | Act Four — And The Plain Loop Charges Twice | The demo's real output: a fresh key on attempt two, a second charge, **£899.98** for one espresso machine — and a gateway that did nothing wrong |
| 11 | And Nothing Went Wrong. That Is The Problem. | No exception, no error log, a valid receipt, and `NaiveCheckoutServiceTest` passing all five tests including the one that asserts £899.98 |
| 12 | So Stop Trying To Tell Them Apart | `PaymentRequest.forOrder` and `CheckoutService.pay` — an idempotency key derived from the order and nothing else, built outside the retry |
| 13 | Act Three — The Same Failure, The Same Key | The demo's real output: `REPLAYED`, card charged **1 time**, £449.99 — and the caller never found out which failure it had suffered |
| 14 | Somebody Has To Keep The Record | The one map inside `PaymentGateway`, checked before any money moves, and why making an operation safe to repeat is work at both ends |
| 15 | What It Costs, And When Not To | Latency the shopper pays, load when you can least afford it, the no-key-no-retry rule, definite answers, and retrying something that is properly down |
| 16 | Thanks for Watching | Like, subscribe, and where the source code lives |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 16 asks for the thumbs up and the subscribe. Both are rendered by
their own slide styles (`poster` and `outro` in `make_slides.py`) and are the
only two scenes with no page number in the footer.

Scene 16 deliberately does not name whichever pattern comes next. Publishing
order on YouTube is not the order these projects were built in, and a rendered
video cannot be corrected without re-uploading it.

Scenes 8, 4, 7, 10 and 13 are not plain text: scene 8 is a `diagram` slide
laid out by hand in `make_slides.py`, and the other four are `console` slides
showing what the demo actually prints, one per act. If you change `RetryDemo`,
`RetryPolicy.threeAttempts` or the gateway's `GATEWAY_LATENCY_MILLIS`, re-check
all four against its real output — every number spoken in the narration is one
the program produces, including 50ms for a single attempt, the 103ms wait, the
203ms recovered checkout, and the two totals the whole video turns on, £449.99
for one charge and £899.98 for two.

Scene order is the argument, and scenes 4 and 9 are the ones to be careful with
if you ever rearrange it. The audience has to watch the pattern *work* — act
one, the backoff, the declined card — and believe in it, before the lost reply
is mentioned at all. Move scene 9 earlier and the discomfort that carries
scenes 10 and 11 has nowhere to come from.

One layout limit worth knowing before adding text: on `bullets` and `quote`
slides the body starts at y=260 and steps 60 pixels a line, and the footer sits
at y≈1022, so **twelve body lines is the maximum**. A thirteenth collides with
the footer, and nothing in the build warns you.

## Related: the animation's narration

[`../docs/animation.html`](../docs/animation.html) has its own optional
narration, generated separately by
[`../docs/make_animation_audio.sh`](../docs/make_animation_audio.sh) into
`docs/audio/`. It uses the same voice and rate as this video so the two
sound consistent. Those clips are short per-step explanations, not the
video script.

## Editing the Script

Narration lives in `scenes.py`, next to the slide it belongs to. Edit the
`narration` field of a scene, re-run `python3 ../../docs/make_narration.py
--force retry` to refresh `narration.md`, then re-run
`./build_video.sh`. The script is written to be spoken rather than read, and
`[[slnc NNN]]` markers insert a pause of NNN milliseconds where a person
would draw breath. They are instructions to `say`, not words:
`make_subtitles.py` strips them, so keep any new ones in that exact form or
they will be read out loud.

One requirement specific to this category: the narration has to stand up with
the screen off. A listener washing up must be able to follow it, so no line
may depend on seeing the slide — the words name the caller, the callee and
the number themselves rather than pointing at them.

## Publishing Notes

The video is encoded to YouTube's recommended settings already (1080p,
H.264, 30 fps, stereo AAC at 48 kHz), so it can be uploaded as-is.
The title, description and tags to paste at upload time live in
[`../docs/youtube.md`](../docs/youtube.md).

**Upload `retry-pattern-explained.mp4`, with `../docs/thumbnail.png` as
the thumbnail and the `.srt` as the captions.** The `.m4a` and the build
scripts have no role on YouTube. `poster.png` is the video's opening frame,
not the thumbnail: it is composed for a full screen, whereas `thumbnail.png`
is drawn at 1280×720 with only the name, one promise and one line of code, so
it survives being shrunk to search-result size.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`GatewayTimeoutException` and `PaymentRequest`. Uploading
`retry-pattern-explained.srt` gives exact wording and makes the video
searchable.

**During upload** — on the *Video elements* step, choose **Add subtitles**
→ **Upload file** → **With timing**, pick the `.srt`, then **Save**.

**After publishing** — YouTube Studio → **Subtitles** → select the video →
next to your language click **Add** → **Upload file** → **With timing** →
choose the `.srt` → **Publish**.

Set the video language (Details → *Show more* → Video language) to English
first, or the subtitle option may not appear.

Two further things that affect how well it plays for viewers:

- **Wait for HD processing.** YouTube serves a low-resolution version
  first; 1080p can take several extra minutes to appear. Code and timeline
  slides are unreadable at 360p, so do not share the link until 1080p is
  available in the quality menu.
- **Set the thumbnail.** Do not let YouTube auto-pick a frame — upload
  `../docs/thumbnail.png` under **Details** → **Thumbnail** → **Upload
  file**. (A custom thumbnail needs a verified channel; if the option is
  missing, verify the account first.)

Suggested description:

> Learn retry with backoff in Java 21, starting from the four-line loop
> everybody writes first — and which rescues a checkout, throws nothing, and
> passes every test written against it. One espresso machine at four hundred
> and forty-nine pounds ninety-nine, a payment gateway across the internet,
> and one call in five failing for reasons that have nothing to do with the
> payment. We add backoff as room for a struggling service rather than
> politeness, jitter so a thousand callers do not return as one wave, and a
> whitelist of what is worth another go, because the opposite rule
> eventually retries a NullPointerException four hundred times. Then the
> failure you cannot see: the card is charged and the reply is lost on the
> way home, which from the caller's side is byte-for-byte the same timeout
> as the one that recovered. The plain loop charges twice, nothing throws,
> and the receipt is valid. The fix is an idempotency key derived from the
> order and built outside the retry — and somebody downstream has to keep
> the record.
