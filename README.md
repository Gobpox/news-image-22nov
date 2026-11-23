[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Gobpox/news-image-22nov/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Gobpox/news-image-22nov/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Picture — Sunday 22 November 2026

A make.fun `news-image-20261122` entry: one 1024×1024 image summing up
Sunday 22 November 2026's world news — 3 heroes, 10 cards and a
22-line ALSO rail: exactly 35 stories across 6 regions, every story dated to the day, with a date
check naming what was excluded and a "not yet known" line.

## Build

`draw.py` renders `entry.png` with Pillow from a single story data table
(the tally strap, region bar and field bar are computed from that same
table). Figures live in `figures.json`, the single registry every panel
draws its numbers from. `main.py` is the competition entry point: it
copies `entry.png` to the output directory, standard library only,
deterministic bytes.

## Structure note

The layout clones, zone by zone, the measured template of edition
21's final winner (superskie): eyebrow with computed counts and a red
rule, giant Playfair date, a "THE DAY IN UTC" timeline bar, hero
panels with an in-scene red statement band, numbered kickers and
status chips, compact 5-across x 2-row cards (single-pictogram strip drawn
at strip scale, flag, status chip, big overlay, headline, deck), a left map with
region-coloured pins and a counted dot legend beside a two-column
ALSO rail, a red-framed DATE CHECK box with tab, and a footer with
the HOW SURE legend and sources line. The story set is locked at
exactly 35 (3 heroes + 10 cards + 22 ALSO briefs); all overlap
audits, the figures registry check and the 300px gate run clean.

## How the page is composed

The canvas is read top to bottom the way a newspaper front page is:
a strap first, then the date, then the day itself. The strap carries
no hand-typed counts — the story total, the region tally and the
field tally are all computed from the same story table the panels
draw from, so the arithmetic on the page can never disagree with the
page itself. Under the date, a timeline bar places the day's turning
points in UTC, because the stories span every timezone and the page
needs one honest clock.

The three heroes are the day's heaviest stories, each with a drawn
scene, a red statement band inside the scene carrying the fact that
matters most, and a deck underneath. The ten cards are built for the
small-size glance: every card's picture strip is a single pictogram
drawn natively at strip size — a drone, three missiles, a megaphone,
a burning factory, a capsized hull, a burning house, an explosion, a
space probe, a racing car, a rising chart — so the topic reads from
the symbol alone before any word is decoded. The ALSO rail then takes
the density: twenty-two one-line briefs, each with its place, its
one-line fact and its source tag, for the reader who wants the whole
day rather than the headlines.

The map is a dot grid, not a coastline tracing: land is a table of
rows in the source, one character per cell, and the numbered pins sit
on the stories that have a place. Beside it the DATE CHECK box does
the page's honesty work in public — it names the famous events that
were checked against the date and excluded because they belong to
another day, and it prints a NOT YET KNOWN line for what Sunday had
not yet decided when the page closed.

## Checking the page

`draw.py` audits itself as it draws. Every text box is recorded, and
at the end three audits run: no two text boxes may intersect or come
within a hair of each other; no rule or frame line may pass through
text; and no text or flag may sit on top of scene graphics it would
fight with. A separate registry check walks the finished source and
confirms that every number on the page is the registry's display for
that figure, that no superseded value survives anywhere — not even in
a comment — and that the tallies a reader can recount by hand (the
strap, the legend, the pins) match the story table. The build is
deterministic: run it twice and the bytes are identical.

## License

MIT — see `LICENSE`. Fonts are Playfair Display and Archivo, both under
the SIL Open Font License 1.1 (see `fonts/OFL-*.txt`).
SPDX-License-Identifier: MIT
