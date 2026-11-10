# Nena — PARAPURA

Arduino UNO + ST7920 128×64 whole-word Sinhala lyrics. Audio plays on the Mac. Uses the user-supplied isigurul_0 (1).ttf, packaged as assets/isigurul_0.ttf, at 24px. Long sung endings hold with progressive dots; instrumental gaps are blank.

Keep the matching MP3 in Downloads. Run player.py or Play Nena.command. Stop with Control+C. Alignment is model-estimated and requires listening feedback for exact synchronization.

LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND.

Install dependencies from the repository root requirements.txt. Upload `NenaLCD/NenaLCD.ino` if the board needs streaming firmware. Supply your own matching MP3 in Downloads, or run `python3 player.py --mp3 /path/to/song.mp3`. The native Mac audio helper compiles on first run using Xcode Command Line Tools.

This package contains the latest saved playback source, alignment, font and generated display assets. Rebuild with `python3 tools/build_display.py`; use the included alignment.json to retain the final timing corrections. Recordings, isolated audio, models, machine executables, playback logs, superseded backups and exploratory analysis scripts are excluded. Audio/model alignment and runtime display checks do not certify exact vocal synchronization by listening.
