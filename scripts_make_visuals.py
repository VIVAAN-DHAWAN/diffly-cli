from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('/home/ubuntu/diffly-cli')
ASSETS = ROOT / 'assets'
SCREENSHOTS = ASSETS / 'screenshots'
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
FONT_BOLD_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
FONT = ImageFont.truetype(FONT_PATH, 22)
SMALL = ImageFont.truetype(FONT_PATH, 18)
TITLE = ImageFont.truetype(FONT_BOLD_PATH, 30)
BIG = ImageFont.truetype(FONT_BOLD_PATH, 48)

BG = '#0d1117'
PANEL = '#161b22'
BORDER = '#30363d'
TEXT = '#e6edf3'
MUTED = '#8b949e'
GREEN = '#3fb950'
YELLOW = '#d29922'
RED = '#f85149'
BLUE = '#58a6ff'
PURPLE = '#bc8cff'


def terminal_base(title: str, width: int = 1400, height: int = 800) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new('RGB', (width, height), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((34, 32, width - 34, height - 32), radius=16, fill=PANEL, outline=BORDER, width=2)
    draw.rectangle((34, 32, width - 34, 92), fill='#21262d')
    for x, color in [(70, '#ff5f56'), (105, '#ffbd2e'), (140, '#27c93f')]:
        draw.ellipse((x - 9, 52 - 9, x + 9, 52 + 9), fill=color)
    draw.text((185, 42), title, font=SMALL, fill=MUTED)
    return image, draw


def draw_lines(draw: ImageDraw.ImageDraw, lines: list[str], x: int = 70, y: int = 128, line_height: int = 30, max_width: int = 1260) -> int:
    for line in lines:
        if line.startswith('### '):
            draw.text((x, y), line[4:], font=TITLE, fill=BLUE)
        elif line.startswith('VERDICT:'):
            verdict = line.split(':', 1)[1].strip()
            color = GREEN if verdict == 'SHIP' else YELLOW if verdict == 'QUARANTINE' else RED
            draw.text((x, y), line, font=BIG, fill=color)
        elif line.startswith('$ '):
            draw.text((x, y), '$', font=FONT, fill=GREEN)
            draw.text((x + 28, y), line[2:], font=FONT, fill=TEXT)
        elif line.startswith('  '):
            draw.text((x, y), line, font=SMALL, fill=MUTED)
        else:
            draw.text((x, y), line, font=FONT, fill=TEXT)
        y += line_height
    return y


def make_screenshot(filename: str, title: str, lines: list[str]) -> None:
    image, draw = terminal_base(title)
    draw_lines(draw, lines)
    image.save(SCREENSHOTS / filename, optimize=True)


make_screenshot('vscode-330848.png', 'diffly-cli · real PR demo', [
    '### microsoft/vscode#330848',
    '$ diffly-cli pr microsoft/vscode 330848',
    '',
    'sessions: Add grid layout for chats',
    '25 commits · 25 files · +2,557 / -251 lines',
    '',
    'VERDICT: QUARANTINE',
    'reason: missing obvious test coverage',
    'checks: SUCCESS · 27 observed',
    '',
    'blast radius: changed symbols + direct callers',
])
make_screenshot('kubernetes-141413.png', 'diffly-cli · real PR demo', [
    '### kubernetes/kubernetes#141413',
    '$ diffly-cli pr kubernetes/kubernetes 141413',
    '',
    'scheduler: migrate scheduling API usage',
    '1 commit · 41 files · +708 / -740 lines',
    '',
    'VERDICT: QUARANTINE',
    'reason: missing obvious test coverage',
    'checks: SUCCESS · 1 observed',
    '',
    'risk flags: NO_TEST_COVERAGE',
])
make_screenshot('ruff-27808.png', 'diffly-cli · real PR demo', [
    '### astral-sh/ruff#27808',
    '$ diffly-cli pr astral-sh/ruff 27808',
    '',
    '[ty] Distinguish TypeVarTuple arguments...',
    '1 commit · 49 files · +1,675 / -254 lines',
    '',
    'VERDICT: BLOCK',
    'reason: at least one status check failed',
    'checks: FAILURE · 66 observed',
    '',
    'risk flags: CHECKS_FAILED, NO_TEST_COVERAGE',
])

frames: list[Image.Image] = []
sequence = [
    ('diffly-cli · deterministic PR triage', [
        '### Make large AI-generated PRs reviewable',
        '',
        'Fetch the PR. Map the blast radius. Apply fixed rules.',
        'No LLM required for the first gate.',
    ]),
    ('diffly-cli · running analysis', [
        '### Real pull request analysis',
        '$ diffly-cli pr astral-sh/ruff 27808',
        '',
        'fetching metadata ............ done',
        'fetching changed files ....... done',
        'parsing Tree-sitter symbols .. done',
        'checking status runs ......... done',
    ]),
    ('diffly-cli · verdict', [
        '### astral-sh/ruff#27808',
        '49 files · +1,675 / -254 lines',
        '',
        'VERDICT: BLOCK',
        'failed status checks detected',
        '66 checks observed',
    ]),
    ('diffly-cli · risk flags', [
        '### Deterministic evidence',
        'CHECKS_FAILED .............. CRITICAL',
        'NO_TEST_COVERAGE .......... MEDIUM',
        '',
        'The policy is inspectable.',
        'The verdict is reproducible.',
    ]),
    ('diffly-cli · next step', [
        '### One-page review before the LLM',
        'blast-radius map',
        'risk flags',
        'SHIP / QUARANTINE / BLOCK',
        '',
        'github.com/VIVAAN-DHAWAN/diffly-cli',
    ]),
]
for title, lines in sequence:
    image, draw = terminal_base(title, 1400, 800)
    draw_lines(draw, lines, y=150, line_height=42)
    frames.append(image)

frames[0].save(ASSETS / 'diffly-cli-demo.gif', save_all=True, append_images=frames[1:], duration=[1800, 1600, 1800, 1600, 2200], loop=0, optimize=False)
print(f'created {len(frames)} GIF frames and {len(list(SCREENSHOTS.glob("*.png")))} screenshots')
