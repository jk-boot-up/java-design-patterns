#!/usr/bin/env bash
#
# Builds the Static Factory Method teaching video.
#
#   1. renders one 1920x1080 slide per scene          (make_slides.py)
#   2. narrates each scene with a female voice        (macOS `say`)
#   3. joins each slide to its narration              (ffmpeg)
#   4. concatenates every scene into the final video  (ffmpeg)
#
# Outputs:
#   static-factory-pattern-explained.mp4   1080p H.264 + AAC, ready for YouTube
#   static-factory-pattern-explained.m4a   audio-only version (podcast / revision)
#   poster.png                             title card, for use as the YouTube thumbnail
#
# Requirements: macOS (for `say`), ffmpeg, python3 with pillow + matplotlib.
#
set -euo pipefail

cd "$(dirname "$0")"

BUILD=build
VOICE="${VOICE:-Samantha}"     # female US English voice
RATE="${RATE:-165}"            # words per minute — unhurried, easier to follow

# Every voice macOS ships by default is the compact 22 kHz tier. Resampling
# that straight up to the 48 kHz the AAC track needs leaves an audible hiss,
# so the narration is cleaned before it is encoded:
#
#   aresample   a long filter, so the upsampling itself adds no grit
#   highpass    drops rumble below the voice
#   afftdn      spectral denoise — this is what removes the hiss
#   equalizer   a small lift around 3 kHz, where consonants live
#   lowpass     hides the empty band above what a 22 kHz source can carry
#   loudnorm    one consistent level, at YouTube's -16 LUFS target
#
# Measured against the unfiltered encode, the noise floor drops about 15 dB.
CLEANUP="aresample=48000:filter_size=256:cutoff=0.98,highpass=f=85,\
afftdn=nr=14:nf=-45,equalizer=f=3000:t=q:w=1.2:g=2.5,lowpass=f=10500,\
loudnorm=I=-16:TP=-1.5:LRA=11"
OUT_VIDEO=static-factory-pattern-explained.mp4
OUT_AUDIO=static-factory-pattern-explained.m4a
OUT_SUBS=static-factory-pattern-explained.srt
OUT_POSTER=poster.png            # first frame, doubles as the YouTube thumbnail

command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
command -v say    >/dev/null || { echo "macOS 'say' is required"; exit 1; }

mkdir -p "$BUILD"
rm -f "$BUILD"/*.aiff "$BUILD"/*.m4a "$BUILD"/scene-*.mp4 "$BUILD"/concat.txt "$BUILD"/joined.mp4

echo "==> 1/4  rendering slides"
python3 make_slides.py "$BUILD"

echo "==> 2/4  writing narration text"
python3 - "$BUILD" <<'PY'
import sys, os
from scenes import SCENES
out = sys.argv[1]
for s in SCENES:
    with open(os.path.join(out, s["key"] + ".txt"), "w") as fh:
        fh.write(s["narration"])
    print("text   ->", s["key"] + ".txt")
PY

echo "==> 3/4  narrating with voice '$VOICE' and building scene clips"
for txt in "$BUILD"/*.txt; do
    key=$(basename "$txt" .txt)
    png="$BUILD/$key.png"
    aiff="$BUILD/$key.aiff"

    say -v "$VOICE" -r "$RATE" -o "$aiff" -f "$txt"

    # A beat of silence at the end of each scene so slides do not snap past.
    #
    # -bf 0 disables B-frames. They save nothing on a static slide, and they
    # push the video track's first timestamp past the audio's, which leaves
    # players showing black for the opening moment instead of the poster.
    ffmpeg -y -loglevel error \
        -loop 1 -i "$png" \
        -i "$aiff" \
        -filter_complex "[1:a]$CLEANUP,apad=pad_dur=0.9[a]" \
        -map 0:v -map "[a]" \
        -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 -bf 0 \
        -c:a aac -b:a 192k -ar 48000 -ac 2 \
        -shortest "$BUILD/scene-$key.mp4"

    echo "scene  -> scene-$key.mp4"
done

echo "==> 4/5  concatenating"
for f in "$BUILD"/scene-*.mp4; do
    echo "file '$(basename "$f")'" >> "$BUILD/concat.txt"
done

ffmpeg -y -loglevel error -f concat -safe 0 -i "$BUILD/concat.txt" \
    -c copy "$BUILD/joined.mp4"

# Two fixes for the opening frame, both lossless:
#
#   -ignore_editlist  drops the edit list the AAC encoder's priming delay
#                     creates, which otherwise starts the video track 21 ms
#                     after the audio and shows black at 0:00.
#   +faststart        moves the moov atom to the front of the file. Without
#                     it the index sits after 20-odd megabytes of video, so a
#                     player has nothing to draw until it has read the lot.
ffmpeg -y -loglevel error -ignore_editlist 1 -i "$BUILD/joined.mp4" \
    -c copy -movflags +faststart "$OUT_VIDEO"

ffmpeg -y -loglevel error -i "$OUT_VIDEO" -vn -c:a aac -b:a 192k -ac 2 \
    -movflags +faststart "$OUT_AUDIO"

# The opening poster doubles as the YouTube thumbnail, so lift it out of the
# build directory where it is easy to find at upload time.
cp "$BUILD/01-poster.png" "$OUT_POSTER"

# Subtitles are timed from the narration audio, so this must run before the
# intermediates are cleaned up.
echo "==> 5/5  generating subtitles"
python3 make_subtitles.py "$BUILD" "$OUT_SUBS"

# Keep only the slides; drop the narration/clip intermediates.
if [ -z "${KEEP_INTERMEDIATE:-}" ]; then
    rm -f "$BUILD"/*.aiff "$BUILD"/*.txt "$BUILD"/scene-*.mp4 "$BUILD"/concat.txt "$BUILD"/joined.mp4
fi

echo
echo "Done."
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT_VIDEO"
echo "  video:     $OUT_VIDEO"
echo "  audio:     $OUT_AUDIO"
echo "  subtitles: $OUT_SUBS"
echo "  poster:    $OUT_POSTER"
