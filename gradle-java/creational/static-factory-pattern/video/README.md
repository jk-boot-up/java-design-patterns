# Static Factory Method — Teaching Video

A narrated, slide-based video that teaches the static factory method using
this project's code. Aimed at beginners with no prior design-pattern
knowledge.

## Output Files

| File | What it is |
| --- | --- |
| `static-factory-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `static-factory-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `static-factory-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The opening title card, 1920×1080. Upload it as the video's custom thumbnail. |

**Runtime:** approximately 12 minutes 30 seconds.
**Narration:** female voice (macOS `Samantha`, US English).

The `.mp4`, `.m4a` and `.srt` are build output and are not committed — run
`./build_video.sh` to produce them. `poster.png` *is* committed, so the title
card is available without a build.

## Source Files

| File | Purpose |
| --- | --- |
| `narration.md` | The full spoken script, scene by scene — read this to review or edit the wording. |
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
hiss. The `CLEANUP` filter chain in `build_video.sh` resamples with a long filter so the
upsampling adds no grit of its own, drops the rumble below the voice, and
lifts the consonant range slightly.

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
| 1 | Poster | Title card, author credit, the plain-language definition of the pattern, and the thumbnail |
| 2 | The Job | One order, five kinds of discount |
| 3 | The First Attempt Does Not Compile | Two constructors, one signature |
| 4 | So Everyone Writes This Instead | The widened constructor, and four unreadable call sites |
| 5 | Why That Hurts | Five separate costs, none of them the type's fault |
| 6 | The Static Factory Method | *Effective Java* Item 1 — and why it is not a GoF pattern |
| 7 | A Vending Machine | The analogy: a labelled button, not reaching inside |
| 8 | The Shape of It | One public door, five classes nobody outside can name |
| 9 | The Type Is Its Own Factory | The `Discount` interface and its six named ways in |
| 10 | Freedom Two: Not to Allocate | `NoDiscount.INSTANCE`, and why `new` could never do it |
| 11 | Freedom Three: to Choose the Class | `percentage(0)` quietly returning something else |
| 12 | What the Client Looks Like | No `new`, no branch, no implementation names |
| 13 | The Same Trick on a Value Type | `Money.pounds` versus `Money.pence` |
| 14 | You Already Use This Every Day | The JDK examples and the naming conventions |
| 15 | Running It | The real program output, including the rejected coupon |
| 16 | Where It Stops | No subclassing, harder to find, and the compile-time ceiling |
| 17 | The Rest of the Family | How the four factory projects relate |
| 18 | One Sentence to Keep | The takeaway |
| 19 | Thanks for Watching | Like, subscribe, and where the source code lives |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 19 asks for the thumbs up and the subscribe. Both are rendered by
their own slide styles (`poster` and `outro` in `make_slides.py`) and are the
only two scenes with no page number in the footer.

## Related: the animation's narration

[`../docs/animation.html`](../docs/animation.html) has its own optional
narration, generated separately by
[`../docs/make_animation_audio.sh`](../docs/make_animation_audio.sh) into
`docs/audio/`. It uses the same voice and rate as this video so the two
sound consistent. Those clips are short per-step explanations, not the
video script.

## Editing the Script

Narration lives in `scenes.py`, next to the slide it belongs to. Edit the
`narration` field of a scene, then re-run `./build_video.sh`.

The script is written to be spoken rather than read, and `[[slnc NNN]]`
markers insert a pause of NNN milliseconds where a person would draw
breath. They are instructions to `say`, not words: `make_subtitles.py`
strips them, so keep any new ones in that exact form or they will be read
out loud.

Keep `narration.md` in sync if you change the wording substantially — it is
the human-readable copy used for review.

Note that currency and symbols are written out in words — "five pounds"
rather than "£5", "ten percent" rather than "10%". Keep that habit, or the
narration will mispronounce them.

## Publishing Notes

The video is encoded to YouTube's recommended settings already (1080p,
H.264, 30 fps, stereo AAC at 48 kHz), so it can be uploaded as-is.

**Upload `static-factory-pattern-explained.mp4`, with `poster.png` as the
thumbnail and the `.srt` as the captions.** The `.m4a` and the build scripts
have no role on YouTube.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`PercentageDiscount`. Uploading `static-factory-pattern-explained.srt` gives
exact wording and makes the video searchable.

**During upload** — on the *Video elements* step, choose **Add subtitles**
→ **Upload file** → **With timing**, pick the `.srt`, then **Save**.

**After publishing** — YouTube Studio → **Subtitles** → select the video →
next to your language click **Add** → **Upload file** → **With timing** →
choose the `.srt` → **Publish**.

Set the video language (Details → *Show more* → Video language) to English
first, or the subtitle option may not appear.

Two further things that affect how well it plays for viewers:

- **Wait for HD processing.** YouTube serves a low-resolution version
  first; 1080p can take several extra minutes to appear. Code slides are
  unreadable at 360p, so do not share the link until 1080p is available in
  the quality menu.
- **Set the thumbnail.** Do not let YouTube auto-pick a frame — upload
  `poster.png`. It is the same image as the opening scene, drawn large and
  bright enough to stay readable at search-result size, and it carries both
  the topic and the author's name. In YouTube Studio: **Details** →
  **Thumbnail** → **Upload file**. (A custom thumbnail needs a verified
  channel; if the option is missing, verify the account first.)

Suggested description:

> Learn the static factory method in Java 21 — Item 1 of Effective Java, and
> the creational technique you have already used every time you wrote
> List.of. We start from a constructor that will not compile, because ten
> percent off and ten pounds off are both a single number, and end with a
> discount type that names its own ways in, shares instances where it can,
> and hides every implementation class from its callers. We also cover,
> honestly, what it cannot do: a static method is resolved at compile time,
> so it cannot be overridden or configured — which is exactly why the other
> factory patterns exist. No prior design-pattern knowledge needed. Full
> source code and written notes are in the repository.
