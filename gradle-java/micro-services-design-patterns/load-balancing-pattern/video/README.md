# Client-Side Load Balancing Pattern — Teaching Video

A narrated, slide-based video that teaches the client-side Load Balancing pattern using this
project's code. Aimed at beginners with no prior microservices knowledge, and
written so that it still works for somebody who is only listening.

## Output Files

| File | What it is |
| --- | --- |
| `load-balancing-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `load-balancing-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `load-balancing-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The video's opening frame, 1920×1080. Not the thumbnail — see the publishing notes below. |

**Runtime:** approximately eighteen and a half minutes.
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
| 1 | Load Balancing | Title card, author credit, the plain-language definition of the pattern, and then the same idea in the online store |
| 2 | The Scenario | Catalog runs as three interchangeable copies, two answering in 10ms and one in 60ms, and the checkout has to ask one of them |
| 3 | The Obvious Answer — Take The First One | `FirstInstanceBalancer` — one correct line, `candidates.get(0)`, and a whole test file written against it that passes |
| 4 | Twelve Requests, One Machine | Act one's real output: 12/0/0 in 120ms, which is the fastest number in the video, while two paid-for machines sit idle |
| 5 | Why That Really Hurts | Money, imaginary headroom, a full outage when one box dies, and why one instance in a test environment hides all of it |
| 6 | The Load Balancing Pattern | The formal definition, and the beginner's version: don't take the first one, put the choosing somewhere you can change it |
| 7 | An Analogy | A row of supermarket tills — you chose, you chose on what you could see, and you will choose again next week |
| 8 | The Roles | `CatalogClient`, the `LoadBalancer` interface, the `observed` default method, and the four strategies with their real numbers |
| 9 | The Caller — Five Lines, No Policy | `CatalogClient.productName` — ask who is up, choose, call, report back, and nothing in the file that knows one machine from another |
| 10 | Take Turns — Fair, And Not Fast | Act two's real output: a perfectly even 4/4/4 that takes 320ms, because round-robin does not know what "slow" means |
| 11 | Prefer The Fast Ones — Measure First | `LeastLatencyBalancer.choose` — the loop that tries every instance once, and the test that goes red if you delete it |
| 12 | It Learned That On Its Own | Act three: 10/1/1 in 170ms, and the believed latencies of 10, 10 and 60 that nobody configured — the argument for balancing in the caller |
| 13 | The Half That Gets Skipped: Herding | `catalog-2` is exactly as fast and got one request in twelve; scale that to a thousand clients and the cluster oscillates |
| 14 | Two Perfect Clients, One Idle Machine | Act four: 2/2/0, neither client at fault, because a counter inside one client counts one client's requests |
| 15 | When To Stop Doing This | Back to the member of staff at the head of the six queues — server-side balancing, and why it is right more often than admitted |
| 16 | Thanks for Watching | Like, subscribe, and where the source code lives |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 16 asks for the thumbs up and the subscribe. Both are rendered by
their own slide styles (`poster` and `outro` in `make_slides.py`) and are the
only two scenes with no page number in the footer.

Scene 16 deliberately does not name whichever pattern comes next. Publishing
order on YouTube is not the order these projects were built in, and a rendered
video cannot be corrected without re-uploading it.

Scenes 8, 4, 10, 12 and 14 are not plain text: scene 8 is a `diagram` slide
laid out by hand in `make_slides.py`, and the other four are `console` slides
showing what the demo actually prints, one per act. If you change
`LoadBalancingDemo` or the latencies in `clusterOf`, re-check all four against
its real output — every number spoken in the narration is one the program
produces, including 120ms for act one, 320ms for act two, 170ms for act three,
and the believed latencies of 10, 10 and 60 milliseconds.

Scene 4 is the one to be careful with if you ever reorder the video. The whole
argument depends on the audience hearing that the naive strategy is the
*fastest* act before they hear anything about round-robin, because the
discomfort that follows is the teaching.

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
--force load-balancing` to refresh `narration.md`, then re-run
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

**Upload `load-balancing-pattern-explained.mp4`, with `../docs/thumbnail.png` as
the thumbnail and the `.srt` as the captions.** The `.m4a` and the build
scripts have no role on YouTube. `poster.png` is the video's opening frame,
not the thumbnail: it is composed for a full screen, whereas `thumbnail.png`
is drawn at 1280×720 with only the name, one promise and one line of code, so
it survives being shrunk to search-result size.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`LeastLatencyBalancer` and `FirstInstanceBalancer`. Uploading
`load-balancing-pattern-explained.srt` gives exact wording and makes the video
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

> Learn load balancing in Java 21, starting from one line — take the first
> instance — and a test suite written against it that passes. Catalog runs
> as three copies, two answering in ten milliseconds and one in sixty, and
> sending everything to the first one is the fastest number in the video
> while two paid-for machines sit idle. We move the choosing behind an
> interface, then compare strategies on their real numbers: round robin is
> perfectly fair and slower, and least-latency learns which copies are quick
> without anybody configuring it. The second half is the half that is
> usually left out. A counter inside one client counts one client's
> requests, so two perfectly written clients leave a machine idle between
> them, and a thousand clients all preferring the same fast copy make the
> cluster oscillate. We finish on when to stop doing this in the caller at
> all.
