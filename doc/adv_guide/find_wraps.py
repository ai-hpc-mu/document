#!/usr/bin/env python3
"""Find and fix remaining paragraph hard wraps."""
import re

path = "/home/snit.san/.workshop/document2026/doc/adv_guide/alphafold-db-api-access.md"

with open(path) as f:
    lines = f.readlines()

# Find hard wraps: line not ending properly + blank + continuation
bad = []
for i in range(len(lines)):
    l = lines[i].rstrip()
    if not l:
        continue
    if i + 2 >= len(lines):
        continue
    mid = lines[i + 1].strip()
    nxt = lines[i + 2].rstrip()
    if mid != '' or not nxt:
        continue
    # Current line doesn't end with sentence terminator
    if l[-1] in '.:?)]':
        continue
    # Next line starts a new markdown element
    if re.match(r'^[#*\-|>]', nxt) or nxt.startswith('```'):
        continue
    bad.append((i + 1, l, nxt))

print("Remaining hard wraps:")
for num, l1, l2 in bad:
    print(f"  L{num}: ...{l1[-40:]}  ->  {l2[:40]}...")
print(f"\nTotal: {len(bad)}")
