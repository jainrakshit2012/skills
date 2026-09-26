# Teaching, quizzes and mock papers

## Teaching a topic

- **Start from what they know.** Ask one question to find their level, then build from there.
- **Explain simply first,** with an everyday analogy if it helps, then give the exam-level version with correct terms.
- **Work one example in the exam's style:** a derivation laid out as the examiner expects, a numerical with every step and unit, a diagram described so they can draw it, or code or pseudocode for programming subjects.
- **Use their textbook's notation** and definitions. If their notes differ from the standard version, say so and tell them which one their examiner is likely to expect (usually the prescribed textbook's).
- **Check understanding** with 2 or 3 short questions ("why does this step work?", "what changes if...?") before moving on. Ask them to explain it back in their own words.

By subject type:

| Subject type | Emphasis |
|---|---|
| Numerical (maths, circuits, thermodynamics, mechanics, signals) | Method first, then the standard problem types from PYQs, then timed practice. Calculate every answer before giving it. |
| Theory (DBMS, OS, CN, software engineering, management) | Definitions with the textbook's keywords, a diagram for each major concept, differences as tables, examples. |
| Derivations | The logical steps in order, what each step uses, and the final result. Have them rewrite it from memory once. |
| Programming and algorithms | Trace the algorithm on a small input, the time complexity, and the code or pseudocode the paper usually asks for. |
| Diagram-heavy (architecture, block diagrams, circuits, cycles) | Which labels earn marks. Have them draw it from memory and send a photo. |

**Doubts:** when time is short, answer directly and clearly. When there is time, give a hint first and let them try. Either way, follow up with one question to confirm the doubt is cleared.

## Quizzes

- 5 to 10 questions, in the formats their paper uses (for example 2-mark definitions, 5-mark short answers, numericals). Include at least one question on an earlier topic for spaced revision.
- Label them as practice questions. Don't present them as PYQs.
- Send the questions, wait for answers, then mark. Don't include answers or hints in the question message.
- For numericals, compute the answer yourself first (with code if available), and give marks for correct method even when the final answer is wrong, as examiners do.
- Mark each answer: correct / partly correct / wrong, one line on why, and the correct idea. Then add every mistake to `prep/mistakes.md`:

```
| Date | Topic | What I got wrong | Correct idea |
|---|---|---|---|
| 2026-09-27 | 2NF | Said 2NF removes transitive dependency | 2NF removes partial dependency; 3NF removes transitive |
```

## Mock papers

1. **Build it in the exact pattern:** same sections, marks, number of questions, internal choices and duration as their real paper. Weight it towards High-tier PYQ topics and their weak topics, but include a few less-asked topics, as a real paper would. You may include genuine PYQs from their papers (say which year) alongside practice questions (labelled as such).
2. **Timed conditions:** tell them to write it in one sitting, by hand if the real exam is handwritten, without notes, within the real duration.
3. **Collect answers:** typed, or photos of handwritten sheets. If a page is unreadable, say which part and ask, rather than guessing.
4. **Mark it** (below), then record the score in `prep/state.md` and the mistakes in `prep/mistakes.md`.

## Marking like a university examiner

Examiners mark quickly against expected points: keywords, structure, diagrams and correct working. Common practice in Indian university exams (confirm with the student's teachers or seniors, since expectations vary):

| Marks | What usually earns full marks |
|---|---|
| 2 marks | A precise definition with the key terms, plus one example or property. About 3 to 5 lines. |
| 5 marks | A short introduction, 4 or 5 points under a heading or two, a diagram or example if the topic has one. About half a page to a page. |
| 10 marks (or more) | An introduction, a labelled diagram, an explanation under subheadings, an example or worked case, advantages and disadvantages or a comparison table where relevant, and a short conclusion. About 1.5 to 2.5 pages. |
| Numericals | Given data, the formula, substitution with units, working, a boxed final answer with units. Most marks come from correct method. |

For each question give: marks awarded out of the total, what earned the marks, what was missing, and a short outline of a full-marks answer (not a full essay unless they ask). Then overall:

```
## Mock paper 1: estimated score 47/70 (67%)

Section A: 16/20. Section B: 31/50.
Time: Section B unfinished (Q7 not attempted). Aim for 18 minutes per 10-mark answer.
Top 3 fixes:
1. Add labelled diagrams to 10-mark answers (lost about 6 marks)
2. 2NF vs 3NF confusion (Q2, Q5): revise with the mistakes log
3. Write the formula before substituting in numericals (lost method marks in Q6)

This is an estimate: real examiners vary.
```

## Answer-writing tips to pass on

- Answer the question asked, and underline key terms.
- Use headings and points rather than one long paragraph.
- Draw a diagram whenever the topic has one; label it.
- Attempt every question; partial answers earn partial marks.
- Manage time by marks: roughly minutes per mark = paper duration ÷ total marks, with 10 minutes kept for checking.
