# Distributed Tracing Pattern — Teaching Video

A narrated, slide-based video that teaches the Distributed Tracing pattern using
this project's code. Aimed at beginners who have never opened a tracing tool, and
written so that it still works for somebody who is only listening.

The running order splits in two. The pattern itself is finished by scene 11 — one
identifier, one parent field, and the subtraction that turns total time into self
time. Scenes 12, 13 and 14 are the bill: a service that opens no span, a context
lost across a thread, and a trace that was thrown away before anybody knew it
would be wanted. None of the three raises an error, which is exactly why they need
a third of the running time.

## Output Files

| File | What it is |
| --- | --- |
| `distributed-tracing-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `distributed-tracing-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `distributed-tracing-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The video's opening frame, 1920×1080. Not the thumbnail — see the publishing notes below. |

**Runtime:** 16 minutes 53 seconds, over 16 scenes and 247 subtitle cues.
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
| 1 | Distributed Tracing | Title card, author credit, the plain-language definition of the pattern, the hospital wristband, and then the same idea in the online store |
| 2 | The Scenario | A nine-hundred-millisecond product page, four healthy services, and one measurement — the complaint |
| 3 | What the Logs Give You | Act 2's real output: two customers interleaved, and pricing that took either 180ms or 220ms depending which finish you subtract |
| 4 | More Logging Does Not Fix It | Thread name, pod name, product id — every candidate field fails the same test: the same across one request, different across the next |
| 5 | The Pattern | One identifier per request, one span per unit of work, and the sentence that carries it: a span records how long it took *and what asked for it* |
| 6 | Three Moves | Give the request an id, open a span around each unit of work, and pass the context down — with the parent as the move people skip |
| 7 | Who Does What | `ProductPage`, `Tracer`, `Span`, `Trace` and `Waterfall`, with the bill down the right-hand side |
| 8 | The One Argument That Is the Pattern | `Tracer.start(context, name)` — a single string field, and why try-with-resources is not a style choice |
| 9 | Seven Spans, and the Column That Matters | Act 3 — six spans name a parent, one does not, and the ranking model's parent is recommendations rather than the page |
| 10 | The Waterfall — That Column, Drawn | Act 4 — indentation is the parent field, position is the start time, and that is the entire rendering rule |
| 11 | Self Time — The Whole Trick | One subtraction: the page's own work is zero, recommendations is charged 60 of its 400, and the ranking model's 340ms is 37% of the page |
| 12 | The Bill, Part One — A Service That Opens No Span | Act 5 — one root, no orphans, 900ms accounted for, and the responsible service absent from the diagram entirely |
| 13 | The Bill, Part Two — One Line, in the Wrong Place | Act 6 — a `ThreadLocal` that does not travel, two separate roots, and a fix that is the same code with one line moved earlier |
| 14 | The Bill, Part Three — The Decision Made Too Early | Act 7 — ten thousand kept, nine hundred and ninety thousand discarded, and request 862,144 gone unrecoverably |
| 15 | What to Take Away | The two questions: does this question need one request or all of them, and where is context handed to something that will run later |
| 16 | Thanks for Watching | The exercise, like, subscribe, and where the source code lives |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 16 asks for the thumbs up and the subscribe. Both are rendered by
their own slide styles (`poster` and `outro` in `make_slides.py`) and are the
only two scenes with no page number in the footer.

Scene 16 deliberately does not name whichever pattern comes next. Publishing
order on YouTube is not the order these projects were built in, and a rendered
video cannot be corrected without re-uploading it.

Scene 7 is a `diagram` slide laid out by hand in `make_slides.py`, and scenes 3,
9, 10, 11, 12, 13 and 14 are `console` slides showing what the demo actually
prints. If you change `ProductPageDemo`, re-check all seven against its real
output — every number spoken in the narration is one the program produces, and
`DemoRunsTest` asserts that those numbers are still the ones it prints.

### Why the bill gets three scenes

Scenes 12 to 14 are close to a third of the running time, and that is on
purpose. The first two moves of this pattern are easy and they work: open spans,
pass the context, and the page that nobody could explain becomes a picture with
a number against every service. Nothing about that success warns you when the
picture is wrong.

Scene 12 is the centre of the video. Partial instrumentation is worse than none,
because none tells you nothing and partial tells you something false,
confidently, with a diagram — and `ProductPageTest` asserts both halves of that:
the trace has one root and no orphans **and** charges the page 60ms it never
spent. Scene 15 then gives the viewer two questions to take away rather than a
recommendation.

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
--force distributed-tracing` to refresh `narration.md`, then re-run
`./build_video.sh`. The script is written to be spoken rather than read, and
`[[slnc NNN]]` markers insert a pause of NNN milliseconds where a person
would draw breath. They are instructions to `say`, not words:
`make_subtitles.py` strips them, so keep any new ones in that exact form or
they will be read out loud.

One requirement specific to this category: the narration has to stand up with
the screen off. A listener washing up must be able to follow it, so no line
may depend on seeing the slide — the words name the caller, the callee and
the number themselves rather than pointing at them. That constraint bites
hardest on scenes 10 and 11, where the slide is a picture made of characters:
the narration describes the shape in order rather than asking the listener to
look at it.

## Publishing Notes

The video is encoded to YouTube's recommended settings already (1080p,
H.264, 30 fps, stereo AAC at 48 kHz), so it can be uploaded as-is.
The title, description and tags to paste at upload time live in
[`../docs/youtube.md`](../docs/youtube.md).

**Upload `distributed-tracing-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.** The
`.m4a` and the build scripts have no role on YouTube. `poster.png` is the
video's opening frame, not the thumbnail: it is composed for a full screen,
whereas `thumbnail.png` is drawn at 1280×720 with only the name, one promise and
one line of code, so it survives being shrunk to search-result size.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`TraceContext` and `AsyncHandoff`, and they routinely mis-hear `parentSpanId`
and `ThreadLocal`. Uploading
`distributed-tracing-pattern-explained.srt` gives exact wording and makes
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

> Learn distributed tracing in Java 21, starting from a product page that
> takes nine hundred milliseconds with four healthy services behind it and
> four sets of correct logs that cannot say which one spent the time. We watch
> two customers interleave in the log until the same service appears to take
> both 180 and 220 milliseconds, find that no extra field fixes it, and build
> the pattern instead: one id per request, one span per unit of work, and the
> one field people skip — the parent. Then we compute self time, which is the
> whole trick, and spend the second half on the bill: a service that opens no
> span and produces a trace that passes every check while blaming the wrong
> code, a context lost across a thread, and a trace sampled away before
> anybody knew it would be wanted. None of the three throws an exception. No
> prior design-pattern knowledge needed, and no Docker, collector or
> OpenTelemetry — it all runs in one JVM. Full source code and written notes
> are in the repository.
