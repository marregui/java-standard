# Java Coding Standard

Version 2.0.1, 2026-10-30. JDK 25 baseline.

This standard says how Java is written, changed and judged in the repositories that follow it. Its first readers are
coding agents (Claude, Codex) that write, change and review code; its second readers are the engineers who own that
code and who will dispute it. Every rule is written so that an agent can apply it without guessing and a human can
check why it exists.

The standard stays standalone: every example is original, and it names no codebase it was distilled from and no
repository that applies it.

## How to read a rule

Each rule is one block:

```text
### G-<section>.<n> <the rule, stated in one line>

**Scope:** <scope> · **From:** <principles> · **Checked by:** <build, test, measure, review> · **Class:** <defect | rule>

**Finding:** <what, found in code, violates the rule>

<why, the detail, and an original example>
```

- **ID.** `G-<section>.<n>`. IDs are never renumbered or reused; a withdrawn rule keeps its heading and says
  *Withdrawn in <version>* with the reason. Cite rules by ID in reviews, commit messages and, where a choice would
  otherwise surprise the reader, in a comment.
- **Scope.** One of four values. *Everywhere*: every module and every thread, tests included. *Everywhere except hot
  path*. *Hot path*: code that runs per event, per row, per message or per frame at rates where an allocation, a boxed
  value, a lock or a megamorphic call shows in a profile; each repository names its hot paths in its Apply section
  (§12), from a measurement, and no other code is hot path. *Skip unless <condition>*: the rule applies only where one
  of the conditions in the table below holds. A section's opening line summarises the scopes of its rules; the rule's
  own Scope line decides.
- **From.** The principles of §0 the rule follows from. When a case is not covered by any rule, the principles decide.
- **Checked by.** *build*: the compiler, Checkstyle or doclint fails the build. *test*: a test or a checker run by CI.
  *measure*: a benchmark or a profile decides. *review*: a reader decides, using the Finding line.
- **Class.** *Defect*: a violation causes a wrong result, a leak, a hang, data loss or a security exposure; it blocks a
  merge on changed lines and wherever the change makes it reachable, and one found elsewhere is reported with its site
  (G-13.3) without blocking. *Rule*: a violation costs readability, cost or consistency; it blocks only on changed
  lines. Where a Finding lists several clauses, the class applies to the clauses that meet its definition; the others
  are class *rule*.
- **Finding.** The condition that makes a site a violation. A site that does not meet it is not a finding, however it
  looks. When writing code, the whole block binds; when reviewing, only the Finding line does.

| Condition (*skip unless*) | Holds where |
|---|---|
| native memory | the code allocates memory outside the Java heap |
| worker pool | the code starts a pool of threads that runs jobs from a queue it owns, on a named hot path |
| resumable I/O | the code parks a request on a socket and resumes it later from a state field |
| incremental parser | the code parses input that arrives in pieces, keeping its position between calls |
| pooled contexts | the code reuses per-connection or per-request context objects from a pool |
| configuration interface | the repository's Apply section names a configuration type of its own |
| hot-path logger | the Apply section names an asynchronous logger of the repository's own for hot paths |
| tracked resources, facades, assertion builder | the repository has the test harness the rule names |
| long-running service | the code runs as a process that stays up and is operated (a server, a daemon, a desktop application) |
| remote calls | the code calls another process over a network |
| messaging | the code produces or consumes messages through a queue, broker or log |
| shared state across nodes | more than one process acts on the same data and one of them must act alone |
| persisted or wire formats | the code writes data another process or a later version reads |
| batch or fan-out calls | one call acts on several items or several peers |
| native code | the code calls native functions |
| latency budget | the Apply section gives the operation a latency budget, or it runs on a hot path |

[`RULES.md`](RULES.md) lists every rule in one table (ID, title, scope, class, check, finding), generated from this file and
checked by CI. Load it first; read a rule's full block before applying it or reporting against it.

## How agents apply this standard

1. **Read the repository's Apply section first** (§12). It names the version followed, the hot paths, the departures
   kept on purpose and what is not applied yet. A site that follows a recorded departure from a rule of class *rule* is
   not a finding, and code written there follows the departure; a departure from a rule of class *defect* does not
   clear a finding (step 4). A rule listed as *not applied yet* is not waived: the entry records the plan, and findings
   against it are still reported. **A repository with no Apply section**: apply the rules scoped *everywhere* and
   *everywhere except hot path*, and the *skip unless* rules whose condition the code shows on its own; treat no code
   as hot path; report the missing Apply section once, as the first finding.
2. **Read before writing** (G-13.1). Read the class, its package, its callers and the module's shared helpers before
   adding code. Reuse what exists; follow the idiom the surrounding code uses for the same concept (G-13.2).
3. **Decide the scope of the code at hand.** Hot-path rules apply only to the hot paths the Apply section names. When
   code looks hot but is not named, apply the everywhere rules, and say in the report which measurement would decide.
4. **Precedence when rules pull apart.** Rules of class *defect* first; then the repository's recorded departures; then
   the other rules of this standard, where on a named hot path a hot-path rule wins over an everywhere rule and
   otherwise the narrower scope wins; then the surrounding code's idiom; then taste. A rule never justifies a change
   that breaks behaviour, a test or a public contract; where a rewrite a rule suggests could change behaviour (an
   exception type, mutability, null handling), it is made only where every caller is in the change.
5. **New code follows the standard; changed lines follow it unless G-13.2 keeps the file's idiom.** *Changed lines*
   are the lines a diff adds or modifies; context lines are not. A new file or a new type follows the standard. An
   improvement outside the changed lines needs the evidence G-13.3 asks for, and goes into its own commit.
6. **Sweeps over existing code are mechanical** (G-13.9). Adding `final` (G-10.2), reordering imports (G-10.11) and
   similar changes to lines the task does not otherwise change are made by a tool, proven by the build and committed
   alone. New and changed lines are written to the rule directly.
7. **Report against the Finding line, with evidence.** A finding names the rule ID, its class, the site as `path:line`,
   the failure sequence or the cost it causes, and the change that resolves it. No finding without a site; a finding
   about the repository as a whole (G-12.1) names the repository root as its site. A concern
   no rule covers may cite a principle; it never blocks a merge and is reported once per change, not per site.
8. **Never claim a check you did not run.** "Builds", "tests pass", "faster" and "no allocation" are claims; each one
   names the command or the measurement that showed it.
9. **When a rule does not fit, say so instead of bending the code.** Name the rule and the reason, and propose a
   departure for the Apply section or a change to this standard.
10. **Examples are idiom.** Every example in this standard follows the rules scoped everywhere; an example that does
    not is a defect of the standard, to be reported as an issue, not copied.

## How to dispute a rule

Open an issue titled `G-<section>.<n>: <the claim>` with the evidence: code, a measurement, or a case the rule gets
wrong. A rule changes by a pull request that updates this file, `RULES.md` and `CHANGELOG.md`. A changed rule is a
major version, a new or withdrawn rule a minor one, a wording fix a patch. A rule two repositories depart from in the
same way is a candidate to change here.

---

## 0. Principles

The rules follow from these. When the rules are silent, an agent applies the principle and names it (step 7: such a concern never blocks).

**P1 The reader comes first.** Code is read far more often than it is written, by people and by agents that did not
write it. A reader should be able to tell from the code alone what it does, what it owns, what changes and why a
surprising choice was made. Names, `final`, small types and comments that say why exist for that reader.

**P2 First principles, with evidence.** A design follows from the constraint it serves (event rates, latency budgets,
data sizes, failure modes), measured, not from habit or fashion. Every threshold, capacity and timeout says what set
it. A claim about performance or behaviour carries the measurement or the test that shows it.

**P3 Correct first; fast where it is measured to matter.** Correctness is not traded. Speed is designed in where the
hot path is (data layout, allocation, contention) and not imposed elsewhere at the reader's expense; the hot-path rules
apply only where a measurement put them.

**P4 Respect existing code; leave it better when the gain is shown.** The code in place encodes decisions, some of
them recorded. A change follows its idiom, and improves what it touches only when the gain is demonstrated (a test, a
measurement, a removed duplicate or defect) and is worth the diff a reviewer has to read.

**P5 Optimise for the lifetime cost.** One idiom per concept, one owner per resource and thread, no duplication, no
surface nobody asked for. A design that is cheaper to change, review and operate for years beats one that is quicker
to write today.

**P6 Observable by design.** A system says what it is doing, how long it takes and where it waits, cheaply enough to
stay on in production: logs that tell an operation's whole story, metrics with a reader, bounds that show their usage,
events a profiler can read.

**P7 The language as it is today.** Current Java states intent better than older forms: closed hierarchies, records,
patterns, virtual threads, scoped values. Use them where they say more with less, within the hot-path rules, and not
as fashion.

---

## 1. Data on the hot path

*Scope:* hot path.

### G-1.1 Primitives, never boxes

**Scope:** hot path · **From:** P3 · **Checked by:** review · **Class:** rule

**Finding:** A boxed number (`Integer`, `Long`, `Double`) or an `Optional` as a field, parameter, return value or collection element on a hot path.

No `Integer`, `Long`, `Double` as fields,
parameters, return values or collection elements on any path that runs per
event, per row or per byte. Absence is a sentinel value, not `null` and not
`Optional`:

```java
public final class Nulls {
    public static final int INT_NULL = Integer.MIN_VALUE;
    public static final long LONG_NULL = Long.MIN_VALUE;
    public static final double DOUBLE_NULL = Double.NaN;

    private Nulls() {}

    // widening preserves nullness
    public static long intToLong(final int v) { return v == INT_NULL ? LONG_NULL : v; }
}
```

*For example:* a `long` nanosecond timestamp with `LONG_NULL` for "none" replaces
`Optional<Instant>`; a `Map<String, Long>` on a per-event path violates this rule.

### G-1.2 Two sentinel families, kept apart

**Scope:** hot path · **From:** P1, P3 · **Checked by:** review, test · **Class:** defect

**Finding:** One constant used both as a collection's "no entry" value and as the domain's null, or a `get()` on a collection whose payload can equal its no-entry value.

A collection's "no entry" value
(`-1` by default) and the domain's null (`MIN_VALUE`) are different constants
for different jobs. When `-1` is a legal payload the collection takes its
no-entry value in the constructor, or the caller uses the two-step
`keyIndex()` / `valueAt()` API (G-1.5) instead of `get()`:

```java
public LongList(final int capacity, final long noEntryValue) { ... }

public long getLastQuiet() {
    return pos > 0 ? data[pos - 1] : noEntryValue;
}
```

### G-1.3 Primitive-specialised collections, one class per key/value shape

**Scope:** hot path · **From:** P3 · **Checked by:** review · **Class:** rule

**Finding:** A `java.util` map, set or list of boxed values, or an iterator, on a hot path.

`IntList`, `LongList`, `IntIntHashMap`, `LongObjHashMap<V>`,
`CharSequenceObjHashMap<V>`, and so on. Storage is a flat `int[]` or `long[]`.
There is no `java.util.Map` on a hot path. Iteration is an indexed loop, never
an iterator:

```java
for (int i = 0, n = list.size(); i < n; i++) {
    consume(list.getQuick(i));
}
```

*For example:* a `HashMap<Long, ThreadState>` keyed by thread id becomes a
`LongObjHashMap<ThreadState>`; a `Map<String, Integer>` of class names becomes
a `CharSequenceIntHashMap`.

### G-1.4 An object list releases its references on `clear()` and `remove`

**Scope:** hot path · **From:** P3 · **Checked by:** review, test · **Class:** defect

**Finding:** An object list whose `clear()` or `remove` keeps references to released elements. (A `java.util` list on a hot path is G-1.3.)

`getQuick` is
unchecked, `remove` nulls the vacated slot, `clear()` nulls every slot so
references are released. Primitive lists do **not** zero on `clear()`, they
reset the position; if stale values matter, use `clear(int)` or fill explicitly.

```java
public final class ObjList<T> implements Mutable {
    private T[] buffer;
    private int pos;

    public void add(final T value) { checkCapacity(pos + 1); buffer[pos++] = value; }
    public T getQuick(final int index) { assert index < pos; return buffer[index]; }
    public int size() { return pos; }

    @Override
    public void clear() { Arrays.fill(buffer, 0, pos, null); pos = 0; }
}
```

### G-1.5 Hash maps use open addressing, a power-of-two table, mixed keys and backward-shift delete

**Scope:** hot path · **From:** P3 · **Checked by:** review, test · **Class:** rule

**Finding:** A get-then-put pair that hashes twice, tombstone deletion, a non-power-of-two table, or keys masked without mixing where the javadoc does not state the range is dense. (A `keyIndex` result used after a mutation is G-1.11.)

One probe returns both the answer and the
slot, so get-or-insert costs one hash and no entry object:

```java
public int keyIndex(final int key) {
    final int index = mix(key) & mask;
    if (keys[index] == noEntryKey) {
        return index;                                   // free slot: >= 0
    }
    if (keys[index] == key) {
        return -index - 1;                              // present:   <  0
    }
    return probe(key, index);
}

private int probe(final int key, int index) {
    while (true) {
        index = (index + 1) & mask;                     // no modulo
        if (keys[index] == noEntryKey) {
            return index;
        }
        if (keys[index] == key) {
            return -index - 1;
        }
    }
}

private static int mix(final int key) {
    final int h = key * 0x9E3779B9;                     // Fibonacci hashing
    return h ^ (h >>> 16);
}

// caller: one probe, no boxing, no Map.Entry
final int i = map.keyIndex(k);
if (i < 0) {
    map.valueAtQuick(i).increment();
} else {
    map.putAt(i, k, newCounter());
}
```

Capacity is rounded up to a power of two from `capacity / loadFactor`; load
factor 0.5 by default. A `free` counter is decremented on insert so the rehash
check is one comparison. Delete re-homes keys that were probed past the freed
slot instead of leaving tombstones. Keys are mixed before masking: object
hash codes with `h ^ (h >>> 16)`, `int` keys with a multiply and a shift as
above, `long` keys with a 64-bit multiply-xorshift, because masking keeps only
low bits and linear probing turns keys that share them (strided ids,
addresses) into one long cluster. Only a key range the map's javadoc states is
dense and sequential is masked directly. `contains(k)` is `keyIndex(k) < 0`; provide
`excludes(k)` because `!contains(k)` reads badly under the sign convention.
When iteration order matters keep a parallel `ObjList` of keys; do not reach
for a linked map.

**Rule:** a `keyIndex` result is valid only until the next mutation.

### G-1.6 `Quick` methods check with `assert` only, `get` throws, `Quiet` returns a sentinel

**Scope:** hot path · **From:** P1 · **Checked by:** review · **Class:** rule

**Finding:** A `Quick` method that checks at run time, or a method that skips its check without the `Quick` suffix.

`Quick` means the caller
has already proven the precondition and the method checks it with `assert`
only (nothing at runtime in production). `get` throws. `Quiet` returns the
sentinel instead of throwing (`getQuiet`, `parseIntQuiet`, `indexOfQuiet`).
Maps follow the same triad: `valueAt(i)` checks the sign, `valueAtQuick(i)`
does not.

Methods that share a name with a JDK collection method (`get`, `getFirst`, `getLast`) keep the
JDK's contract: they throw where the JDK throws.

### G-1.7 Growth doubles, guards against overflow, and never returns less than requested

**Scope:** hot path · **From:** P3 · **Checked by:** review, test · **Class:** defect

**Finding:** Doubling without an `int` overflow guard, or a growth method that returns less capacity than requested without failing.

`checkCapacity(n)` doubles with a floor at the
request; `setPos(n)` pre-sizes for index writes; `extendAndSet(i, v)` is the
sparse write. Guard against `int` overflow when doubling. Document that
`setPos` reveals uninitialised or stale slots.

```java
private static final int MAX_ARRAY_SIZE = Integer.MAX_VALUE - 8;   // the largest array size every JVM allocates

public void checkCapacity(final int capacity) {
    if (capacity < 0 || capacity > MAX_ARRAY_SIZE) {
        throw new IllegalArgumentException("capacity out of range [capacity=" + capacity + ", max=" + MAX_ARRAY_SIZE + "]");
    }
    final int len = data.length;
    if (capacity > len) {
        data = Arrays.copyOf(data, (int) Math.min(Math.max((long) len << 1, capacity), MAX_ARRAY_SIZE));
    }
}

public void extendAndSet(final int index, final long value) {
    if (index < 0 || index >= MAX_ARRAY_SIZE) {
        throw new IllegalArgumentException("index out of range [index=" + index + ", max=" + MAX_ARRAY_SIZE + "]");
    }
    checkCapacity(index + 1);
    if (index >= pos) {
        pos = index + 1;
    }
    data[index] = value;
}
```

### G-1.8 Flat records in primitive lists with slot-offset constants

**Scope:** hot path · **From:** P3 · **Checked by:** review, measure · **Class:** rule

**Finding:** A list of small records or objects, one per row, on a hot path whose measured allocation shows it, where a strided primitive list would do.

Instead
of an object per row, one `LongList` with a power-of-two stride and named
offsets. Packed handles (`(hi << 44) | lo`) and packed type tags
(`tagOf(type) = type & 0xFF`, flags in the upper bits) follow the same idea.

```java
// per-thread timeline: 4 longs per block
static final int SLOT_SIZE  = 4;              // power of two
static final int OFF_START  = 0;
static final int OFF_END    = 1;
static final int OFF_KIND   = 2;
static final int OFF_ID     = 3;

final long start = blocks.getQuick(i * SLOT_SIZE + OFF_START);
```

*For example:* a thread's `(startNanos, endNanos, kind, monitorId)` blocks are one
`LongList` with a 4-slot stride and an `int` kind, not a `List<Block>` of
records.

### G-1.9 Static lookup tables indexed by tag, not maps or enum switches

**Scope:** hot path · **From:** P3 · **Checked by:** review · **Class:** rule

**Finding:** A map, or a `switch` whose every arm only yields a constant, over a dense ordered tag range on a hot path, where a static array would be one load.

When
tags form a dense ordered range, a `static final` array filled in a `static {}`
block is one load per lookup:

```java
private static final int[] TAG_SIZE = new int[Tag.COUNT];
static {
    TAG_SIZE[Tag.BYTE] = 1;
    TAG_SIZE[Tag.INT]  = 4;
    TAG_SIZE[Tag.LONG] = 8;
}
```

State the invariant (dense, ordered, `COUNT` last) in a comment where the tags
are defined; other code depends on it.

### G-1.10 An `int` tag where a value is persisted, sent or switched on a hot path; an enum otherwise

**Scope:** hot path · **From:** P1, P3 · **Checked by:** review · **Class:** rule

**Finding:** An `int` tag with no `nameOf`, or booleans that together encode a kind. (An enum persisted or sent by ordinal is G-15.11.)

`int` when the value is persisted, sent on
a wire, or switched on a hot path; `enum` when in-memory only and carrying
behaviour or a label. Chain constants (`B = A + 1`) and provide `nameOf(int)`.
A bag of booleans that together encode a kind should become an enum so an
object cannot silently lose its kind. Use enhanced `switch` with arrows; a switch
over a dense `int` range compiles to a `tableswitch` (a jump table), a sparse one to a `lookupswitch`.

### G-1.11 A `keyIndex` result is used only until the next mutation

**Scope:** hot path · **From:** P3 · **Checked by:** review, test · **Class:** defect

**Finding:** A `keyIndex` (or slot) result used after any insert, remove or rehash of the same map.

An insert can rehash and a backward-shift delete moves keys, so the slot a `keyIndex` named may hold another key or
none. Take the index, use it, and take it again after any mutation.

---

## 2. Text and formatting

*Scope:* hot path. Final reporting (text, HTML or JSON written once at the end) is exempt, as G-2.3 says.

### G-2.1 `CharSequence` at API boundaries; `String` only for identity or storage

**Scope:** hot path · **From:** P3 · **Checked by:** review · **Class:** rule

**Finding:** A `String` created on a hot path to pass text between components that could take a `CharSequence` window, a stored `CharSequence` that is not copied and not named `...WithBorrowed`, or a `CharSequence` implementation that breaks the interface's contract (an unchecked index, a `subSequence` that throws).

A tokenizer hands out a reusable window over its input; the
consumer takes a snapshot window when it must keep a token, and copies only
when a token has to be *assembled* from parts. A collection that stores a
`CharSequence` copies it unless the method is explicitly named
`...WithBorrowed`, in which case the caller guarantees lifetime and
immutability.

```java
// reusable window over the input; re-pointed, never re-created
public final class Window implements CharSequence {
    private CharSequence base; private int lo, hi;
    public Window of(
            final CharSequence base,
            final int lo,
            final int hi
    ) {
        Objects.checkFromToIndex(lo, hi, base.length());   // intrinsic: one compare per bound
        this.base = base;
        this.lo = lo;
        this.hi = hi;
        return this;
    }
    @Override public int length() { return hi - lo; }
    @Override public char charAt(final int i) { return base.charAt(lo + Objects.checkIndex(i, hi - lo)); }
    @Override public CharSequence subSequence(final int s, final int e) {
        Objects.checkFromToIndex(s, e, hi - lo);
        return new Window().of(base, lo + s, lo + e);   // a new window: the caller may keep it
    }
}
```

### G-2.2 Keyword and name matching allocates nothing

**Scope:** hot path · **From:** P3 · **Checked by:** review · **Class:** rule

**Finding:** `toLowerCase`, `toUpperCase` or `subSequence` used to match names or keywords on a hot path, `equalsIgnoreCase` that forces a `toString()` of a `CharSequence`, or a `| 32` comparison against an expected character that is not a letter.

Length check first,
then per-char comparison; ASCII case folding with `| 32` is applied only where
the expected character is a letter (`'a'` to `'z'`), since `| 32` maps other
characters onto different ones (`'['` onto `'{'`). Never `toLowerCase()` or
`toUpperCase()`; `equalsIgnoreCase` only between two `String`s, never where it
forces a `toString()` of a `CharSequence`. Every comparison and parse helper
has a `(seq, lo, hi)` overload so callers avoid `subSequence`. Lookup maps hash
the raw `CharSequence` and support `keyIndex(seq, lo, hi)`.

```java
public static boolean isMonitorEnter(final CharSequence tok) {
    return tok.length() == 20
            && tok.charAt(0) == 'j' && tok.charAt(1) == 'd' && tok.charAt(2) == 'k' && tok.charAt(3) == '.'
            && (tok.charAt(4) | 32) == 'j' && (tok.charAt(5) | 32) == 'a'
            /* ... */;
}
```

*For example:* thread-name glob matching and event-type dispatch compare
`CharSequence` content, or resolve each event type to an `int` id once and
switch on the id.

### G-2.3 Numbers are formatted and parsed by hand into sinks

**Scope:** hot path · **From:** P3 · **Checked by:** review · **Class:** rule

**Finding:** Any conversion of a number to a new `String` on a hot path outside final reporting: `toString`, `valueOf`, concatenation, `format` or `formatted`, `StringBuilder.toString`, `DecimalFormat`, `MessageFormat`.

`append(sink,
int)` writes digits directly and prints the sentinel as `null`;
`parseInt(cs, lo, hi)` throws the reusable numeric exception (G-5.1);
`parseIntQuiet` returns the sentinel. No `Integer.toString`, `String.valueOf`,
`String.format`, `DecimalFormat` or `Duration.toString()` outside setup and
final reporting.

### G-2.4 A sink protocol is the printing contract; `toString()` is debug-only

**Scope:** hot path · **From:** P1, P3 · **Checked by:** review · **Class:** rule

**Finding:** A type that appears in reports or logs on a hot path and is printed through `toString()` or string concatenation instead of `toSink`.

A self-typed fluent `CharSink<T>` returns `this` from every `put`, and
`putAscii` skips encoding when the caller knows the input is ASCII. Anything
that appears in a report, a log line or an error implements
`toSink(CharSink)`; `toString()` delegates to a thread-local sink and caps its
output so a debugger does not hang on a large structure.

```java
public interface Sinkable { void toSink(CharSink<?> sink); }

public interface CharSink<T extends CharSink<?>> {
    T put(char c);
    T put(CharSequence cs);
    T putAscii(CharSequence cs);
    default T put(final int v)      { Numbers.append(this, v); return self(); }
    default T put(final long v)     { Numbers.append(this, v); return self(); }
    default T put(final Sinkable s) { if (s != null) { s.toSink(this); } return self(); }
    @SuppressWarnings("unchecked") default T self() { return (T) this; }
}
```

The thread-local sink is cleared on every acquisition: never hold it across a
call that may acquire it too.

*For example:* the text and HTML report writers stream into one reusable sink via
`toSink`; no per-row `String` concatenation.

### G-2.5 Under `-ea`, a pool may hand out a fresh instance with a stack trace; its tests also run with `-da`

**Scope:** hot path · **From:** P1 · **Checked by:** review, test · **Class:** rule

**Finding:** An `assert (x = …) != null` that swaps a pooled or reusable object under `-ea`, in a pool whose tests never also run with assertions disabled for its class (`-da:<class>`).

Assertions are on in tests and off in production. An assignment inside an
`assert` can therefore make the test build capture a stack trace that the
production build skips. Stack-trace capture is decided in the constructor
(`writableStackTrace`); overriding `getStackTrace()` changes neither what
`printStackTrace()` nor what a logger prints.

```java
public static ParseException at(final int position) {
    ParseException ex = TL.get();                              // the pooled instance, no stack trace
    assert (ex = new ParseException(true)) != null;            // under -ea: a fresh instance with a trace
    ex.reset(position);
    return ex;
}
```

The trick swaps the object under `-ea`, so the test build no longer exercises
the reuse the production build depends on: a message read after the next
`at(...)` on the same thread is intact in tests and overwritten in production
(G-5.1). Run the pool's own tests a second time with `-da:<class>` so the
production path is tested.

---

## 3. Object lifecycle and reuse

*Scope:* hot path.

### G-3.1 Allocate once, re-point with `of(...)`

**Scope:** hot path · **From:** P3 · **Checked by:** review, measure · **Class:** rule

**Finding:** A heavy object or cursor constructed per call on a hot path where re-pointing one instance with `of(...)` would do.

Heavy objects expose
`of(...)`, `init(...)` or `reopen()` that reset state and return `this`; the
constructor runs once. Flyweight views are re-pointed. A factory that produces
cursors or iterators reuses the same cursor instance across calls and
documents that callers must not hold a copy.

```java
public Cursor cursor(final Source src) {
    return cursor.of(src);        // same field every call
}
```

### G-3.2 `Mutable.clear()` resets logical state; `close()` releases resources

**Scope:** hot path · **From:** P1, P5 · **Checked by:** review, test · **Class:** rule

**Finding:** A `clear()` that leaves a field unreset, or a new field not added to `clear()` and the copy methods.

`clear()` must reset **every** field; put a comment on the constructor or the
field block reminding maintainers to extend `clear()` and any deep-copy method
when a field is added. A `QuietCloseable` narrows `close()` to not throw so
cleanup chains need no try/catch:

```java
public interface Mutable { void clear(); }

public interface QuietCloseable extends Closeable {
    @Override void close();       // no IOException
}
```

### G-3.3 Pooled objects come from an `ObjectPool` that clears each object it hands out

**Scope:** hot path · **From:** P3 · **Checked by:** review, test · **Class:** defect

**Finding:** A pooled object handed out without `clear()`, released twice, or kept after the pool was cleared.

`next()` clears the object
it hands out; mass release is `pool.clear()` in O(1). Individual release is
O(n) and reserved for exceptional cases. A parser owns one pool per node type
and `parse()` starts by clearing all of them.

```java
public final class ObjectPool<T extends Mutable> implements Mutable {
    private final ObjList<T> list = new ObjList<>();
    private final Supplier<T> factory;
    private int pos;

    public T next() {
        if (pos == list.size()) {
            list.add(factory.get());
        }
        final T o = list.getQuick(pos++);
        o.clear();
        return o;
    }

    @Override public void clear() { pos = 0; }
}
```

Thread-local scratch follows the same shape: a `ThreadLocal<StringSink>`
initialised with `StringSink::new`, and `acquire()` / `release()` paired in
`finally` when re-entrancy is possible.

*For example:* per-event stack and frame model objects are pool candidates; per-query
scratch collections are cleared, never re-`new`ed.

### G-3.4 Flyweight records: a moving window, not a value

**Scope:** hot path · **From:** P1 · **Checked by:** review, test · **Class:** defect

**Finding:** A value obtained from a flyweight record kept past the next `hasNext()` without a copy.

One record instance
is reused across rows; `hasNext()` both tests and advances; `toTop()` is cheap
and does not discard cached state; nothing obtained from the record (including
a `CharSequence`) survives the next `hasNext()` unless copied into a sink. When
two values from the same record are compared, use A/B accessor pairs with one
flyweight per column, so reading column 2 does not invalidate column 1.

### G-3.5 Factories are reusable, cursors are per execution, and capability flags default to the safe answer

**Scope:** hot path · **From:** P1, P3 · **Checked by:** review · **Class:** rule

**Finding:** A capability flag whose default is unsafe for the question it answers, or one property used for both optimisation safety and semantic legality.

A factory is built once and executed many times.
Capability flags are boolean `default` methods. A flag consulted for
*optimisation safety* defaults to the unsafe-to-optimise answer; a flag
consulted for *semantic legality* defaults to permissive. The two questions
have opposite safe defaults, so they must never share one property.

### G-3.6 Mark non-retained parameters with `@NotRetained`

**Scope:** hot path · **From:** P1 · **Checked by:** review · **Class:** defect

**Finding:** A callee that keeps a reference to a parameter marked `@NotRetained`, or a caller that reuses a flyweight after passing it to a project method not marked `@NotRetained`, or to a library method whose documentation says it keeps the reference.

A source-retention `@NotRetained`
annotation of the project's own on a parameter means "this method does not keep a
reference"; the caller may reuse the pooled or flyweight argument immediately. Its
absence on a project method's parameter that takes a flyweight signals that the
callee retains it and the caller must pass an owned copy. (`java.beans.Transient`
is a different, method-only annotation; the name avoids it.)

```java
@Retention(RetentionPolicy.SOURCE)
@Target({ElementType.PARAMETER, ElementType.METHOD})
public @interface NotRetained {}

void addFrame(@NotRetained CharSequence className, int line);   // copies className
```

### G-3.7 A null object instead of a null reference on data paths

**Scope:** hot path · **From:** P3 · **Checked by:** review · **Class:** rule

**Finding:** A `null` check inside a per-row or per-event loop that a null object would remove.

A
`NullSource.INSTANCE` that answers every read with the type's sentinel; column
or slot arrays pre-filled with it; a `NOOP_ROW` instead of a `null` row; a
`NullLogRecord.INSTANCE` when the log queue is full. Callers never test for
`null` in the loop.

---

## 4. Resource ownership and cleanup

*Scope:* everywhere; G-4.7 *skip unless* the code uses native memory.

### G-4.1 Every `close()` is idempotent and safe on a half-built object

**Scope:** everywhere · **From:** P5 · **Checked by:** review, test · **Class:** defect

**Finding:** A `close()` that is not idempotent, throws on a half-built object, or sets its closed flag after the real close.

Key
it on an is-open sentinel (`handle != 0`, `buffer != null`) or on a boolean
that is set **before** the real close runs, so a throwing close cannot be
re-entered by a second owner:

```java
@Override
public final void close() {
    if (!closed) {
        closed = true;      // flip first
        doClose();
    }
}
```

### G-4.2 Constructors that acquire resources roll back on failure

**Scope:** everywhere · **From:** P5 · **Checked by:** review, test · **Class:** defect

**Finding:** A constructor that acquires a resource and leaks it when a later step throws.

Assign
non-owning fields (configuration, clock, facades) before the `try`; acquire
owning fields inside it; on any throwable call a close that no subclass can
override (`close()` of a `final` class, or a `private` method) and rethrow
(G-9.5).

```java
public final class Reader implements Closeable {
    public Reader(final Config cfg) {
        this.cfg = cfg;
        try {
            this.index = new IndexBuffer(cfg.indexSize());
            this.input = cfg.files().open(cfg.path());
        } catch (final Throwable e) {
            close();        // final class: idempotent, null-tolerant, not overridable
            throw e;
        }
    }
}
```

### G-4.3 Cleanup attempts every resource and drops no failure

**Scope:** everywhere · **From:** P1, P5 · **Checked by:** review · **Class:** defect

**Finding:** A multi-resource cleanup that stops at the first failure, a cleanup failure dropped, or a writer whose close failure on the success path does not reach the data's owner as an `IOException`.

Never `if (x != null) x.close()`. A list variant nulls each slot.
A best-effort variant threads a failure chain so **every** resource is
attempted and later failures are added as suppressed to the first:

```java
public static <T extends Closeable> T free(final T o) {
    if (o != null) {
        try { o.close(); } catch (final IOException e) { throw new FatalError(e); }
    }
    return null;
}

public static Throwable freeBestEffort(final Throwable primary, final Closeable o) {
    try {
        free(o);
    } catch (final Throwable t) {
        if (primary == null) {
            return t;
        }
        if (t instanceof Error) {
            t.addSuppressed(primary);       // an Error from cleanup wins and carries the primary
            return t;
        }
        primary.addSuppressed(t);
    }
    return primary;
}
```

A failure in `close()` of a reader or a native handle is not control flow; it
becomes an `Error`. A failure in `close()` of a writer is a failed final write:
it reaches the owner of the data as an `IOException`. `free` is for readers and
native handles; a writer is closed by try-with-resources, or by a `freeWriter`
that rethrows the `IOException` to the data's owner. A primary with suppression
disabled (a reusable exception, G-5.1) cannot carry a cleanup failure: the
cleanup failure propagates and the primary's message is logged first.

A writer's data is complete only if its `close()` succeeds. On the success path the close runs as the last step of
the `try` block (or try-with-resources ends normally), so its `IOException` is the result the owner sees. On a
failure path the body's exception is primary and the close failure is suppressed into it: the data is already known
to be incomplete, and the primary says why.

### G-4.4 Detach, then free

**Scope:** everywhere · **From:** P5 · **Checked by:** review · **Class:** defect

**Finding:** A close that frees owned resources while the fields still reference them.

In the real close, copy owned references to
locals, null the fields, then close the locals. A re-entrant close then finds
nothing to do:

```java
private void doClose() {
    final Cursor c = cursor;   cursor = null;
    final Filter f = filter;   filter = null;
    Throwable failure = freeBestEffort(null, c);
    failure = freeBestEffort(failure, f);
    rethrow(failure);
}
```

### G-4.5 Ownership is a tree

**Scope:** everywhere · **From:** P5 · **Checked by:** review · **Class:** defect

**Finding:** An owner that does not close what it built on a failure, or a child closed by two owners.

Composites forward `init`, `close` and `toTop`
to children through interface `default` methods; leaves do nothing. Whoever
builds a partial tree tears it down on failure; a builder that folds a subtree
into a constant closes the subtree it replaced.

### G-4.6 An `Error` poisons an object; a `RuntimeException` leaves it usable

**Scope:** everywhere · **From:** P5 · **Checked by:** review, test · **Class:** defect

**Finding:** An object that stays usable after an `Error` left it half-written.

A `RuntimeException` means the object is
still usable. An `Error` subtype means the object is dead: it sets a
`distressed` flag, refuses further use, and must be closed and reopened. A
half-written row (open-row parity bit set) or a failed rollback poisons the
writer.

### G-4.7 Native memory has an owner, a tag and a size

**Scope:** skip unless native memory · **From:** P5 · **Checked by:** review, test · **Class:** defect

**Finding:** Native memory allocated per operation that is freed by the GC (`Arena.ofAuto()`, a direct or mapped `ByteBuffer`) rather than by a confined arena, native memory from a native allocator or `Unsafe` outside an `Arena`, an arena without a tag or byte count, an address cached across a reallocation, or a length read from a file dereferenced before a range check.

Native memory comes from an `Arena` (G-16.9): a confined arena per owner, or
a shared one that lives as long as its owner, closed per G-4.5. Memory the GC
frees (`Arena.ofAuto()`, direct and mapped `ByteBuffer`s) is one category with
one policy: allowed for long-lived buffers allocated at setup, never per
operation, because its release waits for a collection the code does not
control. Each arena
carries a tag and counts its bytes, so a leak report names the subsystem. An
address or segment is never cached across a reallocation. Fixed-width reads are
assert-guarded, but any length read from a file is range-checked before
dereference, because an out-of-bounds native read crashes the process.

### G-4.8 Cleanup goes through the module's `free` helper

**Scope:** everywhere · **From:** P1, P5 · **Checked by:** review · **Class:** rule

**Finding:** A null-guarded `close()` written inline (in any form: `if (x != null)`, `Optional.ofNullable(x).ifPresent(...)`, `Objects.nonNull`) where the module has a `free` helper for that kind of resource.

One idiom for one concept (G-13.2): a reader sees `x = free(x)` and knows the field is closed, nulled and its failure
handled the module's way.

---

## 5. Errors

*Scope:* everywhere, except G-5.1 and G-5.2, which are hot path.

### G-5.1 Exceptions are reusable, message-building and stack-trace-free

**Scope:** hot path · **From:** P3 · **Checked by:** review, measure · **Class:** rule

**Finding:** A new exception with a stack trace created per event on a hot path, a reusable exception's message read after the next call to its factory on the same thread, or a reusable exception whose `getMessage()` does not return the message it built.

One
instance per thread from a `ThreadLocal`; its factory (`at(...)`) clears the owned sink;
the message is built with `put(...)` overloads for `CharSequence`, `char`,
`int`, `long`, `double` and `Sinkable` — never `Object`, never
`String.format`. The constructor captures no stack trace unless assertions
are on (G-2.5). Pure control-flow signals are `static final INSTANCE` with a private
constructor.

```java
public final class ParseException extends RuntimeException implements Sinkable {
    @Serial
    private static final long serialVersionUID = 1L;
    private static final ThreadLocal<ParseException> TL = ThreadLocal.withInitial(() -> new ParseException(false));
    private final transient StringSink message = new StringSink();
    private int position;

    private ParseException(final boolean trace) {
        super(null, null, false, trace);       // no suppression; a stack trace only when asked (G-2.5)
    }

    public static ParseException at(final int position) {
        ParseException ex = TL.get();
        assert (ex = new ParseException(true)) != null;
        ex.reset(position);
        return ex;
    }

    public ParseException put(final CharSequence cs) { message.put(cs); return this; }
    public ParseException put(final long v)    { message.put(v);  return this; }
    public CharSequence getFlyweightMessage()  { return message; }
    @Override public String getMessage()       { return "[" + position + "] " + message; }   // diagnostics only: allocates
    @Override public void toSink(final CharSink<?> s) { s.put('[').put(position).put("] ").put(message); }

    private void reset(final int position) {
        message.clear();
        this.position = position;
    }
}

public final class BufferFull extends Exception {
    public static final BufferFull INSTANCE = new BufferFull();
    @Serial
    private static final long serialVersionUID = 1L;
    private BufferFull() { super(null, null, false, false); }
}
```

**Rules:** a message read from a reusable exception is invalid after the next
call to its factory on that thread — copy or log it first. `getMessage()` is
overridden to snapshot the sink, so a generic logger, `printStackTrace()` or an
uncaught-exception handler shows the position and the text; it allocates, and
is called only on diagnostic paths. A factory that sets extra
state on the shared instance resets that state at the write site. Readers of
optional state gate on a discriminator (an error code), never on "the field
looks cleared". A reusable exception is never the primary of a cleanup chain
that can fail, because it cannot carry a suppressed exception (G-4.3): catch it,
copy its message, and let the cleanup failure propagate. On virtual threads a
thread-local exception is created once per task (G-16.4); pass one explicitly
or keep that code on platform threads.

*For example:* `new IllegalArgumentException("gap must be positive")` at setup is
fine; anything thrown per event or per frame is not.

### G-5.2 Named static factories, not constructors

**Scope:** hot path · **From:** P1 · **Checked by:** review · **Class:** rule

**Finding:** A hot-path exception built by a constructor where a named factory sets its flags. (Code that derives meaning from message text is G-5.7.)

`ParseException.unexpectedToken(pos, tok)`,
`Failure.critical(errno)`, `Failure.nonCritical()`. Semantic flags
(`isInterruption()`, `isOutOfMemory()`, `isCritical()`) are bit-set accessors
set by the factory together with the message, so callers never re-derive
meaning from message text.

### G-5.3 Message shape is `verb phrase [key=value, key=value]`, ASCII only

**Scope:** everywhere · **From:** P1, P6 · **Checked by:** review · **Class:** rule

**Finding:** An error or log message that omits a value needed to act on it (the offending value, the limit, the identifier), that carries such values other than as `key=value` inside `[...]` after the text, or that contains non-ASCII characters. A message with no values to carry (`gap must be positive`) is not a finding.


```java
throw Failure.critical(errno).put("could not open [file=").put(path).put(", errno=").put(errno).put(']');
```

An error position points at the offending character. A parser distinguishes
"wrong token" (position of that token) from "ran out of input" (end position).

### G-5.4 One checked exception per subsystem boundary; everything else unchecked

**Scope:** everywhere · **From:** P1, P5 · **Checked by:** review · **Class:** rule

**Finding:** A public method of a type the Apply section names as a subsystem entry point that declares more than one checked exception type, or that lets a checked exception of another subsystem escape untranslated. `InterruptedException` and the park signals of G-8.2 do not count.

The checked one walks from the parser to the public entry point
and forces every layer to propagate or translate. Unchecked ones are caught at
the call site and converted into the domain error of that layer.

### G-5.5 `assert` for internal invariants; explicit throw for external input

**Scope:** everywhere · **From:** P3 · **Checked by:** review, test · **Class:** defect

**Finding:** An `assert` guarding file-, user- or peer-controlled input. (A run-time check of an internal invariant on a hot path is G-1.6.)

Asserts document buffer-pointer arithmetic, state-machine preconditions and
"impossible" branches at no run-time cost when disabled, except bytecode size:
each assert adds bytecode that counts against the JIT's inlining limits (35
bytes for a method called from a cold site), so asserts stay out of accessors
that must inline, or the cost is measured (G-13.10). Anything file-, user- or
peer-controlled gets a real check that throws. A `PARANOIA` flag gates
expensive checks that are worth running in some test runs.

### G-5.6 Capture the cause before cleanup

**Scope:** everywhere · **From:** P3 · **Checked by:** review · **Class:** defect

**Finding:** Cleanup run before the original error or `errno` was captured.

Read `errno` (or the original
exception) first, then close, then throw; a cleanup call may overwrite it.

### G-5.7 Code never derives meaning from an exception's message text

**Scope:** everywhere · **From:** P1, P3 · **Checked by:** review · **Class:** defect

**Finding:** A branch, retry decision, status code or test assertion that reads `getMessage()` (or `toString()` of an exception) to decide what happened.

A message is prose for a person and changes with a library version or a locale.
The meaning travels in the type, an error code or a flag set by the factory
(G-5.2); a test asserts the type and the code, and the message only where the
message is itself the contract (a user-facing error).

---

## 6. Logging

*Scope:* G-6.1 to G-6.4 *skip unless* hot-path logger: the Apply section names an asynchronous,
lossy logger of the repository's own, whose class names replace `Log` and `LogFactory` below.
Without one, a hot path logs only through counters and the aggregation of G-14.7, never per
event. G-6.5 everywhere except hot path.

### G-6.1 A fluent chain terminated by `$()`; the record is a reserved slot

**Scope:** skip unless hot-path logger · **From:** P3 · **Checked by:** review, test · **Class:** defect

**Finding:** String concatenation or boxing inside a hot-path log call, or a log chain not terminated.

Typed `$(int|long|double|boolean|char|CharSequence|Throwable)` overloads
write straight into a buffer; no concatenation, no boxing. `$()` appends the
end of line and commits. An unterminated chain leaks the slot and must be
detected and reported.

```java
LOG.info().$("stall detected [thread=").$(threadName).$(", gapMs=").$(gapMs).$(']').$();
```

### G-6.2 Plain `$(CharSequence)` is ASCII-only; `$safe()` for untrusted text

**Scope:** skip unless hot-path logger · **From:** P3 · **Checked by:** review · **Class:** rule

**Finding:** Untrusted text (file, wire, exception message) written without encoding on the hot-path logger.

Literal message text uses `$()`; anything from a file, the wire or an
exception message goes through `$safe()`, which encodes. A reusable exception
is logged as `$safe(e.getFlyweightMessage())`; a foreign throwable as `$(e)`,
which prints the trace into the same record.

### G-6.3 Default logging is lossy; waiting variants are opt-in

**Scope:** skip unless hot-path logger · **From:** P3, P6 · **Checked by:** review · **Class:** rule

**Finding:** A waiting log call on a path where losing the line is acceptable, or a lossy one where it is not.

When the queue
is full the chain becomes a no-op (a shared `NullLogRecord`). `errorW()` and
`infoW()` wait for a slot and are used only where losing the line is worse than
stalling the caller; compute all values before starting such a chain so an
exception cannot leak the slot. `critical()` always waits. `isEnabled()` guards
only *expensive* formatting done outside the chain; the record implements the
sink interface so `toSink(record)` works directly.

### G-6.4 One `private static final` hot-path logger per class

**Scope:** skip unless hot-path logger · **From:** P1 · **Checked by:** review · **Class:** rule

**Finding:** More than one logger per class, or a logger that is not `private static final`.

`private static final Log LOG = LogFactory.getLog(X.class);`, where `Log` and
`LogFactory` are the repository's hot-path logger (not Apache Commons Logging,
which shares the names). One logger per class keeps the logger's name equal to
the class, so routing and filtering by class work; `static final` lets the JIT
fold the level check.

### G-6.5 Off the hot path: `System.Logger`, one per class, messages shaped as G-5.3

**Scope:** everywhere except hot path · **From:** P1, P6 · **Checked by:** review · **Class:** rule

**Finding:** A logger other than `System.Logger` off the hot path, a failure logged without its exception, or a handled condition logged with a stack trace.

`private static final System.Logger LOG = System.getLogger(X.class.getName());`. A
message reads `verb phrase [key=value, key=value]`; a failure logs its exception, a
handled condition logs its message only. The JDK's logger needs no dependency and is
routed by the application, not by the library that logs.

```java
LOG.log(Level.WARNING, "could not save layout [file=" + path + "]", e);
```

---

## 7. Concurrency

*Scope:* G-7.1 to G-7.5 and G-7.9 *skip unless* worker pool; G-7.8 hot path; the others everywhere.

### G-7.1 A ring-queue claim is paired with `done()` in `finally`, and each sequence matches its owners

**Scope:** skip unless worker pool · **From:** P3 · **Checked by:** review, test · **Class:** defect

**Finding:** A `next()` claim not paired with `done()` in a `finally`, a producer spinning on a full queue, or a single-owner sequence used by two threads.

Slots are
pre-allocated from a factory, capacity is a power of two, `get(cursor)` is
`buf[(int) (cursor & mask)]`. The canonical consumer:

```java
while (true) {
    final long c = seq.next();
    if (c > -1) {
        try { process(queue.get(c)); } finally { seq.done(c); }
        return true;
    }
    if (c == -1) {
        return false;
    }
    Thread.yield();   // -2: lost a race
}
```

Every `next() > -1` is paired with `done()` in a `finally`. Producers do not
spin on `-1`: they do the work inline, retry a bounded number of times, or use
a blocking claim when the message must not drop. Choose the narrowest sequence
that is true: single-producer and single-consumer sequences have no CAS and
are unsafe with two callers; multi-owner sequences stamp a per-slot lap flag
because claims can complete out of order. Wire barriers (`pub.then(sub).then(pub)`)
before any `next()`; a fan-out barrier's available index is the minimum across
subscribers.

### G-7.2 Publish with a release store, read with an acquire load; CAS through a `VarHandle` on a `volatile` field

**Scope:** skip unless worker pool · **From:** P3 · **Checked by:** review · **Class:** defect

**Finding:** A single-writer data-path field (sequence, cursor, position) held in an `Atomic*` object, a `sun.misc.Unsafe` field offset, a store-then-load handshake between threads that relies on release/acquire alone, or a reader of a release-published reference that reads it plainly. A counter written by many threads is G-14.5; an ordering dependency without a comment is G-7.13.

Keep the field `volatile` so plain reads have acquire semantics. Use release
stores (`setRelease`) for single-writer publication and acquire loads
(`getAcquire`) or volatile loads to read. Release/acquire does not order a store
before a later load of a different variable: a handshake where each side writes
its own flag and then reads the other's (park and unpark, a Dekker-style flag
pair, two sequence barriers checking each other) uses volatile `set`/`get` or a
`VarHandle.fullFence()` between the store and the load, with a comment naming
the pair. Handing a non-volatile structure to another thread needs no fence:
publish its reference with a release store, and the reader reads that same
reference with an acquire or volatile load before it dereferences it; a plain
read of the reference may see the structure's fields at their default values. Keep `Atomic*` objects for
lifecycle and control state. `sun.misc.Unsafe` field offsets are not used: they
are deprecated for removal and warn on first use in JDK 25. Comment any read
ordering the algorithm depends on.

```java
private static final VarHandle VALUE;

private volatile long value = -1;   // written by the claiming threads, read by every consumer

static {
    try {
        VALUE = MethodHandles.lookup().findVarHandle(Sequence.class, "value", long.class);
    } catch (final ReflectiveOperationException e) {
        throw new ExceptionInInitializerError(e);
    }
}

boolean casValue(final long expected, final long next) {
    return VALUE.compareAndSet(this, expected, next);
}

void publish(final long v) {
    VALUE.setRelease(this, v);
}
```

### G-7.3 Hot shared fields get their own 128 bytes

**Scope:** skip unless worker pool · **From:** P3 · **Checked by:** measure, review · **Class:** rule

**Finding:** Two hot fields written by different threads on one cache line, shown by a profile or benchmark.

Pad by inheritance, with 16 `long`s (128 bytes) before and after the hot field
(the JVM lays out superclass fields first), or use a 128-byte stride in arrays
(16 `long`s, 32 `int`s). 128 bytes covers the 128-byte cache lines of Apple
silicon and the adjacent-line prefetch of x86, and matches HotSpot's own
`ContendedPaddingWidth`. Comment the padding as false-sharing avoidance, and
keep it only where a profile or benchmark shows the sharing (G-13.10).

```java
abstract class LhsPad {
    @SuppressWarnings("unused") long p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14, p15, p16;
}

abstract class HotValue extends LhsPad {
    volatile long value;
}

abstract class RhsPad extends HotValue {
    @SuppressWarnings("unused") long q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12, q13, q14, q15, q16;
}

public final class Cursor extends RhsPad { /* ... */ }
```

### G-7.4 A job returns "did useful work"; workers back off in tiers

**Scope:** skip unless worker pool · **From:** P3 · **Checked by:** review · **Class:** rule

**Finding:** A job that blocks, runs long, or throws from cleanup.

`true`
resets the idle counter; consecutive idle passes escalate from `yield` to a
1 ms sleep to the configured sleep. A job is non-blocking and short. A job
that clones itself per worker frees the clone idempotently and never throws
from cleanup. A serialised job uses a CAS run-guard so the same instance
assigned to N workers runs on at most one; losing the CAS returns `false`.

```java
@Override
public boolean run(final WorkerContext ctx) {
    if (!LOCKED.compareAndSet(this, 0, 1)) {
        return false;
    }
    try {
        return runSerially();
    } finally {
        LOCKED.setRelease(this, 0);
    }
}
```

### G-7.5 Per-worker state is an array indexed by the pool-local worker id; stealers borrow a slot through a CAS probe and release it in `finally`

**Scope:** skip unless worker pool · **From:** P3 · **Checked by:** review · **Class:** defect

**Finding:** A borrowed worker slot not released in `finally`, or a spin loop without a cancellation check.

A
slot leaked on an error path stays lost for as long as the owner lives. Spin
loops between probes yield and check for cancellation; never spin without a
cancellation check.

### G-7.6 Every wait is bounded, re-checks its condition in a loop, and keeps the interrupt status

**Scope:** everywhere · **From:** P5 · **Checked by:** review, test · **Class:** defect

**Finding:** A `LockSupport.park`, `Condition.await`, `Object.wait`, `Thread.join`, `Future.get`, `BlockingQueue.take` or `CountDownLatch.await` with no timeout on a thread that has no other way to be woken on shutdown; a wait whose return is taken as the condition without re-checking it in a loop; a timed wait loop that restarts its full timeout on a wake-up; or an `InterruptedException` caught and neither handled as the stop signal nor restored with `Thread.currentThread().interrupt()`.

A bounded
`parkNanos` means a lost unpark costs one interval instead of a hang. A wait
returns for reasons other than its condition (a spurious wake-up, an old
permit, an interrupt, a timeout), so every wait sits in a loop that re-checks
its condition and the cancellation state; a return never by itself means the
condition holds. Pass a
blocker object so thread dumps say what the thread waits on. Clamp remaining
time to at least 1 ns because `parkNanos(<= 0)` returns immediately.

### G-7.7 Halt is a visible flag, written before the wake-up

**Scope:** everywhere · **From:** P5 · **Checked by:** review, test · **Class:** defect

**Finding:** A halt flag that is not `volatile`, atomic or lock-guarded, a wake-up issued before the flag is written, `Thread.interrupt()` used to stop a worker that touches an `InterruptibleChannel`, or shared resources freed before every worker has finished its cleanup.

Workers observe the flag at the next
iteration, run their own cleanup in nested `try/finally` steps, and count down
the halt latch **last**; the pool frees shared resources only after that latch
releases. The flag is a `volatile` field (or atomic, or guarded by the lock the
worker takes), written before the wake-up: `unpark` and `notify` wake a thread
but publish nothing, so a plain `boolean` can stay `false` in the worker
forever. Nothing uses `Thread.interrupt()` to stop a worker that touches an
`InterruptibleChannel` (`FileChannel`): the interrupt closes the channel for
every user. A worker blocked in network I/O is woken by closing its socket or by
its read timeout (G-15.1); a task run by an executor is cancelled by the
executor's interrupt and treats it as the halt signal.

### G-7.8 On a hot path, locks are the last resort and read-mostly data is read without writing

**Scope:** hot path · **From:** P3, P5 · **Checked by:** review · **Class:** rule

**Finding:** On a hot path, a lock where a single owner, a snapshot or an optimistic read would do, or a read path that writes shared memory (a read-lock counter) without a measurement showing it beats the alternatives.

For read-mostly structures prefer, in order: an immutable snapshot behind a
`volatile` reference that the writer replaces (readers write nothing);
`StampedLock` optimistic reads (`tryOptimisticRead`, `validate`; nothing written
on the read path); a read-write lock. A spinning lock is used only on platform
threads, with a bounded spin that calls `Thread.onSpinWait()` and then parks
(G-16.12), and only where a measurement shows it beats the alternatives
(G-13.10). `synchronized` on a small private lock object serves cold structural
paths; `ReentrantLock` where a timed or interruptible acquire is needed.

### G-7.9 Single-owner latches when exactly one thread waits

**Scope:** skip unless worker pool · **From:** P3 · **Checked by:** review · **Class:** rule

**Finding:** A general latch with a waiter queue where exactly one thread waits.

No waiter queue;
the count may go negative so producers can finish before the owner decides
how many to wait for; the waiting thread keeps consuming its own tasks while
it waits — work stealing, not blocking.


### G-7.10 Every thread has an owner and ends when its owner closes

**Scope:** everywhere · **From:** P5, P6 · **Checked by:** review, test · **Class:** defect

**Finding:** A platform thread or a thread pool created other than through the application's thread factory or the owner that closes it (`new Thread`, `Thread.ofPlatform()`, `Executors.*`, `new *ThreadPoolExecutor`, `new ForkJoinPool`), a platform thread per occurrence of repeated work, or a thread that outlives its owner's close. Virtual threads created per task under G-16.4, joined or cancelled by their owner, are not a finding. (An unnamed thread is G-7.14.)

Threads come from one factory per application, or from the owner that starts them,
never from a bare `new Thread` at a call site. The name says the kind and the owner.
Repeated work goes to the owner's own thread or strand, with at most one request
waiting per key, never to a new thread per occurrence. A test counts the live threads
after a close and asserts the budget.

### G-7.11 Nothing blocks a thread that owns latency

**Scope:** everywhere · **From:** P3, P6 · **Checked by:** review, test, measure · **Class:** defect

**Finding:** A blocking call (process, network, read of unknown size, file I/O that can block, lock wait, credential lookup) on a UI thread, event loop or single-writer loop. (A latency-owning thread with no stall measurement is G-14.12.)

A UI thread, an event loop or a
single-writer state loop hands off every process run, network call, read of unknown
size, lock wait and credential lookup, and measures itself: a stall over its budget is
logged with the stack that caused it, while it lasts, not only once it ends.

### G-7.12 Locks are never assumed reentrant, and never held across foreign callbacks

**Scope:** everywhere · **From:** P1, P3 · **Checked by:** review · **Class:** defect

**Finding:** Code that relies on re-acquiring a lock it already holds, or a lock held across a call to a callback, listener or overridable method supplied from outside the class.

A reentrant acquire hides a re-entry the design did not plan, and a lock held
across a callback is a deadlock waiting for that callback to take a lock of its
own.

### G-7.13 Every `volatile` field names its writer and readers, and every ordering dependency says so

**Scope:** everywhere · **From:** P1 · **Checked by:** review · **Class:** rule

**Finding:** A `volatile` field without a comment naming the threads that write it and the threads that read it, or code that depends on a memory ordering without a comment naming it.

The comment is the only place the threading contract of that field is written
down; without it, the next change cannot tell a single-writer field from a
contended one.

### G-7.14 Every thread is named for its kind and its owner

**Scope:** everywhere · **From:** P1, P6 · **Checked by:** review · **Class:** rule

**Finding:** A thread, platform or virtual, started without a name that says its kind and its owner.

A thread dump, a profile and a JFR recording show threads by name; an unnamed `Thread-17` cannot be traced back to
the code that started it.

---

## 8. State machines and resumable I/O

*Scope:* G-8.1 to G-8.3 *skip unless* resumable I/O; G-8.4 *skip unless* incremental parser;
G-8.5 *skip unless* pooled contexts.

### G-8.1 Resumable state is an `int` plus a dispatch table, not a call stack

**Scope:** skip unless resumable I/O · **From:** P5 · **Checked by:** review · **Class:** defect

**Finding:** A resumable step that sets its state after an operation that can park, so the resume skips or repeats work.

State constants chained `+ 1`; a table of resume actions indexed by state;
`resume()` is `actions.getQuick(state).run()`. Set the state at the top of each
step, before anything that can throw the park signal, so the resume re-enters
the same step.

### G-8.2 Park signals are checked singleton exceptions that name the next operation

**Scope:** skip unless resumable I/O · **From:** P5 · **Checked by:** review · **Class:** defect

**Finding:** A park signal caught and swallowed, or state carried on the singleton signal.

`throw registerForRead()` stores any payload on the context (a
disconnect reason as an `int`) and returns the singleton, because the singleton
cannot carry state. The outer loop maps each signal to a dispatcher operation.
Never catch and swallow a signal.

### G-8.3 Bookmark and reset for speculative writes into a fixed buffer

**Scope:** skip unless resumable I/O · **From:** P5 · **Checked by:** review, test · **Class:** defect

**Finding:** A write into a fixed buffer that cannot rewind on overflow. (An overflow error that does not name the setting to raise is G-5.3.)

Write
a record; on overflow rewind to the last bookmark, flush what fit, re-run the
step. A bookmark at buffer start means one value exceeds the whole buffer — a
hard error that names the configuration knob to raise.

### G-8.4 Byte-level parsers keep their position in fields and return an enum

**Scope:** skip unless incremental parser · **From:** P3 · **Checked by:** review, test · **Class:** defect

**Finding:** An incremental parser that copies entities out of the buffer, keeps positions that do not move on compaction, or returns booleans instead of a result enum.

`COMPLETE | UNDERFLOW | ERROR`. A 256-entry `boolean[]` control-byte table
keeps the common byte on one branch; entity views are `(lo, hi)` windows over
the buffer, never copies; after the caller compacts the buffer it calls
`shift(n)` on the parser so every held offset moves with the data.

```java
public ParseResult parse(final byte[] buf, final int limit) {
    while (at < limit) {
        final byte b = buf[at];
        if (!CONTROL[b & 0xFF]) { at++; continue; }   // hot path: one branch
        switch (b) { /* ... */ }
    }
    return ParseResult.UNDERFLOW;   // call again with more bytes
}
```

*For example:* this is the shape for a single-pass event reader that must not
materialise each event.

### G-8.5 A pooled context has four lifecycle verbs with distinct scopes

**Scope:** skip unless pooled contexts · **From:** P5 · **Checked by:** review · **Class:** defect

**Finding:** A pooled context returned without its security reset, or verbs whose scopes overlap.

A
cheap constructor (acceptance runs on one thread) → `of(handle)` / `init()` per
connection → `reset()` per request → `clear()` when returned to the pool (the
security reset) → `close()` to free resources. Pools are thread-local, no
locking.

---

## 9. Configuration and dependency boundaries

*Scope:* G-9.5 everywhere; G-9.1 to G-9.4 *skip unless* configuration interface.

### G-9.1 Configuration is an interface of primitive and `CharSequence` getters, one per subsystem, nested by composition, no setters

**Scope:** skip unless configuration interface · **From:** P5 · **Checked by:** review · **Class:** rule

**Finding:** A pool size, queue bound or buffer limit that bounds work in production code and is not read from the configuration.

Sizes and capacities
come from getters; production code has no literal pool sizes.

```java
public interface AnalysisConfiguration {
    long stallGapNanos();
    int topN();
    IoConfiguration io();
}
```

### G-9.2 OS, time and randomness sit behind small interfaces exposed by the configuration and defaulting to stateless singletons

**Scope:** skip unless configuration interface · **From:** P5 · **Checked by:** review · **Class:** rule

**Finding:** Direct use of the clock, file system or randomness where the configuration exposes a facade, or a mocking library used to replace one.

A `FilesFacade`, a
`Clock` with one `ticks()` method, a seedable `Rnd`. Consumers pull them from
the configuration at use time. No DI container, no mocking framework: tests
substitute by overriding one getter with an anonymous subclass.

```java
public interface IoConfiguration {
    FilesFacade files();
    default NanoClock clock() { return SystemNanoClock.INSTANCE; }
}
```

*For example:* `System.nanoTime()`, `Clock.systemUTC()`, `Files.*` and the JFR
reader entry point each sit behind an interface with a production `INSTANCE`.

### G-9.3 Three classes per configuration interface

**Scope:** skip unless configuration interface · **From:** P5 · **Checked by:** review · **Class:** rule

**Finding:** A component that reads configuration from a global instead of its constructor.

A `DefaultXxx` with
literal returns (tests and embedding), an `XxxWrapper` that delegates every
call to an `AtomicReference<Xxx>` (selective override and hot reload), and the
parsed production one. Components receive the whole interface by constructor
as a `private final` field; nothing reads a global.

### G-9.4 Settings are parsed once, validated at construction, and unknown keys rejected

**Scope:** skip unless configuration interface · **From:** P1, P5 · **Checked by:** review, test · **Class:** rule

**Finding:** A setting parsed more than once, validated after use, or an unknown key accepted silently in strict mode.

Keys are an enum carrying path, environment
variable name and sensitivity; typed helpers `getInt(props, env, KEY,
default)` validate ranges and relations and throw one configuration exception
naming the key; values are parsed exactly once into final fields; unknown keys
are rejected in strict mode; cross-field validation runs at construction.

*For example:* argument parsing resolves every option once into final primitives,
validates ranges and relations there, and exposes an interface — not a
`Map<String, String>`.

### G-9.5 A constructor must not call an overridable getter

**Scope:** everywhere · **From:** P5 · **Checked by:** build, review · **Class:** defect

**Finding:** A constructor that calls an overridable method.

A subclass that
overrides it sees its own fields uninitialised. javac's `-Xlint:this-escape`
(part of G-10.10) reports it for public extensible classes; review covers the
rest. Where the override must run from the superclass constructor, the
subclass assigns the fields it reads, declared without an initialiser, before `super(...)` (JDK 25,
G-16.8).

---

## 10. Style

*Scope:* everywhere, except G-10.7, which is hot path.

### G-10.1 Member order is mechanical

**Scope:** everywhere · **From:** P1 · **Checked by:** review · **Class:** rule

**Finding:** Members out of the order the rule gives, in a file the change adds or reorders. Order kept for an initialiser dependency or a meaningful sequence is not a finding.

Static final fields → static fields →
instance final fields → instance fields (each band public > protected >
package > private; within a band, declaration order is kept where an
initialiser reads another field or the order carries meaning — chained
constants (G-1.10), slot offsets (G-1.8), tag ranges (G-1.9) — and is otherwise
alphabetical) → static initialisers → constructors → public static methods →
public methods → protected, then package-private methods → private static
methods → private methods → nested types. Enforce with the IDE's arrangement rules or a formatter; do not
hand-order.

### G-10.2 `final` on every declaration that is never reassigned: fields, locals and parameters

**Scope:** everywhere · **From:** P1 · **Checked by:** build, review · **Class:** rule

**Finding:** A declaration never reassigned and not `final`, in the shapes the rule lists.

Owned scratch objects are `private final X x = new
X();` at the declaration and reused for life; mutable state (`data`, `pos`) is
the exception, and the only one for fields. Every other declaration that is
never assigned after it is declared carries `final`, wherever it occurs: a
local variable, a `try`-with-resources variable, a basic-`for` initialiser
variable, an enhanced-`for` variable, a catch parameter (single-type or
multi-catch) and a method or constructor parameter. That the language already
makes some of these final is no reason to leave it off: the word is there so
the reader does not have to know the rule. The absence of `final` then means
exactly one thing: "this one is reassigned, look for the write". Only
declarations without an assignment stay bare: a lambda parameter, a pattern
variable, a local declared without an initialiser and assigned later, and the
parameters of a method without a body (`abstract`, `native`, interface
declarations). A sweep over existing code is applied by a tool (G-13.9);
new and changed lines are written with `final` directly. javac rejects a `final`
on a reassigned variable but never reports a missing one: Checkstyle's
`FinalLocalVariable` (in this standard's `config/checkstyle/checkstyle.xml`)
reports locals, enhanced-`for` variables, catch parameters and method and
constructor parameters that are never reassigned, and leaves out a local declared
without an initialiser; `try`-with-resources variables are left to review.

```java
public long sum(final LongList values, final int from) {
    long total = 0;                                  // reassigned: bare
    for (int i = from, n = values.size(); i < n; i++) {   // i is reassigned, and n shares its declaration: bare
        final long v = values.getQuick(i);
        total += v;
    }
    return total;
}
```

### G-10.3 Nullability annotations from one library, used sparsely

**Scope:** everywhere · **From:** P1 · **Checked by:** review · **Class:** rule

**Finding:** A missing `@Override`, a nullability annotation from a second library, or `@SuppressWarnings` without the inspection id or the reason.

`@NotNull` / `@Nullable` on public API parameters where `null` has defined
behaviour and on returns that can be absent — not on every field. `@TestOnly`
marks production accessors that exist for tests. `@Override` everywhere,
including on interface `default` overrides (neither javac nor Checkstyle
reports a missing one; Error Prone's `MissingOverride` does, where a repository
runs it). `@SuppressWarnings` uses the
inspection id, one per method, with a comment when the reason is not obvious.

### G-10.4 Javadoc only where the contract can surprise; comments say why

**Scope:** everywhere · **From:** P1 · **Checked by:** build, review · **Class:** rule

**Finding:** A comment that restates the code, javadoc on an unsurprising method, or a surprising contract without javadoc. Tests follow G-11.7 instead.

`getQuick` gets javadoc (no bounds check); `add` and `size` do not. Flags with
a safety polarity get long javadoc. Inline comments carry rationale, not
narration. Active voice naming the acting subject.

### G-10.5 Names follow the conventions below

**Scope:** everywhere · **From:** P1 · **Checked by:** review · **Class:** rule

**Finding:** A name that breaks the conventions the rule lists.

`is` / `has` for boolean accessors; `notEmpty()` over `!isEmpty()`;
suffixes `Quick` (unchecked), `Quiet` (sentinel on failure), `At` (takes a raw
`keyIndex`), `0` (private worker behind a public overload); prefixes `Direct`
(off-heap); `Impl` (production implementation of a facade); `Facade` (OS
boundary); `Sink` (append-only writer); plural nouns (`Chars`, `Numbers`,
`Bytes`) for `final` static helper holders with private constructors;
`NO_ENTRY_VALUE` / `*_NULL` for sentinels; `tlXxx` for thread-local statics;
`size()` for a byte count, `length()` reserved for `CharSequence`. A test class
is `<Class>Test`; a test method's name states the behaviour it proves, in
lowerCamelCase (`closesTheChannelOnTimeout`), because the name is what a failure
report shows.

### G-10.6 Interfaces grow by `default` methods only where the default is correct for every implementation

**Scope:** everywhere · **From:** P5 · **Checked by:** review · **Class:** rule

**Finding:** A `default` method whose answer is wrong for an existing implementation (a default `isMutable()` returning `false` with a mutable implementor), an abstract interface method added where a correct default exists, or a type getter a subclass could wrongly override.

A new interface method is a `default` only when its answer is correct for every
existing implementation: the conservative answer (`false`, `null`, or
`UnsupportedOperationException`) where "not supported" is true of them all.
Where an implementation would answer differently, the method is abstract (every
implementor decides) or goes into a new interface; "compiles unchanged" is not a
safety criterion, since a wrong default compiles and misleads every caller. Per-type abstract bases implement the whole interface once;
unsupported type getters are `final` and throw so a subclass cannot
accidentally "support" the wrong type:

```java
public abstract class IntValue implements Value {
    @Override public final boolean getBool()   { throw new UnsupportedOperationException(); }
    @Override public long getLong()            { return Nulls.intToLong(getInt()); }   // widening allowed
    @Override public final int type()          { return Tag.INT; }
}
```

### G-10.7 On a hot path: no streams; lambdas only as one-time strategy objects or on setup paths

**Scope:** hot path · **From:** P3 · **Checked by:** review, measure · **Class:** rule

**Finding:** A stream, a capturing lambda or bound method reference (one that reads a local, a parameter or `this`) evaluated per call, or varargs, on a hot path.

A capturing lambda or a bound method reference (`this::m`, `x::m`)
allocates on every evaluation unless escape analysis removes it; on a hot path it
is created once in a constructor and stored. A non-capturing lambda or a static
or unbound method reference is linked once per call site and is not a finding.
`static class` for nested types unless they need the outer instance.
`equals` / `hashCode` only on value and key types. Varargs and `Object[]` only
in convenience and test factories.

### G-10.8 Braces always, single-type imports, wrapped long signatures, licence headers; current syntax where it costs nothing

**Scope:** everywhere · **From:** P1, P7 · **Checked by:** build, review · **Class:** rule

**Finding:** Missing braces, a signature over the line limit not wrapped one parameter per line, a missing licence header, or an older form where §16 gives a current one.

Enhanced `switch` with
arrows, pattern variables in `instanceof`, pattern `switch` on `Throwable`,
text blocks, records for immutable setup-time values (not for per-event
data); §16 has the rest of current Java. Braces always; single-class imports (G-10.11);
a signature that does not fit the line limit the Apply section names wraps one parameter per line with the
closing paren on its own line; the licence header the Apply section names on every
file.


### G-10.9 Code and comments name no tool, agent or review finding

**Scope:** everywhere · **From:** P1 · **Checked by:** review · **Class:** rule

**Finding:** A class, method, variable or comment that names the tool, agent, review round or finding id that found or requested the code (`// fix for review finding T3`, `// suggested by the linter`). Names of tools the code uses or integrates with are not findings.

A comment explains
the code to its next reader; who or what found the problem belongs to the commit
message or the review.

### G-10.10 Compiler warnings are errors

**Scope:** everywhere · **From:** P5 · **Checked by:** build · **Class:** rule

**Finding:** A build without `-Xlint:all -Werror` and `-Xdoclint:all/private,-missing`, or an excluded lint category without its reason.

`-Xlint:all -Werror`, with each excluded
category named in the build file and the reason beside it. Doclint runs as
`-Xdoclint:all/private,-missing`, so a broken `{@link}` or a malformed tag on any
member fails the build and a missing comment does not (G-10.4 decides where a
comment belongs).

### G-10.11 Imports name single types, in three groups, checked by the build

**Scope:** everywhere · **From:** P1 · **Checked by:** build · **Class:** rule

**Finding:** A wildcard import, a fully qualified type that could be imported, an unused import, or imports out of the group order.

No
wildcards; a type is imported, never written fully qualified, except to tell apart two
types with one simple name. Groups, in this order, each sorted, a blank line between
them: the JDK's own (`java`, `javax`, `jdk`, `com.sun`), then third-party libraries,
then the project's own packages. Static imports form a group of their own, last, ordered the same way.
Checkstyle enforces the order and `UnusedImports` beside it, because `-Xlint` reports
neither.

### G-10.12 A number in code says where it came from

**Scope:** everywhere · **From:** P2 · **Checked by:** review · **Class:** rule

**Finding:** A threshold, budget, capacity or timeout that changes observable behaviour (when work is refused, retried, timed out, dropped or flushed) and whose declaration has no comment saying what set it. A sizing hint that only affects allocation (an initial capacity, a copy-buffer size) is not a finding.

A threshold, budget, capacity or
timeout carries, in its javadoc or the comment on its declaration, the measurement or the requirement that set it: what
was measured, on what, with what margin. A number nobody measured says that too, and
what would settle it.

---

## 11. Tests

*Scope:* everywhere; G-11.1 *skip unless* tracked resources, G-11.2 *skip unless* assertion builder,
G-11.3 *skip unless* facades. Examples use JUnit 5; a repository on JUnit 4 records it in its Apply
section.

### G-11.1 Every test that can acquire a tracked resource runs inside a leak check

**Scope:** skip unless tracked resources · **From:** P5 · **Checked by:** test · **Class:** rule

**Finding:** A test of code that acquires a tracked resource and runs outside the leak check.

The check snapshots the resource counters before the body and asserts
each unchanged after, naming the category that leaked:

```java
/// Proves a reader releases every buffer it took.
@Test
void readerReleasesBuffers() throws Exception {
    assertNoLeak(() -> {
        try (final Reader r = new Reader(cfg)) { r.readAll(); }
    });
}
```

*For example:* for an on-heap tool the equivalent counts every `AutoCloseable`
opened and closed, and asserts pooled and scratch objects are back at their
baseline size.

### G-11.2 One fluent assertion builder whose default path is the strict one

**Scope:** skip unless assertion builder · **From:** P1 · **Checked by:** review · **Class:** rule

**Finding:** A test that opts out of the strict assertion path without a stated reason.

`assertAnalysis(input).returns(expected)` runs the strongest battery (a second
pass, a size cross-check, property checks); opt-outs are named and require a
stated reason. Expected values are multiline text blocks. `.fails(pos, msg)`
asserts the error **position**.

### G-11.3 Fault injection is an anonymous subclass of the facade, failing on the Nth call or on a specific name, installed via the configuration for one test block

**Scope:** skip unless facades · **From:** P5 · **Checked by:** review · **Class:** rule

**Finding:** A mocking library, or fault injection that does not go through the facade.

Test doubles also *track* (handle → name) so leak reports name
the file. No mocking library.

```java
files = new TrackingFilesFacade() {
    @Override
    public long open(final CharSequence name) {
        if (endsWith(name, ".idx") && failures.decrementAndGet() >= 0) {
            return -1;
        }
        return super.open(name);
    }
};
```

### G-11.4 Randomness is a two-seed generator, seeds printed on every run and accepted back through system properties

**Scope:** everywhere · **From:** P2 · **Checked by:** test, review · **Class:** rule

**Finding:** A randomised test whose seed is not printed or cannot be replayed.

One instance per thread. Test
order is randomised so inter-test state leaks surface.

### G-11.5 Concurrency tests: a barrier to start, a latch with a timeout to join, atomics for outcomes asserted once on the main thread, `assertEventually` with backoff instead of `Thread.sleep`, races hunted with seeded repeat loops

**Scope:** everywhere · **From:** P2 · **Checked by:** review · **Class:** rule

**Finding:** `Thread.sleep` used to wait for a condition, an unbounded join, or outcomes asserted on a worker thread.


```java
final CyclicBarrier start = new CyclicBarrier(threads);
final CountDownLatch done = new CountDownLatch(threads);
final AtomicInteger anomalies = new AtomicInteger();
final ThreadFactory factory = Thread.ofPlatform().name("race-worker-", 0).factory();
final List<Thread> workers = new ArrayList<>();
try {
    for (int t = 0; t < threads; t++) {
        final Thread w = factory.newThread(() -> {
            try {
                start.await(10, TimeUnit.SECONDS);
                work(anomalies);
            } catch (final InterruptedException _) {
                Thread.currentThread().interrupt();             // cancelled: stop and keep the status
            } catch (final TimeoutException | BrokenBarrierException | RuntimeException _) {
                anomalies.incrementAndGet();
            } finally {
                done.countDown();
            }
        });
        workers.add(w);
        w.start();
    }
    assertTrue(done.await(60, TimeUnit.SECONDS), "workers did not finish");
} finally {
    for (final Thread w : workers) {                            // runs on success and on a timeout
        w.interrupt();
        assertTrue(w.join(Duration.ofSeconds(10)), "worker did not stop [name=" + w.getName() + "]");
    }
}
assertEquals(0, anomalies.get());
```

### G-11.6 Heavy fixtures are static per class; every mutable piece is reset before each test (`@BeforeEach`); overrides go through a typed `Overrides` object the test configuration consults live

**Scope:** everywhere · **From:** P1, P5 · **Checked by:** review · **Class:** rule

**Finding:** A `Closeable` in a test outside `try`-with-resources, mutable shared state not reset per test, or a copied test where a parameter would do.

`try (final X x = ...)` for every `Closeable` in
tests. Parameterise over modes rather than copy tests. Assert meaning, not
representation. Narrow unit tests need no base class.


### G-11.7 Tests are documented with Markdown comments

**Scope:** everywhere · **From:** P1 · **Checked by:** test · **Class:** rule

**Finding:** A test class or test method without a `///` comment, or a `/** */` comment on one.

A `///` comment (JDK 23,
JEP 467) above every test class and every `@Test`, `@ParameterizedTest`,
`@RepeatedTest` and `@TestFactory` method says what the test proves; `/** */` on a test
is a defect. A checker run by the build or CI counts the misses.

### G-11.8 Tests never touch the user's data

**Scope:** everywhere · **From:** P5 · **Checked by:** review, test · **Class:** defect

**Finding:** A test that reads or writes the user's home data, keychain, preferences or configuration without a named flag.

No test reads or writes the user's home
data, keychain, preferences or real configuration unless a named flag says so; each
test gets its own temporary root.

---

## 12. Applying the standard in a repository

*Scope:* everywhere.

Each repository keeps one Apply section (a file, or a section of its architecture document) with these parts, in this
order:

1. **Version.** The tag of this standard it follows, linked, and its JDK version.
2. **Hot paths.** The code this repository treats as hot path, by package or class, with the measurement that put it
   there.
3. **Applied.** What was applied, when, and how it is enforced (build, test, checker).
4. **Departures kept on purpose.** Rule IDs, the decision, and why. Changing one is a design change, not a local edit.
   Departures from *defect* rules are recorded with the failure they accept and are still reported.
5. **Not applied.** Rule IDs that do not fit the repository, with the reason, and rules not applied yet, with the plan.
   A rule not applied yet is not waived: the entry records the plan, and findings against it are still reported; only
   a departure (part 4) changes what a finding is.
6. **Project packages** (G-10.11): the pattern that names the project's own imports.
7. **Preview features**, if any are enabled, by name (G-16.10).
8. **Doc comments in main code**: `///` or `/** */` (G-16.11).
9. **Nullability annotations**: the one library, if any (G-10.3).
10. **Licence header**: the exact text (G-10.8).
11. **Logging**: `System.Logger` (G-6.5) or the recorded departure, and the hot-path logger, if any (§6).
12. **Test framework** and its lifecycle annotations (§11).
13. **Subsystem entry points**, by package (G-5.4), the **configuration type**, if any (§9), and the **latency
    budgets** of operations that have one (G-14.6).
14. **Line limit** (G-10.8), in characters.

The repository's agent instructions (`AGENTS.md`, `CLAUDE.md`) point to this standard's version and to the Apply
section, so an agent reads both before it writes code.

Where the Apply section is missing or does not give a value, these defaults hold: doc comments in main code `/** */`;
no nullability library; logging `System.Logger`; test framework JUnit 5; line limit 120 characters; no preview
features; no hot paths. The licence header has no default: without an Apply value, G-10.8's header clause is not
checked.

### G-12.1 A repository that follows this standard has an Apply section

**Scope:** everywhere · **From:** P1, P5 · **Checked by:** review · **Class:** rule

**Finding:** A repository whose agent instructions or documentation claim this standard and that has no Apply section, or an Apply section without the version it follows.

The site of the finding is the repository root. Without an Apply section an agent cannot tell a departure from a
violation or a hot path from a cold one, and applies the defaults above.

---

## 13. Changing existing code

*Scope:* everywhere. These rules govern how code is changed; sections 1 to 11 and 14 to 16 govern what the result
looks like.

### G-13.1 Read the code around a change before writing it

**Scope:** everywhere · **From:** P4, P5 · **Checked by:** review · **Class:** rule

**Finding:** A new helper, type or constant that duplicates one already in the class, its package or the module's
shared helpers.

Before adding code, read the class, its package, its callers and the module's shared helpers. Reuse what exists. A
private helper that a second class now needs moves to the shared place, and both call it; a parallel copy is not
written. A duplicate costs twice in every later fix and every later optimisation.

### G-13.2 Follow the surrounding idiom; one idiom per concept

**Scope:** everywhere · **From:** P1, P4, P5 · **Checked by:** review · **Class:** rule

**Finding:** A change that introduces a second way of expressing a concept the file or module already expresses one way
(error handling, lifecycle, threading, logging, null handling, naming).

When the existing idiom is wrong, it is changed everywhere it occurs, in a change of its own, or not at all; a mixture
is worse than either. Where the idiom conflicts with a rule of this standard and the Apply section records no
departure, the change follows the idiom and reports the conflict: the rule ID, the file, and a proposal (a departure
for the Apply section, or a separate change that moves the whole file or module to the rule under G-13.9). A change
never leaves one concept expressed two ways in one file.

### G-13.3 Improve what you touch only when the gain is shown and worth the diff

**Scope:** everywhere · **From:** P2, P4 · **Checked by:** review · **Class:** rule

**Finding:** A refactor or clean-up in a change with no stated evidence of its gain, or one mixed into a behaviour
change; or a defect seen in the changed lines and left without a fix or a note.

Leave the code better than it was found, within the change's reach. The gain is demonstrated by a test that failed
before, a measurement, a removed duplicate, a removed defect or a removed concept. It is worth it when it outweighs the
reviewer's reading and the risk of the edit. An improvement that is not part of the task goes into its own commit with
its evidence in the message.

### G-13.4 Fix a defect at its cause and at every call site, without new structure for one caller

**Scope:** everywhere · **From:** P5 · **Checked by:** review · **Class:** rule

**Finding:** A fix applied at one call site while other call sites keep the defect, or a shared helper, layer or
option introduced for a single call site.

Search for every site that has the same defect before fixing one. Prefer the local, explicit fix (`top + 1L` over a
new overflow helper another module must import) unless two or more sites need it.

### G-13.5 Add no surface nobody asked for

**Scope:** everywhere · **From:** P5 · **Checked by:** review · **Class:** rule

**Finding:** A setting, option, metric, public method or extension point that no requirement asks for, or a method in production code that only tests call and is not marked `@TestOnly` (G-10.3).

Every addition is code to read, test, document and keep compatible. On a hot path, the smaller change is also the
faster one. Cut what another mechanism already covers before adding a new one.

### G-13.6 Agree with another component by reading its output, never by copying its rules

**Scope:** everywhere · **From:** P2, P3 · **Checked by:** review, test · **Class:** defect

**Finding:** Code that re-implements a marshaller's, parser's, loader's or protocol peer's rules (escaping, ordering,
defaults) to predict its output, instead of calling it or parsing what it really produces.

A second copy of another component's rules is a defect waiting for the first input on which the two disagree. Render
through the real component, parse its real output, and test against it.

### G-13.7 A check asserts what something means, not how it is written

**Scope:** everywhere · **From:** P1, P3 · **Checked by:** review, test · **Class:** defect

**Finding:** A validation or a test assertion that depends on representation where meaning was intended: substring
search in serialised text, list order or identity where order carries no meaning, byte counts across two encodings.

State the property in one sentence, then assert that property on parsed values. If the assertion mentions ordering,
escaping, whitespace or a container's shape, it asserts a representation and will refuse something legitimate. A
correct predicate can be unit-tested against every shape the environment might produce, without that environment.

### G-13.8 Every behaviour change comes with a test that fails without it

**Scope:** everywhere · **From:** P2, P3 · **Checked by:** test, review · **Class:** rule

**Finding:** A change to behaviour (a fix, a feature, a changed default) whose tests pass before and after it.

The test is written against the behaviour, not the implementation: a fix's test reproduces the reported failure. A
timing-dependent behaviour is tested by counts and states, not by sleeps (G-11.5).

### G-13.9 Mechanical changes are made by a tool, proven by the build, and committed alone

**Scope:** everywhere · **From:** P1, P4 · **Checked by:** build, review · **Class:** rule

**Finding:** A sweep (adding `final`, reordering imports, renaming across files, reformatting) made by hand, or mixed
with any other change.

A tool applies the change, the build and the full test suite prove it, and a second run of the tool reports nothing
left. The commit contains only that change, so a reviewer can trust it without reading every line.

### G-13.10 A performance claim states its measurement

**Scope:** everywhere · **From:** P2 · **Checked by:** measure, review · **Class:** rule

**Finding:** A change justified by speed, allocation or latency with no before-and-after numbers, or numbers without the
method, the machine and the load.

Measure with a harness that defeats dead-code elimination and warm-up effects (JMH for code, a profiler or JFR for a
running system). Report the median and the spread, the machine, its load during the run and the command. Keep a change
for speed only if the measurement shows a gain beyond the noise.

### G-13.11 Latency under load is measured open-loop

**Scope:** everywhere · **From:** P2 · **Checked by:** measure · **Class:** rule

**Finding:** A latency figure from a closed-loop client (one that waits for each response before sending the next), reported without correction for coordinated omission.

A closed-loop client sends less while the server stalls, so the stall hides from
the histogram. A load test issues requests on a schedule independent of the
responses, or corrects for the missed sends (HdrHistogram's
`recordValueWithExpectedInterval`), and reports percentiles up to the maximum
(G-14.3).

### G-13.12 A change to a public API, a serialised form or a default is checked for compatibility

**Scope:** everywhere · **From:** P4, P5 · **Checked by:** build, review · **Class:** rule

**Finding:** A change to a public signature of a published library, to a serialised or wire form, or to a default value, with no compatibility check and no changelog entry.

A binary-compatibility check against the last release (japicmp, revapi) runs in
CI for published libraries. A changed default is a behaviour change (G-13.8) and
is named in the changelog, because callers who never set the value get the new
behaviour without changing a line.

---

## 14. Observability

*Scope:* each rule's Scope line: G-14.1 everywhere except hot path; G-14.2, G-14.7, G-14.11 and G-14.12 *skip
unless* long-running service; G-14.5 hot path; G-14.6 *skip unless* latency budget; G-14.10 *skip unless* remote calls;
the others everywhere.

### G-14.1 A path that does durable or remote work logs its whole lifecycle

**Scope:** everywhere except hot path · **From:** P6 · **Checked by:** review · **Class:** rule

**Finding:** A path that accepts, queues, sends, persists or executes work on behalf of someone else and logs only its
failures, or logs steps without one key that ties them together.

Log at INFO, keyed by one identifier (request, command, message or job id): accepted, handed to the next component,
completed, and each non-success outcome with what happens next (retried, kept, dropped). A path that is silent when it
works cannot answer "did it happen?", which is the first question an operator asks.

On a hot path the lifecycle is counted (G-14.7) and recorded as a JFR event (G-14.6), not logged per item.

### G-14.2 Every bound shows its usage

**Scope:** skip unless long-running service · **From:** P6 · **Checked by:** review · **Class:** rule

**Finding:** A bounded queue, pool, cache, buffer or rate limit whose current usage cannot be read beside its limit.

Expose usage and limit together (queue depth and capacity, permits in use and total, entries and bound), as a metric
or in a health view. A bound that is reached without anyone seeing it approach looks, from outside, like a hang.

### G-14.3 Latency is a distribution, never only an average

**Scope:** everywhere · **From:** P2, P6 · **Checked by:** review · **Class:** rule

**Finding:** A latency or duration recorded only as a mean, a sum or a last value.

Record a histogram from which percentiles and the maximum can be read. The tail is where users wait and where
contention, pauses and retries show; a mean hides all three.

### G-14.4 Metric names carry their unit; labels have bounded cardinality

**Scope:** everywhere · **From:** P5, P6 · **Checked by:** review · **Class:** rule

**Finding:** A metric name without its unit or kind, or a label whose values come from user input, identifiers, paths,
messages or anything else without a fixed bound.

Name the unit and kind in the name (`…_seconds`, `…_bytes`, `…_total`) and keep labels to small, closed sets. An
unbounded label grows the metric store with traffic and turns monitoring into an outage of its own.

### G-14.5 Counters on a hot path do not share a contended write

**Scope:** hot path · **From:** P3, P6 · **Checked by:** measure, review · **Class:** rule

**Finding:** One counter (an `Atomic*`, field updater, `VarHandle` or `volatile` field that is incremented, or a counter under a lock) written by many threads per event, with no measurement showing the contention is negligible. Claim sequences and run-guards (§7) are not counters.

Use `LongAdder`, or per-thread or per-worker counters summed on read. A single shared counter on a per-message path is
a cache line every core writes, and its cost grows with the number of writing threads; measure it (G-13.10) before
keeping it. When the count only needs to be approximate, say so, and accept the cheaper structure.

### G-14.6 Operations whose latency matters emit JFR events

**Scope:** skip unless latency budget · **From:** P6 · **Checked by:** review · **Class:** rule

**Finding:** An operation with a latency budget and no JFR event, or hand-written timing that only logs a duration. A histogram metric (G-14.3) beside the event is not a finding.

Define a `jdk.jfr.Event` subclass per operation with a stable `@Name`, `@Label` and the fields an analysis needs (the
key, the size, the outcome); `begin()`/`commit()` around the operation; thresholds set by configuration, not code. A
disabled event costs a clock read in `begin()`, an enabled check in `commit()` and the event object, which escape
analysis removes only when the code inlines; compute expensive fields only under `shouldCommit()`, and measure the
disabled cost on a hot path (G-13.10). An enabled event is recorded beside the JVM's own events, so a stall can be
tied to a GC pause, a lock or a park.

### G-14.7 Failures are counted, and a recurring failure is not logged per occurrence

**Scope:** skip unless long-running service · **From:** P6 · **Checked by:** review · **Class:** rule

**Finding:** A failure class with no counter, or a failure that can recur per event logged once per occurrence without
a rate limit or aggregation.

Count each failure class. Log the first occurrence with its exception, then aggregate (count and last cause per
interval). A log flood hides the next, different failure and costs the hot path its latency.

### G-14.8 Every log line and metric has a reader

**Scope:** everywhere · **From:** P5, P6 · **Checked by:** review · **Class:** rule

**Finding:** A metric, gauge or log line that answers no question an operator or developer would ask, or duplicates one
that does.

The javadoc or the metric description names the question. Telemetry without a reader costs storage, attention and, on
a hot path, latency.

### G-14.9 Durations come from a monotonic clock and are compared by subtraction

**Scope:** everywhere · **From:** P1, P3 · **Checked by:** review · **Class:** defect

**Finding:** A duration or timeout computed from wall-clock time, or `System.nanoTime()` values compared with `<` or `>` instead of by subtraction (`t1 - t0 < 0`). (A time value without its unit is G-14.13.)

Measure durations with `System.nanoTime()`, and compare its values only by
subtraction, since the values may wrap: a deadline is `start + timeout`, and it has passed when
`System.nanoTime() - deadline >= 0`. Use wall-clock time only for timestamps a human or another system reads,
in UTC, and say so where printed. Every time value carries its unit (G-14.13).

### G-14.10 The trace context crosses process boundaries

**Scope:** skip unless remote calls · **From:** P6 · **Checked by:** review, test · **Class:** rule

**Finding:** An outgoing call or message that does not carry the current trace or request id, or a receiver that starts a new one when an id arrived.

The id of G-14.1 travels in every outgoing request or message (W3C
`traceparent`, or the protocol's own header) and is read back on receipt, so one
operation's logs, events and spans join across processes.

### G-14.11 A long-running service runs a bounded continuous JFR recording

**Scope:** skip unless long-running service · **From:** P6 · **Checked by:** review · **Class:** rule

**Finding:** A service launched without a continuous recording, or with one that has no age or size bound.

`-XX:StartFlightRecording` with `maxage` and `maxsize`, and settings that enable
lock, park, pinning and allocation events with thresholds, so a stall can be read
after it happened, not reproduced. The bound keeps the disk cost fixed.

### G-14.12 A thread that owns latency measures its own stalls

**Scope:** skip unless long-running service · **From:** P6 · **Checked by:** review, test · **Class:** rule

**Finding:** A UI thread, event loop or single-writer loop with no measurement that logs a stall over its budget, with the stack that caused it, while the stall lasts.

A watchdog on another thread probes the loop on a fixed period; a stall is logged when it starts, not only when it
ends, so a loop that never returns is still seen (G-7.11).

### G-14.13 A time value carries its unit

**Scope:** everywhere · **From:** P1 · **Checked by:** review · **Class:** rule

**Finding:** A numeric time value (field, parameter, local, setting) whose name does not carry its unit.

`timeoutMillis`, `startNanos`; off the hot path a `Duration` or `Instant` carries the unit in its type. A bare
`timeout` read as seconds by one reader and milliseconds by another is a wrong result waiting for a caller.

---

## 15. Distributed systems

*Scope:* each rule's condition (remote calls, messaging, shared state across nodes, persisted or wire formats, batch
or fan-out calls); G-15.6 and G-15.11 everywhere.

### G-15.1 Every remote call has a deadline

**Scope:** skip unless remote calls · **From:** P5 · **Checked by:** review, test · **Class:** defect

**Finding:** A remote call, connect or read with no timeout; a timeout that is not derived from the caller's remaining deadline; or a retry loop whose attempts and backoff can outlast that deadline.

Every connect, request and read has a bound. The caller passes an absolute deadline (a `System.nanoTime()` value in
process, the remaining budget in a wire field); each hop's timeout is the smaller of its own timeout and the remaining
budget less a margin, and a hop with no budget left fails without calling. Retries (G-15.2) spend the same deadline:
no attempt starts that cannot finish before it.

### G-15.2 Retries are bounded, backed off, jittered, and only for safe operations

**Scope:** skip unless remote calls · **From:** P3, P5 · **Checked by:** review, test · **Class:** defect

**Finding:** A retry without an attempt limit, without exponential backoff and jitter, on an error not classified as
retryable, or of an operation that is neither idempotent nor carries an idempotency key.

Classify errors as retryable (timeouts, unavailable, throttled) or not (rejected, invalid). Retry only operations that
are idempotent or carry a key the receiver deduplicates on. Jitter spreads the retries of many clients so a recovering
peer is not hit by all of them at once.

### G-15.3 Only one layer retries an operation

**Scope:** skip unless remote calls · **From:** P5 · **Checked by:** review · **Class:** defect

**Finding:** An operation retried both by a client library and by its caller, or by more than one layer of a call
chain.

Retries multiply across layers: three layers of three attempts make twenty-seven calls into a peer that is already
failing. Name the layer that retries; the others fail fast.

### G-15.4 Consumers match their delivery semantics: an at-least-once consumer is idempotent

**Scope:** skip unless messaging · **From:** P1, P3 · **Checked by:** review, test · **Class:** defect

**Finding:** An at-least-once consumer that is not idempotent, or an effectively-once claim whose deduplication record and effect do not commit atomically. (A producer or consumer that does not state its semantics is G-15.14.)

At-least-once delivery means duplicates: the consumer deduplicates by a key or makes its effect idempotent.
Effectively-once is at-least-once plus deduplication, stated with where the deduplication state lives and how long.

Deduplication gives effectively-once only when the deduplication record and the effect commit atomically (one
transaction, or the message id as the effect's own key in a conditional write), and the deduplication state is kept
longer than the longest redelivery delay the broker allows. State both.

### G-15.5 Ordering is per key, and stated

**Scope:** skip unless messaging · **From:** P1, P3 · **Checked by:** review · **Class:** defect

**Finding:** Code that relies on an order across keys, partitions, connections or nodes that the system does not
guarantee.

State which order is guaranteed (per key, per connection, per partition) and rely on nothing wider.

### G-15.6 Every queue between components is bounded, with an explicit policy when full

**Scope:** everywhere · **From:** P3, P5 · **Checked by:** review, test · **Class:** defect

**Finding:** An unbounded queue or buffer between components this code owns (an executor's work queue included), or a bounded one with no stated policy when full. A UI toolkit's event queue is not a finding.

The policy is one of: block with a timeout, reject with a signal the producer handles, or drop with a counter
(G-14.2). An unbounded queue turns overload into memory exhaustion and latency into minutes. Admit or reject work at
the edge rather than queue it inside.

### G-15.7 Exclusive actions are fenced, not believed

**Scope:** skip unless shared state across nodes · **From:** P3 · **Checked by:** review, test · **Class:** defect

**Finding:** A node that acts as leader, owner or single writer without a fencing token that the shared resource checks on every write (a monotonically increasing epoch, term or version). A lease alone does not resolve it.

A paused process (GC, swap, a stopped container) can wake after its lease ended and write as if it still held it. A
lease limits how long a belief lasts, not what a paused holder can write; the resource rejects writes that carry an
older token than the last one it accepted. Where the resource cannot check a token, the action is not exclusive: say
so, and make the write idempotent or conditional (a compare-and-set on a version).

### G-15.8 Clocks of different nodes do not order events

**Scope:** skip unless shared state across nodes · **From:** P2, P3 · **Checked by:** review · **Class:** defect

**Finding:** Wall-clock timestamps from different nodes compared to decide which event came first or which write wins.

Use sequence numbers, version vectors, a hybrid logical clock, or the timestamp of the one node that owns the decision.

### G-15.9 Wire and stored formats are versioned and read one version back

**Scope:** skip unless persisted or wire formats · **From:** P5 · **Checked by:** test, review · **Class:** defect

**Finding:** A format with no version field; a reader that cannot read the previous version; a new writer whose output the previous version cannot read while both run; or unknown fields dropped silently where they must be kept or rejected.

A rolling upgrade runs two versions at once; a format that cannot be read by the other version stops the upgrade or
loses data.

A new field is written only after every reader understands it (two releases: read it, then write it). The test reads
the previous version's data with the current reader, and the current writer's data with the previous reader.

### G-15.10 Partial failure is a result

**Scope:** skip unless batch or fan-out calls · **From:** P1, P6 · **Checked by:** review, test · **Class:** defect

**Finding:** A batch or fan-out operation that fails as a whole, or reports success as a whole, when some items
succeeded and some failed.

Return an outcome per item. One failed item neither hides the others' results nor makes the caller redo the ones that
succeeded.

### G-15.11 An enum is never persisted or sent by its ordinal

**Scope:** everywhere · **From:** P3, P5 · **Checked by:** review, test · **Class:** defect

**Finding:** An `ordinal()` written to a file, a database, a wire format or a cache shared across versions, or `values()[i]` used to read one back.

Reordering or inserting a constant changes every ordinal after it, so data
written by one build reads back as a different value in the next. Persist an
explicit code (an `int` field or a name) that a test pins.

### G-15.12 Retries spend a budget, and stop when the peer is failing

**Scope:** skip unless remote calls · **From:** P3, P5 · **Checked by:** review, test · **Class:** defect

**Finding:** A retry policy with no budget or circuit breaker, so a failing peer receives more calls than a healthy one, or a throttling reply retried before its stated delay.

A client keeps retries below a fixed share of its calls (a retry budget), or
opens a circuit after consecutive failures and probes before closing it; a
throttling reply's stated delay (`Retry-After`) is honoured.

### G-15.13 Shutdown drains before it closes

**Scope:** skip unless remote calls · **From:** P5, P6 · **Checked by:** test · **Class:** defect

**Finding:** A shutdown that closes connections or pools while requests are in flight, or that waits for them with no deadline.

The order is: report not ready, stop admitting work, finish or hand back the work
in flight within a deadline, then close what is owned (G-7.7, G-4.5). Work not
finished by the deadline is reported, not dropped silently.

### G-15.14 Producers and consumers state their delivery semantics

**Scope:** skip unless messaging · **From:** P1 · **Checked by:** review · **Class:** rule

**Finding:** A producer or consumer whose javadoc does not state at-most-once, at-least-once or effectively-once.

The guarantee is the contract its callers and peers build on; unstated, every reader guesses, and G-15.4 cannot be
checked.

---

## 16. Current Java

*Scope:* the JDK 25 baseline; each rule's Scope line decides (G-16.5 and G-16.7 everywhere except hot path, G-16.9
*skip unless* native code, the others everywhere). Preview features are not used unless the repository's Apply section
enables them (G-16.10).

### G-16.1 A closed set of cases is a sealed hierarchy, switched over exhaustively

**Scope:** everywhere · **From:** P1, P7 · **Checked by:** build, review · **Class:** rule

**Finding:** A closed set of cases modelled as an open hierarchy, a chain of `instanceof` tests over it, or a
`default` branch in a `switch` over a sealed type.

A sealed interface with record implementations, matched by a `switch` with no `default`, makes the compiler find every
place a new case must be handled. On a hot path where the dispatch shows in a profile, an `int` tag (G-1.10) is used
instead.

```java
sealed interface Outcome permits Done, Retry, Failed {}
record Done(long offset) implements Outcome {}
record Retry(Duration after) implements Outcome {}
record Failed(String reason, Throwable cause) implements Outcome {}

long next(final Outcome outcome) {
    return switch (outcome) {
        case Done(long offset) -> offset;
        case Retry(Duration after) -> schedule(after);
        case Failed(String reason, Throwable cause) -> fail(reason, cause);
    };
}
```

### G-16.2 Patterns deconstruct; casts after type tests do not

**Scope:** everywhere · **From:** P1, P7 · **Checked by:** review · **Class:** rule

**Finding:** An `instanceof` test followed by a cast of the same value, or, after a type test or in a `switch` case, a record's accessors called one by one where the pattern of that test could bind them.

A pattern names the type once and binds what is used, so a later change of type cannot leave a stale cast. A pattern does not match `null`: where the value can be `null`, the code says what happens then, instead of relying on an accessor's `NullPointerException`.

### G-16.3 A deliberately unused variable is `_`

**Scope:** everywhere · **From:** P1, P7 · **Checked by:** review · **Class:** rule

**Finding:** An unused lambda parameter, catch parameter, pattern binding or loop variable given a name (`ignored`,
`unused`, `e`) instead of `_`.

`_` tells the reader the value is ignored on purpose, and the compiler rejects any later use of it.

### G-16.4 Virtual threads carry blocking work, one task each; they are never pooled

**Scope:** everywhere · **From:** P3, P7 · **Checked by:** review, measure · **Class:** rule

**Finding:** A platform-thread pool sized to the number of concurrent blocking calls, a pool of virtual threads, virtual threads used for CPU-bound work or for file I/O that can block, or `ThreadLocal` caches on code that runs on virtual threads. (Bounding virtual threads against a resource is G-16.13.)

Blocking I/O fan-out (one task per request, connection or file) runs on virtual threads created per task, owned per G-7.10 and named per
G-7.14. CPU-bound work runs on a bounded set of platform threads. Since JDK 24 `synchronized` no longer pins a virtual
thread to its carrier; native frames still do, so a native call that blocks belongs on a platform thread.

Blocking file I/O (an open, read or write on a file, FIFO or device) holds the carrier: measured on Temurin 25 with
two carriers, 16 virtual threads blocked in a FIFO `open` or a `RandomAccessFile.read` left 14 of them unscheduled for
3 s, and the scheduler added no carrier (`jdk.virtualThreadScheduler.maxPoolSize=6` changed nothing). File I/O that
can block runs on platform threads.
Code that runs on virtual threads does not use `ThreadLocal` caches (G-2.4, G-3.3, G-5.1): each task is a new thread,
so the cache is filled once per task. Pass the scratch object explicitly, or keep that work on a platform thread.

### G-16.5 Context passed down a call tree is a `ScopedValue`

**Scope:** everywhere except hot path · **From:** P1, P5, P7 · **Checked by:** review · **Class:** rule

**Finding:** A `ThreadLocal` that is set before a call and cleared after it to pass context (a request id, a principal, a deadline) to code below on the same thread, or a task handed to another thread that reads a scoped value without binding it inside the task.

A `ScopedValue` (final in JDK 25) is bound for the duration of a call; code below can rebind it for its own callees but
cannot change the caller's binding. It is inherited only by threads forked by `StructuredTaskScope`, a preview API in
JDK 25 (G-16.10): a task submitted to an executor sees the value unbound, so context that crosses a thread hand-off is
captured in the task and bound again inside it:

```java
final RequestId id = REQUEST_ID.get();                          // read on the submitting thread
executor.submit(() -> ScopedValue.where(REQUEST_ID, id).run(() -> handle(job)));
```

A task that reads a scoped value it was not given sees it unbound, and `get()` throws; `orElse` would hide the loss,
so it is used only where an absent value is a valid state. `ThreadLocal` remains the tool for per-thread scratch
objects on platform threads (G-3.3).

### G-16.6 Sequenced collections are read by their ends, not by index arithmetic

**Scope:** everywhere · **From:** P1, P7 · **Checked by:** review · **Class:** rule

**Finding:** In code the change adds, on a `java.util` sequenced collection, `list.get(list.size() - 1)`, `list.get(0)` meant as the first element, or a reversed copy built to iterate backwards, where `getLast()`, `getFirst()` or `reversed()` would do. A project collection follows its own contract (G-1.6).

The method names the intent. `getFirst()` and `getLast()` throw `NoSuchElementException` on an empty collection where `get(0)` throws `IndexOutOfBoundsException`, so existing calls change only where no caller depends on the old exception.

### G-16.7 Off the hot path, a stream collects with `toList()`

**Scope:** everywhere except hot path · **From:** P1, P7 · **Checked by:** review · **Class:** rule

**Finding:** `collect(Collectors.toList())` or `collect(Collectors.toUnmodifiableList())` whose result does not leave the method and is not modified in it. `toUnmodifiableList()` whose rejection of `null` elements the method relies on, said in a comment, is not a finding.

`Stream.toList()` returns an unmodifiable list and allows `null` elements; `toUnmodifiableList()` rejects them. A list
returned or stored keeps its collector unless every reader is in the change, since a caller that modifies it would
fail at run time.

### G-16.8 Constructor arguments are validated before `super(...)`

**Scope:** everywhere · **From:** P1, P7 · **Checked by:** review · **Class:** rule

**Finding:** A static helper method that exists only to validate or compute an argument for `super(...)` or
`this(...)`.

Flexible constructor bodies (final in JDK 25) allow statements before the explicit constructor call that do not read
`this` or call its methods; they may assign the class's own fields that have no initialiser.

### G-16.9 Native code is called through the FFM API

**Scope:** skip unless native code · **From:** P5, P7 · **Checked by:** review · **Class:** rule

**Finding:** New JNI code, `sun.misc.Unsafe` memory access, `Arena.global()` without a recorded departure, native memory freed by the GC used per operation (G-4.7), or a launcher that does not pass `--enable-native-access`.

`java.lang.foreign` (final in JDK 22) calls native functions without C glue code; an `Arena` bounds the lifetime of the
memory it allocates (G-4.7).

Every launcher passes `--enable-native-access=<module>` (or `ALL-UNNAMED`): restricted calls warn in JDK 25 and are to
be denied later. Confined arenas (`Arena.ofConfined()`) are the default; a shared arena is long-lived, never one per
operation, because closing it coordinates with every thread.

### G-16.10 Not used without a recorded decision: preview features, module imports, implicit `var`

**Scope:** everywhere · **From:** P1, P5 · **Checked by:** build, review · **Class:** rule

**Finding:** A preview feature in a repository whose Apply section does not enable it, an `import module` declaration, or `var` where the right-hand side is not a constructor call without a diamond or a cast.

Preview features change between releases and need `--enable-preview` everywhere the code runs. `import module`
(final in JDK 25) hides which types a file uses, against G-10.11. `var` is used only where the right-hand side names
the type, in a constructor call or a cast; a factory call such as `List.of(...)` does not name it, and a diamond
(`new ArrayList<>()`) does not name the type arguments, so there the type is written for the reader.

### G-16.11 Doc comments use one form per kind of source

**Scope:** everywhere · **From:** P1, P7 · **Checked by:** test, review · **Class:** rule

**Finding:** Main code mixing `///` and `/** */` doc comments within one repository, or tests not following G-11.7.

Tests use `///` Markdown comments (G-11.7). Main code uses the form the repository's Apply section names; a change does
not mix the two.

### G-16.12 A spin-wait calls `Thread.onSpinWait()`, is bounded, and runs only on platform threads

**Scope:** everywhere · **From:** P3, P7 · **Checked by:** review · **Class:** rule

**Finding:** A busy-wait loop without `Thread.onSpinWait()`, without a bound after which it parks (G-7.6), or on a virtual thread.

`Thread.onSpinWait()` lets the processor pause the loop and yield its pipeline to
the sibling hyper-thread. A virtual thread that spins holds its carrier and
starves the other virtual threads scheduled there.

### G-16.13 Virtual threads against one resource are bounded before they are created, and every permit is released

**Scope:** everywhere · **From:** P3, P5 · **Checked by:** review, test · **Class:** defect

**Finding:** Virtual threads started per task with no bound, taken before the task is created, on how many are in flight against one resource; or a permit acquired without a `try`/`finally` that releases it on every path, failure and cancellation included.

A semaphore acquired inside each task bounds the tasks that hold the resource, not the tasks that exist: under
overload, millions of virtual threads can wait for a permit and exhaust the heap. Acquire (with a timeout) before
creating the task, or admit at the edge (G-15.6); size the bound from the resource's limit; make the bound and its
usage visible (G-14.2). A permit that a failing task keeps is gone until every later request times out.

```java
if (!permits.tryAcquire(admitTimeoutMillis, TimeUnit.MILLISECONDS)) {
    throw Rejected.overloaded("downstream");                    // admission refused: the caller sees it
}
try {
    Thread.ofVirtual().name("fetch-", seq++).start(() -> {
        try {
            fetch(request);
        } finally {
            permits.release();
        }
    });
} catch (final RuntimeException | Error e) {
    permits.release();                                          // the task never started
    throw e;
}
```

