# Nil Denethi

Word-by-word Sinhala and English lyrics for the Iraj Official Music Video MP3. Audio plays on the Mac; the ST7920 LCD displays lyrics and reveals three dots on selected held endings.

Reuse the [STREAMLCD 1 sketch](../yanne-kohedo/YanneKohedoLCD/). Run `python3 player.py` or double-click the installed **Play Nil Denethi.command** Desktop shortcut. Use `--mp3 /path/to/file.mp3` for the matching recording outside Downloads. Press Control+C to stop.

English backing vocals are rendered without parentheses in macOS Georgia Bold, sized and baseline-aligned to the ISI Gurulugomi Sinhala text. Rebuilding the frames requires the macOS Georgia Bold font; playing the saved frames does not.

To rebuild, install the repository requirements and cache faster-whisper's `base` and `small` models:

```sh
python3 tools/align_song.py /path/to/file.mp3
python3 tools/build_display.py
```

Word timing and sustained vocal lengths are estimates from the recording.
