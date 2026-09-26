#!/usr/bin/env python3
"""
paper_tools.py - live lookups for writing a research paper. Python 3.8+, standard library only.

Everything this prints comes from a live registry response (Crossref, doi.org, OpenAlex).
When a lookup fails, the item is reported as NOT FOUND or UNVERIFIED. Nothing is guessed.

Subcommands
  search    find candidate papers (Crossref by default, free), filter by publisher, type and year
  abstract  print a paper's abstract by DOI (OpenAlex, then Crossref)
  verify    check that DOIs / titles / a .bib file are real, and flag retractions
  cite      format DOIs in a citation style (ieee, springer-lncs, apa, ...) or as BibTeX
  trend     papers per year for one or more topic phrases (OpenAlex), used for topic scoring
  venue     look up a journal by ISSN or name (OpenAlex). Scopus status must be checked by hand.

Examples
  python paper_tools.py search "plant disease detection deep learning" --publisher ieee --type conference --from 2022
  python paper_tools.py abstract 10.1109/access.2023.3263042
  python paper_tools.py verify 10.1016/j.measen.2022.100441 "Deep residual learning for image recognition"
  python paper_tools.py verify --file references.bib
  python paper_tools.py cite 10.1109/access.2023.3263042 10.1016/j.measen.2022.100441 --style ieee
  python paper_tools.py trend "plant disease detection" "crop yield prediction" --from 2019
  python paper_tools.py venue 2665-9174

Optional environment variables
  PAPER_TOOLS_MAILTO   contact email sent to Crossref/OpenAlex for their "polite" pools
  OPENALEX_API_KEY     OpenAlex key, if the free daily budget runs out

Exit codes: 0 = all good, 1 = something not verified / not found, 2 = network or service error.
"""

import argparse
import datetime
import difflib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

CROSSREF = "https://api.crossref.org"
OPENALEX = "https://api.openalex.org"
DOI_ORG = "https://doi.org"
MAILTO = os.environ.get("PAPER_TOOLS_MAILTO", "").strip()
OPENALEX_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
UA = "paper-tools/1.0 (btech-research-paper skill" + (f"; mailto:{MAILTO}" if MAILTO else "") + ")"

# Crossref member IDs (checked against api.crossref.org/members)
CROSSREF_MEMBERS = {
    "ieee": "263",
    "elsevier": "78",
    "springer": "297",
    "acm": "320",
    "wiley": "311",
    "tandf": "301",
    "mdpi": "1968",
}

# Short names for CSL styles served by doi.org content negotiation
STYLES = {
    "ieee": "ieee",
    "springer-lncs": "springer-lecture-notes-in-computer-science",
    "springer-basic": "springer-basic-brackets",
    "apa": "apa",
    "elsevier-harvard": "elsevier-harvard",
    "elsevier-numeric": "elsevier-with-titles",
    "acm": "association-for-computing-machinery",
    "mdpi": "multidisciplinary-digital-publishing-institute",
}
BRACKET_NUMBERED = {"ieee", "elsevier-with-titles", "association-for-computing-machinery"}
DOT_NUMBERED = {"springer-lecture-notes-in-computer-science", "springer-basic-brackets",
                "multidisciplinary-digital-publishing-institute"}
AUTHOR_YEAR = {"apa", "elsevier-harvard"}

DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.I)
ISSN_RE = re.compile(r"^\d{4}-?\d{3}[\dXx]$")


class NetError(Exception):
    pass


def http_get(url, accept="application/json", retries=2):
    """Return the response body as text, None on 404, raise NetError otherwise."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return None
            if e.code == 429 and "openalex" in url:
                raise NetError("OpenAlex daily free budget used up (HTTP 429). Set OPENALEX_API_KEY, "
                               "try again tomorrow, or use --source crossref.")
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(2 * (attempt + 1))
                continue
            raise NetError(f"HTTP {e.code} from {url.split('?')[0]}")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempt < retries:
                time.sleep(2)
                continue
            raise NetError(f"could not reach {url.split('?')[0]} ({e})")
    raise NetError(f"gave up on {url}")


def get_json(url, **kw):
    body = http_get(url, **kw)
    if body is None:
        return None
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None


def openalex_url(path, params=None):
    params = dict(params or {})
    if MAILTO:
        params["mailto"] = MAILTO
    if OPENALEX_KEY:
        params["api_key"] = OPENALEX_KEY
    q = urllib.parse.urlencode(params, safe=":,|\"!")
    return f"{OPENALEX}{path}" + (f"?{q}" if q else "")


def clean_doi(s):
    s = s.strip().rstrip(".,;")
    s = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", s, flags=re.I)
    return s


def norm_title(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = re.sub(r"[{}\\]", "", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def similarity(a, b):
    return difflib.SequenceMatcher(None, norm_title(a), norm_title(b)).ratio()


def first(v, default=""):
    if isinstance(v, list):
        return v[0] if v else default
    return v if v is not None else default


def year_of(csl):
    for key in ("issued", "published-print", "published-online", "published", "created"):
        parts = (csl.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            return str(parts[0][0])
    return "n.d."


def authors_short(authors, n=3):
    names = []
    for a in authors or []:
        name = a.get("family") or a.get("name") or a.get("literal") or ""
        if a.get("given") and a.get("family"):
            name = f"{a['given'][0]}. {a['family']}"
        if name:
            names.append(name)
    if not names:
        return "(no authors listed)"
    return ", ".join(names[:n]) + (" et al." if len(names) > n else "")


def strip_tags(s):
    s = re.sub(r"<jats:title>.*?</jats:title>", " ", s or "", flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


# ---------------------------------------------------------------- search

def cmd_search(a):
    this_year = datetime.date.today().year
    if a.source == "openalex":
        return search_openalex(a, this_year)
    filters = [f"from-pub-date:{a.from_year}", f"until-pub-date:{a.to_year or this_year}"]
    for p in a.publisher:
        if p != "any":
            filters.append(f"member:{CROSSREF_MEMBERS[p]}")
    if a.type == "journal":
        filters.append("type:journal-article")
    elif a.type == "conference":
        # IEEE/ACM register proceedings-article; Springer series (LNNS, LNEE, CCIS...) register book-chapter
        filters += ["type:proceedings-article", "type:book-chapter"]
    else:
        filters += ["type:journal-article", "type:proceedings-article", "type:book-chapter"]
    # Crossref matches any query word, so its own citation/date sort surfaces off-topic papers.
    # Take the most relevant hits first, then re-sort those locally.
    params = {
        "query.bibliographic": a.query,
        "filter": ",".join(filters),
        "rows": a.n if a.sort == "relevance" else min(100, a.n * 5),
        "select": "DOI,title,author,container-title,issued,type,publisher,is-referenced-by-count,abstract,updated-by",
    }
    url = f"{CROSSREF}/works?" + urllib.parse.urlencode(params)
    data = get_json(url)
    items = (data or {}).get("message", {}).get("items", [])
    results = []
    for it in items:
        results.append({
            "doi": it.get("DOI", ""),
            "title": strip_tags(first(it.get("title"), "(untitled)")),
            "authors": authors_short(it.get("author")),
            "year": year_of(it),
            "venue": first(it.get("container-title"), "(no venue)"),
            "type": it.get("type", ""),
            "publisher": it.get("publisher", ""),
            "cited_by": it.get("is-referenced-by-count", 0),
            "abstract_available": bool(it.get("abstract")),
            "notices": [u.get("label") or u.get("type") for u in it.get("updated-by") or []
                        if u.get("type") in ("retraction", "expression_of_concern", "withdrawal", "removal")],
        })
    if a.sort == "cited":
        results.sort(key=lambda r: r["cited_by"], reverse=True)
    elif a.sort == "recent":
        results.sort(key=lambda r: r["year"], reverse=True)
    print_search(results[:a.n], a, "Crossref")
    return 0


def search_openalex(a, this_year):
    filters = [f"publication_year:{a.from_year}-{a.to_year or this_year}", "is_paratext:false", "is_retracted:false"]
    openalex_publishers = {"ieee": "P4310319808", "springer": "P4310319965",
                           "elsevier": "P4310320990", "acm": "P4310319798"}
    pubs = [openalex_publishers[p] for p in a.publisher if p in openalex_publishers]
    if pubs:
        filters.append("primary_location.source.host_organization_lineage:" + "|".join(pubs))
    if a.type == "journal":
        filters.append("primary_location.source.type:journal")
    elif a.type == "conference":
        filters.append("primary_location.source.type:conference|book series")
    sort = {"cited": "cited_by_count:desc", "recent": "publication_date:desc"}.get(a.sort)
    params = {"search": a.query, "filter": ",".join(filters), "per-page": a.n,
              "select": "doi,title,publication_year,type,cited_by_count,primary_location,authorships,abstract_inverted_index"}
    if sort:
        params["sort"] = sort
    data = get_json(openalex_url("/works", params))
    results = []
    for w in (data or {}).get("results", []):
        src = ((w.get("primary_location") or {}).get("source") or {})
        results.append({
            "doi": clean_doi(w.get("doi") or ""),
            "title": w.get("title") or "(untitled)",
            "authors": authors_short([{"literal": (x.get("author") or {}).get("display_name", "")}
                                      for x in w.get("authorships") or []]),
            "year": str(w.get("publication_year") or "n.d."),
            "venue": src.get("display_name") or "(no venue)",
            "type": f"{w.get('type')} / source: {src.get('type')}",
            "publisher": src.get("host_organization_name") or "",
            "cited_by": w.get("cited_by_count", 0),
            "abstract_available": bool(w.get("abstract_inverted_index")),
            "notices": [],
        })
    print_search(results, a, "OpenAlex")
    return 0


def print_search(results, a, source):
    if a.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return
    print(f"Source: {source} | query: {a.query!r} | publisher: {','.join(a.publisher)} | type: {a.type} | "
          f"{a.from_year}-{a.to_year or 'now'} | checked {datetime.date.today().isoformat()}\n")
    if not results:
        print("No results. Try broader keywords, a wider year range, or --publisher any.")
        return
    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['title']}")
        print(f"    {r['authors']} | {r['year']} | {r['venue']} | {r['publisher']}")
        flag = f" | NOTICE: {', '.join(r['notices'])} - do not cite" if r["notices"] else ""
        print(f"    DOI: {r['doi']} | {r['type']} | cited by {r['cited_by']} | "
              f"abstract {'available' if r['abstract_available'] else 'not in registry'}{flag}\n")
    print("Note: these are search hits, not a Scopus list. Read each abstract before using a paper, "
          "and confirm the venue's indexing separately.")


# ---------------------------------------------------------------- abstract

def rebuild_abstract(inv):
    pos = {}
    for word, idxs in (inv or {}).items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def cmd_abstract(a):
    code = 0
    for raw in a.dois:
        doi = clean_doi(raw)
        title, venue, year, text, src = "", "", "", "", ""
        w = get_json(openalex_url(f"/works/doi:{urllib.parse.quote(doi, safe='/:()')}"))
        if w:
            title = w.get("title") or ""
            venue = (((w.get("primary_location") or {}).get("source")) or {}).get("display_name") or ""
            year = str(w.get("publication_year") or "")
            text = rebuild_abstract(w.get("abstract_inverted_index"))
            src = "OpenAlex"
        if not (text and venue):
            c = get_json(f"{CROSSREF}/works/{urllib.parse.quote(doi, safe='/:()')}")
            if c:
                m = c.get("message", {})
                title = title or strip_tags(first(m.get("title")))
                venue = venue or first(m.get("container-title"))
                year = year or year_of(m)
                if not text:
                    text = strip_tags(m.get("abstract", ""))
                    src = "Crossref"
        print(f"DOI: {doi}")
        if not (title or text):
            print("NOT FOUND in OpenAlex or Crossref. Do not describe this paper until the student supplies it.\n")
            code = 1
            continue
        print(f"Title: {title}\nVenue: {venue} ({year})")
        if text:
            print(f"Abstract (from {src}):\n{text}\n")
        else:
            print("Abstract: not available from open registries. Ask the student for the PDF or the publisher "
                  "page text. Do not summarise this paper from memory.\n")
            code = 1
    return code


# ---------------------------------------------------------------- verify

def csl_for_doi(doi):
    """Metadata for any registered DOI (Crossref, DataCite for arXiv, mEDRA...) via doi.org."""
    return get_json(f"{DOI_ORG}/{urllib.parse.quote(doi, safe='/:()')}",
                    accept="application/vnd.citationstyles.csl+json")


def crossref_notices(doi):
    data = get_json(f"{CROSSREF}/works/{urllib.parse.quote(doi, safe='/:()')}")
    if not data:
        return []
    ups = data.get("message", {}).get("updated-by") or []
    return sorted({u.get("label") or u.get("type") for u in ups
                   if u.get("type") in ("retraction", "expression_of_concern", "withdrawal", "removal")})


def describe(csl, doi):
    venue = first(csl.get("container-title")) or csl.get("publisher", "")
    bits = [authors_short(csl.get("author"), 4), f"({year_of(csl)})", strip_tags(first(csl.get("title"))) + ".",
            f"{venue}."]
    if csl.get("volume"):
        bits.append(f"vol. {csl['volume']}")
    if csl.get("issue"):
        bits.append(f"no. {csl['issue']}")
    if csl.get("page"):
        bits.append(f"pp. {csl['page']}")
    bits.append(f"[{csl.get('type', '?')}; {csl.get('publisher', '?')}] doi:{doi}")
    return " ".join(bits)


FIELD_NAME = re.compile(r"\s*(\w[\w-]*)\s*=\s*")
BARE_VALUE = re.compile(r"[^,}\s]*")
COMMA = re.compile(r"\s*,")


def bib_fields(block):
    """Read `name = {value}` / "value" / bare fields in order, respecting nested braces."""
    out, n = {}, len(block)
    pos = block.find(",") + 1
    while 0 < pos < n:
        m = FIELD_NAME.match(block, pos)
        if not m:
            break
        name, j = m.group(1).lower(), m.end()
        if j < n and block[j] == "{":
            depth, k = 0, j
            while k < n:
                depth += {"{": 1, "}": -1}.get(block[k], 0)
                if depth == 0:
                    break
                k += 1
            val, end = block[j + 1:k], k + 1
        elif j < n and block[j] == '"':
            k = block.find('"', j + 1)
            k = n if k == -1 else k
            val, end = block[j + 1:k], k + 1
        else:
            mm = BARE_VALUE.match(block, j)
            val, end = mm.group(0), mm.end()
        out.setdefault(name, re.sub(r"\s+", " ", val).strip())
        c = COMMA.match(block, end)
        if not c:
            break
        pos = c.end()
    return out


def parse_bib(text):
    entries = []
    for block in re.split(r"(?=@\w+\s*\{)", text):
        if not block.strip().startswith("@") or re.match(r"@(comment|string|preamble)\b", block.strip(), re.I):
            continue
        key = re.match(r"\s*@\w+\s*\{\s*([^,\s]+)", block)
        f = bib_fields(block)
        entries.append({"key": key.group(1) if key else "?", "doi": f.get("doi", ""), "title": f.get("title", ""),
                        "year": f.get("year", ""), "author": f.get("author", "")})
    return entries


def verify_one(item):
    """item: dict with doi/title/year/author/key. Returns (status, lines)."""
    label = item.get("key") or item.get("doi") or item.get("title")
    doi = clean_doi(item.get("doi") or "")
    title = item.get("title", "")
    if doi:
        csl = csl_for_doi(doi)
        if not csl:
            return "NOT FOUND", [f"[NOT FOUND] {label}: DOI {doi} is not registered. Likely wrong or invented. Do not cite."]
        lines = []
        status = "VERIFIED"
        reg_title = strip_tags(first(csl.get("title")))
        if title:
            sim = similarity(title, reg_title)
            if sim < 0.85:
                status = "MISMATCH"
                lines.append(f"[MISMATCH] {label}: DOI belongs to a different paper (title similarity {sim:.2f}).")
                lines.append(f"    given:    {title}")
                lines.append(f"    registry: {reg_title}")
        if item.get("year") and year_of(csl) not in ("n.d.", item["year"]):
            lines.append(f"    note: year given {item['year']} but registry says {year_of(csl)}")
            status = "MISMATCH" if status == "VERIFIED" else status
        if item.get("author"):
            fam = [x.get("family", "").lower() for x in csl.get("author") or []]
            given_first = re.split(r"\s+and\s+", item["author"])[0]
            surname = (given_first.split(",")[0] if "," in given_first else given_first.split()[-1]).strip().lower()
            if fam and surname and surname not in fam:
                lines.append(f"    note: first author '{surname}' not in registry authors {fam[:4]}")
                status = "MISMATCH" if status == "VERIFIED" else status
        notices = crossref_notices(doi)
        if notices:
            status = "RETRACTED/NOTICE"
            lines.append(f"[{', '.join(notices).upper()}] {label}: this paper has a post-publication notice. "
                         "Do not cite it as evidence.")
        if status == "VERIFIED":
            lines.insert(0, f"[VERIFIED] {label}")
        lines.append("    " + describe(csl, doi))
        return status, lines

    if not title:
        return "NOT FOUND", [f"[NOT FOUND] {label}: no DOI or title to check."]
    params = {"query.bibliographic": title, "rows": 5,
              "select": "DOI,title,author,container-title,issued,type,publisher"}
    data = get_json(f"{CROSSREF}/works?" + urllib.parse.urlencode(params))
    best, best_sim = None, 0.0
    for it in (data or {}).get("message", {}).get("items", []):
        sim = similarity(title, first(it.get("title")))
        if sim > best_sim:
            best, best_sim = it, sim
    if best and best_sim >= 0.92:
        doi = best["DOI"]
        csl = csl_for_doi(doi) or best
        body = ["    " + describe(csl, doi)]
        notices = crossref_notices(doi)
        if notices:
            return "RETRACTED/NOTICE", [f"[{', '.join(notices).upper()}] {label}: post-publication notice. "
                                        "Do not cite it as evidence."] + body
        if item.get("year") and year_of(csl) not in ("n.d.", item["year"]):
            return "MISMATCH", [f"[MISMATCH] {label}: title found, but year given {item['year']} and registry "
                                f"says {year_of(csl)}. Use the registry details."] + body
        return "VERIFIED", [f"[VERIFIED by title, similarity {best_sim:.2f}] {label}"] + body
    if best and best_sim >= 0.75:
        return "POSSIBLE", [f"[POSSIBLE MATCH {best_sim:.2f} - check by hand] {label}",
                            f"    closest registry record: {strip_tags(first(best.get('title')))} "
                            f"({year_of(best)}) doi:{best.get('DOI')}"]
    return "NOT FOUND", [f"[NOT FOUND] {label}: no registry record matches this title. "
                         "It may be invented, or it may be a thesis/report without a DOI. Do not cite unless the "
                         "student provides the source."]


def cmd_verify(a):
    items = []
    for x in a.items:
        items.append({"doi": x} if DOI_RE.match(clean_doi(x)) else {"title": x})
    if a.file:
        with open(a.file, encoding="utf-8", errors="replace") as f:
            text = f.read()
        if a.file.lower().endswith(".bib") or text.lstrip().startswith("@"):
            items += parse_bib(text)
        else:
            for line in text.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    items.append({"doi": line} if DOI_RE.match(clean_doi(line)) else {"title": line})
    if not items:
        print("Nothing to verify. Pass DOIs/titles or --file.")
        return 1
    counts = {}
    print(f"Checked live against doi.org + Crossref on {datetime.date.today().isoformat()}\n")
    for it in items:
        status, lines = verify_one(it)
        counts[status] = counts.get(status, 0) + 1
        print("\n".join(lines) + "\n")
    print("Summary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    return 0 if set(counts) == {"VERIFIED"} else 1


# ---------------------------------------------------------------- cite

def cmd_cite(a):
    style = STYLES.get(a.style, a.style)
    out, failed = [], []
    for raw in a.dois:
        doi = clean_doi(raw)
        accept = "application/x-bibtex" if style == "bibtex" else f"text/x-bibliography; style={style}"
        body = http_get(f"{DOI_ORG}/{urllib.parse.quote(doi, safe='/:()')}", accept=accept)
        if not body or body.lstrip().startswith("{"):
            failed.append(doi)
            continue
        # DataCite (arXiv) citations arrive with <i> tags; drop them without adding spaces
        out.append(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", body)).strip() if style != "bibtex" else body.strip())
    if style in AUTHOR_YEAR:
        out.sort(key=str.lower)
    for i, text in enumerate(out, 1):
        if style == "bibtex":
            print(text + "\n")
            continue
        text = re.sub(r"^\s*(\[\d+\]|\d+\.)\s*", "", text)
        if style in BRACKET_NUMBERED:
            print(f"[{i}] {text}")
        elif style in DOT_NUMBERED:
            print(f"{i}. {text}")
        else:
            print(text)
    sys.stdout.flush()
    for doi in failed:
        print(f"[UNVERIFIED] could not format {doi} in style '{style}' (DOI not found or style unknown). "
              "Check the DOI with `verify`.", file=sys.stderr)
    if failed:
        return 1
    print(f"\n(Generated from DOI registry metadata on {datetime.date.today().isoformat()}. Compare against the "
          "template's reference examples: journal abbreviations and capitalisation may need hand fixes.)",
          file=sys.stderr)
    return 0


# ---------------------------------------------------------------- trend

def cmd_trend(a):
    this_year = datetime.date.today().year
    to_year = a.to_year or this_year
    table = {}
    for phrase in a.phrases:
        p = phrase.replace(",", " ").replace('"', "").strip()
        term = p if a.loose else f'"{p}"'
        params = {"filter": f"title_and_abstract.search:{term},publication_year:{a.from_year}-{to_year}",
                  "group_by": "publication_year"}
        data = get_json(openalex_url("/works", params))
        table[phrase] = {int(g["key"]): g["count"] for g in (data or {}).get("group_by", [])}
    years = list(range(a.from_year, to_year + 1))
    width = max(len(p) for p in a.phrases)
    print(f"Papers per year with the phrase in title/abstract (OpenAlex, all venues, checked "
          f"{datetime.date.today().isoformat()})\n")
    print(" " * (width + 2) + "".join(f"{y}{'*' if y == this_year else ' '}".rjust(8) for y in years) + "   total")
    for phrase, row in table.items():
        cells = "".join(str(row.get(y, 0)).rjust(8) for y in years)
        print(f"{phrase.ljust(width)}  {cells}   {sum(row.values())}")
    print(f"\n* {this_year} is a partial year; compare complete years only.")
    last_full = min(to_year, this_year - 1)
    base = last_full - 3
    for phrase, row in table.items():
        now, then = row.get(last_full, 0), row.get(base, 0)
        if then:
            print(f"{phrase}: {last_full} vs {base} = {now / then:.1f}x ({then} -> {now})")
        else:
            print(f"{phrase}: {last_full} = {now}, no papers in {base}")
    print("\nRead with care: counts depend on the exact phrase (try 2-3 phrasings) and include non-indexed venues. "
          "This measures research momentum, not Scopus volume.")
    return 0


# ---------------------------------------------------------------- venue

def cmd_venue(a):
    q = a.query.strip()
    if ISSN_RE.match(q):
        issn = q if "-" in q else f"{q[:4]}-{q[4:]}"
        src = get_json(openalex_url(f"/sources/issn:{issn.upper()}"))
        sources = [src] if src else []
    else:
        data = get_json(openalex_url("/sources", {"search": q, "per-page": 5}))
        sources = (data or {}).get("results", [])
    if not sources:
        print(f"No OpenAlex source found for {q!r}. For a journal that claims wide indexing, that is a warning sign. "
              "Conference proceedings are usually listed under their series (e.g. the proceedings series name), "
              "so search for that instead.")
        return 1
    for s in sources:
        counts = {c["year"]: c["works_count"] for c in s.get("counts_by_year") or []}
        recent = ", ".join(f"{y}: {counts[y]}" for y in sorted(counts)[-4:])
        print(f"{s.get('display_name')}  [{s.get('type')}]")
        print(f"  ISSN: {', '.join(s.get('issn') or []) or '-'} | publisher: {s.get('host_organization_name') or '-'}")
        print(f"  open access: {s.get('is_oa')} | in DOAJ: {s.get('is_in_doaj')} | "
              f"APC listed by OpenAlex: {('USD ' + str(s['apc_usd'])) if s.get('apc_usd') else '-'} (confirm on the journal site)")
        print(f"  papers per year: {recent or '-'} | homepage: {s.get('homepage_url') or '-'}\n")
    print(f"Checked {datetime.date.today().isoformat()}.\n"
          "Scopus status: NOT CHECKED. Scopus blocks scripted access. The student must search the ISSN at\n"
          "https://www.scopus.com/sources, confirm coverage is current (not 'discontinued'), and confirm the\n"
          "homepage listed there matches the site they will submit to (hijacked-journal check).")
    return 0


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="find candidate papers")
    s.add_argument("query")
    s.add_argument("--publisher", default="any",
                   help="comma list: " + ",".join(CROSSREF_MEMBERS) + ",any (default any)")
    s.add_argument("--type", choices=["journal", "conference", "any"], default="any")
    s.add_argument("--from", dest="from_year", type=int, default=datetime.date.today().year - 5)
    s.add_argument("--to", dest="to_year", type=int)
    s.add_argument("--n", type=int, default=15)
    s.add_argument("--sort", choices=["relevance", "cited", "recent"], default="relevance")
    s.add_argument("--source", choices=["crossref", "openalex"], default="crossref")
    s.add_argument("--json", action="store_true")

    ab = sub.add_parser("abstract", help="print abstracts by DOI")
    ab.add_argument("dois", nargs="+")

    v = sub.add_parser("verify", help="check DOIs, titles or a .bib/.txt file")
    v.add_argument("items", nargs="*")
    v.add_argument("--file")

    c = sub.add_parser("cite", help="format DOIs in a citation style")
    c.add_argument("dois", nargs="+")
    c.add_argument("--style", default="ieee",
                   help="one of " + ", ".join(list(STYLES) + ["bibtex"]) + ", or any CSL style id")

    t = sub.add_parser("trend", help="papers per year for topic phrases")
    t.add_argument("phrases", nargs="+")
    t.add_argument("--from", dest="from_year", type=int, default=datetime.date.today().year - 6)
    t.add_argument("--to", dest="to_year", type=int)
    t.add_argument("--loose", action="store_true", help="match words anywhere instead of the exact phrase")

    ve = sub.add_parser("venue", help="journal lookup by ISSN or name")
    ve.add_argument("query")

    a = ap.parse_args()
    if a.cmd == "search":
        a.publisher = [p.strip().lower() for p in a.publisher.split(",") if p.strip()]
        bad = [p for p in a.publisher if p != "any" and p not in CROSSREF_MEMBERS]
        if bad:
            ap.error(f"unknown publisher {bad}; choose from {', '.join(CROSSREF_MEMBERS)}, any")
        a.n = max(1, min(a.n, 50))
    handlers = {"search": cmd_search, "abstract": cmd_abstract, "verify": cmd_verify,
                "cite": cmd_cite, "trend": cmd_trend, "venue": cmd_venue}
    try:
        sys.exit(handlers[a.cmd](a))
    except NetError as e:
        print(f"[SERVICE ERROR] {e}\nNothing from this run counts as verified. Retry, or verify by hand.",
              file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
