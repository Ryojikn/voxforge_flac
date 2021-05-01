import os
from pathlib import Path
import pandas as pd

os.system('wget http://www02.smt.ufrj.br/~igor.quintanilha/voxforge-ptbr.tar.gz')

folder = Path('voxforge/')
paths = list(folder.glob('*/*.wav'))
otherpaths = list(folder.glob('*/*/*.wav'))
paths.extend(otherpaths)

prompts = list(folder.glob('*/PROMPTS'))
otherprompts = list(folder.glob('*/*/PROMPTS'))
prompts.extend(otherprompts)

transcripts = []

for prompt in prompts:
    with open(prompt, 'r', encoding="utf-8") as file:
        transcripts.extend(file.readlines())

transcript_paths = [row.split(' ')[0] for row in transcripts]
transcript_texts = [row.replace(transcript_paths[i], '').rstrip().lstrip().lower() for i, row in enumerate(transcripts)]

df = pd.DataFrame({'wav_paths': paths, 'transcript_paths': transcript_paths, 'transcript_texts': transcript_texts})

df['new_wav_paths'] = df['wav_paths'].apply(
                            lambda x: Path(
                                f"{x.as_posix().split('/')[0]}\\audios\\{x.as_posix().split('/')[1]}_{x.as_posix().split('/')[-1]}"
                            ).with_suffix('.flac'))

for i, audio in enumerate(df['wav_paths']):
    if not os.path.exists('voxforge/audios'):
        os.mkdir('voxforge/audios')
    command = f"ffmpeg -i {audio} -ar 16000 {df['new_wav_paths'][i]}"
    os.system(command)

dirs = os.listdir('voxforge/')
dirs.remove('audios')

removed_dirs = [os.system(f'rm -rf voxforge/{directory}') for directory in dirs]

final_df = df[['new_wav_paths', 'transcript_texts']]
final_df.columns = ['wav_paths', 'transcripts']
final_df

final_df.to_csv('voxforge/transcripts.tsv', sep='\t', encoding='utf-8')