"""Align the supplied words to reviewed phrase windows on this MP3's time axis."""
import argparse
import hashlib
import json
from pathlib import Path

from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
from faster_whisper.tokenizer import Tokenizer

ROOT = Path(__file__).resolve().parents[1]


def save(name, data):
    (ROOT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mp3', type=Path)
    parser.add_argument('--vocals', type=Path, help='Time-preserving separated vocal track')
    args = parser.parse_args()
    source = (ROOT / 'lyrics_source.txt').read_text().splitlines()
    expanded = []
    for row in source:
        if row.startswith('='):
            start, end = map(int, row[1:].split(':'))
            expanded.extend(expanded[start:end])
        elif '|' in row:
            expanded.append(row)
    lyrics = []
    for i, (line, phonemes) in enumerate(row.split('|') for row in expanded):
        if len(line.split()) != len(phonemes.split()):
            raise ValueError(f'Line {i + 1}: unmatched phonetic words')
        lyrics.append(dict(id=i, language='si', text=line, alignment_text=phonemes))
    audio = decode_audio(str(args.mp3))
    duration = len(audio) / 16000
    if args.vocals:
        vocals = decode_audio(str(args.vocals))
        if abs(len(vocals) - len(audio)) > 1600:
            raise ValueError('Vocal track must share the MP3 time axis')
        audio = vocals
    models = {name: WhisperModel(name, device='cpu', compute_type='int8', cpu_threads=4, local_files_only=True) for name in ('base', 'small')}
    tokenizer = Tokenizer(models['small'].hf_tokenizer, True, task='transcribe', language='si')
    rows = []
    for count, start, end, *variant in json.loads((ROOT / 'alignment_windows.json').read_text()):
        model = models[variant[0] if variant else 'small']
        if not 0 <= start < end <= duration or end - start >= 30:
            raise ValueError(f'Invalid phrase window: {start}–{end}')
        group = lyrics[len(rows):len(rows) + count]
        clip = audio[round(start * 16000):round(end * 16000)]
        features = model.encode(model.feature_extractor(clip))
        prompt = '... ' + ' '.join(v['alignment_text'] for v in group) + ' ...'
        hits = model.find_alignment(tokenizer, [tokenizer.encode(prompt)], features, len(clip) // 160)[0]
        words = [dict(start=round(start + w['start'], 3), end=round(start + w['end'], 3), probability=float(w['probability'])) for w in hits if w['word'].strip(' .')]
        expected = sum(len(line['text'].split()) for line in group)
        if len(words) != expected:
            raise ValueError(f'{start}–{end}: expected {expected} words, got {len(words)}')
        pos = 0
        for line in group:
            sung = line['text'].split()
            timings = words[pos:pos + len(sung)]
            pos += len(sung)
            for word, timing in zip(sung, timings):
                timing['word'] = word
            rows.append(dict(id=line['id'], start=timings[0]['start'], end=timings[-1]['end'], words=timings))
            print(line['id'] + 1, ' '.join(f"{w['start']:.2f}:{w['word']}" for w in timings), flush=True)
    if len(rows) != len(lyrics):
        raise ValueError('Phrase windows do not cover every lyric')
    # Cross-check collapsed onsets against the neighboring syllables and chorus repeats.
    for line, word, onset in json.loads((ROOT / 'onset_corrections.json').read_text()):
        rows[line - 1]['words'][word - 1]['start'] = onset
    for row in rows:
        row['start'] = row['words'][0]['start']
    flat = [word for row in rows for word in row['words']]
    for current, following in zip(flat, flat[1:]):
        current['end'] = min(max(current['end'], current['start']), following['start'])
    if not all(a['start'] < b['start'] for a, b in zip(flat, flat[1:])):
        raise ValueError('Collapsed word onsets; revise the phrase windows')
    for row in rows:
        row['end'] = row['words'][-1]['end']
    save('lyrics.json', lyrics)
    save('audio.json', dict(duration=duration, sha256=hashlib.sha256(args.mp3.read_bytes()).hexdigest()))
    save('alignment.json', rows)


if __name__ == '__main__':
    main()
