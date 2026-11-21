# Api Aye Hamuwela

Word-by-word Sinhala lyrics for the Uvindu Ayshcharya ft. DILUBeats official music video MP3. Audio plays on the Mac; held phrase endings reveal three dots one at a time on the Arduino UNO’s ST7920 LCD.

Use the [STREAMLCD 1 firmware](../yanne-kohedo/YanneKohedoLCD/). Double-click **Play Api Aye Hamuwela.command** on the Desktop or run `python3 player.py` from this folder. The player checks the recording hash; use `--mp3 /path/to/file.mp3` if the MP3 is not in Downloads. Press Control+C to stop.

To rebuild, install the repository requirements and `faster-whisper` with the `base` and `small` models cached locally:

```sh
python3 tools/align_song.py /path/to/file.mp3
python3 tools/build_display.py
```

Onsets and sustain lengths are model estimates, not listening-certified timestamps.
