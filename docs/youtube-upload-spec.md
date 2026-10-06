# YouTube upload spec

How a pattern video goes from a project folder to YouTube. Each project's
`docs/youtube.md` holds the title, description, chapters, tags and thumbnail;
this spec says which files to upload, what to change on the way, and what to
check before and after a video goes public. The step-by-step plan and the first video's
ready-to-paste sheet are in [youtube-upload-plan.md](youtube-upload-plan.md).

## 1. Which files are uploaded

| What | File | Notes |
| --- | --- | --- |
| Video | `video/<slug>-pattern-explained-amy-slow.mp4` where that file exists (the older projects); otherwise `video/<slug>-pattern-explained.mp4` (projects built with amy-slow as their only voice) | 1920×1080, H.264, 30 fps, AAC 48 kHz: no re-encode needed. **The `.mp4` already contains the narration**, so no audio file is uploaded |
| Captions (optional, recommended) | the `.srt` with the **same name** as the video | text captions, not audio: they make the video searchable and readable with the sound off |
| Thumbnail | the project's own `docs/thumbnail.png` (all 272 projects have one) | 1280×720; always uploaded, never an auto-picked frame; `video/poster.png` is the title card, not the thumbnail |

The `.m4a` beside each video is an audio-only copy for listening offline; it is never part of
an upload. Every video is narrated in the amy-slow voice (Piper `en_US-amy-medium`, speed 0.8);
the older Kokoro builds have been deleted. Videos, audio and captions are never committed to
git; they are uploaded from the local build only.

## 2. Rules for the uploaded text

- **No `http://` or `https://` in the description.** Every scheme prefix is removed, so
  the repository link reads as a bare address:
  `github.com/jk-boot-up/java-design-patterns/tree/main/gradle-java/...`.
  YouTube refused descriptions carrying URLs on this channel. The Markdown files may keep
  full links for readers on GitHub; the stripping happens on the text sent to YouTube.
- **No `<` or `>` characters** in the title or description: YouTube rejects them.
- **The first sentence is the name and the plain definition**
  ("X pattern in Java: …"), as `docs/youtube.md` already has it.
- **Chapters must match the uploaded video.** They are timed from the uploaded video's own
  `.srt`. Some older `docs/youtube.md` files still carry chapters and a runtime from the
  deleted Kokoro build; until those are regenerated, recompute the chapters from the
  amy-slow `.srt` at upload time. The first chapter is `00:00`, and there are at least three,
  or YouTube shows no chapters.
- Title at most 100 characters (aim for 60, which survives search results); description at
  most 5,000 characters; tags at most 500 characters in total.

## 3. Upload settings

| Setting | Value |
| --- | --- |
| Visibility | **Public**, with **Set as instant Premiere** ticked, saved once the checks in section 5 that can be done before saving have passed. Premiere can only be chosen before saving, never afterwards |
| Audience | **No, it's not made for kids** |
| Paid promotion (Show more) | **No, my video doesn't include paid promotion** |
| Altered or synthetic content (Show more) | **No**: the voice is synthetic text-to-speech but imitates no real person, and the video is slides, not realistic footage, so YouTube's disclosure does not apply |
| Category | **Science & Technology** |
| Video language | English, set **before** adding subtitles, or the subtitle option may not appear |
| Subtitles | Video elements → Add subtitles → Upload file → With timing → the matching `.srt` |
| Thumbnail | Details → Thumbnail → Upload file → the project's `docs/thumbnail.png` (needs a verified channel) |
| Playlist | the playlist for the project's category (section 3a: plain or with Frameworks), in learning order |
| End screen and cards | End screen to whichever video is already published; a card to the playlist. Never announce "next pattern" |

## 3a. Two playlists per category: plain and framework

Each video goes into the playlist for its project's category folder under `gradle-java/`.
Two playlists already exist on the channel; the others are created, with the names below, when
the first video of that category is uploaded. Plain-Java and framework videos are never mixed:
each playlist is the name below plus " - Without Frameworks" for plain-Java videos or
" - With Frameworks" for framework versions (a slug that extends a plain one, for example
`circuit-breaker-with-resilience4j-pattern`), e.g. *Micro Services Design Patterns - With
Frameworks*.
Playlists are Public.

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

## 4. Ways to upload

1. **The scripted uploader, `tools/ytupload/ytupload.sh`** (the method in use). It drives
   YouTube Studio in a dedicated Chrome window (`ytupload.sh chrome`) that the channel owner
   signed in to by hand; it never types a password. It is run only when the channel owner asks
   for uploads.
   - `sheet <project>` prints what would be uploaded;
   - `upload <project>` attaches the `.mp4`, fills every field of section 3, and stops on the
     Visibility page; `resume <project>` continues a draft after a failed step without
     attaching the video again;
   - `publish` chooses Public, ticks instant Premiere, saves, prints the link and closes the
     "Video published" dialog;
   - `sync` reads the channel's video list and records every link it can match to a project;
   - `batch <category-or-project>...` uploads and publishes many projects in turn (section 8);
   - `no-paid-promotion <video-id>` fixes that answer on a video already published.
2. **YouTube Studio by hand**, from the upload sheet (section 6), with the same settings.
3. **YouTube Data API script** is not used: videos uploaded through an API project that has
   not passed Google's audit stay locked private, and these videos are published as Public.

## 5. Checks

Videos are saved as **Public** directly, so the checks are split around the save.

Before saving:

- [ ] The description has no `http://`, `https://`, `<` or `>`.
- [ ] Chapters come from the `.srt` of the uploaded file, start at `00:00`, and the last
      chapter starts before the video's end.
- [ ] The thumbnail is the project's `docs/thumbnail.png`, not an auto-picked frame.
- [ ] Audience is "No, it's not made for kids", paid promotion is "No", and altered content (AI use) is "No".
- [ ] The captions are attached, if used.

After saving:

- [ ] Captions show at the right moments at three points in the video (start, middle, end).
- [ ] 1080p processing has finished before the link is shared: code slides are unreadable at 360p.
- [ ] Watch the first and last minute: audio clean, credit line present, no "next pattern" teaser.
- [ ] If anything is wrong, fix it in Studio; switch to Private only if the fix needs a new upload.

## 6. The upload sheet

Before each upload, a sheet is prepared from `docs/youtube.md`: the title, the description with
schemes removed and chapters timed for the uploaded file, the tags, and the file paths above.
This is mechanical and can be scripted from `gradle-java/docs/make_youtube_docs.py`
(its `chapters()` reads the `.srt`; pointing it at the amy-slow `.srt` gives amy-slow chapters,
and the cue count of the scenes must equal the `.srt`'s cue count).

## 7. Worked example: Circuit Breaker (amy-slow)

Project: `gradle-java/micro-services-design-patterns/circuit-breaker-pattern`

- **Video:** `video/circuit-breaker-pattern-explained-amy-slow.mp4` (18:45, 1920×1080, H.264, AAC 48 kHz)
- **Captions (optional):** `video/circuit-breaker-pattern-explained-amy-slow.srt` (205 cues, matching the 205 narration cues)
- **Not uploaded:** `video/circuit-breaker-pattern-explained-amy-slow.m4a`; the `.mp4` already carries the audio
- **Thumbnail:** `docs/thumbnail.png`
- **Title:** `Circuit Breaker in Java - When a Service Stops`
- **Tags:** as in `docs/youtube.md`

**Description changes** from `docs/youtube.md`:

- The repository line becomes
  `github.com/jk-boot-up/java-design-patterns/tree/main/gradle-java/micro-services-design-patterns/circuit-breaker-pattern`.
- The chapters are replaced by the amy-slow timings (the ones currently in `docs/youtube.md`,
  and its 14:25 runtime, are left over from the deleted Kokoro build):

```
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
```

Everything else in the description is used as written.

## 8. Uploading every project (batch rules)

- **Order:** `micro-services-design-patterns` first, then the other categories under
  `gradle-java/` one at a time, projects in alphabetical order within a category.
- **Never twice:** before a batch, `sync` records every video already on the channel. A
  project whose title (from its `docs/youtube.md`) is already on the channel, or which already
  has a link in the registry, is skipped.
- **One video at a time:** the page is never left while a file is still uploading, because
  leaving the page cancels the upload. The script waits for the upload to finish before
  publishing.
- **Thumbnail failure is not fatal:** if attaching `docs/thumbnail.png` fails, the video is
  published without it and the miss is logged, so the thumbnail can be added by hand later.
  Every other setting must succeed, or that project is left as a draft, logged, and the batch
  moves on.
- **A failure never causes a duplicate:** a project that fails after its file was attached is
  recorded in the registry as a draft (with its video ID and the failed step), so no later
  batch uploads it again. Drafts are finished with `resume <project>` then `publish`.
- **Daily limit:** YouTube caps uploads per day. When Studio reports the limit, the batch waits
  (6 hours at a time) and carries on by itself; already-uploaded projects are skipped.
- **Unattended, and cheap to follow:** the batch runs in the background across all categories.
  Progress is written, not watched: `~/.ytupload-chrome/status.txt` holds a one-line summary
  (uploaded, failed, to go, last project), and `~/.ytupload-chrome/batch.log` one line per
  project (its link, or the step that failed). They are read only occasionally, never polled.
- **The registry:** every link is recorded in `gradle-java/docs/youtube-links.json`
  (project path, title, category, video ID, date). It is the single source for:
  - `gradle-java/docs/youtube-links.md` and its themed `.html` twin, the tracking document
    listing every pattern with its YouTube link, by category; and
  - the **YouTube** link beside each project in the repository's `index.md` / `index.html`
    (generated by `gradle-java/docs/make_index.py`).
  Both are regenerated after each batch.

