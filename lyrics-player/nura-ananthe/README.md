# Nura Ananthe LCD player

Cozzy ft. Kshia — Nura Ananthe. The supplied 26 Sinhala lyric lines display word by word on Arduino UNO + ST7920 128×64. Audio plays on the Mac. Font: supplied ISI Gurulugomi, 24px. Long vocal words gain three persistent dots one at a time; punctuation alone does not determine sustain effects. Timing is locally model-estimated.

Keep the matching MP3 in Downloads. Run `python3 player.py` or double-click `Play Nura Ananthe.command`. Stop with Control+C.

LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND. Compatible with existing streaming firmware.

Upload `NuraAnantheLCD/NuraAnantheLCD.ino` if the board needs the streaming firmware. Install Python dependencies from the repository root requirements.txt. Supply your own matching MP3 in Downloads, or use `python3 player.py --mp3 /path/to/song.mp3`. The Mac audio helper compiles on first run using Xcode Command Line Tools.

Saved timing is the latest playback snapshot, with model-estimated vocal synchronization. Rebuild display assets with `python3 tools/build_display.py`. Optional analysis tools require requirements-analysis.txt, the faster-whisper base model cached locally, and Kim_Vocal_2.onnx at ~/.cache/audio-models/. To regenerate estimated timing, run isolate_vocals.py, align_vocals.py, refine_vocal_boundaries.py, select_sustains.py, then build_display.py from tools/. Regenerating alignment may change saved timing refinements. Recordings, analysis stems, models, playback logs and superseded backups are excluded.
