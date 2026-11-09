"""Aplica filmlook.py quadro a quadro num vídeo (grão diferente a cada quadro).
Uso: python3 filmlook_video.py entrada.mp4 saida.mp4"""
import os, subprocess, sys, tempfile, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from filmlook import filmlook
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
with tempfile.TemporaryDirectory() as d:
    subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-q:v', '2', f'{d}/%05d.png'], check=True)
    fs = sorted(glob.glob(f'{d}/*.png'))
    for i, f in enumerate(fs):
        filmlook(Image.open(f), seed=i).save(f)
    fps = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=r_frame_rate',
                          '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', fps, '-i', f'{d}/%05d.png', '-c:v', 'libx264',
                    '-crf', '16', '-pix_fmt', 'yuv420p', dst], check=True)
