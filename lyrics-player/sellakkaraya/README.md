# Sellakkaraya

The supplied launcher repeats continuously; Ctrl+C stops playback. The font is ISI Gurulugomi.

## Upload firmware

Open `SellakkarayaLCD/SellakkarayaLCD.ino` in Arduino IDE and upload for Arduino UNO,
or run from this song folder:

```sh
arduino-cli compile --fqbn arduino:avr:uno SellakkarayaLCD
arduino-cli board list
arduino-cli upload --fqbn arduino:avr:uno --port /dev/cu.YOUR_ARDUINO SellakkarayaLCD
```

Install the U8g2 library and Arduino AVR Boards first. The existing LCD wiring
is D10=CS, D11=SID/MOSI, D13=SCLK, D8=RESET, PSB=GND. Firmware serial baud: 115200.

## Play

Activate the repository virtual environment, then run from this song folder:

```sh
python3 player.py --mp3 "$HOME/Downloads/Sellakkaraya - Kaizer Kaiz Ft. Lil Neo.mp3"
python3 player.py --loop
```

Without an audio argument, the default is `~/Downloads/Sellakkaraya - Kaizer Kaiz Ft. Lil Neo.mp3`.
Use `--port /dev/cu.YOUR_ARDUINO` if more than one board is connected.
Press Ctrl+C to stop. Music comes from the Mac output.

Expected MP3 SHA-256:

```text
08763eae1b0ede529247ae49b78bc77272ea1f0da6d0d3555554164b81ef5f72
```

Playback rejects a different MP3 because the saved timing may no longer fit it.

## Edit and rebuild

Edit `lyrics_isi.txt` with the matching legacy font encoding. The Unicode file
is a readable reference; rendering uses the legacy font source. Rebuild bitmaps:

```sh
python3 tools/render.py
```

This updates `frames.bin` and `manifest.json`. Run `python3 tools/build_timings.py` afterward to update the saved lyric identity and timing.

Use `--dry` to check saved cue data without audio or USB. Timing changes should be checked against actual vocals; a successful USB acknowledgement does not establish musical synchronization.
