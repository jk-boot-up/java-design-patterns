# Event Sourcing Pattern — Teaching Video

A narrated, slide-based video that teaches the Event Sourcing pattern using this
project's code. Aimed at beginners with no prior knowledge of event stores, logs
or CQRS, and written so that it still works for somebody who is only listening.

The running order gives the pattern's costs as much room as its benefits: three
of the sixteen scenes are the bill. This is the most over-applied pattern in the
course, and a video that only sold it would be doing the viewer a disservice.

## Output Files

| File | What it is |
| --- | --- |
| `event-sourcing-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `event-sourcing-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `event-sourcing-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The video's opening frame, 1920×1080. Not the thumbnail — see the publishing notes below. |

**Runtime:** 17 minutes 00 seconds, over 16 scenes and 251 subtitle cues.
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
| 1 | Event Sourcing | Title card, author credit, the plain-language definition of the pattern, the bank statement, and then the same idea in the online store |
| 2 | The Scenario | The loyalty scheme, the row with `140` in it, and a customer ringing up to ask why |
| 3 | The Naive Approach — Keep the Total | `CurrentStateLoyaltyAccounts.award` — four facts arrive, one is used, and the order id and date are dropped |
| 4 | What the Row Can Say | Act 1's real output: the entire answer support can give, and why an audit log is a second copy of the truth |
| 5 | Three Weeks Later, a Bug | Act 2 — a doubled £45 order and one honest £100 order write the same number, so the bug destroys the evidence of itself |
| 6 | The Pattern | The balance was never something the shop was told. It was arithmetic over four facts, and then the facts were thrown away |
| 7 | Three Moves | Past-tense facts, an append-only log, and no stored balance anywhere — with why the past tense is not a style preference |
| 8 | Who Does What | `LoyaltyEvent`, `LoyaltyEventStore`, `EventSourcedLoyaltyAccounts` with no balance field, and a `SnapshotStore` that is only ever a cache |
| 9 | The Fold — and Why It Is 140 | The five-line fold, and Act 4's dated walk that a support agent can read down the phone |
| 10 | The Query Nobody Wrote in Advance | Act 3 — the duplicate hunt written three weeks after the bug shipped, and a repair that edits, deletes and appends nothing |
| 11 | The Bill — Reading Gets Expensive | Act 6's real figures: 5,000 events read per balance, and the snapshot that fixes it by storing a balance again |
| 12 | The Bill — A Snapshot Can Be Quietly Wrong | 90 against 45, with nothing thrown and nothing logged, and why the cure is to delete every snapshot and refold |
| 13 | The Bill — Erasure, and Old Events | Acts 7 and 8 — a right to be forgotten meeting a log with no delete, and a query that calmly reports zero duplicates |
| 14 | Event Sourcing Is Not CQRS | Act 9 builds each one without the other, so the two sentences that separate them can be shown rather than asserted |
| 15 | When to Reach for It | The one question — will anybody ever need to know how this number got to be what it is? |
| 16 | Thanks for Watching | The correcting-event exercise, like, subscribe, and where the source code lives |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 16 asks for the thumbs up and the subscribe. Both are rendered by
their own slide styles (`poster` and `outro` in `make_slides.py`) and are the
only two scenes with no page number in the footer.

Scene 16 deliberately does not name whichever pattern comes next. Publishing
order on YouTube is not the order these projects were built in, and a rendered
video cannot be corrected without re-uploading it.

Scenes 8, and 4, 5, 10 and 11 are not plain text: scene 8 is a `diagram` slide
laid out by hand in `make_slides.py`, and the other four are `console` slides
showing what the demo actually prints. If you change `LoyaltyBalanceDemo`,
re-check all four against its real output — every number spoken in the
narration is one the program produces, and `DemoRunsTest` asserts that those
numbers are still the ones it prints.

### Why the costs get three scenes

Scenes 11, 12 and 13 are a third of the running time after the title card, and
that is on purpose. Replay cost, a snapshot that is silently wrong, erasure
against an append-only log, and events that can never gain a field added later
are the four things that actually decide whether this pattern is the right
choice — and they are the four things most introductions leave out. Scene 15
then gives the viewer a single question to take away instead of a
recommendation. A pattern taught without its bill is a sales pitch.

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
--force event-sourcing` to refresh `narration.md`, then re-run
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

**Upload `event-sourcing-pattern-explained.mp4`, with `../docs/thumbnail.png` as
the thumbnail and the `.srt` as the captions.** The `.m4a` and the build
scripts have no role on YouTube. `poster.png` is the video's opening frame,
not the thumbnail: it is composed for a full screen, whereas `thumbnail.png`
is drawn at 1280×720 with only the name, one promise and one line of code, so
it survives being shrunk to search-result size.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`EventSourcedLoyaltyAccounts` and `PointsRedeemed`. Uploading
`event-sourcing-pattern-explained.srt` gives exact wording and makes the video
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

> Learn event sourcing in Java 21 through a loyalty scheme, a row with a
> hundred and forty in it, and a customer ringing up to ask why. The version
> that keeps the total is shown fairly: four facts arrive, one is used, and
> the order id and the date are dropped on the floor. Three weeks later a
> bug doubles an order — and because a doubled forty-five and an honest
> hundred write the same number, the bug destroys the evidence of itself.
> The insight is that the balance was never something the shop was told; it
> was arithmetic over facts that were then thrown away. So we store past-
> tense facts in an append-only log with no stored balance anywhere, and the
> balance becomes a five-line fold and a dated walk a support agent can read
> down the phone. Then the second half, which is the reason this is the most
> over-applied pattern in the course: reading gets expensive, the snapshot
> that fixes it can be quietly wrong with nothing thrown and nothing logged,
> a right to be forgotten meets a log with no delete, and event sourcing
> turns out not to be CQRS.
