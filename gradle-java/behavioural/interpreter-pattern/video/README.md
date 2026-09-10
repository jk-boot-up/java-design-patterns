# Interpreter Pattern — Teaching Video

A narrated, slide-based video that teaches the Interpreter pattern using this
project's code. Aimed at beginners with no prior design-pattern knowledge.

## Output Files

| File | What it is |
| --- | --- |
| `interpreter-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `interpreter-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `interpreter-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The opening title card, 1920×1080. Upload it as the video's custom thumbnail. |

**Runtime:** approximately 12 minutes.
**Narration:** female voice (macOS `Samantha`, US English).

None of the four are committed — they are build output. Run
`./build_video.sh` to produce them.

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
| 1 | Poster | Title card, author credit, the plain-language definition of the pattern, and the thumbnail |
| 2 | The Scenario | Three promotions, each a code, a percentage and a rule — and the first one as four perfectly good lines of Java |
| 3 | Two Copies, Two Bugs, No Exceptions | SAVE15 giving money away and FREESHIP withholding it, neither of them throwing |
| 4 | The Naive Approach | `NaiveVoucherRules` — one method per offer, one branch inside each, and a release for every rule change |
| 5 | Why That Hurts | Rule changes as code changes, owners who cannot read their own offers, no answer to "why?", and no place for a typo to be caught |
| 6 | The Interpreter Pattern | The formal definition, and the beginner's version: one small class per kind of phrase, and a big phrase may hold small ones |
| 7 | An Analogy | Sentence diagrams — a noun phrase drops in wherever a noun does, however big it is |
| 8 | The Roles | `Rule`, the terminals, the non-terminals, the `Order` as context, and the one loop that is the recursion |
| 9 | Two Kinds of Class, and That Is All | `CountryIs` as a whole terminal, `AndRule` as a whole non-terminal, and what `AndRule` does not know about its parts |
| 10 | The Tree Can Explain Itself — and Refuse a Typo | `describe()` rebuilding the sentence from the objects, and `RuleParser` naming the phrase it cannot read |
| 11 | The Tests | Asserting the grammar — precedence, the parse/describe round trip — and pinning the naive version's wrong answer on purpose |
| 12 | Running It | The same overseas order through both: 15% off from the branches, 0% from the rule tree |
| 13 | Wrap Up | Interpreter against Composite and Strategy, the one class per phrase cost, and when two `if` statements are the better answer |
| 14 | Thanks for Watching | Like, subscribe, and where the source code lives |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 14 asks for the thumbs up and the subscribe. Both are rendered by
their own slide styles (`poster` and `outro` in `make_slides.py`) and are the
only two scenes with no page number in the footer.

Scene 14 deliberately does not name whichever pattern comes next. Publishing
order on YouTube is not the order these projects were built in, and a rendered
video cannot be corrected without re-uploading it.

Scenes 8 and 12 are hand-drawn rather than text: scene 8 is a `diagram` slide
laid out in `make_slides.py`, and scene 12 is a `console` slide showing the
demo's actual output. If you change `VoucherRuleDemo`, re-check scene 12
against what the program really prints.

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
out loud. Keep `narration.md` in sync if you change the wording
substantially — it is the human-readable copy used for review.

One wording note specific to this pattern: the narration never uses the word
"recursion". "A rule can hold rules" carries the whole idea and frightens
nobody, and the slides follow the same rule.

## Publishing Notes

The video is encoded to YouTube's recommended settings already (1080p,
H.264, 30 fps, stereo AAC at 48 kHz), so it can be uploaded as-is.
The title, description and tags to paste at upload time live in
[`../docs/youtube.md`](../docs/youtube.md).

**Upload `interpreter-pattern-explained.mp4`, with `poster.png` as the
thumbnail and the `.srt` as the captions.** The `.m4a` and the build
scripts have no role on YouTube.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`RuleParser` and `BasketOver`. Uploading
`interpreter-pattern-explained.srt` gives exact wording and makes the video
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
  first; 1080p can take several extra minutes to appear. Code slides are
  unreadable at 360p, so do not share the link until 1080p is available in
  the quality menu.
- **Set the thumbnail.** Do not let YouTube auto-pick a frame — upload
  `poster.png`. It is the same image as the opening scene, drawn large and
  bright enough to stay readable at search-result size, and it carries both
  the topic and the author's name. In YouTube Studio: **Details** →
  **Thumbnail** → **Upload file**. (A custom thumbnail needs a verified
  channel; if the option is missing, verify the account first.)
