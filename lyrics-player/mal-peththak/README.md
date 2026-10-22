# Mal Peththak Se Susinidu Sitha — 6th Lane / Nirwanaya

The final played version: Sinhala and English lyrics appear progressively,
letter by letter, on an Arduino UNO + ST7920 128×64 LCD. Earlier letters stay
still and solid. Sinhala vowel signs and conjuncts are revealed together;
fast rap can group letters to fit the LCD transfer rate. No blinking cursor,
whole-word dither fade, section headings or sound-effect comments are displayed.
Instrumental gaps are blank. The spoken telephone dialogue itself is included.

## Upload

This uses the same `STREAMLCD 1` firmware as Sellakkaraya and Sandawathiye.
If that firmware is already on your UNO, you can run this player directly.
Otherwise open `MalPeththakLCD/MalPeththakLCD.ino` in Arduino IDE, or run:

```sh
arduino-cli compile --fqbn arduino:avr:uno MalPeththakLCD
arduino-cli upload --fqbn arduino:avr:uno --port /dev/cu.YOUR_ARDUINO MalPeththakLCD
```

Dependencies: Arduino AVR Boards and U8g2. LCD wiring: D10=CS, D11=SID/MOSI,
D13=SCLK, D8=RESET, PSB=GND. USB serial runs at 115200 baud.

## Play

Install the repository `requirements.txt` in a Python 3 environment on macOS.
From this song folder:

```sh
python3 player.py
python3 player.py --mp3 "/path/to/your/song.mp3"
python3 player.py --loop
python3 player.py --start 83 --stop 94
python3 player.py --verify
python3 player.py --dry
```

`Play Mal Peththak.command` plays once; Ctrl+C stops it. Music plays through the
Mac output. The first lyric starts at about 21.55 seconds. The default MP3 is
`~/Downloads/Mal Peththak Se Susinidu Sitha (මල් පෙත්තක් සේ සුසිනිදු සිත) 6th Lane Nirwanaya Sinhala Songs.mp3`.
The recording is not included. Saved timing is bound to its SHA-256:

```text
407d7e5c6d4c194e9293b97278405cd85b1c4c769979d30123f397b3597ca6c6
```

The player compiles `tools/audio_clock.m` locally with clang and AVFoundation.
No prebuilt Mac executable is bundled.

## Edit/rebuild

`lyrics_unicode.txt` contains the 134 cleaned lyric lines; `lyrics.json` is the
rendering source. `alignment.json` preserves the final per-word timing, including
the user's chorus-warp corrections. Regenerate the display after editing:

```sh
python3 tools/build_display.py
```

The supplied ISI Gurulugomi font and local SinKey Unicode→ISI rules render Sinhala
at 24px. English uses 18px Arial from the local Mac installation. Arial.ttf is not
redistributed; to rebuild elsewhere, provide your own licensed Arial.ttf in
`assets/`. Normal playback uses the supplied bitmaps and does not need Arial.
`regex` groups Sinhala graphemes to avoid splitting vowel marks from letters.

Existing `frames.bin`, `manifest.json` and `timings.json` are ready to play.
`previews/letter-reveal.gif` demonstrates the effect. Other previews show exact
LCD pixels. About 50–85ms are needed for each physical frame; dense letter
updates can be coalesced while the audio clock continues normally.

Optional analysis scripts and saved intermediate alignments are included for
new calibration. Install `requirements-analysis.txt` for those tools. They need
local faster-whisper models and the same MP3. `warp_chorus.py` accepts the original
feature cache explicitly with `--features /path/to/features.npy` (hop=2048 at
16kHz); that analysis cache is not bundled. `prepare_lyrics.py`,
`finalize_alignment.py` and re-alignment scripts can replace edited data: use
those only when deliberately rebuilding the analysis, not for normal playback.

Timing is derived from local forced alignment, spectral chorus matching and
selected independent spoken-word onsets. It is not fully listening-confirmed.
USB CRC/ACK checks validate transfer, not musical alignment.
