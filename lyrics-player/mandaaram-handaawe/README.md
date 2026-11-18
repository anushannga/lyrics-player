# Mandaaram Handaawe

Word-by-word Sinhala lyrics for Arduino UNO + ST7920. Audio plays on the Mac. The song uses the same `STREAMLCD 1` firmware as [Yanne Kohedo](../yanne-kohedo/YanneKohedoLCD/); no re-upload is needed if that song already works.

```sh
python3 player.py
```

Use `--mp3 /path/to/file.mp3` if the exact Channuka Official Visualiser recording is not in Downloads. The player checks the MP3 hash before playback. `--start` and `--stop` preview selected seconds; Control+C stops playback.

Selected held phrase endings reveal `.` → `..` → `...` one dot at a time during the aligned vocal interval. The three dots stay until that lyric page changes.

To regenerate assets, install `faster-whisper` with the `base` and `small` models cached locally, plus the repository dependencies:

```sh
python3 tools/align_song.py /path/to/file.mp3
python3 tools/build_display.py
```

The word onsets are model estimates for this recording. A successful Arduino frame acknowledgment verifies delivery, not audible synchronization or LCD contrast.
