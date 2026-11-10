# Bo Mal — Janana Kuda ft. Ranudi de Zoysa

Arduino UNO + ST7920 128×64 Sinhala lyric player. Audio plays on the Mac. ISI Gurulugomi 24px matches the previous clear-font players. The supplied lines are expanded to performed repetitions; whole words appear at saved vocal cues. Long final words hold with progressive dots. Music and unprovided dialogue are blank.

Keep the matching MP3 in Downloads. Run player.py or Play Bo Mal.command. Stop with Control+C. Timings are locally model-estimated and need listening feedback for exact synchronization.

LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND.

Evidence-based sync correction: the Araliya bridge starts at 153.64s; the earlier 136s placement was wrong. The second pre-chorus and chorus use a 124.44s repeat offset verified by spectral comparison. Sustain dots stay inside aligned sung intervals while the final image holds until the next lyric. Human-listened exact word synchronization remains unconfirmed.

Install dependencies from the repository root requirements.txt. Upload `BoMalLCD/BoMalLCD.ino` if the board needs streaming firmware. Supply your own matching MP3 in Downloads, or run `python3 player.py --mp3 /path/to/song.mp3`. The native Mac audio helper compiles on first run using Xcode Command Line Tools.

This package contains the latest saved playback source, alignment, font and generated display assets. Rebuild with `python3 tools/build_display.py`; use the included alignment.json to retain the final timing corrections. Recordings, isolated audio, models, machine executables, playback logs, superseded backups and exploratory analysis scripts are excluded. Audio/model alignment and runtime display checks do not certify exact vocal synchronization by listening.
