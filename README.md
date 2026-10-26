# Lyrics Player

Arduino UNO + ST7920 128×64 Sinhala LCD lyric players by Pasan Anushanga.
Music plays through a Mac while an Arduino UNO displays Sinhala lyrics over USB.
This repository contains the latest played versions of all six projects.

## Songs

| Song | Source | Display style |
| --- | --- | --- |
| Sellakkaraya | [sellakkaraya](lyrics-player/sellakkaraya/) | Rendered Sinhala pages, smooth transitions, continuous replay |
| Sandawaka Mathaka | [sandawaka-mathaka](lyrics-player/sandawaka-mathaka/) | Stored lyric bitmaps, 30 timed lines, dissolve transitions |
| Sandawathiye | [sandawathiye](lyrics-player/sandawathiye/) | Word reveal, fixed ellipses, music-note animation in the middle solo |
| Mal Peththak | [mal-peththak](lyrics-player/mal-peththak/) | Sinhala/English lyrics with calm letter reveal |

| Aadariye | [aadariye](lyrics-player/aadariye/) | Whole-word reveal, separate hook scenes, progressive sustain dots |
| Adare Wediwela | [adare-wediwela](lyrics-player/adare-wediwela/) | Vocal-aligned word reveal, selected phrase-final sustain dots |

## Requirements

- macOS with Python 3 and Xcode Command Line Tools (`clang` and AVFoundation).
- Arduino UNO, ST7920 128×64 LCD in serial mode, and a USB cable.
- Arduino IDE or `arduino-cli`, Arduino AVR Boards, and the U8g2 library.
- Python packages from `requirements.txt`.
- Your local copy of each MP3; audio recordings are not included.

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## LCD connections

| ST7920 signal | Arduino UNO |
| --- | --- |
| RS / CS | D10 |
| R/W / SID | D11 / MOSI |
| E / SCLK | D13 / SCK |
| RST | D8 |
| PSB | GND (serial mode) |
| VSS | GND |
| VDD | 5V |

Set the LCD contrast using its contrast circuit. Keep the wiring used by the
sketches. These projects play audio on the Mac, not through an Arduino speaker.

## Run a song

Open the song folder linked above and follow its README. Upload its own Arduino
sketch before running its player; Sandawaka uses a different firmware protocol.
The timing files are tied to the exact MP3 SHA-256 hash to prevent accidental
playback with an incompatible edit of a song. The streaming players accept
`--mp3 /path/to/file.mp3`; Sandawaka accepts the audio path as a positional argument.

`tools/audio_clock.m` is compiled locally when playback first starts. No prebuilt
Mac executables are included. Source paths and launchers are relative to each
song folder. Double-click launchers use `python3` from your PATH; running from an
activated virtual environment in Terminal is the most predictable option.

The saved lyric and timing data are the final project snapshots. Sandawathiye's
vocal timing is locally estimated and has selected manual corrections; it has
not been fully confirmed by listening. `--offset` is for an overall adjustment,
not a replacement for correcting individual word cues.

## Layout

```text
lyrics-player/
  sellakkaraya/
    SellakkarayaLCD/          # Arduino sketch
    player.py                # Mac playback + LCD transport
  sandawaka-mathaka/
    LyricsKaraokeClear/      # Arduino sketch + lyric bitmap header
    play.py                  # Mac playback + LCD cues
  sandawathiye/
    SandawathiyeLCD/          # Arduino sketch
    player.py                # Mac playback + word reveal
  aadariye/
    AadariyeLCD/             # Arduino sketch
    player.py                # Separate hook scenes and sustain dots
  adare-wediwela/
    AdareWediwelaLCD/         # Arduino sketch
    player.py                # Word reveal and selected sustain dots
  mal-peththak/
    MalPeththakLCD/           # Arduino sketch
    player.py                # Sinhala/English letter reveal
```

Each song also contains lyrics, timing data, fonts, generated display assets,
source build tools, and a preview image. `SOURCE_SNAPSHOT.json` records the source
file hashes before the portable launchers and sketch-folder layout were prepared.
Recordings, machine binaries, playback logs, and superseded project versions are
excluded. See [NOTICES.md](NOTICES.md) for asset attribution.
