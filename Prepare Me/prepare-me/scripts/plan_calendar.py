#!/usr/bin/env python3
"""
plan_calendar.py - build the day-by-day skeleton of an exam study plan from a date sheet.
Python 3.8+, standard library only.

It does the date arithmetic (days left, weekdays, gaps between papers) so the plan never
miscounts, and it shares study sessions between subjects:
  - the last free day before each exam is revision for that exam
  - the evening of an exam day goes to the next exam
  - every other session is shared by weight, earliest exam first, so a subject with a short
    gap before its paper starts early
Claude then fills each session with topics.

Examples
  python plan_calendar.py --exam "DBMS=2026-10-12" --exam "OS=2026-10-14" --exam "CN=2026-10-15" \
      --weight DBMS=3 --weight CN=2 --hours 6
  python plan_calendar.py --exam "Maths-III=2026-09-28" --today 2026-09-26 --today-sessions 1
"""

import argparse
import datetime as dt
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

SESSION_NAMES = {1: ["Study"], 2: ["Morning", "Evening"], 3: ["Morning", "Afternoon", "Evening"]}


def pair(s):
    if "=" not in s:
        raise argparse.ArgumentTypeError(f"expected NAME=VALUE, got {s!r}")
    k, v = s.rsplit("=", 1)
    return k.strip(), v.strip()


def date_arg(s):
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"dates must be YYYY-MM-DD, got {s!r}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exam", action="append", type=pair, required=True,
                    help='"Subject=YYYY-MM-DD", once per paper')
    ap.add_argument("--weight", action="append", type=pair, default=[],
                    help='"Subject=N", how much study the subject needs: 1 (easy/strong) to 5 (hard/weak). Default 1')
    ap.add_argument("--today", type=date_arg, default=dt.date.today(), help="YYYY-MM-DD (default: today)")
    ap.add_argument("--today-sessions", type=int, help="sessions still left today (default: all)")
    ap.add_argument("--hours", type=float, default=6.0, help="study hours on a full free day (default 6)")
    ap.add_argument("--sessions", type=int, default=3, help="sessions per full free day (default 3)")
    ap.add_argument("--off", action="append", type=date_arg, default=[], help="YYYY-MM-DD with no study")
    ap.add_argument("--no-exam-evening", action="store_true", help="no study on exam days")
    a = ap.parse_args()

    today = a.today
    if a.sessions < 1:
        ap.error("--sessions must be at least 1")
    names = SESSION_NAMES.get(a.sessions, [f"S{i + 1}" for i in range(a.sessions)])
    hours_per = a.hours / a.sessions

    exams, warnings = [], []
    for subj, d in a.exam:
        date = date_arg(d)
        if date < today:
            warnings.append(f"{subj}: exam date {date} is before today ({today}); left out.")
            continue
        exams.append((subj, date))
    if not exams:
        print("No upcoming exams to plan for.")
        return 1
    exams.sort(key=lambda e: e[1])
    subjects = [s for s, _ in exams]
    if len(set(subjects)) != len(subjects):
        ap.error("each subject should appear once; use different names for different papers")
    exam_date = dict(exams)
    weights = {s: 1.0 for s in subjects}
    for subj, w in a.weight:
        if subj not in weights:
            ap.error(f"--weight for unknown subject {subj!r}; subjects are {subjects}")
        weights[subj] = max(0.1, float(w))
    off = set(a.off)
    exam_days = {}
    for s, d in exams:
        exam_days.setdefault(d, []).append(s)
    last = exams[-1][1]

    # 1. sessions: (date, index, label); each is due for the first exam strictly after its date
    sessions = []
    day = today
    while day < last:
        if day in off:
            pass
        elif day in exam_days:
            if not a.no_exam_evening and any(d > day for _, d in exams):
                sessions.append((day, a.sessions - 1))
        else:
            n = a.sessions
            if day == today and a.today_sessions is not None:
                n = max(0, min(a.sessions, a.today_sessions))
            for i in range(a.sessions - n, a.sessions):
                sessions.append((day, i))
        day += dt.timedelta(days=1)

    def due(sess):
        return next(s for s, d in exams if d > sess[0])

    assign = {}      # session -> (subject, kind)
    # 2. revision: sessions on the last study day before each exam date, if they are due for that exam
    for d, subs in sorted(exam_days.items()):
        before = [x for x in sessions if x[0] < d and exam_date[due(x)] == d]
        if not before:
            warnings.append(f"{', '.join(subs)}: no study time before the exam; revise from the sheets only.")
            continue
        last_day = max(x[0] for x in before)
        rev = [x for x in before if x[0] == last_day]
        for i, x in enumerate(rev):
            assign[x] = (subs[i % len(subs)], "revise")

    # 3. study: share the free sessions by weight, earliest exam first
    free = [x for x in sessions if x not in assign]
    reachable = [s for s in subjects if any(x[0] < exam_date[s] for x in free)]
    total_w = sum(weights[s] for s in reachable) or 1
    target = {s: (len(free) * weights[s] / total_w if s in reachable else 0.0) for s in subjects}
    got = {s: 0 for s in subjects}
    for x in free:
        if x[0] in exam_days:   # the evening after a paper goes to the next paper
            assign[x] = (due(x), "study")
            got[due(x)] += 1
    for x in free:
        if x in assign:
            continue
        upcoming = [s for s in subjects if exam_date[s] > x[0]]
        needy = [s for s in upcoming if got[s] + 0.5 <= target[s]]
        pick = min(needy or upcoming, key=lambda s: (exam_date[s], -weights[s]))
        assign[x] = (pick, "study")
        got[pick] += 1

    # 4. print
    print(f"Study-plan skeleton | today {today} ({today:%a}) | {a.hours:g} h on a free day = "
          f"{a.sessions} x {hours_per:g} h sessions\n")
    print("| Date | Day | " + " | ".join(names) + " | Note |")
    print("|---|---|" + "---|" * len(names) + "---|")
    day = today
    while day <= last:
        cells = []
        for i in range(a.sessions):
            x = (day, i)
            if x in assign:
                subj, kind = assign[x]
                cells.append(f"Revise {subj}" if kind == "revise" else subj)
            else:
                cells.append("-")
        note = []
        if day in exam_days:
            note.append("EXAM: " + ", ".join(exam_days[day]))
        if day in off:
            note.append("day off")
        if not (day in exam_days or day in off or any(k[0] == day for k in assign)):
            note.append("past sessions" if day == today else "")
        print(f"| {day} | {day:%a} | " + " | ".join(cells) + f" | {'; '.join(n for n in note if n)} |")
        day += dt.timedelta(days=1)

    print("\n| Subject | Exam | Days left | Weight | Study sessions (target) | Revision sessions | Hours |")
    print("|---|---|---|---|---|---|---|")
    for s in subjects:
        study = sum(1 for v in assign.values() if v == (s, "study"))
        rev = sum(1 for v in assign.values() if v == (s, "revise"))
        print(f"| {s} | {exam_date[s]} ({exam_date[s]:%a}) | {(exam_date[s] - today).days} | {weights[s]:g} | "
              f"{study} ({target[s]:.1f}) | {rev} | {(study + rev) * hours_per:g} |")
        if study + 0.5 < target[s]:
            warnings.append(f"{s}: {study} study sessions against a fair share of {target[s]:.1f}, because its "
                            "exam comes early. Cover its high-weightage topics first.")
        if study == 0 and rev == 0 and not any(w.startswith(f"{s}: no study time") for w in warnings):
            warnings.append(f"{s}: no study time at all before the exam.")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"- {w}")
    print("\nThis is a skeleton: fill each session with specific topics, and move sessions around if the "
          "student prefers. Re-run it whenever the date sheet or weights change.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
