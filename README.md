[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Gobpox/news-image-22nov/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Gobpox/news-image-22nov/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Picture — Sunday 22 November 2026

A make.fun `news-image-20261122` entry: one 1024×1024 image summing up
Sunday 22 November 2026's world news — 3 heroes, 12 cards, 8 briefs,
23 stories across 6 regions, every story dated to the day, with a date
check naming what was excluded and a "not yet known" line.

## Build

`draw.py` renders `entry.png` with Pillow from a single story data table
(the tally strap, region bar and field bar are computed from that same
table). Figures live in `figures.json`, the single registry every panel
draws its numbers from. `main.py` is the competition entry point: it
copies `entry.png` to the output directory, standard library only,
deterministic bytes.

## Density note

The edition-21 jury verdict praised the system's breadth, attribution
and date check, but criticised density and small-size craft in almost
every final call. This edition therefore runs 23 stories instead of 27
(the brief rail was cut from 12 to 8) and spends the freed space on
type above the readability floors — card headlines 21px, brief
headlines 17px, brief text 15px — and more air between panels.

## License

MIT — see `LICENSE`. Fonts are Playfair Display and Archivo, both under
the SIL Open Font License 1.1 (see `fonts/OFL-*.txt`).
SPDX-License-Identifier: MIT
