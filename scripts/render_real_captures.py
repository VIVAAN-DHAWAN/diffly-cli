from __future__ import annotations

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
CAPTURES = ROOT / 'assets' / 'real-captures'
SCREENSHOTS = ROOT / 'assets' / 'screenshots'
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
SMALL_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
FONT = ImageFont.truetype(FONT_PATH, 20)
SMALL = ImageFont.truetype(FONT_PATH, 16)
BOLD = ImageFont.truetype(SMALL_PATH, 22)

ANSI_RE = re.compile(r'\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\))')
BG = '#0d1117'
PANEL = '#161b22'
BORDER = '#30363d'
TEXT = '#e6edf3'
MUTED = '#8b949e'
GREEN = '#3fb950'
BLUE = '#58a6ff'
YELLOW = '#d29922'
RED = '#f85149'


def clean_capture(path: Path) -> list[str]:
    raw = path.read_text(encoding='utf-8', errors='replace')
    lines = []
    for raw_line in raw.splitlines():
        line = ANSI_RE.sub('', raw_line).replace('\r', '')
        if line.startswith('Script started on ') or line.startswith('Script done on '):
            continue
        if line.strip():
            lines.append(line)
    return lines


def render(lines: list[str], title: str, height: int = 980) -> Image.Image:
    image = Image.new('RGB', (1500, height), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((24, 24, 1476, height - 24), radius=14, fill=PANEL, outline=BORDER, width=2)
    draw.rectangle((24, 24, 1476, 82), fill='#21262d')
    for x, color in [(60, '#ff5f56'), (94, '#ffbd2e'), (128, '#27c93f')]:
        draw.ellipse((x - 8, 46 - 8, x + 8, 46 + 8), fill=color)
    draw.text((170, 36), title, font=SMALL, fill=MUTED)

    y = 110
    for line in lines[:34]:
        if line.startswith('$ '):
            draw.text((58, y), line, font=FONT, fill=GREEN)
        elif line.startswith('# PR triage'):
            draw.text((58, y), line, font=BOLD, fill=BLUE)
        elif line.startswith('# **BLOCK**'):
            draw.text((58, y), line, font=BOLD, fill=RED)
        elif line.startswith('# **QUARANTINE**'):
            draw.text((58, y), line, font=BOLD, fill=YELLOW)
        elif line.startswith('# **SHIP**'):
            draw.text((58, y), line, font=BOLD, fill=GREEN)
        elif line.startswith('## '):
            draw.text((58, y), line, font=BOLD, fill=BLUE)
        elif line.startswith('Wrote '):
            draw.text((58, y), line, font=FONT, fill=GREEN)
        else:
            draw.text((58, y), line[:112], font=FONT, fill=TEXT)
        y += 27
        if y > height - 48:
            break
    return image


names = ['vscode-330848', 'kubernetes-141413', 'ruff-27808']
frames: list[Image.Image] = []
for name in names:
    lines = clean_capture(CAPTURES / f'{name}.ansi')
    image = render(lines, f'diffly-cli · captured terminal session · {name}')
    image.save(SCREENSHOTS / f'{name}.png', optimize=True)
    frames.append(image)

# The GIF contains only frames rendered from real captured CLI transcripts.
frames[0].save(ROOT / 'assets' / 'diffly-cli-demo.gif', save_all=True, append_images=frames[1:], duration=[2200, 2200, 2800], loop=0, optimize=False)
print(f'rendered {len(frames)} screenshots and one GIF from real terminal captures')
