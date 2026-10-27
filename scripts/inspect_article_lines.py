# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

p = Path(r'c:\followUPSHEET\healing_touch\docs\articles\3m-micropore-tan-tape-1533-0-clinical-mechanism.html')
text = p.read_text(encoding='utf-8')
for i, line in enumerate(text.splitlines(), 1):
    if 'نسخ' in line or 'هاشتاج' in line:
        print(f"Line {i}: {line[:120]}")
