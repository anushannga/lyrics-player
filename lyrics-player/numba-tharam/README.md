# Numba Tharam — Suneera Sumanga

Arduino UNO + ST7920 128×64 whole-word Sinhala lyric player. Audio plays on the Mac. Font: ISI Gurulugomi 24px. The 24 user-supplied lines are locally aligned to the recording. Long word endings hold with progressive dots. Instrumental sections are blank. Timing is model-estimated and needs listening feedback for exact synchronization.

Keep the matching MP3 in Downloads. Run player.py or Play Numba Tharam.command. Stop with Control+C. LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND.

Install dependencies from the repository root requirements.txt. Upload `NumbaTharamLCD/NumbaTharamLCD.ino` if the board needs streaming firmware. Supply your own matching MP3 in Downloads, or run `python3 player.py --mp3 /path/to/song.mp3`. The Mac audio helper builds on first run using Xcode Command Line Tools.

This package contains the latest saved playback source, alignment, fonts and display assets. Rebuild the display with `python3 tools/build_display.py`. Audio recordings, isolated vocal stems, machine binaries, playback logs, superseded backups and exploratory timing scripts are excluded. Saved timing is model-derived; exact vocal synchronization has not been certified by listening.
