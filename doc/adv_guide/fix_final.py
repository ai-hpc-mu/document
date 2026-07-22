#!/usr/bin/env python3
"""Fix hard-wrapped paragraphs in alphafold-db-api-access.md."""
import re

path = "/home/snit.san/.workshop/document2026/doc/adv_guide/alphafold-db-api-access.md"

with open(path) as f:
    lines = f.readlines()

result = []
i = 0
while i < len(lines):
    line = lines[i].rstrip()
    # Check if this is a hard wrap: current line + blank + indented continuation
    if (line and
        i + 2 < len(lines) and
        lines[i + 1].strip() == '' and
        lines[i + 2].startswith('  ')):
        # Continuation line starts with indentation (continuation of list item or prose)
        cont = lines[i + 2].rstrip()
        if cont[-1:] != '\n' if lines[i + 2].endswith('\n') else True:
            result.append(line + ' ' + cont.strip() + '\n')
            i += 3
            continue
    result.append(line + '\n')
    i += 1

# Collapse 3+ blank lines to 2
text = re.sub(r'\n{4,}', '\n\n\n', ''.join(result))

# Ensure single trailing newline
text = text.rstrip('\n') + '\n'

with open(path, 'w') as f:
    f.write(text)

# Verify no more hard wraps
with open(path) as f:
    lines = f.readlines()

remaining = 0
for i in range(len(lines)):
    l = lines[i].rstrip()
    if not l:
        continue
    if (i + 2 < len(lines) and
        lines[i + 1].strip() == '' and
        l[-1] not in '.:?)]' and
        not re.match(r'^[#*\-|>`]', lines[i + 2].rstrip())):
        remaining += 1
        print(f"  Still wrapped: L{i+1}: ...{l[-30:]} + {lines[i+2].rstrip()[:30]}")

print(f"Remaining hard wraps: {remaining}")
print(f"Final lines: {len(lines)}")
