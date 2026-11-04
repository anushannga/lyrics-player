# Numba Kagedo — DILU Beats

Whole-word Sinhala LCD player for Arduino UNO + ST7920. Uses ISI Gurulugomi 24px, matching Nura Ananthe. Audio plays on the Mac. The 33 performed lyric lines, including both repeated post-choruses use locally model-estimated word timing. Exact sync needs listening feedback. Unprovided intro vocals are blank.

Keep the matching MP3 in Downloads. Run player.py or Play Numba Kagedo.command. Stop with Control+C. Connections: CS D10, SID D11, SCLK D13, RESET D8, PSB GND.

Timing review: both Kolam/Paawee post-choruses repeat twice. The final display now continues through 218.9 seconds. One collapsed bridge phrase uses evenly spaced display cues pending listening confirmation; see timing_review_notes.json.

Install dependencies from the repository root requirements.txt. Upload `NumbaKagedoLCD/NumbaKagedoLCD.ino` if the board needs streaming firmware. Supply your own matching MP3 in Downloads, or run `python3 player.py --mp3 /path/to/song.mp3`. The Mac audio helper builds on first run using Xcode Command Line Tools.

This package contains the latest saved playback source, alignment, fonts and display assets. Rebuild the display with `python3 tools/build_display.py`. Audio recordings, isolated vocal stems, machine binaries, playback logs, superseded backups and exploratory timing scripts are excluded. Saved timing is model-derived; exact vocal synchronization has not been certified by listening.
