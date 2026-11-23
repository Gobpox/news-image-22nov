[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Gobpox/news-image-22nov/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Gobpox/news-image-22nov/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Picture — Sunday 22 November 2026

A make.fun `news-image-20261122` entry: one 1024×1024 image summing up
Sunday 22 November 2026's world news — 3 heroes, 12 cards and a
20-line ALSO rail: 35 stories across 6 regions, every story dated to the day, with a date
check naming what was excluded and a "not yet known" line.

## Build

`draw.py` renders `entry.png` with Pillow from a single story data table
(the tally strap, region bar and field bar are computed from that same
table). Figures live in `figures.json`, the single registry every panel
draws its numbers from. `main.py` is the competition entry point: it
copies `entry.png` to the output directory, standard library only,
deterministic bytes.

## Structure note

Edition 21's top 10 were counted directly from their artefacts: 35-43
stories each, built as 13-15 large pictured stories over a dense
one-line "ALSO" rail of 21-30 briefs. This entry follows that
structure: 3 heroes + 12 cards pictured large (card headlines 21px),
plus a 20-line ALSO ON SUNDAY rail of numbered one-line briefs
(place, key fact, source) at 14px, the brief-text floor. Density is
quarantined in the rail; the pictured layer stays airy.

## License

MIT — see `LICENSE`. Fonts are Playfair Display and Archivo, both under
the SIL Open Font License 1.1 (see `fonts/OFL-*.txt`).
SPDX-License-Identifier: MIT
