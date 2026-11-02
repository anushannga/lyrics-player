# Deviyange Bare — Drill Team ft. Sanuka

Arduino UNO + ST7920 128×64 player. Audio plays on the Mac; the supplied 130 Sinhala lyric lines display word by word using the supplied Su Naga (su_naga.ttf) legacy font at 24px.

Keep the matching MP3 in Downloads. Run `python3 player.py`, or double-click `Play Deviyange Bare.command`. Stop with Control+C.

The rap uses short word cues. Long content words in the melodic choruses gain three persistent dots one at a time. Saved timing is locally model-estimated and needs listening feedback to confirm exact synchronization. Unprovided intro/outro vocal effects are blank.

LCD: CS D10, SID D11, SCLK D13, RESET D8, PSB GND. Compatible with the existing streaming firmware.

Upload `DeviyangeBareLCD/DeviyangeBareLCD.ino` if the board needs the streaming firmware. Install Python dependencies from the repository root requirements.txt. Supply your own matching MP3 in Downloads, or use `python3 player.py --mp3 /path/to/song.mp3`. The native Mac audio helper compiles on first run using Xcode Command Line Tools.

The saved alignment and display assets are the latest played snapshot. Rebuild the display with `python3 tools/build_display.py`. Optional analysis tools require requirements-analysis.txt, locally cached faster-whisper models, and Kim_Vocal_2.onnx in ~/.cache/audio-models/. Analysis scripts record the development workflow; intermediate audio and superseded alignment experiments are excluded. Start from the included alignment.json when rebuilding the final display. Regenerating audio alignment may change saved timing refinements.
