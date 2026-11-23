# Radhawani

Word-by-word Sinhala lyrics for the Supun Perera and Charitha Attalage Official Video MP3. Audio plays on the Mac; the Arduino UNO’s ST7920 LCD shows the lyrics and adds `.` → `..` → `...` one at a time at selected held endings.

Reuse the [STREAMLCD 1 firmware](../yanne-kohedo/YanneKohedoLCD/). Double-click **Play Radhawani.command** on the Desktop or run `python3 player.py` from this folder. Use `--mp3 /path/to/file.mp3` if needed; playback checks the recording hash. Press Control+C to stop.

To rebuild, install the repository dependencies and cache the `faster-whisper` `base` and `small` models locally:

```sh
python3 tools/align_song.py /path/to/file.mp3
python3 tools/build_display.py
```

Word onsets and sustain lengths are audio alignment estimates, not listening-certified.

The player sends lyric frames 65 ms early to compensate for USB/LCD transfer time. Use `--offset` in seconds to override this calibration.
