# Sandawathiye

The final supplied Sinhala lyrics include “රැඳෙන්නෑ මා නෙත් මානයේ...” and “සඳවතියේ මා ඇයි තනි කෙරුවේ...”. Only explicitly supplied ellipses are shown, as fixed dots. The solo after the latter phrase shows animated music-note/dot groups. Other instrumental gaps stay blank. Word reveals start at stored onset times rather than before them. The first “ඇයි” onset is corrected to 56.04 seconds. The font is THARU DIGITAL NIKINI; font size is 20 pixels.

## Upload firmware

Open `SandawathiyeLCD/SandawathiyeLCD.ino` in Arduino IDE and upload for Arduino UNO,
or run from this song folder:

```sh
arduino-cli compile --fqbn arduino:avr:uno SandawathiyeLCD
arduino-cli board list
arduino-cli upload --fqbn arduino:avr:uno --port /dev/cu.YOUR_ARDUINO SandawathiyeLCD
```

Install the U8g2 library and Arduino AVR Boards first. The existing LCD wiring
is D10=CS, D11=SID/MOSI, D13=SCLK, D8=RESET, PSB=GND. Firmware serial baud: 115200.

## Play

Activate the repository virtual environment, then run from this song folder:

```sh
python3 player.py --mp3 "$HOME/Downloads/Sandawathiye Ridma Weerawardena Charitha Attalage.mp3"
```

Without an audio argument, the default is `~/Downloads/Sandawathiye Ridma Weerawardena Charitha Attalage.mp3`.
Use `--port /dev/cu.YOUR_ARDUINO` if more than one board is connected.
Press Ctrl+C to stop. Music comes from the Mac output.

Expected MP3 SHA-256:

```text
95ed343995ec257db29f8f187114191962ceff8b486d55ecec65cabb992440cb
```

Playback rejects a different MP3 because the saved timing may no longer fit it.

## Edit and rebuild

Edit `lyrics_isi.txt` with the matching legacy font encoding. The Unicode file
is a readable reference; rendering uses the legacy font source. Rebuild bitmaps:

```sh
python3 tools/build_karaoke.py
```

This updates `frames.bin` and `manifest.json`. It also rebuilds `timings.json` using the final per-word alignment snapshot.

Use `--dry` to check saved cue data without audio or USB. Timing changes should be checked against actual vocals; a successful USB acknowledgement does not establish musical synchronization.
