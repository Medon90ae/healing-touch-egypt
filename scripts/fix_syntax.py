# -*- coding: utf-8 -*-
with open('c:/followUPSHEET/healing_touch/antigravity_social_automation.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        "---------------------------------------------------------------------",
    ]
    if discovered_studies:"""

replacement = """        "---------------------------------------------------------------------",
    ])
    if discovered_studies:"""

if target in text:
    text = text.replace(target, replacement)
    with open('c:/followUPSHEET/healing_touch/antigravity_social_automation.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed syntax error successfully')
else:
    print('Target not found, inspecting around line 1005...')
