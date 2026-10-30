# Java Coding Standard

One coding standard for Java, applied by several repositories. [`STANDARD.md`](STANDARD.md) holds the rules,
each with an ID (`G-<section>.<n>`) that code, comments and reviews cite. IDs are never renumbered or reused.

| File | Holds |
|---|---|
| [`STANDARD.md`](STANDARD.md) | The rules, their scope (everywhere, hot path, *skip unless*) and how a repository applies them (§12) |
| [`config/checkstyle/checkstyle.xml`](config/checkstyle/checkstyle.xml) | The Checkstyle rules the build enforces; a repository's build copies the file of the tag it follows |
| [`CHANGELOG.md`](CHANGELOG.md) | What each version changed |

A repository follows a tagged version and keeps an Apply section of its own (§12): the version, its hot paths, what it
applied, its departures kept on purpose, and what it has not applied. The rules live here and nowhere else; an Apply
section cites them by ID and does not restate them.

The standard stays standalone: every example is original, and it names no codebase it was distilled from and no
repository that applies it.

Versions are tags `vX.Y.Z`: a new or withdrawn rule is a minor version, a changed rule a major one, a wording fix a
patch.

Licensed under the Apache License 2.0.
