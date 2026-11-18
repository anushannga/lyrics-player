# Sansarini

Arduino UNO + ST7920 word-by-word Sinhala lyrics for Yasas Medagedara’s Lyric Video recording. Selected held words reveal `.` → `..` → `...` on the LCD. Audio plays on the Mac.

Use the same `STREAMLCD 1` firmware as [Yanne Kohedo](../yanne-kohedo/YanneKohedoLCD/). Run `python3 player.py` from this folder or double-click **Play Sansarini.command** on the Desktop. Use `--mp3 /path/to/recording.mp3` if the original recording is not in Downloads; the player checks the MP3 hash. Press Control+C to stop.

To rebuild, install the repository requirements and `faster-whisper` with its `base` and `small` models cached, then run:

```sh
python3 tools/align_song.py /path/to/recording.mp3
python3 tools/build_display.py
```

Word timings are audio-alignment estimates, not listening-certified timestamps.
