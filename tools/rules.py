#!/usr/bin/env python3
"""Checks STANDARD.md and writes RULES.md, the one-table index agents load first.

usage: rules.py [--root DIR]           check STANDARD.md, then write RULES.md
       rules.py [--root DIR] --check   check STANDARD.md and that RULES.md is up to date; write nothing

Reads `STANDARD.md` and `tools/released-ids.txt` under the repository root (`--root`, default the parent of this
script's folder); writes `RULES.md` there unless `--check` is given or a check fails.

Exit 0 when every check passes; 1 when one fails, every failure printed to stderr as `STANDARD.md:<line>: <what>`
(or `RULES.md: <what>`); 2 on a usage error. The count of rules and failures goes to stdout.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass, replace
from itertools import pairwise
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent

HEADING = re.compile(r"^### G-(\d+)\.(\d+) (\S.*)$")
META = re.compile(r"^\*\*Scope:\*\* (.+?) · \*\*From:\*\* (.+?) · \*\*Checked by:\*\* (.+?) · \*\*Class:\*\* (.+)$")
CONDITION_ROW = re.compile(r"^\| ([^|*]+?) \| ")
CONDITION_TABLE = "| Condition (*skip unless*)"
FINDING = "**Finding:** "
SCOPES = frozenset({"everywhere", "everywhere except hot path", "hot path"})
CLASSES = frozenset({"defect", "rule"})
PRINCIPLES = frozenset(f"P{n}" for n in range(1, 8))
CHECKS = frozenset({"build", "test", "measure", "review"})
# a rule's Scope line sits within this many lines after its heading
META_REACH = 11


@dataclass(frozen=True, slots=True)
class Rule:
    """One rule block of the standard: its heading, where it is, and its Scope line and Finding."""

    rule_id: str
    key: tuple[int, int]
    title: str
    line: int
    scope: str = ""
    principles: str = ""
    checks: str = ""
    klass: str = ""
    finding: str = ""


def conditions(lines: Sequence[str]) -> set[str]:
    """The skip-unless conditions defined by the table under "How to read a rule"."""
    start = next(i for i, line in enumerate(lines) if line.startswith(CONDITION_TABLE))
    found = set()
    for line in lines[start + 2:]:
        match = CONDITION_ROW.match(line)
        if not match:
            break
        found.update(c.strip() for c in match[1].split(","))
    return found


def parse(lines: Sequence[str]) -> tuple[list[Rule], list[str]]:
    """The rule blocks of the standard, outside fenced code, and every format failure found."""
    rules: list[Rule] = []
    failures: list[str] = []
    fenced = False
    allowed = SCOPES | {f"skip unless {c}" for c in conditions(lines)}
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fenced = not fenced
            continue
        heading = HEADING.match(line)
        if fenced or not heading:
            continue
        rule = Rule(f"G-{heading[1]}.{heading[2]}", (int(heading[1]), int(heading[2])), heading[3], i + 1)
        nonblank = [n for n in lines[i + 1:i + 1 + META_REACH] if n.strip()]
        if nonblank and "Withdrawn in" in nonblank[0]:
            rules.append(replace(rule, scope="withdrawn", finding=nonblank[0].strip("*_ ")))
            continue
        meta = META.match(nonblank[0]) if nonblank else None
        if not meta:
            failures.append(f"STANDARD.md:{i + 1}: {rule.rule_id} has no Scope · From · Checked by · Class line")
            continue
        scope, principles, checks, klass = meta[1], meta[2], meta[3], meta[4]
        if klass not in CLASSES:
            failures.append(f"STANDARD.md:{i + 1}: {rule.rule_id} has an unknown class '{klass}'")
        if scope not in allowed:
            failures.append(f"STANDARD.md:{i + 1}: {rule.rule_id} has an unknown scope '{scope}'")
        if not {p.strip() for p in principles.split(",")} <= PRINCIPLES:
            failures.append(f"STANDARD.md:{i + 1}: {rule.rule_id} names an unknown principle in '{principles}'")
        if not {c.strip() for c in checks.split(",")} <= CHECKS:
            failures.append(f"STANDARD.md:{i + 1}: {rule.rule_id} has an unknown check in '{checks}'")
        start = lines.index(nonblank[1], i + 1) if len(nonblank) > 1 else -1
        if start < 0 or not lines[start].startswith(FINDING):
            failures.append(f"STANDARD.md:{i + 1}: {rule.rule_id} has no Finding line after its Scope line")
            continue
        finding: list[str] = []
        for text in lines[start:]:
            if not text.strip():
                break
            finding.append(text.strip())
        rules.append(replace(rule, scope=scope, principles=principles, checks=checks, klass=klass,
                             finding=" ".join(finding)[len(FINDING):]))
    return rules, failures


def check(rules: Sequence[Rule], released: Sequence[str]) -> list[str]:
    """IDs unique, in order, and every released ID still present."""
    failures: list[str] = []
    seen: dict[str, int] = {}
    for rule in rules:
        if rule.rule_id in seen:
            failures.append(f"STANDARD.md:{rule.line}: {rule.rule_id} also at line {seen[rule.rule_id]}")
        seen[rule.rule_id] = rule.line
    for prev, rule in pairwise(rules):
        if rule.key <= prev.key:
            failures.append(f"STANDARD.md:{rule.line}: {rule.rule_id} comes after {prev.rule_id}")
    failures.extend(f"STANDARD.md: released rule {rid} is missing; withdraw it, never remove it"
                    for rid in released if rid not in seen)
    return failures


def version_of(lines: Sequence[str]) -> str:
    """The release the version line names, `v2.0.4` for `Version 2.0.4, 2026-11-02`; empty without one."""
    return next((line.split(",")[0].replace("Version ", "v") for line in lines if line.startswith("Version ")), "")


def render(rules: Sequence[Rule], version: str) -> str:
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
    for rule in rules:
        cells = [rule.rule_id, rule.title, rule.scope, rule.klass, rule.checks, rule.finding]
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    return "\n".join(out) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    """Checks the standard under the root; writes its index, or with `--check` compares it. Returns the exit code."""
    parser = argparse.ArgumentParser(description="Check STANDARD.md and write RULES.md, its one-table index.")
    parser.add_argument("--check", action="store_true", help="also check RULES.md is up to date; write nothing")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                        help="the repository root holding STANDARD.md (default: the parent of tools/)")
    args = parser.parse_args(argv)
    index = args.root / "RULES.md"
    lines = (args.root / "STANDARD.md").read_text(encoding="utf-8").splitlines()
    released = (args.root / "tools" / "released-ids.txt").read_text(encoding="utf-8").split()
    rules, failures = parse(lines)
    failures += check(rules, released)
    text = render(rules, version_of(lines))
    if args.check:
        if not index.exists() or index.read_text(encoding="utf-8") != text:
            failures.append("RULES.md: out of date; run tools/rules.py")
    elif not failures:
        index.write_text(text, encoding="utf-8")
    for failure in failures:
        print(failure, file=sys.stderr)
    print(f"{len(rules)} rules, {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
