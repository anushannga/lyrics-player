# Me Hitha Sanasa

Word-by-word Sinhala lyrics for Uvindu Ayshcharya’s Lyrics Video MP3. Audio plays on the Mac. On the Arduino UNO’s ST7920 LCD, selected held endings add `.` → `..` → `...` one at a time.

Reuse the [STREAMLCD 1 firmware](../yanne-kohedo/YanneKohedoLCD/). Double-click **Play Me Hitha Sanasa.command** on the Desktop or run `python3 player.py` from this folder. Use `--mp3 /path/to/file.mp3` if needed; the player checks the recording hash. Press Control+C to stop.

To rebuild with the repository requirements and local `faster-whisper` `base` and `small` models:

```sh
python3 tools/align_song.py /path/to/file.mp3
python3 tools/build_display.py
```

Word onsets and sustain lengths are estimated from the recording, not listening-certified.
