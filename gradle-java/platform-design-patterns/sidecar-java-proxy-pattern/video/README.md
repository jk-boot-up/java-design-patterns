# Sidecar With a Java Proxy — Teaching Video

A narrated, slide-based video that shows one sidecar proxy being replaced by
another, written in a different language, on the same port, beside a service
that is never restarted. Aimed at beginners, and written so that it still works
for somebody who is only listening.

This is the **second of three Sidecar videos, and it does not re-teach the
first.** Scene 2 is the only recap, and it is about a minute long because the
rest of the video is worthless without it. Everything after that is one gap:
nginx has no directive for waiting between retries, because it retries by moving
to the next entry in an upstream group and that move is immediate.

The running order splits in three. Scenes 3 to 6 establish the gap and make the
case that nobody wrote a bug — the sentence the payment provider asked for does
not exist in nginx's configuration language, which is a different situation from
a mistake because there is nothing to correct. Scenes 7 to 10 are the swap and
what it proves. Scenes 12 to 14 are the bill, which is longer than the benefit,
and scene 15 is the narrow rule that is the reason the video ends by advising
most viewers not to do any of this.

## Output Files

| File | What it is |
| --- | --- |
| `sidecar-java-proxy-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `sidecar-java-proxy-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `sidecar-java-proxy-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The video's opening frame, 1920×1080. Not the thumbnail — see the publishing notes below. |

**Runtime:** 19 minutes 59 seconds, over 17 scenes and 301 subtitle cues.
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

The pipeline is the category's shared one, unchanged from `../../sidecar-pattern/video/build_video.sh`
apart from the output names. Its design — why the audio is encoded exactly once
at the mux, why loudness normalisation runs in two passes, why there is
deliberately no denoiser in the cleanup chain, and what the timestamp-continuity
check after the mux is for — is documented in full in
[`../../sidecar-pattern/video/README.md`](../../sidecar-pattern/video/README.md).
Read that before changing any of the ffmpeg calls here.

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
| 1 | Sidecar with a Java Proxy | Title card, author credit, the plain-language definition — the contract is an address — the kettle, the plug and the fuse, and the warning that this video is a follow-on |
| 2 | One Minute On Where We Are | The only recap of §41: the retry policy left the service, it lives in a proxy next door, and checkout's whole configuration is one local address |
| 3 | The Letter From The Provider | March — at most three attempts, *and wait properly between them* — and the fact that the shop can say only the first half |
| 4 | Three Attempts That Bought Nothing | Act 2 — the provider's own log: 1 ms, 2 ms, 3 ms, all inside a wobble that clears at 300 ms, and a £47.99 coffee maker NOT PAID |
| 5 | Nobody Wrote A Bug | The upstream group: a list of servers, the same address three times, and no backoff directive anywhere — correct for a pool of machines, wrong in front of one supplier |
| 6 | Three Ways Out, Two Of Them Bad | Put the waiting back in the service; script the proxy in Lua; or put a different proxy on the port — and why the third is only available because the contract is an address |
| 7 | The Loop, With The Sentence Missing | `NginxProxy.forward`, ending on the comment where the waiting would go if it could be said at all |
| 8 | Forty Lines Of Java | `JavaProxy.forward` — the same loop plus four lines — why the doubling matters, and the honest note about the jitter this one deliberately does not have |
| 9 | The Swap | Act 4 — `port.install(java)`, one line, and it takes a proxy: no service to notify, no restart, one payments service ever constructed |
| 10 | The Same Wobble, The Same Three Attempts | Act 5 — 1 ms, 202 ms, 603 ms, charged. Same allowance, no extra traffic, only the spacing changed |
| 11 | What Is Actually In This Program | `PaymentsService`, `LocalPort`, the `Proxy` interface and its two implementations, one shared `ProxyPolicy`, and the provider's `CallLog` |
| 12 | The Gap In The Middle Of A Swap | Act 6 — a healthy everything, a £31.50 kettle refused, zero attempts reaching the provider, and nothing in the provider's dashboards to show it happened |
| 13 | A Claim Is Not A Demonstration | Act 7 — 22 lines of nginx configuration against 40 of Java, on one port, with a service source file that is byte for byte identical in both runs |
| 14 | The Bill, Which Is Longer | Somebody else's config became your code; TLS, access logs and pooling are gone until you write them; a JVM per service; and the fence that came down with the limitation |
| 15 | The Rule To Take Away | Swap the proxy when the thing you need cannot be said in the configuration language *at all* — and the option itself being the real prize |
| 16 | What To Remember | The contract is an address; ask better before asking more; prove it by identity rather than behaviour; a swap is a rollout |
| 17 | Thanks for Watching | Where the source lives, like, subscribe, and an invitation to disagree with the rule |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 17 asks for the thumbs up and the subscribe. Both are rendered by
their own slide styles (`poster` and `outro` in `make_slides.py`) and are the
only two scenes with no page number in the footer.

Scene 17 deliberately does not name whichever pattern comes next. Publishing
order on YouTube is not the order these projects were built in, and a rendered
video cannot be corrected without re-uploading it.

Scene 11 is a `diagram` slide laid out by hand in `make_slides.py`, scenes 7 and
8 are `code` slides, and scenes 4, 9, 10, 12 and 13 are `console` slides showing
what the demo actually prints. If you change `ProxySwapDemo`, re-check all five
against its real output — every number spoken in the narration is one the
program produces, and `DemoRunsTest` asserts that those numbers are still the
ones it prints, including that no line grows past 76 columns.

### Why the recap is only one scene

The category's rule for the three Sidecar projects is that §42 and §43 must not
re-teach what a sidecar is. If a draft of either finds itself explaining what a
sidecar is for more than one scene, it has drifted.

That is why scene 1 says out loud that this is a follow-on and names the video
to watch first, and why scene 2 is a minute rather than five. The cost of that
decision is that somebody arriving here cold will be lost, and the script
accepts it rather than trying to serve both audiences badly.

### Why the bill is three scenes and the benefit is two

The failure mode of this material is that it reads as an argument for writing
your own proxy, and it is not one. Most viewers should keep nginx, accept the
gap, and spend the afternoon on something else.

So scene 12 shows a completely healthy system losing a payment because of the
swap itself, scene 14 goes through what forty lines of your own code actually
costs, and the last item on that bill is the one that appears on no invoice: a
configuration language is a fence, and taking the limitation away takes the
fence down with it. Scene 15 then makes the rule narrow on purpose — *cannot be
said at all*, not *awkward* — so that the thing the viewer remembers is the bar,
not the technique.

The point of the video is not the swap. It is that the swap was *available*, in
an afternoon, because the contract was an address.

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
--force sidecar-java-proxy`, then re-run `./build_video.sh`. The script is
written to be spoken rather than read, and `[[slnc NNN]]` markers insert a pause
of NNN milliseconds where a person would draw breath. They are instructions to
`say`, not words: `make_subtitles.py` strips them, so keep any new ones in that
exact form or they will be read out loud.

One requirement specific to this category: the narration has to stand up with
the screen off. A listener washing up must be able to follow it, so no line may
depend on seeing the slide — the words name the proxy, the millisecond and the
outcome themselves rather than pointing at them. That constraint bites hardest
on scenes 4 and 10, where the slide is a block of arrival times: the narration
reads each attempt out as a sentence, in order, so that the listener arrives at
the third one in the same order the payment provider did.

## Publishing Notes

The video is encoded to YouTube's recommended settings already (1080p,
H.264, 30 fps, stereo AAC at 48 kHz), so it can be uploaded as-is.
The title, description and tags to paste at upload time live in
[`../docs/youtube.md`](../docs/youtube.md).

**Upload `sidecar-java-proxy-pattern-explained.mp4`, with `../docs/thumbnail.png`
as the thumbnail and the `.srt` as the captions.** The `.m4a` and the build
scripts have no role on YouTube. `poster.png` is the video's opening frame, not
the thumbnail: it is composed for a full screen, whereas `thumbnail.png` is drawn
at 1280×720 with only the name, one promise and one line of code, so it survives
being shrunk to search-result size.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear `JavaProxy`, `LocalPort` and
`ProxyPolicy`, they render *nginx* as *engine X* about half the time, and they
turn "sidecar" into "side car". Uploading
`sidecar-java-proxy-pattern-explained.srt` gives exact wording and makes the
video searchable.

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

> Watch a sidecar proxy be replaced, on the same port, by one written in a
> different language — while the service beside it keeps running and is never
> told. An online shop takes payments through a proxy running next door, which
> is twenty-two lines of nginx configuration. In March the payment provider asks
> for two things: at most three attempts per payment, and a proper wait between
> them. The shop can say the first half and not the second, and three weeks
> later a bad three hundred milliseconds costs it a sale — three attempts at one,
> two and three milliseconds, all inside the wobble, and a £47.99 order NOT PAID.
> Nobody wrote a bug: nginx has no retry counter, it has an upstream group, and
> moving to the next entry is immediate by design. The sentence the provider
> asked for does not exist in the language the policy is written in. So we put
> forty lines of Java on the port instead — the same loop plus four lines — and
> the same three attempts arrive at one, two hundred and two, and six hundred and
> three milliseconds, and the payment goes through with no extra traffic to the
> provider at all. The service is not rebuilt, not restarted, and not told; a
> test asserts it is the same object afterwards rather than that it merely
> behaves the same. Then the bill, which is longer than the benefit: somebody
> else's configuration became your code to test and patch, TLS termination and
> access logs and connection pooling are gone until you write them, a JVM now
> sits beside every service, a request arriving mid-swap is refused with zero
> attempts reaching the provider — and nothing now stops the next person putting
> the shop's refund rules in the proxy, because the limitation and the fence were
> the same thing. Finishing with the narrow rule: swap the proxy when the thing
> you need cannot be said in the configuration language at all — not when it is
> awkward. Java 21, no Docker, no Kubernetes and no network needed; it all runs
> in one JVM. Watch the Sidecar video first. Full source code and written notes
> are in the repository.
