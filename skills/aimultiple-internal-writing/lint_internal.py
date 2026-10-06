#!/usr/bin/env python3
"""Form check for internal text (cards, messages, reports, handoffs).

  python3 lint_internal.py FILE [--lang tr|en] [--fail-over 2.5] [--json]

Score = rule hits per 100 words (code, URLs and paths excluded). Long lists
are reported as info and are not scored. Exit code 1 if the score is above
--fail-over. Checks form only, not truth or usefulness.
"""

import argparse
import json
import re
import sys

MAX_INSTRUCTION = 20
MAX_SENTENCE = 25
MAX_LIST = 5

COMMON = {
    "semicolon": r";",
    "em_dash": r"—",
    "italic_emphasis": r"(?<![\*\w])\*(?=\S)[^*\n]+?(?<=\S)\*(?![\*\w])|(?<![_\w])_(?=\S)[^_\n]+?(?<=\S)_(?![_\w])",
}

EN = {
    "contraction": r"\b\w+(?:n't|'re|'ve|'ll|'d)\b",
    "present_perfect": r"\b(?:has|have|had)\s+(?:not\s+)?(?:\w+ed|been|done|made|gone|seen|written|run|built|taken|given|found|got|gotten|sent|kept|left|put|set)\b",
    "phrasal_verb": r"\b(?:spin|spins|spun) (?:up|down)\b|\b(?:kick|kicks|kicked) off\b|\b(?:roll|rolls|rolled) out\b|\b(?:dive|dives|dived) into\b|\b(?:reach|reaches|reached) out\b|\b(?:circle|circles|circled) back\b|\b(?:double|doubles|doubled) down\b|\b(?:wrap|wraps|wrapped) up\b",
    "long_word": r"\b(?:utilize[sd]?|utilization|leverage[sd]?|leveraging|facilitate[sd]?|commence[sd]?|initiate[sd]?|prior to|subsequent to|in order to|regarding|obtain(?:s|ed)?|additionally|furthermore|moreover)\b",
    "opener_closer": r"\b(?:great question|good question|let me know if|hope this helps|hope that helps|happy to (?:help|clarify)|feel free to|in summary|to summarize|to recap|in conclusion)\b",
    "hedge": r"\b(?:perhaps|arguably|presumably|it is worth noting|it should be noted|it is important to note|please note that)\b",
    "vague_estimate": r"\b(?:some work|a bit of work|a while|shortly|fairly soon|in a bit)\b",
    "not_x_but_y": r"\bnot (?:just |only )?\w+(?: \w+){0,5}, (?:but|it's|it is)\b|\bit's not \w+(?: \w+){0,5}, it's\b",
}

TR = {
    "bureaucratic_ending": r"\w+(?:mektedir|maktadır|mektedirler|maktadırlar)\b",
    "nominal_form": r"\b\w+(?:ması|mesi) (?:gerekmektedir|gerekiyor|yapıldı|yapılmalıdır|sağlandı)\b|\b\w+ yapılması\b",
    "opener_closer": r"(?i)\b(?:harika soru|güzel soru|umarım işine yarar|umarım yardımcı|başka bir şey olursa|yardımcı olabileceğim|özetle|kısacası|sonuç olarak)\b",
    "hedge": r"(?i)\b(?:belki de|aslında|bir nevi|bir bakıma|bir şekilde)\b",
    "vague_estimate": r"(?i)\b(?:biraz zaman|bir süre sonra|yakında|kısa sürede)\b",
    "not_x_but_y": r"\b\w+ değil, \w+",
}

# Turkish passive: consonant stem + -ıl/-il/-ul/-ül, vowel stem + -n, and "edil-".
# Info only: "düşündü" or "bulundu" can be false hits.
TR_PASSIVE = re.compile(
    r"\b(?:\w{2,}[bcçdfgğhjklmnprsştvyz](?:ıl|il|ul|ül)|\w{2,}[aeıioöuü]n|edil)"
    r"(?:dı|di|du|dü|mış|miş|muş|müş|ıyor|iyor|uyor|üyor|ecek|acak|meli|malı)\b"
)

# Turkish sentence that opens an inline list with a colon: 3+ words before ": ",
# 3+ comma-separated items after it. Nobody writes Turkish mail like this.
# "Bütçe: ..." label lines have a short prefix and do not match.
TR_COLON_LIST = re.compile(r"^(?:\S+\s+){2,}\S+:\s+[^:]+,[^:]+,[^:]+$")

IMPERATIVE_EN = re.compile(r"^(?:add|apply|ask|check|close|copy|create|delete|fix|log|make|move|open|post|read|remove|rerun|run|send|set|start|update|upload|use|write)\b", re.I)


def clean(text: str) -> str:
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " CODE ", text)
    text = re.sub(r"https?://\S+", " URL ", text)
    text = re.sub(r"(?:~|\.{1,2})?/[\w./-]+", " PATH ", text)
    return text


def detect_lang(text: str) -> str:
    tr = len(re.findall(r"[ğışçöüĞİŞÇÖÜ]", text))
    return "tr" if tr / max(len(text), 1) > 0.005 else "en"


def words(s: str) -> int:
    return len(re.findall(r"[\wğışçöüĞİŞÇÖÜ'’-]+", s))


def lines_with_sentences(text: str):
    """Yield (line_no, sentence, is_list_item) for prose and list items."""
    for no, line in enumerate(text.split("\n"), 1):
        raw = line.strip()
        if not raw or raw.startswith(("#", "|")):
            continue
        is_item = bool(re.match(r"^(?:[-*+]|\d+[.)])\s+", raw))
        body = re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", raw)
        body = re.sub(r"\*\*|__", "", body)
        for s in re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9\"“])", body):
            if s.strip():
                yield no, s.strip(), is_item


def long_lists(text: str):
    hits, run, start = [], 0, 0
    for no, line in enumerate(text.split("\n") + [""], 1):
        if re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", line):
            run, start = run + 1, start or no
            continue
        if run > MAX_LIST:
            hits.append((start, f"list of {run} items (cap {MAX_LIST} for action lists)"))
        run, start = 0, 0
    return hits


def lint(text: str, lang: str):
    body = clean(text)
    found = []
    for no, s, is_item in lines_with_sentences(body):
        n = words(s)
        cap = MAX_INSTRUCTION if (is_item or (lang == "en" and IMPERATIVE_EN.match(s))) else MAX_SENTENCE
        if n > cap:
            found.append(("long_sentence", no, f"{n} words > {cap}: {s[:70]}"))
        if lang == "tr" and TR_COLON_LIST.match(s):
            found.append(("colon_list", no, f"list after a colon inside a sentence: {s[:70]}"))
    rules = dict(COMMON, **(EN if lang == "en" else TR))
    flags = 0 if lang == "tr" else re.I
    for name, pat in rules.items():
        for no, line in enumerate(body.split("\n"), 1):
            if name == "italic_emphasis":
                line = re.sub(r"^\s*[-*+]\s+", "", line)
            elif name not in COMMON:
                # Quoted examples and "(not X)" counter-examples are not the writer's own words.
                line = re.sub(r'"[^"\n]*"|“[^”\n]*”|\((?:not|değil)\b[^)]*\)', " ", line)
            for m in re.finditer(pat, line, flags):
                found.append((name, no, m.group(0)))
    info = long_lists(body)
    if lang == "tr":
        for no, line in enumerate(body.split("\n"), 1):
            for m in TR_PASSIVE.finditer(line):
                info.append((no, f"possible passive '{m.group(0)}': if the actor is known, write it active"))
    total_words = sum(words(l) for l in body.split("\n"))
    score = round(100 * len(found) / max(total_words, 1), 2)
    return found, info, total_words, score


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--lang", choices=["tr", "en"])
    ap.add_argument("--fail-over", type=float, default=2.5)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    text = open(args.file, encoding="utf-8").read()
    lang = args.lang or detect_lang(text)
    found, info, n_words, score = lint(text, lang)

    if args.json:
        print(json.dumps({"lang": lang, "words": n_words, "score_per_100w": score,
                          "hits": [{"rule": r, "line": l, "text": t} for r, l, t in found],
                          "info": [{"line": l, "text": t} for l, t in info]}, ensure_ascii=False, indent=1))
    else:
        for rule, line, txt in sorted(found, key=lambda x: x[1]):
            print(f"L{line:<4} {rule:<20} {txt}")
        for line, txt in info:
            print(f"L{line:<4} {'info':<20} {txt}")
        print(f"lang={lang} words={n_words} hits={len(found)} score={score}/100w target<{args.fail_over}")
    sys.exit(1 if score > args.fail_over else 0)


if __name__ == "__main__":
    main()
