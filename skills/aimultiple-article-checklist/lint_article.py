#!/usr/bin/env python3
"""Mechanical checks on the structural rules in aimultiple-article-checklist/SKILL.md.

The rules were written down long before this script existed and were still missed, because a
rule enforced nowhere is not a rule. Everything checkable is checked here.

Usage:  python3 lint_article.py <draft.md> [--strict]

Exit 1 if any FAIL fires. WARN never sets the exit code: those are rules with legitimate
exceptions, and the author decides. --strict makes WARN fail too.

Judgement rules that cannot be mechanised, and still need a human read:
  research depth, source quality, Surfer score, sponsorship placement, whether a takeaway is
  actually non-obvious, whether the intro beats the top 3 Google results.
"""
import re
import sys

# H2s are noun phrases naming a section. A finite verb makes the header a claim sentence,
# which is the format Berkk rejected on 2026-08-05 ("A broad-panel shortlist does not carry
# to multivariate data"). Questions are exempt: "What are agentic LLM systems?" is house style.
CLAIM_VERBS = (
    r"\b(is|are|was|were|does|do|did|has|have|had|can|cannot|will|should|must|"
    r"changes?|carries|carry|shows?|conceals?|favors?|favours?|depends?|beats?|leads?|"
    r"hides?|makes?|needs?|reveals?|proves?|means?|wins?|loses?|breaks?|holds?)\b"
)
QUESTION_START = r"^(what|why|how|when|where|which|who|is|are|do|does|can|should)\b"

# Matched on word boundaries. A substring test flags "very" inside "every", which is how the
# first version of this file reported filler in a clean article.
FILLER = (
    "basically", "simply", "very", "more and more", "these days", "in fact",
    "over time", "for a long time", "this article", "our article",
)
# "just" is filler as an intensifier and legitimate as a quantifier ("just below 0.5"), so it
# is only flagged when it is not doing measurement work.
JUST_OK = r"just\s+(below|above|under|over|before|after|short|outside|inside|enough)\b"


def main(path, strict=False):
    text = open(path).read()
    fails, warns = [], []

    def fail(rule, detail=""):
        fails.append((rule, detail))

    def warn(rule, detail=""):
        warns.append((rule, detail))

    lines = text.split("\n")
    h1 = [l for l in lines if re.match(r"^# ", l)]
    h2 = [l[3:].strip() for l in lines if re.match(r"^## ", l)]
    h3 = [l[4:].strip() for l in lines if re.match(r"^### ", l)]

    # ---- banned characters and emphasis ----
    for name, ch in (("em dash", "—"), ("en dash", "–"),
                     ("curly quote", "’"), ("curly double quote", "“")):
        if ch in text:
            fail("no %s" % name, "%d occurrence(s)" % text.count(ch))
    italics = re.findall(r"(?<![\*\w])\*[^*\n]{1,80}\*(?![\*\w])", text)
    if italics:
        fail("no italic emphasis", str(italics[:3]))
    if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", text):
        fail("no emoji in prose")

    # ---- headers ----
    # Published drafts often carry no H1: the title lives in WordPress, not the markdown.
    # Zero or one is fine, two competing titles is not.
    if len(h1) > 1:
        fail("at most one H1", "%d found" % len(h1))
    for h in h2:
        if re.search(r"\b(19|20)\d{2}\b", h):
            fail("no year in a header", h)
        if not re.match(QUESTION_START, h, re.I) and re.search(CLAIM_VERBS, h, re.I):
            fail("H2 is a noun phrase, not a claim sentence", h)
        if len(h.split()) > 12:
            warn("H2 over 12 words", h)
        rest = h.split()[1:]
        # Acronyms and hyphenated caps (A-CODE-LLM, HIVE-COTE) are not title casing.
        capped = [w for w in rest
                  if w[:1].isupper() and not w.isupper() and not re.search(r"[A-Z]{2}", w)]
        if len(capped) >= 3 and len(capped) / len(rest) >= 0.5:
            warn("H2 looks title-cased; lowercase common nouns", h)
    for h in h3:
        if re.search(r"\b(19|20)\d{2}\b", h):
            fail("no year in a header", h)
    if len(h2) != len(set(h2)):
        fail("no two H2s with identical text", "breaks the table of contents")
    if len(text.split()) > 500 and len(h2) < 3:
        fail("articles over 500 words need more than two H2s", "%d H2s" % len(h2))

    # empty H2 sections and oversized ones
    idx = [i for i, l in enumerate(lines) if re.match(r"^## ", l)] + [len(lines)]
    total_words = len(text.split())
    for a, b in zip(idx, idx[1:]):
        body = "\n".join(lines[a + 1:b])
        title = lines[a][3:].strip()
        if not body.strip():
            fail("no H2 with empty body", title)
        share = len(body.split()) / total_words if total_words else 0
        if share > 0.40 and not re.search(r"^### ", body, re.M):
            fail("no H2 over 40% of the article without H3s", "%s at %.0f%%" % (title, share * 100))

    # ---- intro ----
    if h1:
        after_h1 = text.split(h1[0], 1)[1]
        intro = after_h1.split("\n## ", 1)[0]
        n = len(intro.split())
        if n > 90:
            fail("intro is a few sentences, not a wall", "%d words before the first H2" % n)
        elif n > 60:
            warn("intro is getting long", "%d words" % n)

    # ---- charts ----
    if re.search(r"\[CHART\s+C", text):
        fail("no chart description block in the body",
             "charts embed as [nivo_charts id=\"...\" /]; meaning goes in body takeaways")
    embeds = re.findall(r"\[nivo_charts id=\"([^\"]+)\"", text)
    for e in embeds:
        if not e.isdigit():
            warn("chart id is still a placeholder", e)

    # ---- paragraphs ----
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    body_paras = [p for p in paras
                  if not p.startswith(("#", "|", "-", "*", "[nivo_charts"))]
    for p in body_paras:
        visible = re.sub(r"\[efn_note\].*?\[/efn_note\]", "", p, flags=re.S)
        if len(visible) > 430:
            warn("paragraph over 430 characters", visible[:70] + "...")

    # ---- bold budget ----
    bold = sum(len(m) for m in re.findall(r"\*\*(.+?)\*\*", text, re.S))
    if total_words and bold / len(text) > 0.05:
        fail("bold under 5% of body text", "%.1f%%" % (100 * bold / len(text)))

    # ---- bullets ----
    runs, run = [], 0
    for l in lines:
        if re.match(r"^\s*[-*] ", l):
            run += 1
        else:
            if run:
                runs.append(run)
            run = 0
    if run:
        runs.append(run)
    if runs and max(runs) > 8:
        warn("bullet list over 8 items; prose by default", "longest run %d" % max(runs))

    # ---- filler ----
    # Citation titles are quoted source text, not our prose: "MiniRocket: A Very Fast (Almost)
    # Deterministic Transform" is not a filler violation.
    low = re.sub(r"\[efn_note\].*?\[/efn_note\]", " ", text, flags=re.S).lower()
    hits = [f for f in FILLER if re.search(r"\b%s\b" % re.escape(f), low)]
    for m in re.finditer(r"\bjust\b", low):
        if not re.match(JUST_OK, low[m.start():]):
            hits.append("just")
            break
    if hits:
        warn("filler words present", ", ".join(hits))

    # ---- report ----
    print("%s: %d words, %d H2, %d H3, %d charts"
          % (path, total_words, len(h2), len(h3), len(embeds)))
    for r, d in fails:
        print("  FAIL  %s   %s" % (r, d))
    for r, d in warns:
        print("  WARN  %s   %s" % (r, d))
    if not fails and not warns:
        print("  clean")
    print("%d fail, %d warn" % (len(fails), len(warns)))
    return 1 if (fails or (strict and warns)) else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(args[0], strict="--strict" in sys.argv))
