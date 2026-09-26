# Prepare Me

A Claude skill that gets a university student ready for their semester exams, whether they have three weeks or one night.

When a student says "prepare me for my DBMS exam" or "my Maths-III paper is on Monday", this skill makes Claude act like an exam coach. It works from the student's own syllabus, date sheet and previous-year papers, finds their weak topics, plans their days, teaches, tests them in the real paper pattern, and gives them revision sheets for the last day.

## Why this exists

Generic AI exam help goes wrong in ways that cost marks: a syllabus from a different university, "previous year questions" that were never asked, "important questions that will surely come", a formula with a wrong sign, or a study plan that miscounts the days to the exam. This skill ties every answer to the student's real exam and uses two small scripts for the parts that must be exact: counting past-paper topics and doing date arithmetic.

## What the skill does

**Step 0: Intake.** Claude asks about the university, subject, exam dates, syllabus, paper pattern (sections, marks, choices) and previous-year papers, 3 to 5 questions at a time. It also asks about the student's target (pass safely, 60%+, top grade), because that changes the strategy.

**Step 1: PYQ analysis.** Claude reads the student's previous-year papers (PDFs or photos), tags each question with its unit and topic, and runs `pyq_analysis.py`. The report gives exact unit weightage, topics ranked by how many papers they appeared in, questions repeated across years (even when reworded), and syllabus topics never asked.

**Step 2: Diagnosis.** A quick 8 to 12 question test across units plus the student's confidence rating per unit. Weightage × weakness gives a priority list.

**Step 3: Study plan.** `plan_calendar.py` turns the date sheet into a day-by-day skeleton: revision the day before each paper, the evening after a paper going to the next one, and study time shared by subject difficulty. Claude fills each session with topics.

**Step 4: Daily loop.** Teach the topic in the textbook's notation, check understanding, quiz in the exam's formats, and log every mistake.

**Step 5: Mock papers.** Full timed papers in the exact pattern, answered typed or as photos of handwritten sheets, marked the way university examiners mark (keywords, diagrams, steps), with an estimated score and the top three fixes.

**Step 6: Revision sheets and exam eve.** One page per unit, a formula sheet per subject, rapid-fire questions, a morning checklist, and a reminder to sleep.

It adapts to the time left: **crash mode** for today or tomorrow (most-asked topics only), **short mode** for 2 to 7 days, and **full mode** for 8 days or more.

## Rules Claude follows

- The syllabus, paper pattern and dates come from the student's documents or the university's official site, never from memory.
- A question is called a PYQ only if it is in a paper the student provided. Everything else is labelled a practice question.
- "Important topics" are backed by counts ("asked in 4 of 5 papers"), and nothing is ever called guaranteed.
- Numerical answers are calculated before they are given, and definitions follow the student's textbook.
- Mock scores are labelled as estimates.
- No help during a live exam.

## The scripts

Both need only Python 3 and have no dependencies.

```bash
# Exact weightage and frequency from tagged past-paper questions
python scripts/pyq_analysis.py prep/pyq/dbms.csv --syllabus prep/pyq/dbms_topics.txt --out prep/pyq/dbms_report.md

# Day-by-day plan skeleton from a date sheet
python scripts/plan_calendar.py --exam "DBMS=2026-10-05" --exam "OS=2026-10-07" --exam "CN=2026-10-08" \
    --weight DBMS=3 --hours 6 --off 2026-10-02
```

The CSV for `pyq_analysis.py` has one row per question: `paper,qno,marks,unit,topic,question`. Sample output:

```
| Tier | Topic | Unit | Papers (of 4) | Times asked | Total marks | Usual marks | Last asked |
| High | Normalization | 3 | 4 | 5 | 34 | 10 | May 2025 |
| Medium | Concurrency control | 4 | 2 | 3 | 22 | 10 | Dec 2024 |

**2. Describe ACID properties of transactions.** (asked in 2 of 4 papers)
- Dec 2023, Q3 (10 marks): Explain ACID properties of a transaction with a neat diagram.
- Dec 2024, Q2 (10 marks): Describe ACID properties of transactions.
```

Sample output from `plan_calendar.py`:

```
| Date | Day | Morning | Afternoon | Evening | Note |
| 2026-10-04 | Sun | Revise DBMS | Revise DBMS | Revise DBMS |  |
| 2026-10-05 | Mon | - | - | OS | EXAM: DBMS |
| 2026-10-06 | Tue | Revise OS | Revise OS | Revise OS |  |
```

### Limits

- Topic tagging is done by Claude, and the counts are only as good as the tagging. The script flags topic names that look like duplicates.
- Repeated-question matching is based on wording, so it can miss a repeat phrased very differently or group two similar but different questions. Claude should check the groups.
- The plan is a skeleton. Students should move sessions to suit themselves, and re-run it when dates change.

## Repository contents

```
prepare-me/
├── SKILL.md                          The workflow Claude follows
├── README.md
├── scripts/
│   ├── pyq_analysis.py               Weightage, topic frequency, repeated questions
│   └── plan_calendar.py              Study-plan skeleton from the date sheet
└── references/
    ├── diagnosis-and-planning.md     Diagnostic test, priority list, plan format
    ├── teaching-and-testing.md       Teaching, quizzes, mock papers, examiner-style marking
    └── pyq-and-revision.md           Reading papers, the CSV, the report, revision sheets
```

## Installation

**Claude apps (web, desktop).** Upload `prepare-me.zip` (or zip the `prepare-me` folder yourself) in the Skills section of Claude's settings. Skills must be enabled for your account or organization.

**Claude Code.** Copy the folder into your skills directory:

```bash
cp -r prepare-me ~/.claude/skills/      # all projects
cp -r prepare-me .claude/skills/        # one project
```

Claude then uses the skill when a student asks for exam help. You can also ask for it by name.

## Author

Rakshit Jain
