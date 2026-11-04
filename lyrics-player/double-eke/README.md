# Double Eke — Keefa

Arduino UNO + ST7920 128×64 lyric player. Audio plays on the Mac; whole Sinhala words stream over USB. Uses the same Su Naga font at 24px as the latest Deviyange Bare player. Supplied lyrics are matched to the recording; repeated sections are placed at their performed times. Short rap words have no unnecessary sustain dots.

Keep the matching MP3 in Downloads. Run `python3 player.py` or double-click `Play Double Eke.command`. Stop with Control+C. Timings are locally model-estimated and need listening feedback for exact sync.

LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND. Existing streaming firmware is compatible.

Install dependencies from the repository root requirements.txt. Upload `DoubleEkeLCD/DoubleEkeLCD.ino` if the board needs streaming firmware. Supply your own matching MP3 in Downloads, or run `python3 player.py --mp3 /path/to/song.mp3`. The Mac audio helper builds on first run using Xcode Command Line Tools.

This package contains the latest saved playback source, alignment, fonts and display assets. Rebuild the display with `python3 tools/build_display.py`. Audio recordings, isolated vocal stems, machine binaries, playback logs, superseded backups and exploratory timing scripts are excluded. Saved timing is model-derived; exact vocal synchronization has not been certified by listening.
