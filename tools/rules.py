#!/usr/bin/env python3
"""Checks STANDARD.md and writes RULES.md, the one-table index agents load first.

usage: rules.py           check STANDARD.md, then write RULES.md
       rules.py --check   check STANDARD.md and that RULES.md is up to date; write nothing

Exit 0 when every check passes; otherwise every failure is printed as `STANDARD.md:<line>: <what>` and the exit is 1.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STANDARD = ROOT / "STANDARD.md"
INDEX = ROOT / "RULES.md"
RELEASED = ROOT / "tools" / "released-ids.txt"

HEADING = re.compile(r"^### G-(\d+)\.(\d+) (\S.*)$")
META = re.compile(r"^\*\*Scope:\*\* (.+?) · \*\*From:\*\* (.+?) · \*\*Checked by:\*\* (.+?) · \*\*Class:\*\* (.+)$")
SCOPES = {"everywhere", "everywhere except hot path", "hot path"}
CONDITION_ROW = re.compile(r"^\| ([^|*]+?) \| ")
CLASSES = {"defect", "rule"}
PRINCIPLES = {f"P{n}" for n in range(1, 8)}
CHECKS = {"build", "test", "measure", "review"}


def conditions(lines: list[str]) -> set[str]:
    """The skip-unless conditions defined by the table under "How to read a rule"."""
    start = next(i for i, l in enumerate(lines) if l.startswith("| Condition (*skip unless*)"))
    found = set()
    for line in lines[start + 2:]:
        m = CONDITION_ROW.match(line)
        if not m:
            break
        found.update(c.strip() for c in m[1].split(","))
    return found


def parse(lines: list[str]) -> tuple[list[dict], list[str]]:
    """The rule blocks of the standard, outside fenced code, and every format failure found."""
    rules, failures, fenced = [], [], False
    allowed = SCOPES | {f"skip unless {c}" for c in conditions(lines)}
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fenced = not fenced
            continue
        m = HEADING.match(line)
        if fenced or not m:
            continue
        rule = {"id": f"G-{m[1]}.{m[2]}", "key": (int(m[1]), int(m[2])), "title": m[3], "line": i + 1}
        rest = [l for l in lines[i + 1:i + 12]]
        nonblank = [l for l in rest if l.strip()]
        if "Withdrawn in" in (nonblank[0] if nonblank else ""):
            rule.update(scope="withdrawn", principles="", checks="", klass="", finding=nonblank[0].strip("*_ "))
            rules.append(rule)
            continue
        meta = META.match(nonblank[0]) if nonblank else None
        if not meta:
            failures.append(f"STANDARD.md:{i + 1}: {rule['id']} has no Scope · From · Checked by · Class line")
            continue
        scope, principles, checks, klass = meta[1], meta[2], meta[3], meta[4]
        if klass not in CLASSES:
            failures.append(f"STANDARD.md:{i + 1}: {rule['id']} has an unknown class '{klass}'")
        if scope not in allowed:
            failures.append(f"STANDARD.md:{i + 1}: {rule['id']} has an unknown scope '{scope}'")
        if not {p.strip() for p in principles.split(",")} <= PRINCIPLES:
            failures.append(f"STANDARD.md:{i + 1}: {rule['id']} names an unknown principle in '{principles}'")
        if not {c.strip() for c in checks.split(",")} <= CHECKS:
            failures.append(f"STANDARD.md:{i + 1}: {rule['id']} has an unknown check in '{checks}'")
        start = lines.index(nonblank[1], i + 1) if len(nonblank) > 1 else -1
        if start < 0 or not lines[start].startswith("**Finding:** "):
            failures.append(f"STANDARD.md:{i + 1}: {rule['id']} has no Finding line after its Scope line")
            continue
        finding = []
        for l in lines[start:]:
            if not l.strip():
                break
            finding.append(l.strip())
        rule.update(scope=scope, principles=principles, checks=checks, klass=klass,
                    finding=" ".join(finding)[len("**Finding:** "):])
        rules.append(rule)
    return rules, failures


def check(rules: list[dict]) -> list[str]:
    """IDs unique, in order, and every released ID still present."""
    failures, seen = [], {}
    for prev, rule in zip([None] + rules, rules):
        if rule["id"] in seen:
            failures.append(f"STANDARD.md:{rule['line']}: {rule['id']} also at line {seen[rule['id']]}")
        seen[rule["id"]] = rule["line"]
        if prev and rule["key"] <= prev["key"]:
            failures.append(f"STANDARD.md:{rule['line']}: {rule['id']} comes after {prev['id']}")
    for rid in RELEASED.read_text().split():
        if rid not in seen:
            failures.append(f"STANDARD.md: released rule {rid} is missing; withdraw it, never remove it")
    return failures


def render(rules: list[dict], version: str) -> str:
    """RULES.md: one row per rule, in the standard's order."""
    out = [
        "# Rules index",
        "",
        f"Generated from [`STANDARD.md`](STANDARD.md) {version} by `tools/rules.py`; do not edit by hand. One row per",
        "rule. Read the rule's block in the standard before applying it or reporting a finding against it.",
        "",
        "| ID | Rule | Scope | Class | Checked by | Finding |",
        "|---|---|---|---|---|---|",
    ]
    for r in rules:
        cells = [r["id"], r["title"], r["scope"], r["klass"], r["checks"], r["finding"]]
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    return "\n".join(out) + "\n"


def main() -> int:
    lines = STANDARD.read_text().splitlines()
    version = next((l.split(",")[0].replace("Version ", "v") for l in lines if l.startswith("Version ")), "")
    rules, failures = parse(lines)
    failures += check(rules)
    text = render(rules, version)
    if "--check" in sys.argv[1:]:
        if not INDEX.exists() or INDEX.read_text() != text:
            failures.append("RULES.md: out of date; run tools/rules.py")
    elif not failures:
        INDEX.write_text(text)
    for f in failures:
        print(f)
    print(f"{len(rules)} rules, {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
