# Working on this repository

This repository is the Java Coding Standard itself. When asked to apply the standard to code in another repository,
read that repository's Apply section and `RULES.md`, then the blocks of the rules that touch the code, as
`STANDARD.md` "How agents apply this standard" says.

When editing the standard:

- Every rule is one block in the format of `STANDARD.md` "How to read a rule": heading `### G-<section>.<n> <title>`,
  then the `**Scope:** · **From:** · **Checked by:**` line, then the `**Finding:**` line, then the detail.
- Never renumber, reuse or delete an ID. A withdrawn rule keeps its heading, and its first line reads
  `*Withdrawn in <version>: <reason>*`. Released IDs are listed in `tools/released-ids.txt`; add the new ones when a
  version is tagged.
- Examples are original. Name no codebase the rules were distilled from and no repository that applies them.
- After any edit run `python3 tools/rules.py`, which checks every block and regenerates `RULES.md`; commit both files.
- Record the change in `CHANGELOG.md` under the next version: a changed rule is major, a new or withdrawn rule minor, a
  wording fix a patch.
