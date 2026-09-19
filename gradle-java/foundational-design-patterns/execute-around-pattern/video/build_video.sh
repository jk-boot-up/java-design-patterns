#!/usr/bin/env bash
#
# Builds the Execute Around pattern teaching video.
#
#   1. renders one 1920x1080 slide per scene          (make_slides.py)
#   2. narrates each scene with a female voice        (macOS `say`)
#   3. joins each slide to its narration              (ffmpeg)
#   4. concatenates every scene into the final video  (ffmpeg)
#
# Outputs:
#   execute-around-pattern-explained.mp4   1080p H.264 + AAC, ready for YouTube
#   execute-around-pattern-explained.m4a   audio-only version (podcast / revision)
#   poster.png                               title card, for use as the YouTube thumbnail
#
# Requirements: macOS (for `say`), ffmpeg, python3 with pillow + matplotlib.
#
set -euo pipefail

cd "$(dirname "$0")"

BUILD=build
VOICE="${VOICE:-Samantha}"     # female US English voice
RATE="${RATE:-145}"            # words per minute -- the pace educational YouTube settles on
FPS=30

# Every voice macOS ships by default is the compact 22 kHz tier, so the
# narration gets a light touch-up on its way to the 48 kHz the AAC track
# needs:
#
#   aresample   a long filter, so the upsampling itself adds no grit
#   highpass    drops rumble below the voice
#   equalizer   a small lift around 3 kHz, where consonants live
#
# There is deliberately no denoiser in that list. An earlier version ran
# afftdn over the narration to kill the hiss the upsample leaves behind, and
# by the numbers it worked — about 15 dB off the noise floor. It also made
# the voice noticeably worse. A spectral denoiser assumes a real, roughly
# stationary noise floor to subtract; synthesised speech has almost none, so
# afftdn ends up subtracting parts of the speech instead and leaves it
# warbling. The faint hiss is much the lesser problem, so it stays.
CLEANUP="aresample=48000:filter_size=512:cutoff=0.98:linear_interp=1,\
highpass=f=75,equalizer=f=3000:t=q:w=1.5:g=1.5"

# Levelling is deliberately NOT part of CLEANUP. Run per scene it re-measures
# on every clip, so a quiet scene gets pushed up to match a loud one and the
# level audibly steps at each join. Applied once over the whole narration it
# gives one consistent level, at YouTube's -16 LUFS target.
#
# It is also applied in two passes -- see step 5, where the measured numbers
# are fed back in. One pass is not enough.
LOUDNORM="loudnorm=I=-16:TP=-1.5:LRA=11"

OUT_VIDEO=execute-around-pattern-explained.mp4
OUT_AUDIO=execute-around-pattern-explained.m4a
OUT_SUBS=execute-around-pattern-explained.srt
OUT_POSTER=poster.png            # first frame, doubles as the YouTube thumbnail

command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
command -v say    >/dev/null || { echo "macOS 'say' is required"; exit 1; }

mkdir -p "$BUILD"
rm -f "$BUILD"/*.aiff "$BUILD"/*.wav "$BUILD"/*.m4a "$BUILD"/scene-*.mp4 \
      "$BUILD"/concat.txt "$BUILD"/concat-audio.txt \
      "$BUILD"/joined.mp4 "$BUILD"/narration.wav "$BUILD"/muxed.mp4

echo "==> 1/5  rendering slides"
python3 make_slides.py "$BUILD"

echo "==> 2/5  writing narration text"
python3 - "$BUILD" <<'PY'
import sys, os
from scenes import SCENES
out = sys.argv[1]
for s in SCENES:
    with open(os.path.join(out, s["key"] + ".txt"), "w") as fh:
        fh.write(s["narration"])
    print("text   ->", s["key"] + ".txt")
PY

echo "==> 3/5  narrating with voice '$VOICE' and building scene clips"
#
# Audio and video are kept apart until the very last step, and that split is
# the whole point of this stage.
#
# AAC is a lapped format: every separately encoded clip carries priming
# samples at its head and padding at its tail. Concatenating such clips with
# `-c copy` cannot strip either, so each join leaves a hole in the timeline —
# the voice cuts out for a moment at every scene change, and the gaps add up
# to tens of seconds of missing audio over a full video.
#
# So each scene's narration is written as lossless WAV here, and the entire
# narration is encoded to AAC exactly once, at step 5. One encode, one set of
# priming samples, no internal joins.
for txt in "$BUILD"/*.txt; do
    key=$(basename "$txt" .txt)
    png="$BUILD/$key.png"
    aiff="$BUILD/$key.aiff"
    raw="$BUILD/$key.raw.wav"
    wav="$BUILD/$key.wav"

    say -v "$VOICE" -r "$RATE" -o "$aiff" -f "$txt"

    # Clean the speech and add a beat of silence so slides do not snap past.
    ffmpeg -y -loglevel error -i "$aiff" \
        -af "$CLEANUP,apad=pad_dur=0.9" \
        -c:a pcm_s16le -ar 48000 -ac 2 "$raw"

    # Round the scene up to a whole number of video frames, then pad the audio
    # to exactly that length. Audio and video then agree per scene, so slide
    # changes cannot drift away from the narration however many scenes there are.
    frames=$(python3 -c "
import subprocess, math
d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries',
    'format=duration','-of','default=nw=1:nk=1','$raw']).strip())
print(int(math.ceil(d * $FPS)))")
    target=$(python3 -c "print($frames / $FPS)")

    ffmpeg -y -loglevel error -i "$raw" \
        -af "apad" -t "$target" \
        -c:a pcm_s16le -ar 48000 -ac 2 "$wav"

    # Video only. -bf 0 disables B-frames: they save nothing on a static slide
    # and they push the video track's first timestamp past the audio's, which
    # leaves players showing black for the opening moment instead of the poster.
    ffmpeg -y -loglevel error \
        -loop 1 -i "$png" \
        -frames:v "$frames" \
        -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r "$FPS" -bf 0 \
        -an "$BUILD/scene-$key.mp4"

    rm -f "$raw"
    echo "scene  -> scene-$key.mp4  ($frames frames, ${target}s)"
done

echo "==> 4/5  concatenating"
for f in "$BUILD"/scene-*.mp4; do
    echo "file '$(basename "$f")'" >> "$BUILD/concat.txt"
done
for f in "$BUILD"/*.wav; do
    echo "file '$(basename "$f")'" >> "$BUILD/concat-audio.txt"
done

ffmpeg -y -loglevel error -f concat -safe 0 -i "$BUILD/concat.txt" \
    -c copy "$BUILD/joined.mp4"

# Lossless join: PCM in, PCM out, so this cannot introduce a seam.
ffmpeg -y -loglevel error -f concat -safe 0 -i "$BUILD/concat-audio.txt" \
    -c:a pcm_s16le -ar 48000 -ac 2 "$BUILD/narration.wav"

echo "==> 5/5  muxing"
# Loudness normalisation, measured first and then applied as one flat gain.
#
# Left to itself loudnorm runs in dynamic mode: it rides the level as it goes,
# and on some narrations that makes it emit a timestamp discontinuity partway
# through — a hole in the finished audio, in the middle of a sentence, with
# nothing wrong anywhere upstream of it. Measuring the whole narration first
# and handing the numbers back with linear=true reduces it to a single
# constant gain, which cannot do that, and which also stops it pumping
# between quiet and loud lines.
echo "    measuring loudness"
MEASURED=$(ffmpeg -hide_banner -nostats -i "$BUILD/narration.wav" \
    -af "$LOUDNORM:print_format=json" -f null - 2>&1 | python3 -c "
import json, sys
txt = sys.stdin.read()
blob = txt[txt.rindex('{'):]
m = json.loads(blob[:blob.index('}') + 1])
print(':'.join([
    'measured_I='      + m['input_i'],
    'measured_TP='     + m['input_tp'],
    'measured_LRA='    + m['input_lra'],
    'measured_thresh=' + m['input_thresh'],
    'offset='          + m['target_offset'],
    'linear=true']))")

# The single AAC encode of the whole narration, levelled once across the lot.
ffmpeg -y -loglevel error -i "$BUILD/joined.mp4" -i "$BUILD/narration.wav" \
    -map 0:v -map 1:a -c:v copy \
    -af "$LOUDNORM:$MEASURED" -c:a aac -b:a 192k -ar 48000 -ac 2 \
    "$BUILD/muxed.mp4"

# Two fixes for the opening frame, both lossless:
#
#   -ignore_editlist  drops the edit list the AAC encoder's priming delay
#                     creates, which otherwise starts the video track 21 ms
#                     after the audio and shows black at 0:00.
#   +faststart        moves the moov atom to the front of the file. Without
#                     it the index sits after 20-odd megabytes of video, so a
#                     player has nothing to draw until it has read the lot.
ffmpeg -y -loglevel error -ignore_editlist 1 -i "$BUILD/muxed.mp4" \
    -c copy -movflags +faststart "$OUT_VIDEO"

ffmpeg -y -loglevel error -i "$OUT_VIDEO" -vn -c:a copy \
    -movflags +faststart "$OUT_AUDIO"

# The opening poster doubles as the YouTube thumbnail, so lift it out of the
# build directory where it is easy to find at upload time.
cp "$BUILD/01-poster.png" "$OUT_POSTER"

# Subtitles are timed from the scene clips, so this must run before the
# intermediates are cleaned up.
echo "==> generating subtitles"
python3 make_subtitles.py "$BUILD" "$OUT_SUBS"

# Verify the audio timeline is continuous. A gap here means either a scene join
# or the loudness pass has gone wrong again — the two ways this has broken so
# far. Either is easy to miss in a spot check and ruins the whole video, so it
# is worth failing the build over.
python3 - "$OUT_VIDEO" <<'PY'
import subprocess, sys
out = subprocess.check_output([
    "ffprobe", "-v", "error", "-select_streams", "a",
    "-show_entries", "packet=pts_time", "-of", "csv=p=0", sys.argv[1]]).decode()
pts = [float(x.rstrip(",")) for x in out.split() if x.strip()]
nominal = 1024 / 48000
gaps = [(pts[i - 1], pts[i] - pts[i - 1])
        for i in range(1, len(pts)) if pts[i] - pts[i - 1] > nominal * 1.5]
if gaps:
    print("  FAIL: %d gap(s) in the audio timeline:" % len(gaps))
    for t, d in gaps[:10]:
        print("    at %.3fs  gap=%.3fs" % (t, d))
    sys.exit(1)
print("  audio timeline continuous: %d packets, no gaps" % len(pts))
PY

# Keep only the slides; drop the narration/clip intermediates.
if [ -z "${KEEP_INTERMEDIATE:-}" ]; then
    rm -f "$BUILD"/*.aiff "$BUILD"/*.wav "$BUILD"/*.txt "$BUILD"/scene-*.mp4 \
          "$BUILD"/concat.txt "$BUILD"/concat-audio.txt \
          "$BUILD"/joined.mp4 "$BUILD"/narration.wav "$BUILD"/muxed.mp4
fi

echo
echo "Done."
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT_VIDEO"
echo "  video:     $OUT_VIDEO"
echo "  audio:     $OUT_AUDIO"
echo "  subtitles: $OUT_SUBS"
echo "  poster:    $OUT_POSTER"
