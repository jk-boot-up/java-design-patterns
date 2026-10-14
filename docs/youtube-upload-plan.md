# YouTube upload plan

A plan for publishing the pattern videos on the channel, starting with Circuit Breaker. It
follows the rules in [youtube-upload-spec.md](youtube-upload-spec.md). This is a plan only:
nothing is uploaded until the channel owner does it.

## The plan, step by step

1. **Pick the files** from the project's local build (none of them are in git):
   - the video: the `-amy-slow.mp4` (older projects) or the plain `.mp4` (newer projects).
     The `.mp4` contains picture and narration together, so **no separate audio is uploaded**;
     the `.m4a` beside it is an audio-only copy and stays local;
   - the thumbnail: that project's own `docs/thumbnail.png` (every project has one);
   - optionally, the captions: the `.srt` with the same name as the video (text, not audio).
2. **Prepare the text** from the project's `docs/youtube.md`:
   - the title as written;
   - the description, with every `http://` and `https://` removed, and the chapters timed
     from the uploaded video's own `.srt`;
   - the tags as written.
3. **Upload in YouTube Studio**: Create, then Upload videos, then select the `.mp4`.
4. **Details page**:
   - paste the title and description;
   - **Thumbnail**: Upload file, then choose the project's `docs/thumbnail.png`;
   - **Playlists**: the playlist for the project's category (see the table below); if it
     does not exist yet, create it there with New playlist, Public;
   - **Audience**: select **"No, it's not made for kids"**;
   - **Paid promotion** (under Show more): select **"No, my video doesn't include paid promotion"**;
   - **Altered content** (under Show more): select **No**. The narration is a synthetic
     text-to-speech voice, but it imitates no real person, and the video is slides, not
     realistic footage, so it does not meet YouTube's definition of altered or synthetic
     content;
   - under Show more: tags, language English, category Science & Technology.
5. **Video elements**: optionally add the captions (Upload file, With timing, the `.srt`),
   then an end screen and a playlist card.
6. **Check before saving**: the project's thumbnail is showing, "not made for kids" and
   altered content "No" are selected, the description has no
   `http://` or `https://`, the chapters start at `00:00`, and the captions are attached if used.
7. **Visibility**: choose **Public**, tick **Set as instant Premiere**, and save. Premiere
   cannot be added once the video is public.
8. **Check after publishing**: the chapters appear under the progress bar, the captions are in
   sync if added, and the first and last minute sound clean. Share the link only after 1080p
   processing has finished, because code slides are unreadable at lower quality.
9. **Repeat per project**, a few at a time, in learning order for the playlist.

## Playlists by category

Each category has **two** playlists, so plain-Java and framework videos are never mixed: each
playlist is the name below plus a suffix: **" - Without Frameworks"** for the plain-Java videos,
**" - With Frameworks"** for the framework versions (a slug that extends a plain one, such as
`retry-with-resilience4j`). For example *Structural Design Patterns in Java - Without
Frameworks* and *Structural Design Patterns in Java - With Frameworks*. The
uploader picks the right one and creates it on first use.

| Category folder | Playlist | Status |
| --- | --- | --- |
| `micro-services-design-patterns` | Micro Services Design Patterns | exists |
| `behavioural` | Behavioral Design Patterns in Java | exists |
| `architectural-design-patterns` | Architectural Design Patterns in Java | create on first upload |
| `concurrency-design-patterns` | Concurrency Design Patterns in Java | create on first upload |
| `creational` | Creational Design Patterns in Java | create on first upload |
| `domain-driven-design-patterns` | Domain-Driven Design Patterns in Java | create on first upload |
| `enterprise-design-patterns` | Enterprise Design Patterns in Java | create on first upload |
| `foundational-design-patterns` | Foundational Design Patterns in Java | create on first upload |
| `functional-design-patterns` | Functional Design Patterns in Java | create on first upload |
| `messaging-integration-patterns` | Messaging and Integration Patterns in Java | create on first upload |
| `platform-design-patterns` | Platform Design Patterns in Java | create on first upload |
| `security-design-patterns` | Security Design Patterns in Java | create on first upload |
| `structural` | Structural Design Patterns in Java | create on first upload |
| `testing-design-patterns` | Testing Design Patterns in Java | create on first upload |

## Rollout: every project to YouTube

The channel owner asked for every project under `gradle-java/` to be uploaded, following the
batch rules in section 8 of [youtube-upload-spec.md](youtube-upload-spec.md).

**Already on the channel** before the batch began (uploaded by the owner, plus Circuit Breaker):
api-composition, api-gateway, api-gateway-with-spring-cloud-gateway, async-request-reply,
backpressure, backpressure-with-reactor, bulkhead, bulkhead-with-resilience4j, cache-aside,
cache-aside-with-redis, circuit-breaker (all in `micro-services-design-patterns`).

**Order of the batch:**

| # | Category | Projects | Playlist |
| --- | --- | --- | --- |
| 1 | micro-services-design-patterns | 58 (11 already up) | Micro Services Design Patterns |
| 2 | architectural-design-patterns | 22 | Architectural Design Patterns in Java |
| 3 | behavioural | 20 | Behavioral Design Patterns in Java |
| 4 | concurrency-design-patterns | 24 | Concurrency Design Patterns in Java |
| 5 | creational | 9 | Creational Design Patterns in Java |
| 6 | domain-driven-design-patterns | 9 | Domain-Driven Design Patterns in Java |
| 7 | enterprise-design-patterns | 30 | Enterprise Design Patterns in Java |
| 8 | foundational-design-patterns | 21 | Foundational Design Patterns in Java |
| 9 | functional-design-patterns | 5 | Functional Design Patterns in Java |
| 10 | messaging-integration-patterns | 31 | Messaging and Integration Patterns in Java |
| 11 | platform-design-patterns | 20 | Platform Design Patterns in Java |
| 12 | security-design-patterns | 9 | Security Design Patterns in Java |
| 13 | structural | 8 | Structural Design Patterns in Java |
| 14 | testing-design-patterns | 6 | Testing Design Patterns in Java |

272 projects in all.

**Steps:**

1. `ytupload.sh sync`: record the links of every video already on the channel in
   `gradle-java/docs/youtube-links.json`.
2. `ytupload.sh batch micro-services-design-patterns`: upload and publish the rest of the
   category, one video at a time, skipping anything already up. A failed thumbnail does not
   stop a video; any other failed step leaves that project as a draft and is logged.
3. After each batch, regenerate the tracking document `gradle-java/docs/youtube-links.md`
   (and `.html`) and the repository index (`index.md` / `index.html`), which shows a
   **YouTube** link beside every uploaded project.
4. Repeat step 2 for each category in the order above.
5. When YouTube's daily upload limit is reached, the batch stops; it is run again the next day
   with the same command.

**Where progress is kept:** the registry `gradle-java/docs/youtube-links.json` and the tracking
document generated from it show which projects are uploaded and which are still to go.

**Known gaps:** captions (the `.srt`) are not uploaded by the script yet. The `docs/youtube.md`
files still carry the deleted Kokoro videos' chapter times, but the uploader recomputes the
chapters from the amy-slow `.srt` at upload time, so uploads are not affected.

## Resuming (state saved 14 October 2026)

**Resumed and finished on 14 October 2026; nothing is running.** All 272 projects are Public with custom thumbnails, and the registry matches the channel one for one. Before the next run, check `~/.ytupload-chrome/status.txt` and the tail of `batch.log`.

- **Stop rule (owner, 7 October):** when YouTube refuses a custom thumbnail, the stream stops for the day and is **not** restarted automatically. `stream.py` exits at the limit.
- **14 October:** `retry-pattern` was uploaded. `backpressure-with-reactor-pattern` (`_aTqu5e_6oE`) and `valet-key-pattern` (`oJ53K32YMnQ`) turned out to be Public already (premiered 6 and 7 October, thumbnails in place); only the registry still called them drafts, so it was corrected. `ytupload.finish_draft()` and `resume()` now find a draft with `draft_row()`: Studio's Filter box first asks for a property (Title), and a row has to match the title whole, because "Valet Key" is also the start of "Valet Key with Amazon S3 Presigned URLs".
- **14 October, with the owner's go-ahead:** the broken drafts of `write-through-cache-pattern` and `clean-architecture-with-spring-pattern` were deleted forever and both were uploaded fresh (`v4DNzP75bss`, `8wgBTD3dx_c`).
- **Stray drafts:** Studio's Channel content also lists 9 old drafts without a playable video, left by failed attempts (titles such as "retry pattern explained amy slow"); every one duplicates a Public video. The owner asked on 14 October to delete them, but Claude Code's permission check blocked the scripted deletion, so they are still there: delete them by hand in Studio (row Options, Delete forever), or allow the deletion and ask again.

**Where it stands:** all 272 videos have been rebuilt with the new outro ("If you found this
useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps
the channel grow and bring you more content. Thanks for watching!") in the amy-slow voice.
188 are Public on YouTube with their thumbnails; the rest are being uploaded. The 108
videos published before 4 October were deleted by the channel owner and are being re-uploaded
from the rebuilt files. Each category has two playlists, "... - Without Frameworks" and
"... - With Frameworks".

**How the uploads run:** `tools/ytupload/stream.py` uploads one video at a time, and only after
`tools/ytupload/verify.py` passes it. The checks: amy-slow voice, fresh build, new outro in the
captions *and* heard in the audio by speech-to-text, 1920x1080 H.264 with AAC audio, loudness
-16 LUFS, true peak at most -0.5 dB, length matching the captions, a 1280x720 thumbnail and valid
YouTube fields. When YouTube refuses a custom thumbnail the stream stops for the day; on the next
run (only when the channel owner asks) it first re-tries the refused thumbnail.

**To check:** `~/.ytupload-chrome/status.txt` (one line), `~/.ytupload-chrome/batch.log` (one line per
video), `~/.ytupload-chrome/stream/stream.log`, and the registry `gradle-java/youtube-links.json`.

**To resume after a restart or in a new session:**

1. Start the upload Chrome if it is not running: `tools/ytupload/ytupload.sh chrome` (sign in if asked).
2. Start the stream: `tools/ytupload/.venv/bin/python -u tools/ytupload/stream.py >> ~/.ytupload-chrome/stream/stream.log 2>&1 &`
   It skips everything already in the registry, so it is safe to start again at any time.
3. Speech-to-text for `verify.py` lives outside the repository in `~/.cache/videocheck`
   (`python3 -m venv ~/.cache/videocheck && ~/.cache/videocheck/bin/pip install faster-whisper`).

**Open items:**
- `foundational-design-patterns/null-object-pattern`: two earlier attempts stalled after attaching
  the file; its entry was cleared so it uploads fresh. One or two stray drafts titled "Null Object in
  Java - The Discount That Is Not There" may remain in Studio; delete them by hand.
- `micro-services-design-patterns/backpressure-with-reactor-pattern`: a draft exists (ID `_aTqu5e_6oE`);
  finishing it timed out twice and it has one more try. If it fails again, finish it with
  `ytupload.sh resume <project>` then `ytupload.sh publish`, or delete the draft and clear its entry.
- `messaging-integration-patterns/splitter-aggregator-with-camel-pattern` clipped (true peak +1 dB)
  because its cached narration from 28 September peaked at full scale; it was re-voiced with
  `videokit.sh build ... --version=amy-slow --force` and now passes. If another video fails the
  peak check, do the same.
- Empty old playlists to delete by hand: "Micro Services Design Patterns", "Behavioral Design
  Patterns in Java", "Concurrency Design Patterns in Java with Frameworks".
- Nothing from this work is committed yet (scripts, outro text, narration docs, tools/ytupload).

## First video: Circuit Breaker

Project: `gradle-java/micro-services-design-patterns/circuit-breaker-pattern`

| What | Value |
| --- | --- |
| Video | `gradle-java/micro-services-design-patterns/circuit-breaker-pattern/video/circuit-breaker-pattern-explained-amy-slow.mp4` (18:45, 1920×1080, H.264, AAC 48 kHz) |
| Thumbnail | `gradle-java/micro-services-design-patterns/circuit-breaker-pattern/docs/thumbnail.png` (1280×720) |
| Captions (optional) | `gradle-java/micro-services-design-patterns/circuit-breaker-pattern/video/circuit-breaker-pattern-explained-amy-slow.srt` (205 cues) |
| Not uploaded | `gradle-java/micro-services-design-patterns/circuit-breaker-pattern/video/circuit-breaker-pattern-explained-amy-slow.m4a` |
| Visibility | Public, instant Premiere |
| Audience | No, it's not made for kids |
| Paid promotion | No |
| Altered or synthetic content | No |
| Category and language | Science & Technology, English |
| Playlist | Micro Services Design Patterns (already exists) |

### Title

```
Circuit Breaker in Java - When a Service Stops
```

### Description (ready to paste)

No `http://` or `https://`, and the chapters are timed for the amy-slow video.

```
Circuit breaker pattern in Java 21: a circuit breaker watches calls to another service, and after too many failures stops calling it for a while and fails fast instead, like a fuse that trips. We start from a service that has stopped answering — not refusing, which would be easy, but simply not replying. The retry loop is presented fairly: no bug, the right page, every test passing, and nine seconds spent producing a page you could have had immediately. The third cost is the one that actually breaks the shop: while those threads wait, checkout cannot get one. We use a fuse box as the analogy and then build the breaker as three questions inside one method, with the states named as a wire rather than a door — closed, open, half open — and a success that resets rather than decrements. Six pages, three calls, three refusals, and the clock stops moving. Then the hinge: a breaker makes failures fast, not invisible. Checkout has no fallback, so speed buys it a fast honest no, and the same wiring with one different catch block prints a receipt for money that never moved.

CHAPTERS
00:00 Introduction
01:24 The Scenario
02:28 The Obvious Answer — Just Try Again
03:18 Act One — Retry, Applied To An Outage
04:10 Three Costs — And The Third Closes The Shop
05:22 The Fuse Box
06:20 One Word That Reads Backwards
07:18 The Whole Decision, In One Method
08:30 Act Two — Six Pages, With A Breaker
09:54 The Pieces, And What Each One Decides
11:20 Act Three — It Lets Itself Back In
12:34 Now The Half That Gets Left Out
13:38 Act Four — Checkout, Where There Is No Fallback
14:48 Act Five — The Fallback That Lies
16:10 What It Costs, And When Not To
17:19 Thanks for Watching

SOURCE CODE, WRITTEN NOTES AND AN INTERACTIVE ANIMATION
github.com/jk-boot-up/java-design-patterns/tree/main/gradle-java/micro-services-design-patterns/circuit-breaker-pattern

WHAT YOU NEED FIRST
Java 21 and a working knowledge of classes and interfaces. No prior design-pattern knowledge is assumed. The full prerequisites are in docs/prerequisites.md in the repository.
```

### Tags

```
circuit breaker pattern, resilience4j, fault tolerance java, design patterns, java design patterns, gang of four, java 21, software design, clean code, object oriented design, java tutorial, ecommerce, programming tutorial
```
