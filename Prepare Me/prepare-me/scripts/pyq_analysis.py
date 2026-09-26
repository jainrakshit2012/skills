#!/usr/bin/env python3
"""
pyq_analysis.py - turn tagged previous-year questions (PYQs) into exact weightage and frequency tables.
Python 3.8+, standard library only.

Input: a CSV with one row per question or sub-question, written by Claude from the student's
uploaded papers. This script only counts, so every number in the report is exact.

  paper,qno,marks,unit,topic,question
  May 2024,1a,2,1,Normalization,Define 2NF with an example.
  May 2024,3,10,2,Transactions,Explain ACID properties with a neat diagram.

Optional syllabus file (one topic per line, "unit|topic" or just "topic") lists topics that were
never asked, so they are not forgotten.

Examples
  python pyq_analysis.py prep/pyq/dbms.csv
  python pyq_analysis.py prep/pyq/dbms.csv --syllabus prep/pyq/dbms_topics.txt --out prep/pyq/dbms_report.md
"""

import argparse
import csv
import difflib
import re
import sys
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
SEASONS = {"summer": 5, "winter": 12, "spring": 4, "autumn": 10, "odd": 12, "even": 5}
# Instruction words that change between years while the concept stays the same
INSTRUCTIONS = re.compile(
    r"\b(with (a )?neat (labelled )?(diagram|sketch)s?|with (a )?suitable examples?|with (an )?examples?|"
    r"write (a )?short notes? on|short notes? on|what do you (mean|understand) by|what (is|are)|"
    r"explain|describe|discuss|define|briefly|in detail|differentiate between|distinguish between|"
    r"compare|illustrate|state|list|give|derive|elaborate|justify|write|mention|enumerate)\b")
STOP = set("a an the of in on and or to for with its is are by using between how why which what "
           "their this that any two three four various different".split())
REQUIRED = ["paper", "qno", "marks", "unit", "topic", "question"]


def paper_key(name, order):
    low = name.lower()
    year = re.search(r"(19|20)\d{2}", low)
    month = next((v for k, v in MONTHS.items() if k in low), None) or \
        next((v for k, v in SEASONS.items() if k in low), 0)
    return (int(year.group(0)) if year else 9999, month, order)


def concept(q):
    q = re.sub(r"^\s*(q(uestion)?\.?\s*)?\d+\s*[a-z]?[).:-]?\s*", "", q.lower())
    q = INSTRUCTIONS.sub(" ", q)
    q = re.sub(r"[^a-z0-9+ ]", " ", q)
    return [w for w in q.split() if w not in STOP]


def same_question(a, b):
    ta, tb = set(a), set(b)
    if not ta or not tb:
        return False
    jaccard = len(ta & tb) / len(ta | tb)
    ratio = difflib.SequenceMatcher(None, " ".join(a), " ".join(b)).ratio()
    return jaccard >= 0.6 or ratio >= 0.8


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def fmt(x):
    return f"{x:g}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--syllabus", help="text file of syllabus topics, 'unit|topic' or 'topic' per line")
    ap.add_argument("--out", help="also write the report to this markdown file")
    a = ap.parse_args()

    with open(a.csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cols = [c.strip().lower() for c in reader.fieldnames or []]
        missing = [c for c in REQUIRED if c not in cols]
        if missing:
            sys.exit(f"CSV is missing columns: {', '.join(missing)}. Needed: {','.join(REQUIRED)}")
        rows = [{k.strip().lower(): (v or "").strip() for k, v in r.items() if k} for r in reader]
    rows = [r for r in rows if r["paper"] and r["question"]]
    if not rows:
        sys.exit("No questions found in the CSV.")

    out, warn = [], []
    p = out.append

    first_seen = {}
    for r in rows:
        first_seen.setdefault(r["paper"], len(first_seen))
    papers = sorted(first_seen, key=lambda n: paper_key(n, first_seen[n]))
    n_papers = len(papers)
    blank_marks = sum(1 for r in rows if num(r["marks"]) is None)
    if blank_marks:
        warn.append(f"{blank_marks} question(s) have no marks; counted as 0 marks.")
    for r in rows:
        r["m"] = num(r["marks"]) or 0.0
        r["unit"] = r["unit"] or "?"
        r["topic"] = r["topic"] or "(untagged)"

    paper_marks = defaultdict(float)
    paper_count = defaultdict(int)
    for r in rows:
        paper_marks[r["paper"]] += r["m"]
        paper_count[r["paper"]] += 1

    p(f"# PYQ analysis: {a.csv}\n")
    p(f"**Papers analysed ({n_papers}):** " + "; ".join(
        f"{x} ({fmt(paper_marks[x])} marks tagged, {paper_count[x]} questions)" for x in papers))
    p("\nFrequency shows what has been asked before, not what will be asked. Where papers offer a choice "
      "(Q2a OR Q2b), both options are counted.")
    if n_papers < 3:
        p(f"\n**Only {n_papers} paper(s): treat the tiers below as weak evidence.** 3 to 5 recent papers give a "
          "much better picture.")
    warn_at = len(out)   # warnings are inserted here, above the tables they affect

    # Unit weightage
    unit_paper = defaultdict(lambda: defaultdict(float))
    for r in rows:
        unit_paper[r["unit"]][r["paper"]] += r["m"]
    total_all = sum(paper_marks.values()) or 1
    p("\n## Unit weightage (marks per paper)\n")
    p("| Unit | " + " | ".join(papers) + " | Total | Share | Asked in |")
    p("|---|" + "---|" * (n_papers + 3))
    unit_order = sorted(unit_paper, key=lambda u: (num(u) is None, num(u) or 0, u))
    for u in unit_order:
        cells = [fmt(unit_paper[u].get(x, 0)) for x in papers]
        tot = sum(unit_paper[u].values())
        asked = sum(1 for x in papers if unit_paper[u].get(x, 0) > 0)
        p(f"| {u} | " + " | ".join(cells) + f" | {fmt(tot)} | {100 * tot / total_all:.0f}% | {asked}/{n_papers} |")

    # Topic frequency
    topics = defaultdict(lambda: {"papers": set(), "times": 0, "marks": 0.0, "unit": set(), "marks_list": []})
    for r in rows:
        t = topics[r["topic"]]
        t["papers"].add(r["paper"])
        t["times"] += 1
        t["marks"] += r["m"]
        t["unit"].add(r["unit"])
        if num(r["marks"]) is not None:
            t["marks_list"].append(r["m"])

    def tier(k):
        share = k / n_papers
        return "High" if share >= 0.6 else "Medium" if share >= 0.3 else "Low"

    p("\n## Topics by frequency\n")
    p("Tier: High = asked in at least 60% of papers, Medium = 30-59%, Low = under 30%.\n")
    p("| Tier | Topic | Unit | Papers (of " + str(n_papers) + ") | Times asked | Total marks | Usual marks | Last asked |")
    p("|---|---|---|---|---|---|---|---|")
    for name, t in sorted(topics.items(), key=lambda kv: (-len(kv[1]["papers"]), -kv[1]["marks"], kv[0])):
        k = len(t["papers"])
        ml = t["marks_list"]
        usual = fmt(max(sorted(set(ml), reverse=True), key=ml.count)) if ml else "?"
        last = max(t["papers"], key=lambda n: paper_key(n, first_seen[n]))
        p(f"| {tier(k)} | {name} | {', '.join(sorted(t['unit']))} | {k} | {t['times']} | {fmt(t['marks'])} | "
          f"{usual} | {last} |")

    names = sorted(topics)
    for i, x in enumerate(names):
        for y in names[i + 1:]:
            if difflib.SequenceMatcher(None, x.lower(), y.lower()).ratio() >= 0.85:
                warn.append(f"Topic names '{x}' and '{y}' look like the same topic; use one name and re-run.")

    # Repeated questions
    concepts = [concept(r["question"]) for r in rows]
    parent = list(range(len(rows)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if rows[i]["paper"] != rows[j]["paper"] and same_question(concepts[i], concepts[j]):
                parent[find(i)] = find(j)
    groups = defaultdict(list)
    for i in range(len(rows)):
        groups[find(i)].append(rows[i])
    repeats = [g for g in groups.values() if len({r["paper"] for r in g}) >= 2]
    repeats.sort(key=lambda g: (-len({r["paper"] for r in g}), -sum(r["m"] for r in g)))

    p("\n## Repeated questions (same or nearly the same question in different papers)\n")
    if not repeats:
        p("No question repeats across these papers.")
    for n, g in enumerate(repeats, 1):
        g.sort(key=lambda r: paper_key(r["paper"], first_seen[r["paper"]]))
        k = len({r["paper"] for r in g})
        p(f"**{n}. {g[-1]['question']}** (asked in {k} of {n_papers} papers)")
        for r in g:
            p(f"- {r['paper']}, Q{r['qno']} ({fmt(r['m'])} marks): {r['question']}")
        p("")

    # Syllabus topics never asked
    if a.syllabus:
        with open(a.syllabus, encoding="utf-8-sig") as f:
            syl = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        asked = {t.lower() for t in topics}
        never = []
        for line in syl:
            unit, _, topic = line.rpartition("|")
            best = max((difflib.SequenceMatcher(None, topic.lower(), t).ratio() for t in asked), default=0)
            if best < 0.8:
                never.append((unit.strip() or "?", topic.strip()))
        p("\n## Syllabus topics not asked in these papers\n")
        p("Lower priority, not zero priority: a topic can appear for the first time in any year.\n")
        if never:
            for unit, topic in never:
                p(f"- Unit {unit}: {topic}")
        else:
            p("Every syllabus topic has been asked at least once.")

    if warn:
        out[warn_at:warn_at] = ["\n## Fix these first\n"] + [f"- {w}" for w in warn]

    report = "\n".join(out)
    print(report)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(report + "\n")
        print(f"\n(Report written to {a.out})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
