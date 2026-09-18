# Externalised Configuration Pattern — Teaching Video

A narrated, slide-based video that teaches the Externalised Configuration pattern
using this project's code. Aimed at beginners who have never used a config server
or a feature flag, and written so that it still works for somebody who is only
listening.

The running order is unusual for this series. The pattern itself is finished by
scene 9, and scenes 10 to 15 are the bill — the outage, the two ways a bad value
fails, and the four guards that have to be rebuilt outside the program. This is an
easy pattern to adopt and an easy one to adopt badly, and the second half is the
half that decides which.

## Output Files

| File | What it is |
| --- | --- |
| `externalised-configuration-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `externalised-configuration-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `externalised-configuration-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The video's opening frame, 1920×1080. Not the thumbnail — see the publishing notes below. |

**Runtime:** 24 minutes 46 seconds, over 17 scenes and 366 subtitle cues.
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
| 1 | Externalised Configuration | Title card, author credit, the plain-language definition of the pattern, the greengrocer's chalk board, and then the same idea in the online store |
| 2 | The Scenario | Free delivery over £50, the three baskets every act uses, and marketing asking for £35 at 16:30 on a Friday |
| 3 | Where the Number Lives Today | `HardCodedCheckout`'s constant — named, typed, in one place, and not wrong |
| 4 | What Changing One Number Costs | Act 2's real output: 135 minutes of work, a window that closes at five, live Monday 10:45, and the challenge to delete a step from the list |
| 5 | The Pattern | Behaviour values against policy values, and the sentence the whole pattern rests on: the pipeline does not make a policy value safer, it makes it late |
| 6 | Three Moves | Read from outside, read per use, keep a default — and the third move, that the compiler, the type, the reviewer and the history all stayed behind |
| 7 | Who Does What | `ConfiguredCheckout`, `SettingsReader`, `MoneySetting`, `ConfigSource` and `ChangeLog`, with the invoice down the right-hand side |
| 8 | The One Line That Is the Pattern | `ConfiguredCheckout.quote` — identical arithmetic, one different line, and why the read sits inside the method rather than in the constructor |
| 9 | Four Seconds | Act 3 — nothing configured changes no behaviour at all, then `35` lands and ORD-7102 flips to free on the next quote |
| 10 | The Bill, Part One — When the Source Goes Away | Act 4 — the shop survives the outage on its default, and loses the promotion with no error and no alarm |
| 11 | The Bill, Part Two — A Number Nobody Checked | Act 5 — `-1` parses, every basket ships free, nothing throws, and the first symptom is the margin report on Monday |
| 12 | The Bill, Part Three — Not a Number at All | Act 6 — the word `fifty` takes the shop down from a text box, and why the loud failure is the better one |
| 13 | The Four Guards, and What Replaces Them | The compiler, the reviewer, version control and the revert, each with its replacement — four ordinary pieces of code |
| 14 | Declared, and Validated at the Boundary | Act 7 — the declared range and why £5 and £200 are business judgements, and the fallback to the last good value rather than the compiled default |
| 15 | The Trail, and a Rollback in Four Seconds | Acts 8 and 9 — five changes in a day and none in git, and a rollback that is a lookup rather than an act of memory |
| 16 | What to Externalise, and What Never To | The two questions to ask, and the line between a parameter that lives forever and a feature flag that is meant to die |
| 17 | Thanks for Watching | The widen-the-range exercise, like, subscribe, and where the source code lives |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 17 asks for the thumbs up and the subscribe. Both are rendered by
their own slide styles (`poster` and `outro` in `make_slides.py`) and are the
only two scenes with no page number in the footer.

Scene 17 deliberately does not name whichever pattern comes next. Publishing
order on YouTube is not the order these projects were built in, and a rendered
video cannot be corrected without re-uploading it.

Scene 7 is a `diagram` slide laid out by hand in `make_slides.py`, and scenes 4,
9, 10, 11, 12, 14 and 15 are `console` slides showing what the demo actually
prints. If you change `FreeDeliveryDemo`, re-check all seven against its real
output — every number spoken in the narration is one the program produces, and
`DemoRunsTest` asserts that those numbers are still the ones it prints.

### Why the bill gets six scenes

Scenes 10 to 15 are more than a third of the running time, and that is on
purpose. The first two moves of this pattern work on their own: read the value
from outside, keep a default, and the change that used to take a weekend now
takes four seconds. Nothing forces you to do the third move, and so most teams
do not — which is how `-1` reaches a live shop with nothing in its way.

Scene 11 is the centre of the video. The quiet failure has no exception, no log
line and no alert, because nothing is broken: the program was told the threshold
is minus one pound and is applying it faithfully. `TheBillTest` asserts that
behaviour and **passes**, which is the point. Scene 16 then gives the viewer two
questions to take away rather than a recommendation.

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
--force externalised-configuration` to refresh `narration.md`, then re-run
`./build_video.sh`. The script is written to be spoken rather than read, and
`[[slnc NNN]]` markers insert a pause of NNN milliseconds where a person
would draw breath. They are instructions to `say`, not words:
`make_subtitles.py` strips them, so keep any new ones in that exact form or
they will be read out loud.

One requirement specific to this category: the narration has to stand up with
the screen off. A listener washing up must be able to follow it, so no line
may depend on seeing the slide — the words name the caller, the callee and
the number themselves rather than pointing at them. Money is spoken in words
("thirty-five pounds", not "£35") for the same reason: `say` reads a currency
symbol inconsistently, and a listener cannot see the digits.

## Publishing Notes

The video is encoded to YouTube's recommended settings already (1080p,
H.264, 30 fps, stereo AAC at 48 kHz), so it can be uploaded as-is.
The title, description and tags to paste at upload time live in
[`../docs/youtube.md`](../docs/youtube.md).

**Upload `externalised-configuration-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.** The
`.m4a` and the build scripts have no role on YouTube. `poster.png` is the
video's opening frame, not the thumbnail: it is composed for a full screen,
whereas `thumbnail.png` is drawn at 1280×720 with only the name, one promise and
one line of code, so it survives being shrunk to search-result size.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`ConfiguredCheckout` and `GuardedSettings`, and they routinely mis-hear
`delivery.freeOver`. Uploading
`externalised-configuration-pattern-explained.srt` gives exact wording and makes
the video searchable.

**During upload** — on the *Video elements* step, choose **Add subtitles**
→ **Upload file** → **With timing**, pick the `.srt`, then **Save**.

**After publishing** — YouTube Studio → **Subtitles** → select the video →
next to your language click **Add** → **Upload file** → **With timing** →
choose the `.srt` → **Publish**.

Set the video language (Details → *Show more* → Video language) to English
first, or the subtitle option may not appear.

Two further things that affect how well it plays for viewers:

- **Wait for HD processing.** YouTube serves a low-resolution version
  first; 1080p can take several extra minutes to appear. Code and console
  slides are unreadable at 360p, so do not share the link until 1080p is
  available in the quality menu.
- **Set the thumbnail.** Do not let YouTube auto-pick a frame — upload
  `../docs/thumbnail.png` under **Details** → **Thumbnail** → **Upload
  file**. (A custom thumbnail needs a verified channel; if the option is
  missing, verify the account first.)

Suggested description:

> Learn externalised configuration in Java 21, starting from a constant that
> is not wrong: free delivery over fifty pounds, named, typed as money, in
> exactly one place, and a reviewer would approve it without a comment. Then
> marketing ask at half past four on a Friday for thirty-five pounds by
> Saturday morning, and the release pipeline prices that at a hundred and
> thirty-five minutes of work, live on Monday at a quarter to eleven — two
> days late for a weekend promotion. Nothing in that pipeline is
> unreasonable; the value is simply sitting somewhere with an engineering
> change speed. So we move the read outside and into the method, and the
> same change takes four seconds. The second half is the half most write-ups
> leave out. A constant was getting four guards for free — the compiler, a
> reviewer, version control and a revert — and moving the value outside
> throws all four away. Minus one parses, ships every basket free, and
> nothing throws or logs. The word fifty takes the shop down from a text
> box. We rebuild each guard deliberately, and finish on what to externalise
> and what never to.
