[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Eizdy-ez/news-21-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Eizdy-ez/news-21-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 in One Image

Sum up the world's news of Saturday 21 November 2026 in one image — a program that writes the image to `/output/entry.png`. Entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261121).

## The image

An original editorial front page (1024 × 1024 PNG, drawn programmatically with Pillow — no photographs, no copied artwork) that a viewer with no news feed can read. Tiered like a real front page: the three biggest stories get pictures, the next six get cards, and sixteen more run as a text-only list — 25 stories in all:

- **Heroes — Iran strikes US bases in Bahrain; drones set the Russian cargo ship Sparta II ablaze off Finland; COP31 deadlocked over fossil fuels in overtime in Antalya.**
- **Cards — FBI probes a suspected hack of the NCIC crime database; AI sell-off erases the Nasdaq's 2026 gains (S&P 500 −3.7%, in correction); Mexico captures cartel boss "Chapo Isidro"; UK & EU sign their biggest post-Brexit deal; a strong quake shakes Peru's Andes; an Anthropic mathematician claims an AI-assisted proof of the Riemann hypothesis.**
- **Also on Saturday:** a world map with numbered pins, and sixteen more stories, each in its own outlined box with a number on a coloured background — the Kryvyi Rih missile strike; Geneva killer-robot talks (128 nations, accord aimed by 2028); three Houthi missiles intercepted over Riyadh; the EU–Indonesia trade pact; BepiColombo entering orbit around Mercury; the M6.8 Timor-Leste quake; the Nigeria funeral boat toll; tainted alcohol in Manipur; England beating the All Blacks 37–12; BTS taking five MAMA awards; France's cost-of-living marches; the Basra power-station fire; the ICJ ruling fallout; Trump defending his Putin ties; the Gaza food-vehicle strike; and the M5.5 Qinghai quake.

## How it works

- `draw.py` — draws `entry.png` from scratch (run it again to regenerate the image).
- `main.ts` — Node 22, standard library only. It copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). No network access.
- `entry.png` — the 1024 × 1024 image itself.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Two runs write byte-identical files (verified: same sha256).

## License

MIT — see [LICENSE](LICENSE).
