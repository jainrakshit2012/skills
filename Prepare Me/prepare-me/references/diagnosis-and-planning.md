# Diagnosis and planning

## The diagnostic test

Aim: find weak topics in 15 to 20 minutes, not grade the student.

- **8 to 12 questions** spread across all units, weighted towards units with high PYQ weightage.
- **Mix of types**, matching the paper: 2 or 3 definitions or short-answer questions, 3 or 4 concept questions ("why", "what happens if", "difference between"), 1 or 2 numerical or problem questions for numerical subjects, and 1 question that needs a diagram or steps.
- **Ask, then wait.** Send the questions, let the student answer (typed, or a photo of their working), then mark. Never put answers in the same message as the questions.
- In crash mode, skip the test and ask for a confidence rating per unit only.

Also ask for a **confidence rating per unit** (1 = never studied, 3 = understand it but can't write an answer, 5 = could write full answers now). Students often rate themselves higher than their test shows. Where the two disagree, trust the test and tell them kindly.

## Priority list

Combine weightage and weakness for each topic:

| | Weak (test wrong or confidence 1-2) | Moderate | Strong (test right, confidence 4-5) |
|---|---|---|---|
| **High weightage** (High tier, or a big share of marks) | 1. Do first | 2. Do next | 5. Quick revision only |
| **Medium weightage** | 3 | 4 | 6 |
| **Low or never asked** | 7 (only if time allows, or if the student aims for a top grade) | 8 | 9. Skip |

Without PYQs, use the syllabus marks split if the university publishes one, otherwise treat units as equal and say so.

A student aiming to pass should secure priorities 1 to 4 fully rather than skim everything. A student aiming for a top grade needs coverage of 7 and 8 as well.

## Building the plan

1. Run `scripts/plan_calendar.py`:
   - `--exam "Subject=YYYY-MM-DD"` once per paper, from the date sheet (check the dates with the student).
   - `--weight Subject=N` from 1 to 5: higher for harder or weaker subjects, and for subjects with more high-priority topics.
   - `--hours` realistic hours per full free day (ask; students overestimate, so plan for about 80% of what they say).
   - `--off YYYY-MM-DD` for days they can't study, and `--today-sessions N` if part of today is already gone.
   - `--sessions 2` or `3` to match how they like to work.
2. Fill every session with specific topics from the priority list, in priority order. Put a numerical or problem-heavy topic in their most alert session.
3. Each study session ends with a short quiz (Step 4 of the skill). Leave the last session before each revision day for a mock paper where time allows.
4. **Spaced revision:** in full mode, bring back earlier topics briefly 1 day, 3 days and 7 days after first study, and review the mistakes log every few days.
5. Write the plan to `prep/plan.md` as a table the student can tick off.

## Plan format

```
## Study plan: <subject(s)> (made <date>, <n> days to the first paper)

| Date | Day | Session | Topics | Done |
|---|---|---|---|---|
| 2026-09-27 | Sun | Morning | DBMS U3: 1NF, 2NF, 3NF (PYQ High, weak) + quiz | [ ] |
| 2026-09-27 | Sun | Afternoon | DBMS U3: BCNF, decomposition + quiz | [ ] |
| 2026-09-27 | Sun | Evening | Mistakes log + 10 two-mark questions from U1 | [ ] |
```

Inside a 2 to 3 hour session, suggest 45 to 50 minutes of focused work with a 10 minute break, phone out of reach, and a few minutes of recall at the end (write down what you remember without looking).

## Re-planning

Ask how the day went at the start of each session. If they're behind, don't just push everything back: drop or shrink low-priority topics, and re-run the calendar if exam dates, hours or weights change. Tell them plainly what has been dropped and why.
