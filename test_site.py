import os
from pathlib import Path
from bs4 import BeautifulSoup

root = Path('c:/Users/user/Olifant Web Studio')
files = [
    'index.html','about.html','services.html','portfolio.html','contact.html',
    'regcorp/index.html','regcorp/about.html','regcorp/services.html','regcorp/contact.html',
    'newlysly/index.html','newlysly/shop.html','newlysly/cart.html','newlysly/checkout.html',
]

print('=== File existence ===')
all_ok=True
for f in files:
    p = root / f
    status = 'OK' if p.exists() else 'MISSING'
    print(f'{f}: {status}')
    if not p.exists(): all_ok=False

print('\n=== Quick internal link scan ===')
links_ok=0
links_bad=0

for f in files:
    p = root / f
    if not p.exists():
        continue
    with p.open('r', encoding='utf-8', errors='ignore') as fh:
        soup = BeautifulSoup(fh, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('#') or href.startswith('http') or href.startswith('mailto:') or href.startswith('tel:'):
            continue
        # local relative path
        target = (p.parent / href).resolve()
        if target.exists():
            links_ok += 1
        else:
            links_bad += 1
            print(f'Broken link in {f}: {href} -> {target}')

print(f'Valid local links: {links_ok}, broken local links: {links_bad}')

# Perform config check
from pathlib import Path
for p in root.rglob('*.html'):
    if p.stat().st_size == 0:
        print('Empty file:', p)

print('\n=== Completed tests ===')
