# Literature review

## Reference targets by paper type

| Paper type | Target |
|---|---|
| Conference paper (Scopus-indexed proceedings) | 14 to 20 references |
| Journal article | Usually more. Check the target journal's author guidelines, since some set a maximum. |
| Review or survey paper | Many more, and a systematic method (PRISMA-style) is often expected. Confirm with the venue. |

A typical mix for 14 to 20 references (adjust it to the topic):

- **6 to 9 direct competitors:** the same problem, published in the last 3 to 5 years
- **3 or 4 method papers:** the techniques used or compared, including the original paper for each method (for example the ResNet paper if they use ResNet)
- **1 to 3 dataset, benchmark or tool papers:** the dataset's own paper, if there is one
- **1 or 2 recent surveys**
- **1 or 2 sources on why the problem matters:** prefer papers or official reports to news articles

Most references should be from the last five years. Foundational works can be older.

## Search strategy

1. **Build keyword sets:** problem terms × method terms × domain terms, with synonyms (for example "leaf disease", "plant pathology" and "crop disease").
2. **Search in this order,** stopping once you have enough good candidates:
   - `search "<q>" --publisher ieee --type conference`
   - `search "<q>" --publisher ieee --type journal`
   - `search "<q>" --publisher springer,elsevier,acm`
   - Add `--sort cited` to find foundational and heavily cited work, and `--sort recent` for the latest.
   - Use `--source openalex` when Crossref's results are poor. This draws on OpenAlex's free daily budget.
3. **Read the abstracts** of the shortlist with `abstract`. Drop anything off-topic, anything with no evaluation, anything flagged for retraction or another notice, and anything from a venue that looks predatory.
4. **Snowball** from the best 2 or 3 papers: look at their references and at the papers that cite them (through web search or the publisher's page). Verify every new find.
5. If the student can use Scopus or IEEE Xplore through the college library, they can run the same queries there and send you DOIs. That list is often the best quality available. Verify it anyway.

When choosing papers, favour a peer-reviewed venue from a recognised publisher, a clear method and evaluation, and relevance to the problem over raw citation count. Recent papers naturally have fewer citations.

## Literature matrix format

Keep it in `paper/literature_matrix.md`:

| # | Authors (year) | Title | Venue (type) | Problem | Method | Dataset | Metric and result, as reported | Limitation or gap | DOI | Read |
|---|---|---|---|---|---|---|---|---|---|---|

- **Read** records how much was actually read: `abstract`, `full text` or `student read`.
- **Metric and result** is filled only from what was read. If the abstract gives no numbers, write "not in abstract" rather than filling it in from memory.
- **Limitation or gap** can be stated by the paper or inferred by you. Mark inferred ones "(inferred)".

## From the matrix to the gap

1. Group the rows into 2 to 4 themes, usually by approach.
2. For each theme, note what has been solved and what hasn't, using the limitation column.
3. A gap is a pattern across limitations, and it cites the rows it comes from. For example: "existing approaches evaluate only on lab-condition images [3], [5], [8]", or "none report inference cost on low-end devices [2], [4], [6], [9]".
4. Check that the student's method actually addresses the gap. If it doesn't, go back to the topic.
5. Write 2 to 4 contributions. Each must be testable and map to a result in Stage 4.

## Writing Related Work

- Organise it by theme, with a topic sentence for each paragraph. Compare and contrast; don't write lists of the form "[1] did X. [2] did Y."
- End each paragraph with what that line of work leaves open.
- The last paragraph states the gap and how this paper addresses it.
- A comparison table (reference, method, dataset, reported result, limitation) is common in IEEE conference papers and useful to reviewers.
- Use citation markers in the target style if you know it. Otherwise use keys such as `[@Jackulin2022]` and convert them in Stage 5.
- Size it to the template's page budget. In a short conference paper, Related Work is usually around a page.
