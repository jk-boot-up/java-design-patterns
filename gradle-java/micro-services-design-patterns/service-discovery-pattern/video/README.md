# Service Discovery Pattern — Teaching Video

A narrated, slide-based video that teaches the Service Discovery pattern using this
project's code. Aimed at beginners with no prior microservices knowledge, and
written so that it still works for somebody who is only listening.

## Output Files

| File | What it is |
| --- | --- |
| `service-discovery-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `service-discovery-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `service-discovery-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The video's opening frame, 1920×1080. Not the thumbnail — see the publishing notes below. |

**Runtime:** approximately 12 minutes.
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
| 1 | Service Discovery | Title card, author credit, the plain-language definition of the pattern, and then the same idea in the online store |
| 2 | The Scenario | Pricing runs as three interchangeable copies, and the checkout needs an address for one of them |
| 3 | The Obvious Answer — Write It Down | `HardcodedPricingClient` — four correct lines holding one address, and why it was the right code when there was one instance |
| 4 | Then Somebody Deploys Pricing | The demo's real act-one output: a routine rolling deploy takes checkout down while two healthy instances sit idle |
| 5 | Why That Really Hurts | A constant is not a question you can ask again — no retry, no failover, and nothing the client could have done better |
| 6 | The Service Discovery Pattern | The formal definition, and the beginner's version: instances put themselves on a shared list, and the caller asks that list every time |
| 7 | An Analogy | A taxi rank against a driver's mobile number — you do not insist on Dave, you take the next one on the rank |
| 8 | The Roles | `DiscoveringPricingClient`, `ServiceRegistry`, `Lease` and the four instances, with `HardcodedPricingClient` shown as the trap |
| 9 | The Registry — and the One Line That Matters | `ServiceRegistry.instances` — the lease comparison that quietly drops an instance that stopped heartbeating |
| 10 | The Caller — Ask, Then Try The Next One | `DiscoveringPricingClient.price` — the lookup, the loop over the candidates, the `STALE` note, and an honest failure if all of them are down |
| 11 | A Deployment, and a Scale-Up, With a Registry | Act two's real output: the same deploy that broke act one now passes unnoticed, and a fourth instance becomes usable without a redeploy |
| 12 | The Half That Gets Skipped: A Crash | Act three — a crash leaves the registry briefly lying, the client is handed a dead name, notes it `STALE` and succeeds 5ms later on the next one |
| 13 | The Lease Expires, and the List Corrects Itself | Act four — with no client in it at all, the lease runs out at 3000ms and the registry stops offering the dead instance |
| 14 | What the Tests Pin Down | Nineteen deterministic tests, including the one that pins the hardcoded client's outage and the one that proves the registry is consulted on every call |
| 15 | The Costs, Honestly | One more thing to run, a list that is sometimes wrong, heartbeat traffic, and the retry loop callers must now carry |
| 16 | Thanks for Watching | Like, subscribe, and where the source code lives |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 16 asks for the thumbs up and the subscribe. Both are rendered by
their own slide styles (`poster` and `outro` in `make_slides.py`) and are the
only two scenes with no page number in the footer.

Scene 16 deliberately does not name whichever pattern comes next. Publishing
order on YouTube is not the order these projects were built in, and a rendered
video cannot be corrected without re-uploading it.

Scenes 8, 4, 11, 12 and 13 are not plain text: scene 8 is a `diagram` slide
laid out by hand in `make_slides.py`, and the other four are `console` slides
showing what the demo actually prints, one per act. If you change
`ServiceDiscoveryDemo` or `LEASE_MILLIS`, re-check all four against its real
output — every number spoken in the narration is one the program produces,
including the 3000ms lease and the 5ms cost of skipping a dead instance.

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
--force api-gateway` to refresh `narration.md`, then re-run
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

**Upload `service-discovery-pattern-explained.mp4`, with `../docs/thumbnail.png` as
the thumbnail and the `.srt` as the captions.** The `.m4a` and the build
scripts have no role on YouTube. `poster.png` is the video's opening frame,
not the thumbnail: it is composed for a full screen, whereas `thumbnail.png`
is drawn at 1280×720 with only the name, one promise and one line of code, so
it survives being shrunk to search-result size.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`ProductPageGateway` and `NaiveMobileApp`. Uploading
`service-discovery-pattern-explained.srt` gives exact wording and makes the video
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

> Learn service discovery in Java 21, starting from four correct lines of
> code that hold one machine's address. Pricing runs as three
> interchangeable copies, and a routine rolling deploy takes the checkout
> down while two healthy copies sit idle — because a constant is not a
> question you can ask again. We build the registry instead: instances put
> themselves on a shared list with a lease, and the caller asks that list on
> every call. Then we spend the second half on the part that gets skipped. A
> crash leaves the registry briefly lying, the client is handed the name of
> a dead machine, and what saves it is not the registry but the caller's
> willingness to try the next one. We watch the lease expire with no client
> involved at all, and we close on the costs: one more thing to run, a list
> that is sometimes wrong, and a retry loop every caller now has to carry.
