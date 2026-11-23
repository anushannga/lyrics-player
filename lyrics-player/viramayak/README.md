# Viramayak

Word-by-word Sinhala lyrics for BHASHI’s Official Audio 2020 recording. Audio plays on the Mac; the Arduino UNO’s ST7920 LCD reveals lyrics and adds `.` → `..` → `...` at selected held endings.

Reuse the [STREAMLCD 1 firmware](../yanne-kohedo/YanneKohedoLCD/). Run `python3 player.py` from this folder or double-click **Play Viramayak.command** if using the installed Desktop shortcut. Supply `--mp3 /path/to/file.mp3` if the matching recording is not in Downloads. Press Control+C to stop.

To rebuild, install the repository dependencies and cache the `faster-whisper` `base` and `small` models locally:

```sh
python3 tools/align_song.py /path/to/file.mp3
python3 tools/build_display.py
```

Vocal timings are estimates from the recording. The player sends lyric frames 65 ms early to compensate for LCD transfer time.
