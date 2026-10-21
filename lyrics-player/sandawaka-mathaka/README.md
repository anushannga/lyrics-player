# Sandawaka Mathaka

The player includes all 30 lyric cues and a manual `--tap` calibration mode. The font is ISI Disapamok.

## Upload firmware

Open `LyricsKaraokeClear/LyricsKaraokeClear.ino` in Arduino IDE and upload for Arduino UNO,
or run from this song folder:

```sh
arduino-cli compile --fqbn arduino:avr:uno LyricsKaraokeClear
arduino-cli board list
arduino-cli upload --fqbn arduino:avr:uno --port /dev/cu.YOUR_ARDUINO LyricsKaraokeClear
```

Install the U8g2 library and Arduino AVR Boards first. The existing LCD wiring
is D10=CS, D11=SID/MOSI, D13=SCLK, D8=RESET, PSB=GND. Firmware serial baud: 9600.

## Play

Activate the repository virtual environment, then run from this song folder:

```sh
python3 play.py "$HOME/Downloads/Sandawaka Mathaka.mp3"
```

Without an audio argument, the default is `~/Downloads/Sandawaka Mathaka.mp3`.
Use `--port /dev/cu.YOUR_ARDUINO` if more than one board is connected.
Press Ctrl+C to stop. Music comes from the Mac output.

Expected MP3 SHA-256:

```text
b65d631b65fcacef1ef6401b18a06cf70ab5b6a7bcd2c3383506e4648bf2c195
```

Playback rejects a different MP3 because the saved timing may no longer fit it.

## Edit and rebuild

Edit `lyrics_isi.txt` with the matching legacy font encoding. The Unicode file
is a readable reference; rendering uses the legacy font source. Rebuild bitmaps:

```sh
python3 tools/render_lyrics.py
```

This updates the bitmap header in `LyricsKaraokeClear/`; rebuild and reupload the Arduino sketch afterward. Timing/lyric identity must agree before playback. `tools/build_timings.py` rebuilds timing from the saved alignment data.

Use `--dry` to check saved cue data without audio or USB. Timing changes should be checked against actual vocals; a successful USB acknowledgement does not establish musical synchronization.
