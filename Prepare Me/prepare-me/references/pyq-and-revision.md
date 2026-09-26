# PYQ analysis and revision sheets

## Reading the papers

- Read every paper the student gives you (PDF, scan or photo). For scanned PDFs, use OCR if a PDF tool is available; otherwise read the page images.
- Write exactly what the paper says. If a question is unreadable or cut off, mark it `[unreadable]` and ask the student; don't reconstruct it.
- Note the paper's pattern while reading (sections, marks, choices, duration). It is the best source for the mock papers.
- Record which paper each question came from. Use names that include month and year ("May 2024", "Dec 2023 (odd sem)") so the script can order them.

## The CSV

Save to `prep/pyq/<subject>.csv`, one row per question or sub-question:

```
paper,qno,marks,unit,topic,question
Dec 2023,1a,2,1,ER model,Define weak entity set.
Dec 2023,2,10,3,Normalization,Explain 1NF 2NF and 3NF with suitable examples.
May 2024,3,10,4,Concurrency control,Explain two phase locking protocol.
```

- **unit:** the syllabus unit number (or name) the question belongs to.
- **topic:** use the syllabus's topic names and exactly the same spelling every time, because the script counts by name. Keep topics at a useful size: "Normalization", not "2NF" in one row and "Normal forms" in another.
- **Internal choice** (Q2a OR Q2b): enter both options as separate rows.
- **Questions spanning two topics:** tag the main one.
- If the marks aren't printed, leave the field blank (the script warns you).

Also save the syllabus topics to `prep/pyq/<subject>_topics.txt`, one per line as `unit|topic`, so the report can list topics that were never asked.

## Running and reading the report

```
python scripts/pyq_analysis.py prep/pyq/dbms.csv --syllabus prep/pyq/dbms_topics.txt --out prep/pyq/dbms_report.md
```

1. **Fix these first:** clear any warnings (duplicate topic names, blank marks) and re-run.
2. **Unit weightage:** marks per unit per paper and the overall share. It shows where the marks are.
3. **Topics by frequency:** High (asked in at least 60% of papers), Medium (30 to 59%), Low. With fewer than 3 papers the tiers are weak evidence; say so.
4. **Repeated questions:** the same question asked in different years, even when the wording changes. These are the first answers to prepare, as full-marks outlines.
5. **Never asked:** lower priority, not zero priority.

When you tell the student about it, quote the numbers: "Normalization appeared in all 4 papers, 34 marks in total; ACID properties was asked for 10 marks in Dec 2023 and Dec 2024." Never turn this into "this will come". A fair summary is: "these topics have been asked most often, so they are the safest place to start."

## Revision sheet (one page per unit)

```
# DBMS Unit 3: Normalization (PYQ: High tier, 30% of marks)

## Must-know definitions
- Functional dependency: ... (textbook wording)
- 2NF: ...

## Formulas and rules
- Closure of attributes: ... (when to use it)

## Diagrams to practise
- Decomposition example (from PYQ Dec 2023 Q2)

## Standard answers to prepare
- "Explain 1NF, 2NF, 3NF with examples" (asked in 3 of 4 papers, 10 marks): outline...

## Common mistakes (from your mistakes log)
- 2NF removes partial dependency, 3NF removes transitive dependency

## 2-mark rapid fire
- 5 to 10 quick questions with one-line answers
```

## Formula sheet (one per subject)

- Group formulas by unit. For each: the formula, what each symbol means with units, when to use it, and one common trap.
- Take every formula from their textbook or notes, or check it (for example by working a quick example or checking the units). A wrong formula on a revision sheet does more damage than a missing one.
- Keep it to one or two pages so it can be read in 10 minutes on the morning of the exam.

If the student wants a printable file, save the sheets as markdown in `prep/sheets/` and offer a PDF or Word version using a PDF or docx skill if one is available.
