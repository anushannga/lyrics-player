# Adare Wediwela LCD player

Piyath Rajapakse — Adare Wediwela, using the lyrics supplied by the user.
Audio plays on the Mac; complete Sinhala words and progressive sustain dots stream over USB to the existing Arduino UNO ST7920 firmware.

Run `./Play Adare Wediwela.command`. Keep the matching MP3 in Downloads.
Font: supplied ISI Gurulugomi. Connections: CS D10, SID D11, SCLK D13, RESET D8, PSB GND.
Timing is locally model-aligned; playback feedback is needed to confirm precise vocal synchronization.

Refinement: isolate vocals locally with Kim Vocal 2, align each bounded phrase, compare chorus repetitions spectrally, trim silent word lead-ins, and select long phrase-final vocal words for progressive ellipses. Run tools/isolate_vocals.py, tools/align_vocals.py, tools/check_repeats.py, tools/refine_vocal_boundaries.py, tools/select_sustains.py, then tools/build_display.py to rebuild. Precise human-listened synchronization is not certified.

Upload `AdareWediwelaLCD/AdareWediwelaLCD.ino` with Arduino IDE or arduino-cli. Install the repository root requirements. Supply your own matching MP3 in Downloads, or use `python3 player.py --mp3 /path/to/song.mp3`. Prebuilt frames and timing are included; analysis models and audio stems are not. Rebuilding analysis needs requirements-analysis.txt, the cached faster-whisper small model, and (for vocal isolation) Kim_Vocal_2.onnx in ~/.cache/audio-models/.
