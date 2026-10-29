#!/usr/bin/env python3
"""Count results from a filled session log.

Usage: python3 tally.py private/session1.csv
       python3 tally.py --selftest
"""
import csv
import math
import statistics
import sys
from collections import defaultdict


def sign_test(a, b):
    """Exact two-sided sign test on the two kinds of discordant pairs."""
    n = a + b
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(a, b) + 1)) / 2**n)


def yes(value):
    return value.strip().lower() in ("y", "yes")


def matches(row):
    return row["answer_type"].strip() in row["gold_type"].split("|")


def timing(rows):
    xs = [float(r["first_words_s"]) for r in rows if r["first_words_s"].strip()]
    if not xs:
        return "no timings"
    return f"median {statistics.median(xs):.1f}s, max {max(xs):.1f}s (n={len(xs)})"


def tally(rows):
    main = [r for r in rows if r["run"] == "1" and r["answer_type"].strip()]

    def group(kind, version):
        return [r for r in main if r["kind"] == kind and r["version"] == version]

    simple, complex_ = group("depth", "simple"), group("depth", "complex")
    trap_a, trap_b = group("trap", "A"), group("trap", "B")
    builds = sorted({r["build"].strip() for r in main if r["build"].strip()})
    out = [f"Builds: {', '.join(builds) or 'not recorded'}"]

    out.append(f"Depth, simple answered directly (type 1-2): {sum(map(matches, simple))}/{len(simple)}; "
               f"visible thinking on {sum(yes(r['thinking']) for r in simple)}; correct {sum(yes(r['correct']) for r in simple)}")
    out.append(f"Depth, complex in an allowed type: {sum(map(matches, complex_))}/{len(complex_)}; "
               f"visible thinking on {sum(yes(r['thinking']) for r in complex_)}; "
               f"Report/artifact on {sum(r['answer_type'].strip() == '4' for r in complex_)}; "
               f"asked a question on {sum(r['answer_type'].strip() == '5' for r in complex_)}; "
               f"correct {sum(yes(r['correct']) for r in complex_)}")

    a = {r["pair"]: yes(r["correct"]) for r in trap_a}
    b = {r["pair"]: yes(r["correct"]) for r in trap_b}
    both = sorted(a.keys() & b.keys())
    a_only = sum(a[p] and not b[p] for p in both)
    b_only = sum(b[p] and not a[p] for p in both)
    out.append(f"Trap, easy version (A) correct: {sum(a.values())}/{len(a)}")
    out.append(f"Trap, trap version (B) correct: {sum(b.values())}/{len(b)}")
    out.append(f"Trap pairs where only A was right: {a_only}; only B was right: {b_only}; "
               f"sign test p = {sign_test(a_only, b_only):.3f}")
    by_cat = defaultdict(list)
    for r in trap_b:
        by_cat[r["category"]].append(yes(r["correct"]))
    out.append("Trap version correct by category: "
               + (", ".join(f"{c} {sum(v)}/{len(v)}" for c, v in sorted(by_cat.items())) or "none"))

    for label, rs in (("depth simple", simple), ("depth complex", complex_), ("trap A", trap_a), ("trap B", trap_b)):
        out.append(f"Time to first words, {label}: {timing(rs)}")

    runs = defaultdict(list)
    for r in rows:
        if r["answer_type"].strip():
            runs[(r["pair"], r["version"])].append(r)
    repeated = [rs for rs in runs.values() if len(rs) >= 3]
    if repeated:
        same = sum(len({r["answer_type"].strip() for r in rs}) == 1 for rs in repeated)
        spreads = []
        for rs in repeated:
            xs = [float(r["first_words_s"]) for r in rs if r["first_words_s"].strip()]
            if len(xs) >= 2:
                spreads.append(max(xs) - min(xs))
        line = f"Noise check: same answer type on every run for {same}/{len(repeated)} prompts"
        if spreads:
            line += f"; median timing spread {statistics.median(spreads):.1f}s"
        out.append(line)
    return "\n".join(out)


def selftest():
    assert abs(sign_test(11, 1) - 0.00635) < 1e-4
    assert sign_test(0, 0) == 1.0 and sign_test(3, 3) == 1.0
    base = dict(sitting="1", order="1", run="1", category="date", tabs="", prompt="", gold_answer="",
                gold_type="1|2|3", build="1.55", thinking="n", first_words_s="1.0", notes="")
    rows = [dict(base, pair="t01", kind="trap", version="A", answer_type="1", correct="y"),
            dict(base, pair="t01", kind="trap", version="B", answer_type="1", correct="n"),
            dict(base, pair="d01", kind="depth", version="simple", gold_type="1|2", answer_type="3", thinking="y", correct="y")]
    text = tally(rows)
    assert "only A was right: 1; only B was right: 0" in text, text
    assert "simple answered directly (type 1-2): 0/1; visible thinking on 1" in text, text
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif len(sys.argv) == 2:
        with open(sys.argv[1], newline="") as f:
            print(tally(list(csv.DictReader(f))))
    else:
        sys.exit(__doc__)
