#!/usr/bin/env python3
"""Finish fixing: collapse excessive blank lines, double backticks."""
import re

path = "/home/snit.san/.workshop/document2026/doc/adv_guide/alphafold-db-api-access.md"

with open(path) as f:
    text = f.read()

# 1. Remaining double backticks -> single
text = re.sub(r'``([^`]+)``', r'`\1`', text)

# 2. Collapse hard-wrapped paragraphs: a partial line, blank, continuation -> join
def fix_paragraphs(text):
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        # Check if this is a hard-wrapped paragraph line
        # Current line doesn't end with sentence-ending punctuation
        # Next line is blank
        # Line after that is NOT a header/list/code/markdown element
        if (0 < len(line) < 120
            and line[-1] not in '.:?)]|'
            and not re.match(r'^#{1,6}\s', line)
            and not re.match(r'^[-*]\s', line)
            and not line.startswith('```')
            and not line.startswith('|')
            and not line.startswith('> ')
            and i + 2 < len(lines)
            and lines[i + 1].strip() == ''
            and lines[i + 2].strip()
            and not re.match(r'^#{1,6}\s', lines[i + 2])
            and not re.match(r'^[-*]\s', lines[i + 2])
            and not lines[i + 2].startswith('```')
            and not lines[i + 2].startswith('|')
            and not lines[i + 2].startswith('> ')):
            out.append(line + " " + lines[i + 2].rstrip())
            i += 3
            continue
        out.append(line)
        i += 1
    return "\n".join(out)

text = fix_paragraphs(text)

# 3. Collapse 3+ consecutive blank lines to 2
text = re.sub(r'\n{4,}', '\n\n\n', text)

# Ensure ends with single newline
text = text.rstrip('\n') + '\n'

with open(path, 'w') as f:
    f.write(text)

dt = len(re.findall(r'``', text)) // 2
print(f"Double backticks remaining: {dt}")
print(f"Lines: {text.count(chr(10))}")
