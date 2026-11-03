#!/usr/bin/env python3
"""Tests of rules.py on small standards written to temporary repository roots.

usage: python3 -I tools/test_rules.py   (exit 0 when every test passes, 1 otherwise)
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("rules", HERE / "rules.py")
rules = importlib.util.module_from_spec(SPEC)
sys.modules["rules"] = rules
SPEC.loader.exec_module(rules)

HEAD = """# Standard

Version 9.9.1, 2026-11-03

| Condition (*skip unless*) | Meaning |
|---|---|
| native memory, native code | the code holds memory outside the heap |

"""

FIRST = """### G-1.1 First rule

**Scope:** everywhere · **From:** P1 · **Checked by:** build · **Class:** rule

**Finding:** A thing that
wraps onto a second line.
"""

SECOND = """### G-1.2 Second rule

**Scope:** skip unless native code · **From:** P2, P3 · **Checked by:** review, test · **Class:** defect

**Finding:** A cell with a | pipe.
"""

WITHDRAWN = """### G-1.3 Gone rule

*Withdrawn in 2.0.0: merged into G-1.1.*
"""

FENCED = """```markdown
### G-0.1 An example heading inside fenced code
```
"""


class RulesTest(unittest.TestCase):
    """rules.main: checks a standard, writes its index, and compares it with --check."""

    def root(self, standard: str, released: str = "G-1.1\n") -> Path:
        """A repository root holding `standard` as STANDARD.md and `released` as the released IDs."""
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / "tools").mkdir()
        (root / "STANDARD.md").write_text(standard, encoding="utf-8")
        (root / "tools" / "released-ids.txt").write_text(released, encoding="utf-8")
        return root

    def run_main(self, *argv: str) -> tuple[int, str, str]:
        """The exit code, stdout and stderr of one run."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = rules.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_writes_one_row_per_rule_and_then_checks_clean(self) -> None:
        root = self.root(HEAD + FENCED + FIRST + "\n" + SECOND + "\n" + WITHDRAWN)

        code, out, err = self.run_main("--root", str(root))
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, "3 rules, 0 failure(s)\n")
        index = (root / "RULES.md").read_text(encoding="utf-8")
        self.assertIn("[`STANDARD.md`](STANDARD.md) v9.9.1 by", index)
        rows = [line for line in index.splitlines() if line.startswith("| G-")]
        self.assertEqual(rows, [
            "| G-1.1 | First rule | everywhere | rule | build | A thing that wraps onto a second line. |",
            "| G-1.2 | Second rule | skip unless native code | defect | review, test | A cell with a \\| pipe. |",
            "| G-1.3 | Gone rule | withdrawn |  |  | Withdrawn in 2.0.0: merged into G-1.1. |",
        ])
        self.assertEqual(self.run_main("--root", str(root), "--check")[0], 0)

    def test_check_reports_a_stale_index_and_writes_nothing(self) -> None:
        root = self.root(HEAD + FIRST)
        (root / "RULES.md").write_text("stale\n", encoding="utf-8")

        code, _, err = self.run_main("--root", str(root), "--check")
        self.assertEqual(code, 1)
        self.assertEqual(err, "RULES.md: out of date; run tools/rules.py\n")
        self.assertEqual((root / "RULES.md").read_text(encoding="utf-8"), "stale\n")

    def test_each_broken_standard_fails_with_its_line_and_writes_no_index(self) -> None:
        cases = [
            ("duplicate id", HEAD + FIRST + "\n" + FIRST, "G-1.1",
             "STANDARD.md:16: G-1.1 also at line 9"),
            ("out of order", HEAD + SECOND + "\n" + FIRST, "",
             "STANDARD.md:15: G-1.1 comes after G-1.2"),
            ("released id missing", HEAD + FIRST, "G-1.1 G-1.9",
             "STANDARD.md: released rule G-1.9 is missing; withdraw it, never remove it"),
            ("unknown class", HEAD + FIRST.replace("**Class:** rule", "**Class:** hint"), "G-1.1",
             "STANDARD.md:9: G-1.1 has an unknown class 'hint'"),
            ("unknown scope", HEAD + FIRST.replace("everywhere", "skip unless tuesday"), "G-1.1",
             "STANDARD.md:9: G-1.1 has an unknown scope 'skip unless tuesday'"),
            ("unknown principle", HEAD + FIRST.replace("**From:** P1", "**From:** P1, P8"), "G-1.1",
             "STANDARD.md:9: G-1.1 names an unknown principle in 'P1, P8'"),
            ("unknown check", HEAD + FIRST.replace("**Checked by:** build", "**Checked by:** build, hope"), "G-1.1",
             "STANDARD.md:9: G-1.1 has an unknown check in 'build, hope'"),
            ("no Scope line", HEAD + "### G-1.1 First rule\n\nJust prose.\n", "G-1.1",
             "STANDARD.md:9: G-1.1 has no Scope · From · Checked by · Class line"),
            ("no Finding line", HEAD + FIRST.replace("**Finding:** ", "Found: "), "G-1.1",
             "STANDARD.md:9: G-1.1 has no Finding line after its Scope line"),
        ]
        for name, standard, released, failure in cases:
            with self.subTest(name):
                root = self.root(standard, released)
                code, out, err = self.run_main("--root", str(root))
                self.assertEqual(code, 1)
                self.assertIn(failure + "\n", err)
                self.assertRegex(out, r"^\d+ rules, [1-9]\d* failure\(s\)\n$")
                self.assertFalse((root / "RULES.md").exists())


if __name__ == "__main__":
    unittest.main()
