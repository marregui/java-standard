# Changelog

## 2.0.0 (2026-10-30)

- Written for coding agents first: every rule is one block with its scope, the principles it follows from, how it is
  checked (build, test, measure, review), its class (*defect* blocks a merge on changed lines and where the change
  makes it reachable; *rule* blocks only on changed lines) and a Finding line that says what counts as a violation. `RULES.md`, generated from the standard and
  checked by CI, lists every rule in one table.
- Front matter: how to read a rule, a closed list of scopes with a table of *skip unless* conditions, how agents apply
  the standard (load order, a repository without an Apply section, precedence, changed lines, sweeps, reporting),
  how to dispute a rule.
- §0 Principles P1–P7, from which the rules follow and which decide where no rule applies.
- New sections: §13 Changing existing code (G-13.1–G-13.12), §14 Observability (G-14.1–G-14.11), §15 Distributed
  systems (G-15.1–G-15.13), §16 Current Java on the JDK 25 baseline (G-16.1–G-16.12). New rules in existing sections:
  G-5.7 (no meaning from message text), G-7.12 (locks never assumed reentrant or held across callbacks), G-7.13
  (`volatile` fields name their threads).
- §12 adds the JDK version, preview features, doc-comment form, nullability library, licence header, logging, test
  framework, subsystem entry points, configuration type and latency budgets to a repository's Apply section.
- Changed rules (IDs unchanged): G-1.5 mixes keys before masking; G-1.7 fails instead of returning less capacity;
  G-2.2 folds case only for letters; G-2.5 allows the `-ea` swap only where the pool's tests also run with `-da`; G-3.6 `@Transient` renamed
  `@NotRetained`; G-4.2 closes through a method no subclass overrides; G-4.3 never drops an `Error` from cleanup and
  keeps a writer's close failure an `IOException`; G-4.7 allocates from an `Arena`; G-5.1 example captures a trace
  only under `-ea` and passes the `serial` lint; G-6.1–G-6.4 apply only with a hot-path logger of the repository's
  own; G-7.2 uses `VarHandle` only and names the store-load handshake; G-7.3 pads 128 bytes; G-7.7 says how to wake
  I/O; G-7.8 applies to hot paths and prefers snapshots and optimistic reads; G-10.1 keeps order where initialisers
  depend on it; G-10.5 test methods are named for the behaviour, not `testXxx`; G-10.7 exempts non-capturing lambdas;
  G-10.8 wraps only signatures over the line limit the Apply section names; G-10.10 runs doclint without `missing`; G-14.1 is off hot paths;
  G-15.1 propagates deadlines; G-15.7 requires a fencing token; G-15.9 is compatible in both directions. Findings
  of many rules narrowed so they can be decided at the site. Examples follow the everywhere rules.
- Conformance: a rule *not applied yet* is not waived; G-12.1 requires an Apply section (site: the repository root);
  defaults hold where the Apply section gives no value.
- One class per rule: mixed rules split into G-1.11 (`keyIndex` after a mutation), G-4.8 (`free` helper), G-7.14
  (thread names), G-14.12 (stall measurement), G-14.13 (time units), G-15.14 (stated delivery semantics), G-16.13
  (virtual threads bounded before creation, permits released).
- Concurrency: G-7.2 requires an acquire read of a release-published reference; G-7.6 a predicate loop around every
  wait; G-7.7 a visible halt flag written before the wake-up; G-16.4 moves blocking file I/O off virtual threads
  (measured: no carrier compensation on Temurin 25); G-16.5 shows how to rebind a scoped value in a task.
- Contracts: G-2.1's `Window` honours `CharSequence`; G-5.1's exception overrides `getMessage()`; G-10.6 allows a
  default only where it is correct for every implementation; G-4.3 defines a writer's close failure on both paths;
  G-4.7 and G-16.9 share one policy for GC-freed native memory; G-16.6 applies to `java.util` collections.
- Consistency: every title states its rule in one line; section scope summaries match their rules; claims about which
  tool checks a rule match the tools (`config/checkstyle/checkstyle.xml` now checks G-10.2, G-10.8 and G-10.11, tested
  with Checkstyle 14.3.0; a missing `@Override` is left to review or Error Prone).
- Static imports go last (G-10.11), for every repository; test methods are named for the behaviour they prove (G-10.5).

## 1.0.0 (2026-10-30)

- The rules of the high-throughput guidelines of 2026-09-21, IDs unchanged, each section with its scope: everywhere,
  hot path, or *skip unless*.
- New rules: G-6.5 (`System.Logger` off the hot path), G-7.10 (threads have an owner, a name and a kind), G-7.11
  (nothing blocks a thread that owns latency), G-10.9 (no tool or review finding named in code), G-10.10 (warnings are
  errors, doclint), G-10.11 (single-type imports in three groups: JDK, third-party, project; checked by the build), G-10.12 (a number says where it came from),
  G-11.7 (`///` test documentation), G-11.8 (tests never touch the user's data).
- §12 replaced by how a repository applies the standard.
