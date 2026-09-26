# Topic scoring

## What "market standard" means here

Two markets judge a B.Tech paper topic:

1. **The research market**: reviewers at Scopus-indexed conferences and journals. They reward a clear, new contribution, credible evaluation and relevance to current work. They reject the tenth near-identical paper on an overused dataset.
2. **The industry and societal market**: whether someone would use or pay for this, whether it matches what industry needs now, and what it's worth to the student for placements, internships and higher studies.

A good score needs both, and it needs to be feasible for this student before their deadline.

## Rubric (out of 100)

| # | Criterion | Max | Full marks when... | Where the evidence comes from |
|---|---|---|---|---|
| 1 | Novelty and clarity of contribution | 20 | The student can state a specific difference from verified existing work: new data, a harder setting, a real constraint, a justified new combination, or a deployment | Live `search` results and the student's answers |
| 2 | Research momentum | 10 | The area is active or growing, not a dead end | `trend` output |
| 3 | Industry and societal relevance | 15 | A named user, a real problem and a plausible path to use | Judgment, plus web sources if you cite any |
| 4 | Feasibility | 20 | Doable with their skills, compute, budget and time before the deadline | The student's answers |
| 5 | Access to data or experiments | 10 | The data or setup is in hand, or public with a licence that allows use | The student's answers and the dataset page, checked |
| 6 | Measurability | 15 | Clear metrics, baselines they can actually run, and a test protocol | The student's answers |
| 7 | Venue fit | 10 | Matches the scope of realistic Scopus-indexed venues in their branch | Where similar papers were published (from `search`) |

**Bands**

- **80 to 100, strong:** proceed.
- **65 to 79, good:** proceed and make the listed fixes.
- **50 to 64, weak:** reframe before Stage 1.
- **Below 50:** change the topic, or treat the work as a learning exercise. Explain why.

Score each criterion on its own evidence and don't round up to be kind. If the student's answers were too thin to score a criterion, say so and ask, rather than guessing.

## Reading the `trend` output

- **Momentum (criterion 2):** compare complete years only, since the current year is partial. Rising counts mean an active area. If counts are flat or falling, try other phrasings before marking it down; the field may simply use newer terms.
- **Volume and novelty are separate questions.** High and rising volume means the area is popular and crowded. The novelty score then has to come from a specific angle, not from the topic. Very low volume means either a niche opportunity or something that isn't a recognised research problem. Run a search to find out which.
- **Counts include venues that aren't indexed.** They measure momentum, not Scopus acceptance. Say so when you report them.
- **Phrasing matters.** Use 2 or 3 phrasings. Use `--loose` for topics that combine concepts (for example "federated learning healthcare"); the exact phrase rarely appears in papers.

## Topics that are already crowded (judgment)

These framings come up very often in undergraduate submissions. They aren't banned, but on their own they score low on novelty (8/20 or less) until the student adds a specific angle. Before you say a topic is crowded, run a quick `search` and show the student how many near-identical papers exist, so the point rests on evidence rather than on your say-so.

- Predicting a disease (heart disease, diabetes and so on) with classical ML on a small public table of data, such as a UCI dataset
- Classifying plant or leaf disease with a CNN on PlantVillage. These are lab-condition images, so near-perfect accuracy is expected, and reviewers know the result doesn't carry over to real fields.
- Fake news, spam or sentiment classification with TF-IDF and standard classifiers
- MNIST digits, face-mask detection or emotion detection with off-the-shelf CNNs
- Stock price prediction with an LSTM on historical prices alone
- Attendance through face recognition, generic chatbots, and generic "smart home with Arduino/NodeMCU" or "IoT-based monitoring" projects with no evaluation

Angles that genuinely raise novelty (the student must be able to deliver them):

- Real data they collected themselves, or a realistic setting: field images, noisy data, testing on a different dataset from the one they trained on
- A deployment constraint that is actually measured: latency, memory, energy or cost on a low-end device
- A controlled comparison that nobody has published. Verify with a search that it really is missing.
- A local problem with local data: a regional language, local crops, Indian road or grid conditions
- Explainability or robustness that is evaluated, not just mentioned
- An honest replication or comparative study, framed as exactly that

## Output template

```
## Topic assessment: <working title>

**Score: NN/100 (<band>)**

| Criterion | Score | Why | Evidence |
|---|---|---|---|
| Novelty and contribution | 12/20 | <one line> | search (live): 40+ near-identical IEEE conference papers, 2022-25 |
| Research momentum | 9/10 | <one line> | trend (live, OpenAlex, <date>): 338 -> 1,240 papers a year, 2022 -> 2025 |
| Industry and societal relevance | 11/15 | <one line> | judgment |
| Feasibility | 16/20 | <one line> | your answers: 3 months, laptop GPU, dataset in hand |
| Access to data | 8/10 | <one line> | dataset page checked <date> |
| Measurability | 10/15 | <one line> | your answers: accuracy only, no baseline yet |
| Venue fit | 7/10 | <one line> | similar papers in IEEE conference proceedings |

**Biggest risks:** 1 to 3 bullets.

**How to raise the score:** 2 or 3 concrete, feasible changes, each naming the criterion it improves (for example "+6 novelty").

**Sharper title options:** 2 or 3.

**Next:** Confirm this topic, or one of the reframings, and I'll start the literature review.
```

The Evidence column must say where each claim came from: "search (live)", "trend (live)", "your answer" or "judgment". Never present judgment as data.
