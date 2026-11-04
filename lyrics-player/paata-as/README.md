# Paata As — Praveen Madhubhashana ft. DILU Beats

Arduino UNO + ST7920 128×64 whole-word Sinhala lyric player. Music plays on the Mac. Font: ISI Gurulugomi 24px. The 36 supplied lines expand to 48 performed lines including repeated post-choruses. Long word endings hold until the next lyric, with progressive dots. Music-video dialogue and instrumental breaks are blank.

Keep the matching MP3 in Downloads. Run player.py or Play Paata As.command. Stop with Control+C. Timings are locally model-estimated; exact sync needs listening feedback.

LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND. Compatible with existing streaming firmware.

Install dependencies from the repository root requirements.txt. Upload `PaataAsLCD/PaataAsLCD.ino` if the board needs streaming firmware. Supply your own matching MP3 in Downloads, or run `python3 player.py --mp3 /path/to/song.mp3`. The Mac audio helper builds on first run using Xcode Command Line Tools.

This package contains the latest saved playback source, alignment, fonts and display assets. Rebuild the display with `python3 tools/build_display.py`. Audio recordings, isolated vocal stems, machine binaries, playback logs, superseded backups and exploratory timing scripts are excluded. Saved timing is model-derived; exact vocal synchronization has not been certified by listening.
