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

## License

MIT — see `LICENSE`. Fonts are Playfair Display and Archivo, both under
the SIL Open Font License 1.1 (see `fonts/OFL-*.txt`).
SPDX-License-Identifier: MIT
