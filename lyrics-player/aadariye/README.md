# Aadariye — Miran Archana X Cozzy

Arduino UNO + ST7920 128×64 lyric player for the supplied MP3. Music plays
through the Mac. All 57 supplied Sinhala lyric lines are retained, using the
previous ISI Gurulugomi font at 24px. Whole words appear at their saved vocal
onsets. Text never scrolls or uses a blinking/dither fade.

## Current hold behavior

Each short hook word (“ආදරියේ”, “මගේ”, “රැයේ”) has its own centered screen.
The current word stays visible until the next saved word onset, when the screen
changes to that word. No two hook lines are displayed together. Word onsets and
progressive dot timing are retained from the latest calibration. There are no
extra blank-screen commands inside hooks.

Sustained words gain `.`, `..`, then `...` at one quarter, one half and three
quarters of the aligned vocal duration. Added dots stay while the word stays.
Dots use one typographic baseline per row and a one-pixel word gap, so vowel
marks/descenders cannot push dots lower on particular words.

Hook timing comes from locally isolated vocals. Six “මගේ” entries have targeted
ASR/listening-feedback onset corrections; the other word timings are retained. The third hook's clip excludes the preceding
phrase tail. Normal lyric playback uses the original full MP3, not isolated audio.
This is model-derived timing, not listening-confirmed exact vocal synchronization.

## Run

Double-click `Play Aadariye.command`, or run from this folder:

```sh
python3 player.py
python3 player.py --loop
python3 player.py --verify
python3 player.py --dry
python3 player.py --start 42 --stop 59
```

First verse entry: about 4.22 seconds. Song duration: 236.930612 seconds.
Ctrl+C stops playback. Positive `--offset` delays text; negative advances it.
The MP3 SHA-256 is checked against the timing file. Default audio is the supplied
`Miran Archana X Cozzy - Aadariye ...mp3` in Downloads.

The existing STREAMLCD 1 firmware is compatible. The included source is
`AadariyeLCD.ino`. LCD wiring remains CS=10, SID/MOSI=11, SCLK=13, RESET=8,
PSB=GND; USB serial is 115200 baud. Audio comes from the Mac, not the UNO.

## Files and rebuilding

- `lyrics_unicode.txt`, `lyrics.json`: the supplied lyric lines and rendering text.
- `assets/isigurul_0.ttf`, `assets/isi-rules.json`: font and local SinKey mapping.
- `alignment.json`: current ordered per-word timing.
- `vocal_onset_corrections.json`: isolated-vocal hook timings applied by finalization.
- `frames.bin`, `manifest.json`, `timings.json`: ready-to-play generated data.
- `sustain_marks.json`: selected dot-bearing words and their aligned durations.
- `previews/paired-hook-holds.png`: the current two-row word holds.
- `effect_validation.json`, `verification.json`: software/hardware checks.

For display-only rebuilding while retaining timing:

```sh
python3 tools/build_display.py
```

`tools/finalize_alignment.py` applies the saved timing corrections when
re-finalizing from the original alignment. Pillow, regex and pyserial are
needed; the audio-clock helper is compiled with macOS clang/AVFoundation if needed.

Optional analysis scripts use faster-whisper, NumPy, SciPy, PyAV and ONNX Runtime.
`tools/isolate_hooks.py` uses the official Kim Vocal 2 ONNX model from
https://github.com/TRvlvr/model_repo/releases/tag/all_public_uvr_models,
held locally in `~/.cache/audio-models/`. Its SHA-256 is checked in the script.
No MP3 or derived vocal audio is uploaded to any service. Analysis stems stay
under `analysis/`; normal playback does not require any model or stem file.
Sinhala-script alignment produced collapsed timestamps and was excluded;
phonetic alignment of the known supplied text is used instead.

CRC/ACK checks establish transfer integrity and pixel layout, not exact musical
synchronization. No GitHub upload is performed automatically for this project.

All six hook “මගේ” entries explicitly retain progressive dots even after onset
calibration shortens their measured duration. Their corrected word onset times
remain unchanged.

“මගේ...” now remains on screen through the following pause until the next lyric
starts. Blank-screen cues after that word are suppressed; subsequent word onset
times and three-dot animation timing remain unchanged.

All three “රැයේ...” scenes explicitly retain three progressive dots and hold
until their own next vocal onset (2.98s, 2.84s and 3.62s respectively), without
a fixed copied duration or any change to the next word timing.

Upload `AadariyeLCD/AadariyeLCD.ino` with Arduino IDE or arduino-cli. Install the repository root requirements. Supply your own matching MP3 in Downloads, or use `python3 player.py --mp3 /path/to/song.mp3`. Prebuilt frames and timing are included; analysis models and audio stems are not. Rebuilding analysis needs requirements-analysis.txt, the cached faster-whisper small model, and (for vocal isolation) Kim_Vocal_2.onnx in ~/.cache/audio-models/.
