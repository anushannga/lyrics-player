# Bowitiya Mal LCD player

Ravi Jay ft. Nipuni Sharada — Bowitiya Mal. Audio plays on the Mac; whole Sinhala words stream to the Arduino UNO + ST7920 128×64 display using ISI Gurulugomi at 24px.

The 28 supplied lines are retained, and supplied verses are reused where sung again. Unprovided vocal effects and instrumental parts are blank. Long sung words receive three progressive dots; rapid rap words are shown without unnecessary punctuation effects. Word timing is locally estimated from bounded vocal phrases.

Keep the matching MP3 in Downloads and run `python3 player.py`, or double-click `Play Bowitiya Mal.command`. Stop with Control+C.

LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND. Existing streaming firmware is compatible.

Upload `BowitiyaMalLCD/BowitiyaMalLCD.ino` if the board needs the streaming firmware. Install Python dependencies from the repository root requirements.txt. Supply your own matching MP3 in Downloads, or use `python3 player.py --mp3 /path/to/song.mp3`. The Mac audio helper compiles on first run using Xcode Command Line Tools.

Saved timing is the latest playback snapshot, with model-estimated vocal synchronization. Rebuild display assets with `python3 tools/build_display.py`. Optional analysis tools require requirements-analysis.txt, the faster-whisper base model cached locally, and Kim_Vocal_2.onnx at ~/.cache/audio-models/. To regenerate estimated timing, run isolate_vocals.py, align_vocals.py, refine_vocal_boundaries.py, select_sustains.py, then build_display.py from tools/. Regenerating alignment may change saved timing refinements. Recordings, analysis stems, models, playback logs and superseded backups are excluded.
