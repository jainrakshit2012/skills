# B.Tech Research Paper

A Claude skill that takes an engineering student from "I need to publish a paper" to a submission-ready paper for a Scopus-indexed conference or journal, without made-up references.

When a student asks Claude for help with a research paper, this skill makes Claude act like a strict research guide. It questions the student about the topic, scores the topic, and then works through the paper one stage at a time. Every reference is checked against live DOI registries before Claude uses it. Claude never invents results, and it never promises indexing or acceptance.

## Why this exists

AI-written papers fail in predictable ways: citations to papers that don't exist, DOIs that point to a different paper, accuracy numbers nobody measured, and confident claims such as "this conference is Scopus indexed" based on nothing. The student is the one who pays for these mistakes, through desk rejection, retraction or a misconduct case. This skill turns "don't hallucinate" into a checked process.

## What the skill does

**Step 0: Grills the student on the topic and scores it.** Claude asks 3 to 5 pointed questions at a time: the problem and the user, the stage of the work, the data, the deadline, and the target venue. It then scores the topic out of 100 on seven criteria: novelty, research momentum, industry relevance, feasibility, access to data, measurability and venue fit. Each score shows where its evidence came from: live publication counts, live searches, the student's answers, or Claude's judgment. The assessment ends with concrete ways to raise the score and sharper title options.

**Stage 1: Literature review.** Claude asks whether the paper is for a conference, a journal or a review. A Scopus-indexed conference paper needs 14 to 20 references. Claude searches IEEE first, then Springer, Elsevier and ACM, reads the abstracts, and builds a literature matrix with a verified DOI on every row. It derives the research gap from that matrix and drafts the Related Work section.

**Stage 2: Methodology.** The student describes the method in their own words. Claude asks for missing details, using a checklist for each project type (ML/DL, IoT, software, simulation and experimental), and drafts the section. Anything unknown stays as a `[TODO]`.

**Stage 3: Methodology strengthening.** If the student is struggling, Claude gives ranked fixes (baselines, leakage, metrics, ablation, scope), each with an effort level and a check against the deadline. Otherwise it does a quick reviewer-style audit.

**Stage 4: Results.** Every number comes from the student's own logs. Claude writes specific results (metric, data, comparison, meaning), compares with published work only when the setups match, and raises red flags such as 99% accuracy or accuracy alone on imbalanced data before a reviewer does.

**Stage 5: References, venue and template.** Claude asks where the paper is going and verifies the venue live: who publishes the proceedings, whether last year's volume is on IEEE Xplore or SpringerLink and in Scopus, and any predatory or hijacked warning signs. It asks the student to upload the publisher's template, picks the citation style, generates the reference list from DOI metadata, and runs a final audit.

**Then assembly.** Title, abstract, introduction, conclusion and a pre-submission checklist, which covers the similarity check and the publisher's rules on disclosing AI use.

## The verification script

`scripts/paper_tools.py` needs only Python 3 and has no dependencies. It checks everything against live data:

```bash
python scripts/paper_tools.py search "plant disease detection deep learning" --publisher ieee --type conference --from 2022
python scripts/paper_tools.py abstract 10.1109/access.2023.3263042
python scripts/paper_tools.py verify --file references.bib
python scripts/paper_tools.py cite 10.1109/access.2023.3263042 10.1109/cvpr.2016.90 --style ieee
python scripts/paper_tools.py trend "plant disease detection" "crop yield prediction" --from 2019
python scripts/paper_tools.py venue 2169-3536
```

| Command | What it does | Data source |
|---|---|---|
| `search` | Finds papers, filtered by publisher (ieee, springer, elsevier, acm, wiley, tandf, mdpi), type (conference or journal) and year | Crossref (free) |
| `abstract` | Prints abstracts, so Claude summarises only what it has read | OpenAlex, falling back to Crossref |
| `verify` | Checks DOIs, titles or a whole `.bib` file | doi.org and Crossref (free) |
| `cite` | Formats references from DOIs in IEEE, Springer LNCS, APA, Elsevier, ACM, MDPI or BibTeX | doi.org (free) |
| `trend` | Counts papers per year for a topic phrase, for topic scoring | OpenAlex |
| `venue` | Looks up a journal by ISSN or name | OpenAlex |

`verify` reports each reference as one of:

```
[VERIFIED] good2023
[MISMATCH] wrongdoi: DOI belongs to a different paper (title similarity 0.33).
[MISMATCH] x: title found, but year given 2019 and registry says 2016. Use the registry details.
[NOT FOUND] "A Novel Hybrid Quantum-CNN Framework for ...": no registry record matches this title.
[EXPRESSION OF CONCERN, RETRACTION] 10.1016/S0140-6736(20)31180-6: ... Do not cite it as evidence.
```

The exit code is 0 only when everything is verified, so it can be used as a gate before submission.

### Limits

- **Scopus blocks scripted access.** The script can't confirm Scopus indexing. The skill tells Claude to say so and walk the student through checking scopus.com/sources by hand.
- **OpenAlex has a free daily budget** of about 100 searches without a key. If it runs out, set `OPENALEX_API_KEY` or wait a day. `search`, `verify` and `cite` don't use OpenAlex.
- **Registry metadata is occasionally wrong** (missing pages, titles in all capitals). The skill tells Claude to correct it from the publisher's page, never from memory.
- **Paywalled papers:** abstracts are usually open, but full text isn't. The student supplies PDFs through their institution's access.
- **Coverage:** papers without a DOI, such as some theses and reports, show as NOT FOUND and have to be checked by hand.

Optional environment variables: `PAPER_TOOLS_MAILTO` (a contact email sent to Crossref and OpenAlex for faster, "polite" access) and `OPENALEX_API_KEY`.

## Repository contents

```
btech-research-paper/
├── SKILL.md                         The workflow Claude follows
├── README.md
├── scripts/
│   └── paper_tools.py               Live search, verification and citation formatting
└── references/                      Loaded by Claude when it reaches each stage
    ├── topic-scoring.md             Rubric, evidence rules, crowded topics, output template
    ├── literature-review.md         Reference targets, search order, matrix, gap, Related Work
    ├── methodology.md               Question checklists by project type, structure, fixes
    ├── results.md                   Structure, writing specific results, red flags
    └── venues-and-templates.md      Venue verification, templates, citation styles, final audit
```

## Installation

**Claude apps (web, desktop).** Upload `btech-research-paper.zip` (or zip the `btech-research-paper` folder yourself) in the Skills section of Claude's settings. Skills must be enabled for your account or organization. If the code sandbox can't reach the internet, the skill falls back to web search and marks anything it couldn't check as UNVERIFIED.

**Claude Code.** Copy the folder into your skills directory:

```bash
# For all your projects
cp -r btech-research-paper ~/.claude/skills/

# For one project only
cp -r btech-research-paper .claude/skills/
```

Once installed, Claude uses the skill automatically when a student asks for help with a research paper, a conference or journal paper, a literature review, or turning a project into a paper. You can also ask for it by name.

## Customising

- **Reference target:** the 14 to 20 range for conference papers is in `SKILL.md` (Stage 1) and `references/literature-review.md`.
- **Scoring weights:** edit the rubric table in `references/topic-scoring.md`.
- **Publishers:** add a Crossref member ID to `CROSSREF_MEMBERS` in `scripts/paper_tools.py`. Look the ID up at `https://api.crossref.org/members?query=<name>`.
- **Citation styles:** `cite --style` accepts any CSL style ID supported by doi.org, as well as the short names listed above.

## Author

Rakshit Jain
