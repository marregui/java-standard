# Changelog

## 1.0.0 (2026-10-30)

- The rules of the high-throughput guidelines of 2026-09-21, IDs unchanged, each section with its scope: everywhere,
  hot path, or *skip unless*.
- New rules: G-6.5 (`System.Logger` off the hot path), G-7.10 (threads have an owner, a name and a kind), G-7.11
  (nothing blocks a thread that owns latency), G-10.9 (no tool or review finding named in code), G-10.10 (warnings are
  errors, doclint), G-10.11 (single-type imports in three groups: JDK, third-party, project; checked by the build), G-10.12 (a number says where it came from),
  G-11.7 (`///` test documentation), G-11.8 (tests never touch the user's data).
- §12 replaced by how a repository applies the standard.
