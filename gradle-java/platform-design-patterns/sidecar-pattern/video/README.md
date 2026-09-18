# Sidecar Pattern — Teaching Video

A narrated, slide-based video that teaches the Sidecar pattern using this
project's code. Aimed at beginners who have never run a proxy, a container or a
service mesh, and written so that it still works for somebody who is only
listening.

The running order splits in two. Scenes 2 to 6 are the problem, and they take
longer than a problem usually does on purpose: the audience has to *believe*
that nobody was careless before the pattern can look like anything other than
bureaucracy. Scene 5 is the hinge — the fault is an absence, a method nobody
wrote, which is why no review, no test and no linter caught it. Scene 6 is the
incident, and it is the pivot of the whole video: the service that misbehaved
succeeds and stays green, and the service that fails is correct in every line.
Scenes 11, 12 and 13 are the bill — a second process per service, a second thing
that can be down, and a millisecond on every call — and scene 14 is the
admission that in one program this structure *is* Decorator.

## Output Files

| File | What it is |
| --- | --- |
| `sidecar-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `sidecar-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `sidecar-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The video's opening frame, 1920×1080. Not the thumbnail — see the publishing notes below. |

**Runtime:** 18 minutes 36 seconds, over 16 scenes and 271 subtitle cues.
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
| 1 | Sidecar | Title card, author credit, the plain-language definition of the pattern, the restaurant kitchen and the one telephone, and then the same idea in the online store |
| 2 | The Scenario | Four services that charge cards — checkout, refunds, subscription billing, marketplace payouts — four teams, four repositories, one payment provider behind all of them |
| 3 | Sixteen Copies of Four Decisions | Act 1 — attempts, backoff, deadline and TLS profile, decided four times, none of them a fact about the shop |
| 4 | March — The Change Lands Three Times | Act 2 — three pull requests in one afternoon, the fourth service nobody opened, and why nobody was careless or even wrong |
| 5 | The Incident Is an Absence, Not a Mistake | `applyPolicyReview()` in three services and missing from the fourth — an absence has nothing to compare against, and the test that pins it |
| 6 | Two In The Morning, Three Weeks Later | Act 3 — a 300 ms wobble, a 12-attempt account allowance, billing spending six of them and marketplace payouts refused at 13 |
| 7 | The Pattern | The sentence, and the two phrases carrying it — **separate process** and **beside** — with the near miss each one rules out, and why a shared library does not fix it |
| 8 | Who Does What | `TakesPayments`, `ServiceBehindASidecar`, `Sidecar` and one shared `SidecarConfig`, with the four old services and the gateway's `CallLog` alongside |
| 9 | What Is Left In The Service | `ServiceBehindASidecar.pay` in one line, the proxy's loop reading a config it does not own, and the `HOP_MILLIS` line that is the bill |
| 10 | The Same Night, With A Proxy Beside Each Service | Act 4 — the same wobble, the same allowance, 12 of 12 attempts and nobody refused: the policy stated once rather than applied four times |
| 11 | The Bill, Part One — Twice As Many Things To Run | Act 5 — 16 copies → 4, four edit sites → one, four processes → eight, and the rule that shop facts may not move into a proxy |
| 12 | The Bill, Part Two — A Second Thing That Can Be Down | Act 6 — the proxy fails to start, zero attempts reach the gateway, and a failure that is rarer but wider than the one it replaced |
| 13 | The Bill, Part Three — One Millisecond, On Every Call | Act 7 — 600 ms against 603 ms, nothing on a payment and fifty per cent on a 2 ms internal call, and the arithmetic that decides a service mesh |
| 14 | The Admission — This Is Decorator, Until You Deploy It | The structure is Decorator; what differs is where the code runs — and the two questions that decide between them |
| 15 | What to Take Away | Count the copies not the services; the failure lands where the cause is not; you have met this already; it is where the code runs — and all four fail silently |
| 16 | Thanks for Watching | The three costs as running code, like, subscribe, and where the source lives |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 16 asks for the thumbs up and the subscribe. Both are rendered by
their own slide styles (`poster` and `outro` in `make_slides.py`) and are the
only two scenes with no page number in the footer.

Scene 16 deliberately does not name whichever pattern comes next. Publishing
order on YouTube is not the order these projects were built in, and a rendered
video cannot be corrected without re-uploading it.

Scene 8 is a `diagram` slide laid out by hand in `make_slides.py`, scenes 5 and
9 are `code` slides, and scenes 3, 4, 6, 10, 11, 12 and 13 are `console` slides
showing what the demo actually prints. If you change `PaymentsDemo`, re-check
all seven against its real output — every number spoken in the narration is one
the program produces, and `DemoRunsTest` asserts that those numbers are still
the ones it prints, including that no line grows past 76 columns.

### Why the problem gets five scenes

Scenes 2 to 6 are a third of the running time before the pattern is even named,
and that is the single most deliberate decision in the script.

The failure mode of teaching this pattern is that the audience files it under
"somebody forgot to update a service", concludes that the answer is a better
checklist, and stops listening. So scene 4 spends its time establishing that the
fourth service was not missed through carelessness — it runs overnight, it is
owned by another team, it had no open work that sprint, and there was no fourth
place to look unless you already knew there was one. Scene 5 then shows the
fault in the code and shows that it is an *absence*: a method nobody wrote. A
wrong value can be compared against three right ones. An absence cannot.

Scene 6 is therefore the centre of the video. The service with the stale copy
succeeds, gets its money, and leaves every one of its own dashboards green,
while the service whose every line is correct is refused because it happened to
arrive fourth. The cause and the failure are in different repositories, owned by
different people. That is the thing a checklist does not fix, and it is what the
pattern actually buys.

The same discipline runs through the bill. All three costs in scenes 11 to 13
are prices rather than mistakes, scene 14 concedes that in one program this is
Decorator, and scene 15 ends on the warning that every takeaway can be got wrong
without anything failing — because from inside each service, each service is
right.

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
--force sidecar`, then re-run `./build_video.sh`. The script is written to be
spoken rather than read, and `[[slnc NNN]]` markers insert a pause of NNN
milliseconds where a person would draw breath. They are instructions to `say`,
not words: `make_subtitles.py` strips them, so keep any new ones in that exact
form or they will be read out loud.

One requirement specific to this category: the narration has to stand up with
the screen off. A listener washing up must be able to follow it, so no line may
depend on seeing the slide — the words name the service, the proxy and the
number themselves rather than pointing at them. That constraint bites hardest on
scene 6, where the slide is a four-row table of the night's payments: the
narration tells it as a story in order instead, one service at a time, so that
the listener arrives at the refusal in the same order the gateway did. Scene 11
does the same for the three-row before-and-after table, reading each row along
its length rather than naming a grid.

## Publishing Notes

The video is encoded to YouTube's recommended settings already (1080p,
H.264, 30 fps, stereo AAC at 48 kHz), so it can be uploaded as-is.
The title, description and tags to paste at upload time live in
[`../docs/youtube.md`](../docs/youtube.md).

**Upload `sidecar-pattern-explained.mp4`, with `../docs/thumbnail.png` as the
thumbnail and the `.srt` as the captions.** The `.m4a` and the build scripts
have no role on YouTube. `poster.png` is the video's opening frame, not the
thumbnail: it is composed for a full screen, whereas `thumbnail.png` is drawn at
1280×720 with only the name, one promise and one line of code, so it survives
being shrunk to search-result size.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`SidecarConfig` and `ServiceBehindASidecar`, they render `TLS1.3` as
something unrecognisable, and they turn "sidecar" into "side car" about half
the time. Uploading `sidecar-pattern-explained.srt` gives exact wording and
makes the video searchable.

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

> Learn the Sidecar pattern in Java 21, starting from an online shop that
> charges cards in four places — checkout, refunds, subscription billing and
> marketplace payouts — with one payment provider behind all four. Each of the
> four teams had to decide the same four things before going live: how many
> times to retry, when to give up, which TLS profile to present, and what to
> count. Sixteen copies of four decisions, and not one of them a fact about the
> shop. When the provider changes its retry policy in March, the change lands in
> three services and misses the fourth — not through carelessness, but because
> there was no fourth place to look. Three weeks later, at two in the morning,
> that stale copy spends half the account's attempt allowance and a completely
> correct service is refused. Then we stand a proxy beside each service, state
> the policy once, and run the same night clean. Then the bill, which is most of
> the second half: twice as many processes to run and patch, a second thing that
> can be down and takes every call with it, and one millisecond on every call —
> the arithmetic that decides whether a service mesh belongs in your system.
> Finishing with the admission most write-ups skip: in one program this
> structure is Decorator, and what makes it a different pattern is not the code
> but where the code runs. No prior design-pattern knowledge needed, and no
> Docker, Kubernetes or network — it all runs in one JVM. Full source code and
> written notes are in the repository.
