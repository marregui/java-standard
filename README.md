# Java Coding Standard

One standard for how Java is written, changed and reviewed, for coding agents (Claude, Codex) first and for the
engineers who own the code. Every rule has an ID (`G-<section>.<n>`), a scope, the principles it follows from, how it
is checked, whether a violation is a defect or a rule, and what counts as a finding.

| File | Holds |
|---|---|
| [`STANDARD.md`](STANDARD.md) | How to read a rule, how agents apply the standard, the principles (§0) and the rules (§1–§16) |
| [`RULES.md`](RULES.md) | Every rule in one table, generated from `STANDARD.md`; the file an agent loads first |
| [`config/checkstyle/checkstyle.xml`](config/checkstyle/checkstyle.xml) | The checks javac cannot make (G-10.2, G-10.8, G-10.11); a repository copies the file of the tag it follows and sets `projectPackagePattern` from its Apply section |
| [`CHANGELOG.md`](CHANGELOG.md) | What each version changed |
| [`tools/rules.py`](tools/rules.py) | Checks every rule block and regenerates `RULES.md`; CI runs `tools/rules.py --check` |

## Following it in a repository

1. Pick a tag (`vX.Y.Z`) and link it.
2. Write the repository's Apply section (§12): version and JDK, hot paths with their measurement, what is applied and
   how it is enforced, departures kept on purpose, what is not applied yet, project packages, preview features.
3. Point the repository's `AGENTS.md` and `CLAUDE.md` at the tag and the Apply section, so agents read both before
   they write code.

## Disputing a rule

Open an issue titled `G-<section>.<n>: <the claim>` with the evidence: code, a measurement, or a case the rule gets
wrong. A rule changes by pull request. A changed rule is a major version, a new or withdrawn rule a minor one, a wording
fix a patch. IDs are never renumbered or reused.

The standard stays standalone: every example is original, and it names no codebase it was distilled from and no
repository that applies it.

Licensed under the Apache License 2.0.
