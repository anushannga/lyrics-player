# Aye Me Wage LCD player

Music plays on the Mac; the connected Arduino UNO streams whole Sinhala words to the ST7920 128×64 LCD. Uses the supplied ISI Gurulugomi font at 24px.

Double-click `Play Aye Me Wage.command` or run `python3 player.py`.
Keep `Aye Me Wage.mp3` in Downloads. Press Control+C to stop.

The 41 user-provided lyric lines are preserved. Word timing is derived locally from isolated vocals and bounded phrases. Sustained content words gain three persistent dots one at a time; punctuation alone does not add them. Vocal timing remains model-estimated until confirmed during playback.

LCD: CS D10, SID D11, SCLK D13, RESET D8; PSB GND. Existing streaming firmware is compatible; upload AyeMeWageLCD/AyeMeWageLCD.ino only if the board does not already have it.

Install Python dependencies from the repository root requirements.txt. Supply your own matching MP3 in Downloads, or run `python3 player.py --mp3 /path/to/song.mp3`. Audio recordings, isolated stems and prebuilt Mac executables are excluded. The native audio helper compiles on first run using Xcode Command Line Tools.

Saved timing is the final playback snapshot. Display assets can be rebuilt with `python3 tools/build_display.py`. Optional analysis tools require requirements-analysis.txt, the faster-whisper base model cached locally, and Kim_Vocal_2.onnx at ~/.cache/audio-models/. To regenerate timing: isolate_vocals.py, align_vocals.py, refine_vocal_boundaries.py, select_sustains.py, then build_display.py, all in tools/.
