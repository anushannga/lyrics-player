# Ithin Maa Numbawa Banda LCD player

Audio plays on the Mac; Sinhala lyrics stream to an Arduino UNO + ST7920 128×64 LCD. Font: supplied ISI Gurulugomi, 24px, matching the Nura Ananthe player. Whole words appear at saved vocal onsets. Repeated lyrics are expanded to match the recording. Instrumental and wordless sections are blank.

Keep Ithin Maa Numbawa Banda.mp3 in Downloads. Run `python3 player.py`, or double-click `Play Ithin Maa Numbawa Banda.command`. Stop with Control+C.

Timing is model-derived locally and needs listening feedback for exact vocal synchronization. LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND. Existing streaming firmware is compatible.

The 20 supplied unique lines expand to 46 performed lyric lines: two choruses before the bridge and three after it. Transcription windows and spectral repeat evidence are retained locally.

Upload `IthinMaaNumbawaBandaLCD/IthinMaaNumbawaBandaLCD.ino` if the board needs the streaming firmware. Install Python dependencies from the repository root requirements.txt. Supply your own matching MP3 in Downloads, or use `python3 player.py --mp3 /path/to/song.mp3`. The native Mac audio helper compiles on first run using Xcode Command Line Tools.

The saved alignment and display assets are the latest played snapshot. Rebuild the display with `python3 tools/build_display.py`. Optional analysis tools require requirements-analysis.txt, locally cached faster-whisper models, and Kim_Vocal_2.onnx in ~/.cache/audio-models/. Analysis scripts record the development workflow; intermediate audio and superseded alignment experiments are excluded. Start from the included alignment.json when rebuilding the final display. Regenerating audio alignment may change saved timing refinements.
