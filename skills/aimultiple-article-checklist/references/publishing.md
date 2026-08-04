# Publishing checklist — detail

## Title

- Great titles are the highest-leverage optimization. Few words, big impact.
- Include the current year until June if it fits naturally. After June, start rotating the next year or a shorter evergreen variant.
- Include a specific number when you can justify it (example: "7 <topic> benchmarks we ran in 2026"). Numbers signal effort.
- Change the title from the WordPress title field at the top of the editor. Do not touch the SEO title / slug field (it is managed downstream).
- Never put the year in an H2 or H3. Those rot and are painful to bulk-update.

## Permalink

- Must match the target keyword, not the title.
- WordPress rewrites the permalink the first time you save. After the first save, manually check and correct the permalink so it equals the keyword slug.

## Meta description / snippet

- Include the main relevant terms for the keyword.
- Exclude filler like "This article". Lead with content.
- Keep it readable as a Google result preview.

## Category

- Single category, most specific (leaf-level).
- Do not add parent categories. If you add "Financial Close", the system infers "Finance" automatically.
- Exception: articles at the intersection of a technology and an industry get one category per axis. Example: `chatgpt-use-cases-fashion` gets a tech category and an industry category.

## Archetype tag

Tag every article with its archetype (vendor list, vs article, use case, how-to, etc.). Used for analytics and clustering.

## Featured image

Every article should carry a featured image. Follow AIMultiple image guidelines.

## Tags

- `NewArticleTag`: apply to every new article.
- `EditTag`: apply to every article the analyst wrote OR substantively edited. One EditTag per article, old editors removed. If you want credit for an article's ranking, your EditTag must be on it.
- Archetype tag: as above.

Analyst tag lookups live in the `Analysts` sheet of the AIMultiple roster Google Sheet. Contact Hazal if you do not have tags.

## Link audit

Before publishing, verify:
1. Every internal link points to `research.aimultiple.com` or `aimultiple.com` (not `research-headless.aimultiple.com`).
2. Every external link has "open in new tab" enabled.
3. Every customer link carries the AIMultiple tracking tag.
4. Every external source passes the domain authority / spam risk check (websiteseochecker.com).

## Plagiarism check

Run smallseotools plagiarism checker against the final draft. Any hit is a blocker until resolved. Google treats duplicate content as a ranking penalty.

## Final read-through

1. Intro: better than the top 3 Google results on clarity or insight density.
2. Second paragraph foreshadows what the article delivers.
3. Structure: H2/H3/H4 hierarchy is clean. Bullets used where helpful.
4. CTA present at or near the end.
5. Featured image set.
6. Permalink matches the target keyword.
7. Bold text under 5% of body.
8. No em dashes anywhere in the body.

## Not publish-ready

Do not send unfinished drafts for review. Reviewers waste time flagging issues the author already knows about. Finish the draft first, then request review.
