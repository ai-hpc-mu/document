#!/usr/bin/env python3
"""Fix reST -> Markdown: line-by-line state machine."""
import re

path = "/home/snit.san/.workshop/document2026/doc/adv_guide/alphafold-db-api-access.md"

with open(path, "r") as f:
    lines = f.readlines()

output = []
i = 0
stats = {"code": 0, "literal": 0, "table": 0, "important": 0, "headers": 0}

while i < len(lines):
    line = lines[i]

    # 1. Title line: add #
    if i == 0 and line.startswith("AlphaFold DB Skill"):
        output.append("# " + line.lstrip("\n"))
        i += 1
        # skip === underline
        if i < len(lines) and re.match(r'^={3,}\s*$', lines[i]):
            i += 1
        continue

    # 2. Setext H2: Word\n---
    if i + 1 < len(lines) and re.match(r'^[-]{3,}\s*$', lines[i + 1]):
        output.append("## " + line.rstrip())
        stats["headers"] += 1
        i += 2
        if i < len(lines) and lines[i].strip() == "":
            i += 1
        continue

    # 3. Setext H3: Word\n~~~
    if i + 1 < len(lines) and re.match(r'^[~]{3,}\s*$', lines[i + 1]):
        output.append("### " + line.rstrip())
        stats["headers"] += 1
        i += 2
        if i < len(lines) and lines[i].strip() == "":
            i += 1
        continue

    # 4. .. code-block:: lang
    m = re.match(r'^\.\. code-block:: (\S+)\s*$', line)
    if m:
        lang = m.group(1)
        i += 1  # skip directive
        # skip blank line(s) after directive
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        # collect indented content
        code_lines = []
        while i < len(lines):
            l = lines[i]
            # lines inside code blocks start with 3 spaces
            if l.startswith("   "):
                code_lines.append(l[3:])
                i += 1
            else:
                break
        # strip trailing blank lines
        while code_lines and code_lines[-1].strip() == "":
            code_lines.pop()
        body = "".join(code_lines)
        output.append(f"\n```{lang}\n{body}\n```\n")
        stats["code"] += 1
        continue

    # 5. .. list-table::
    if line.startswith(".. list-table::"):
        i += 1
        # skip :option lines and blank
        while i < len(lines) and (lines[i].startswith("   :") or lines[i].strip() == ""):
            i += 1
        # parse rows
        header = None
        rows = []
        cur = []
        while i < len(lines):
            l = lines[i].rstrip()
            ms = re.match(r'^   \* -(?: )?(.*)$', l)
            md = re.match(r'^     -(?: )?(.*)$', l)
            if ms:
                if cur:
                    if header is None:
                        header = cur
                    else:
                        rows.append(cur)
                cur = [ms.group(1)]
                i += 1
            elif md and cur:
                cur.append(md.group(1))
                i += 1
            elif l.strip() == "" or (not l.startswith("   ")):
                # blank line or non-table content ends the table
                if cur:
                    if header is None:
                        header = cur
                    else:
                        rows.append(cur)
                    cur = []
                if l.strip() == "":
                    i += 1
                break
            else:
                i += 1
        if cur:
            if header is None:
                header = cur
            else:
                rows.append(cur)

        if header:
            cols = len(header)
            output.append(f"\n| {' | '.join(header)} |\n")
            output.append(f"| {' | '.join(['---'] * cols)} |\n")
            for r in rows:
                c = [v.replace("|", "\\|") for v in r]
                while len(c) < cols:
                    c.append("")
                output.append(f"| {' | '.join(c)} |\n")
        stats["table"] += 1
        i += 1
        continue

    # 6. :: literal block
    if line.rstrip() == "::":
        i += 1
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        quoted = []
        while i < len(lines) and (lines[i].startswith("  ") or lines[i].startswith("\t")):
            s = lines[i].strip()
            if s:
                quoted.append(s)
            i += 1
        for q in quoted:
            output.append(f"> {q}\n")
        output.append("\n")
        stats["literal"] += 1
        continue

    # 7. .. important::
    if re.match(r'^\.\. important::\s*$', line):
        i += 1
        body = []
        while i < len(lines) and (lines[i].startswith("   ") or
               (lines[i].strip() == "" and i + 1 < len(lines) and lines[i + 1].startswith("   "))):
            s = lines[i].strip()
            if s:
                body.append(s)
            i += 1
        if i < len(lines) and lines[i].strip() == "":
            i += 1
        output.append(f"\n> **Important:** {' '.join(body)}\n\n")
        stats["important"] += 1
        continue

    # 8. Double backticks -> single
    out = re.sub(r'``([^`]+)``', r'`\1`', line)
    output.append(out)
    i += 1

result = "\n".join(output)
# collapse 3+ blank lines to 2
result = re.sub(r'\n{4,}', '\n\n\n', result)
# ensure trailing newline
if not result.endswith("\n"):
    result += "\n"

with open(path, "w") as f:
    f.write(result)

print(f"Fixed {path}")
print("  Conversions:")
print(f"    Headers (setext->atx):     {stats['headers']}")
print(f"    Code blocks:               {stats['code']}")
print(f"    Tables:                    {stats['table']}")
print(f"    Literal blocks (::):       {stats['literal']}")
print(f"    Admonitions (important):   {stats['important']}")

# Verify
rest = re.findall(r'\.\. \w+::', result)
if rest:
    print(f"  WARN: {len(rest)} reST remain: {rest}")
else:
    print("  OK: no remaining reST directives")
cb = len(re.findall(r'```', result)) // 2
print(f"  Output fenced code blocks: {cb}")
