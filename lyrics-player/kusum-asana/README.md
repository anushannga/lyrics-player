# Kusum Asana — Janana Kuda ft. Nirmani Gunawardhane

Arduino UNO + ST7920 128×64 whole-word Sinhala lyric player. Font: ISI Gurulugomi 24px. Audio plays on the Mac. Supplied lyrics expand to 44 performed lines including repeated sections. Long phrase endings hold until the next lyric with progressive dots; instrumental gaps are blank. Word timing is model-estimated and requires listening feedback for exact sync.

Keep the matching MP3 in Downloads. Run player.py or Play Kusum Asana.command. Stop with Control+C. LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND.

Sync review: isolated vocal alignment replaces the initial full-mix timing; reviewed phrase changes are in vocal_sync_review.json. Exact listening confirmation remains pending.

Install dependencies from the repository root requirements.txt. Upload `KusumAsanaLCD/KusumAsanaLCD.ino` if the board needs streaming firmware. Supply your own matching MP3 in Downloads, or run `python3 player.py --mp3 /path/to/song.mp3`. The native Mac audio helper compiles on first run using Xcode Command Line Tools.

This package contains the latest saved playback source, alignment, font and generated display assets. Rebuild with `python3 tools/build_display.py`; use the included alignment.json to retain the final timing corrections. Recordings, isolated audio, models, machine executables, playback logs, superseded backups and exploratory analysis scripts are excluded. Audio/model alignment and runtime display checks do not certify exact vocal synchronization by listening.
