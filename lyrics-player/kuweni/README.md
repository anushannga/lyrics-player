# Kuweni

Word-by-word Sinhala lyrics timed to the Ridma Weerawardena, Dinupa Kodagoda and Charitha Attalage Official Video MP3. Audio plays on the Mac; the Arduino UNO’s ST7920 LCD shows the lyrics and progressive `.` → `..` → `...` on selected held endings.

Reuse the [STREAMLCD 1 firmware](../yanne-kohedo/YanneKohedoLCD/). Double-click **Play Kuweni.command** on the Desktop or run `python3 player.py` in this folder. Use `--mp3 /path/to/file.mp3` if needed. The player checks the recording hash. Press Control+C to stop.

To regenerate with the repository requirements and local `faster-whisper` `base` and `small` models:

```sh
python3 tools/align_song.py /path/to/file.mp3
python3 tools/build_display.py
```

Word onsets and sustain lengths are estimates from the recording, not listening-certified.
