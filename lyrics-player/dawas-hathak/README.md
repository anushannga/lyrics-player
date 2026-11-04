# Dawas Hathak — Ramidu feat. DILU Beats

Arduino UNO + ST7920 128×64 Sinhala lyric player. Music plays on the Mac; complete words stream over USB. Font: ISI Gurulugomi at 24px, matching Nura Ananthe.

The supplied lyrics are locally aligned against the recording. Long phrase-final words gain persistent dots one at a time. Instrumental gaps are blank. Timing is model-estimated and needs listening feedback for exact vocal synchronization.

Keep the matching MP3 in Downloads. Run `python3 player.py` or double-click `Play Dawas Hathak.command`. Stop with Control+C.

LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND. Compatible with the existing streaming firmware.

Install dependencies from the repository root requirements.txt. Upload `DawasHathakLCD/DawasHathakLCD.ino` if the board needs streaming firmware. Supply your own matching MP3 in Downloads, or run `python3 player.py --mp3 /path/to/song.mp3`. The Mac audio helper builds on first run using Xcode Command Line Tools.

This package contains the latest saved playback source, alignment, fonts and display assets. Rebuild the display with `python3 tools/build_display.py`. Audio recordings, isolated vocal stems, machine binaries, playback logs, superseded backups and exploratory timing scripts are excluded. Saved timing is model-derived; exact vocal synchronization has not been certified by listening.
