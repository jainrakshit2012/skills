# Results

## Ask the student for

- Raw logs and CSVs, metric printouts, confusion matrices, training curves, hardware readings and survey responses
- The configuration used for each run
- Which split each number comes from

Every number in the Results section must trace back to one of these.

## Structure

1. **Setup recap:** hardware, software, splits and number of runs. Keep it short and point back to the Methodology section.
2. **Main results table:** the proposed method against the baselines under the same protocol, with the best value in bold and ± standard deviation if there were several runs.
3. **Comparison with published work:** only where the dataset, metric and protocol match. Cite the verified source and note any differences.
4. **Ablation or sensitivity analysis**
5. **Figures:** confusion matrix, training curves, example outputs, a photo of the hardware setup
6. **Discussion:** why the method works, where it fails (with examples from an error analysis) and the trade-offs (for example accuracy against speed)
7. **Limitations**

## Writing clear, specific results

Pattern: **[result] [metric] on [data and conditions], [comparison], [what it means].**

| Vague | Clear and specific |
|---|---|
| "The model achieved excellent accuracy." | "The model reached 94.1% accuracy and a macro-F1 of 0.91 on the held-out test set (1,824 images)." |
| "Our method outperforms existing methods." | "Macro-F1 is 3.2 points higher than the ResNet-50 baseline trained on the same split (0.91 vs 0.88)." |
| "The system is fast." | "Median inference time is 38 ms per image on a Raspberry Pi 4 (n = 500), against 210 ms for the baseline." |
| "Results are significant." | Use "significant" only when a statistical test was run, and name the test and the p-value. |

Use the exact numbers from the student's logs, keep decimal places consistent and always give units. The numbers in the abstract and conclusion must match the tables.

## Red flags to raise before a reviewer does

- **Accuracy of 99% or more:** check for leakage, duplicates across splits, or a dataset that is too easy
- **Accuracy alone on imbalanced classes**
- **Tuning on the test set**
- **Comparing with a paper that used a different dataset or split** as if the numbers were equivalent
- **A single run or a tiny test set** (for example 30 samples): present the result as preliminary
- **Poor figures:** unlabelled axes, screenshots or unreadable fonts
- **Claims beyond the evidence,** such as "outperforms the state of the art" without a direct, comparable comparison

## Figures and tables from the student's data

You can write plotting code (for example matplotlib) that reads the student's files. Never plot made-up data, not even as an "example": placeholder plots have a way of ending up in submitted papers. Save figures at 300 dpi or as vector files (PDF or SVG), with fonts readable at column width. Build tables from the student's numbers, and when a value is missing, show `[TODO]` in the table rather than a guess.
