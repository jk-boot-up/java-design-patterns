# Backends for Frontends Pattern — Teaching Video

A narrated, slide-based video that teaches the Backends for Frontends pattern
using this project's code. Aimed at beginners who have never run more than one
backend service, and written so that it still works for somebody who is only
listening.

The running order splits in two. Scenes 2 to 6 are the problem, and they take
longer than a problem usually does on purpose: the obvious fix — a `?fields=`
query parameter — has to be shown *working*, and shown to reduce the payload by
exactly as much as the finished pattern does, or the audience leaves believing
this pattern is about bytes. Only once that fix is on screen and succeeding does
scene 6 ask for the one field it cannot deliver. Scenes 12, 13 and 14 are the
bill: a business rule copied into a backend, the gateway confusion, and the
count that turns a pattern into a department.

## Output Files

| File | What it is |
| --- | --- |
| `backends-for-frontends-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `backends-for-frontends-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `backends-for-frontends-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The video's opening frame, 1920×1080. Not the thumbnail — see the publishing notes below. |

**Runtime:** 18 minutes 30 seconds, over 16 scenes and 263 subtitle cues.
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
| 1 | Backends for Frontends | Title card, author credit, the plain-language definition of the pattern, the two waiters and one kitchen, and then the same idea in the online store |
| 2 | The Scenario | One copper coffee maker, six fields on a phone, fifteen on a desktop, five services underneath, and two teams who are both being reasonable |
| 3 | The First Design — The Phone Calls Everybody | Act 1 — five sequential calls from the device, 1767 bytes, 29 fields available and 6 drawn |
| 4 | The Second Design — One Endpoint For Everybody | Act 2 — one round trip, 1755 bytes, 212 drawn, 87% thrown away on arrival |
| 5 | And the Obvious Fix Works | `?fields=…` → 212 bytes. The same saving the pattern gets, from a query parameter — and why the story does not end there |
| 6 | The Request That Cannot Be Served | The delivery sentence: half an hour of work, five weeks of queue, and an organisational failure with a technical cause |
| 7 | The Pattern | The sentence, and the three words carrying it — **each**, **own**, **shape** — with the near miss each one rules out |
| 8 | Who Does What | `ClientBackend` with `MobileBff` and `WebBff` both live at once, `Shop` underneath, `Screens` as the ruler, and the two rejected designs off to one side |
| 9 | A Backend That Knows One Screen | `MobileBff.productScreen` — four internal calls, no call to recommendations, pence turned into `"£47.99"`, and the five-week field in four lines |
| 10 | Two Backends, Two Documents | Act 3 — the phone's six fields read out, the desktop's fifteen, and the delivery field deliberately different in each |
| 11 | The Same Product, Three Ways | Act 4 — device calls 5 → 1 → 1, internal calls 5 → 5 → 4, and 196 bytes against 1755: the cost relocated, not deleted |
| 12 | The Bill, Part One — One Rule, Two Answers | Act 5 — a discount rule copied into one backend, a saving advertised that the shop may not claim, nothing thrown and nothing logged |
| 13 | The Bill, Part Two — Where the Shared Jobs Go | Act 6 — eight copies across two backends against four behind a gateway, and the question that settles which pattern you are in |
| 14 | The Bill, Part Three — How Many Is Too Many | Act 7 — six clients, three genuine disagreements, and the weekly cost of every backend that exists |
| 15 | What to Take Away | Resource or screen; the saving is a queue, not bytes; shape inside and belief behind; one per disagreement — and that all four fail silently |
| 16 | Thanks for Watching | The exercise, like, subscribe, and where the source code lives |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 16 asks for the thumbs up and the subscribe. Both are rendered by
their own slide styles (`poster` and `outro` in `make_slides.py`) and are the
only two scenes with no page number in the footer.

Scene 16 deliberately does not name whichever pattern comes next. Publishing
order on YouTube is not the order these projects were built in, and a rendered
video cannot be corrected without re-uploading it.

Scene 8 is a `diagram` slide laid out by hand in `make_slides.py`, scene 9 is a
`code` slide, and scenes 3, 4, 5, 10, 11, 12, 13 and 14 are `console` slides
showing what the demo actually prints. If you change `ProductScreenDemo`,
re-check all eight against its real output — every number spoken in the
narration is one the program produces, and `DemoRunsTest` asserts that those
numbers are still the ones it prints.

### Why the problem gets five scenes

Scenes 2 to 6 are a third of the running time before the pattern is even named,
and that is the single most deliberate decision in the script.

The failure mode of teaching this pattern is that the audience files it under
"making responses smaller". So scene 4 puts the waste on screen — eighty-seven
per cent of the download discarded — and then scene 5 *fixes it*, honestly and
completely, with a query parameter that gets the payload down to two hundred and
twelve bytes: the same figure the finished pattern reaches, with no new process
to run. The narration says so out loud: if this pattern were about payload size,
the story would end there.

Scene 6 is therefore the centre of the video. The phone team asks for one
sentence of text, joined from stock, the delivery rules and the clock — half an
hour of work that waits five weeks, because a field on a shared endpoint is a
change to a contract five other clients also hold. That is what the query
parameter cannot fix, and it is what the pattern actually buys.

The same discipline runs through the bill. Scene 12's divergence throws nothing,
logs nothing, and passes both backends' tests; scene 15 ends on the warning that
all four takeaways can be got wrong without anything failing, because from inside
each backend, each backend is right.

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
--force backends-for-frontends` to refresh `narration.md`, then re-run
`./build_video.sh`. The script is written to be spoken rather than read, and
`[[slnc NNN]]` markers insert a pause of NNN milliseconds where a person
would draw breath. They are instructions to `say`, not words:
`make_subtitles.py` strips them, so keep any new ones in that exact form or
they will be read out loud.

One requirement specific to this category: the narration has to stand up with
the screen off. A listener washing up must be able to follow it, so no line
may depend on seeing the slide — the words name the caller, the callee and
the number themselves rather than pointing at them. That constraint bites
hardest on scene 10, where the slide is two JSON documents side by side: the
narration reads the phone's six fields out one at a time, by name and value,
rather than asking the listener to compare two columns. Scene 11 does the same
for the three-row table, saying each column along its row instead of naming the
grid.

## Publishing Notes

The video is encoded to YouTube's recommended settings already (1080p,
H.264, 30 fps, stereo AAC at 48 kHz), so it can be uploaded as-is.
The title, description and tags to paste at upload time live in
[`../docs/youtube.md`](../docs/youtube.md).

**Upload `backends-for-frontends-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.** The
`.m4a` and the build scripts have no role on YouTube. `poster.png` is the
video's opening frame, not the thumbnail: it is composed for a full screen,
whereas `thumbnail.png` is drawn at 1280×720 with only the name, one promise and
one line of code, so it survives being shrunk to search-result size.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`MobileBff` and `ClientBackend`, they render `BFF` as three separate words,
and they routinely turn `?fields=` into something unrecognisable. Uploading
`backends-for-frontends-pattern-explained.srt` gives exact wording and makes
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

> Learn the Backends for Frontends pattern in Java 21, starting from one online
> shop, one coffee maker, and two screens that disagree about what a product is
> — six fields on a phone, fifteen on a desktop. We watch the phone make five
> calls before a pixel is drawn, replace them with one shared endpoint that
> throws away eighty-seven per cent of what it sends, and then fix that
> completely with a query parameter — because if this pattern were about payload
> size, the story would end there. It does not: the next thing the phone team
> asks for is one line of delivery text they could write in an afternoon and
> wait five weeks to ship. That queue is what the pattern removes. Then the
> bill, which is most of the second half: a discount rule copied into one
> backend so the same product advertises a saving on the phone and none on the
> desktop, with nothing thrown and every test passing; where the shared jobs go
> and how to tell this pattern from an API gateway; and why six clients need
> three backends rather than six. No prior design-pattern knowledge needed, and
> no Docker, HTTP or framework — it all runs in one JVM. Full source code and
> written notes are in the repository.
