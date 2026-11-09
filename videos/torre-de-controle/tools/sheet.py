"""Folha de revisão de um ou mais clipes: 6 quadros por clipe, uma linha por clipe.
Uso: python3 sheet.py saida.jpg clipe1.mp4 [clipe2.mp4 ...]"""
import subprocess, sys, tempfile, os
from PIL import Image, ImageDraw
out, clips = sys.argv[1], sys.argv[2:]
rows = []
with tempfile.TemporaryDirectory() as d:
    for c in clips:
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', c],
                                   capture_output=True, text=True).stdout)
        ims = []
        for i in range(6):
            t = 0.15 + i * (dur - 0.3) / 5
            f = os.path.join(d, f'{len(rows)}_{i}.png')
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', c, '-frames:v', '1', '-vf', 'scale=240:-1', f], check=True)
            ims.append(Image.open(f).convert('RGB'))
        rows.append((os.path.basename(c), ims))
    w, h = rows[0][1][0].size
    sheet = Image.new('RGB', (w * 6, (h + 18) * len(rows)), 'white'); dr = ImageDraw.Draw(sheet)
    for r, (name, ims) in enumerate(rows):
        dr.text((4, r * (h + 18) + 3), name, fill='black')
        for i, im in enumerate(ims): sheet.paste(im.resize((w, h)), (i * w, r * (h + 18) + 18))
    sheet.save(out, quality=88)
