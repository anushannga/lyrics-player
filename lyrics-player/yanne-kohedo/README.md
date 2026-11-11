# Yanne Kohedo — local lyric player

Audio: Downloads/noname.mp3, duration 304.614 seconds. Arduino UNO + ST7920 128×64; ISI Gurulugomi 24px.

Whole words appear against the Mac audio clock. Sustained final words show three progressive dots, then hold until the next word or long instrumental break. First lyric: 47.32 seconds.

20 supplied lyric lines. Local phonetic alignment plus 19 targeted onset corrections using independent recognition and selected separated-vocal clips. Timings are estimates and have not been confirmed by listening.

Run Play Yanne Kohedo.command. Stop with Control+C. LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND.

Install dependencies using the root requirements.txt. Upload `YanneKohedoLCD/YanneKohedoLCD.ino` if the board needs the streaming firmware. Keep the matching recording as Downloads/noname.mp3, or supply a path:

```sh
python3 player.py --mp3 /path/to/song.mp3
```

The Mac audio helper compiles from tools/audio_clock.m on first playback. Rebuild display assets with `python3 tools/build_display.py` using the saved final alignment.json and the matching MP3 in Downloads. Recordings, isolated vocals, models, machine executables, logs and exploratory analysis scripts are excluded.
