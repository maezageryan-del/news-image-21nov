# The World in One Day — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/maezageryan-del/news-image-21nov/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/maezageryan-del/news-image-21nov/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A broadsheet front page that sums up Saturday 21 November 2026 in one image:
38 verified stories across 7 regions — Russian missiles landing in Poland,
a massive overnight barrage on Kyiv, the Nasdaq's −5.3% AI sell-off, COP31
running into overtime, Bitcoin below $60,000, and 25 more stories from the
same day. Three lead panels, ten medium panels, a markets strip, a pinned
world map, and a date check that keeps Thursday's news out.

Every story here happened, or was first reported, on Saturday 21 November
2026. Officials' counts are attributed to their sources.

## How to run

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=/output node main.ts
```

`render.py` (Python 3, PIL only) reads `stories.json` and draws the
1024×1024 front page to `entry.png`. `main.ts` (Node 22, standard library
only) verifies the PNG and copies it byte-for-byte to
`$MAKEFUN_OUTPUT_DIR/entry.png`. No network is used; two runs are
byte-identical.

## Bounty

[news-image-20261121 on make.fun](https://make.fun/bounty/news-image-20261121)

Entry by [@nimble-beacon-24](https://make.fun/r/htn7pdyx) — try make.fun
via the referral link: https://make.fun/r/htn7pdyx

## License

MIT — see [LICENSE](LICENSE).
