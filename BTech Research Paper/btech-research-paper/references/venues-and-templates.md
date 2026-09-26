# Venues, templates and reference styles

Facts about venues change every year: indexing, fees, deadlines, page limits, series coverage. Check each one live in this session, give the link and the date checked, and say plainly when something could not be verified. Past indexing is evidence, not a guarantee.

## What to ask first

- The publisher and the venue's name
- The call-for-papers or author-guidelines link, and the deadline
- Whether the college requires Scopus indexing (many do, for final-year credit or placements)
- Their budget for registration fees or APCs

## Verifying a conference

Check all of these before recommending or confirming a conference:

1. **Official site and call for papers:** who organises it, the dates, and the named publication partner.
2. **Proceedings publisher:**
   - IEEE: is the conference listed in IEEE's conference search with a conference record number?
   - Springer: which book series (for example LNNS, LNEE, CCIS, AISC or SIST)?
   - Elsevier: Procedia?
   - Anyone else: name them.
3. **Previous edition:** find last year's proceedings on IEEE Xplore, SpringerLink or ScienceDirect, and check whether that volume appears in Scopus. This is the strongest check available. Tell the student that it is evidence, not a promise for this year.
4. **Series status:** Scopus coverage of a book series can change. The student checks the series on Scopus Sources.
5. **Fees and dates:** take these from the official page only, and note the date you checked.

Warning signs:

- "Guaranteed Scopus publication" or "guaranteed acceptance"
- Acceptance within days
- Payment demanded before review
- No named publication partner, or a partner whose own site doesn't list the conference
- One organiser running dozens of unrelated conferences
- Contact through a free email address only

## Verifying a journal

1. Run `venue <ISSN>` for the publisher, homepage, open-access status and the APC recorded by OpenAlex.
2. **The student checks Scopus.** Walk them through it: open https://www.scopus.com/sources and search by ISSN. Open the title and confirm that the coverage years are current, that it isn't marked discontinued, and that the publisher matches.
3. **Check for hijacking.** The site they will submit through must match the homepage listed by Scopus or the publisher. Fake copies of real journals exist. Retraction Watch maintains a Hijacked Journal Checker; find the current link with a web search.
4. Web search for "<journal name> discontinued Scopus" to catch recent removals.
5. Take the APC, review time and scope from the journal's official page.

## Templates

Before formatting, ask the student to upload the template: the Word .docx, the LaTeX .zip, .cls or .tex, or the author-guidelines PDF.

Extract and record these in `paper/state.md`:

- Paper size (A4 or US Letter), margins and number of columns
- Fonts and sizes for the title, headings, body and captions
- Heading numbering style (I., A., 1) and so on)
- Abstract word limit and number of keywords
- Page limit, and whether references count towards it
- Reference style and the example entries
- Figure and table caption placement and style
- Author block format, and any required notice (such as a copyright line)

For a .docx template, use a Word/docx skill if one is available. For LaTeX, work in the .tex files. For a guidelines PDF only, extract the rules from it.

Common template families are listed below. The names are stable, but each venue sets its own details, so confirm against the actual file: the IEEE conference template (Word, or LaTeX `IEEEtran`), the Springer proceedings template (`llncs`), Elsevier `elsarticle` and the Procedia template, ACM `acmart`, and the MDPI template.

## Choosing the citation style

Confirm the style against the template's own reference examples; they win over this table.

| Publisher or venue | Usual style | `cite --style` | In-text form |
|---|---|---|---|
| IEEE conference or journal | IEEE numeric | `ieee` | [1], [2]-[4], numbered in order of first citation |
| Springer proceedings series (LNCS, LNNS, LNEE, CCIS, ...) | Springer LNCS numeric | `springer-lncs` | [1]; check whether the template orders by citation or alphabetically |
| Springer journals | Varies (numeric or author-year) | `springer-basic` | As the journal specifies |
| Elsevier journals | Varies by journal | `elsevier-numeric` or `elsevier-harvard` | As the journal's Guide for Authors specifies |
| Elsevier Procedia | Numeric (check the template) | `elsevier-numeric` | [1] |
| ACM | ACM Reference Format | `acm` | [1] |
| MDPI | MDPI numeric | `mdpi` | [1] |
| Venues using APA | APA 7 | `apa` | (Author, Year) |

## Fixing references by hand after `cite`

- **IEEE:** abbreviate journal names if the template's examples do. Format conference names as "in Proc. ..." and months as abbreviations (Jan., Feb.).
- **Capitalisation:** title case or sentence case, as the style requires.
- **arXiv:** add the arXiv identifier if the template asks for it, and label the entry as a preprint.
- **Registry errors:** registry metadata sometimes has missing pages or titles in all capitals. Compare with the publisher's page and correct from that page, never from memory.

## Final reference audit

- `verify --file paper/references.bib` reports every entry as VERIFIED.
- Every in-text citation has an entry, and every entry is cited in the text.
- The count meets the target (14 to 20 for a conference paper).
- There are no duplicates, no retracted or flagged papers, and no preprint where a published version exists.
- The recency mix is right: most references are from the last five years.
- Numbering and order follow the style.
- Give the student a verification log: each reference, how it was verified and the date.
