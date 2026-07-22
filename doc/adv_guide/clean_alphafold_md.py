#!/usr/bin/env python3
"""Cleanup: fix remaining double backticks and hard-wrapped paragraphs."""
import re

path = "/home/snit.san/.workshop/document2026/doc/adv_guide/alphafold-db-api-access.md"

with open(path) as f:
    text = f.read()

# 1. Double backticks -> single
text = re.sub(r'``([^`]+)``', r'`\1`', text)

# 2. Fix hard-wrapped paragraphs
lines = text.split('\n')
out = []
i = 0
while i < len(lines):
    curr = lines[i].rstrip()
    # Join mid-sentence hard wraps: short line ending without punctuation,
    # blank line, then a continuation line
    if (i + 2 < len(lines) and
        lines[i + 1].strip() == '' and
        curr and curr[-1] not in '.:?)]-|' and
        not re.match(r'^[#*\-|>]', curr) and
        not curr.startswith('```') and
        len(curr) < 100):
        nxt = lines[i + 2].rstrip()
        if (nxt and
            not re.match(r'^[#*\-|>`]', nxt) and
            not nxt.startswith('```')):
            out.append(curr + ' ' + nxt)
            i += 3
            continue
    out.append(curr)
    i += 1

text = '\n'.join(out)

# 3. Collapse 3+ blank lines to 2
text = re.sub(r'\n{4,}', '\n\n\n', text)

# Ensure single trailing newline
text = text.rstrip('\n') + '\n'

with open(path, 'w') as f:
    f.write(text)

# Verify
count = text.count('\n')
dticks = re.findall(r'``', text)
print(f"Lines: {count}, Double backticks remaining: {len(dticks) // 2}")
