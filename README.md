# The World in One Day — 26 November 2026

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261126-navy)](https://make.fun/c/news-image-20261126/)

One image summing up the world's news of **Thursday 26 November 2026**,
for the [make.fun news-image-20261126 competition](https://make.fun/c/news-image-20261126/)
($100, top 50).

## The page

A single 1024 × 1024 cream newspaper page, dense but tidy:

- **3 big leads** — the US tariff plan for 14 partners, Kim's tactical-nuke
  order, and fire in the Gulf (Ras Tanura claim, Hormuz mine claims).
- **10 more illustrated cards** — Jerusalem judges on Case 4000, Kyiv's
  jet/refinery claims, the Cairo tanker fire (31 dead), the postponed 100th
  Macy's parade, the first foreigner aboard Tiangong, S&P's Nvidia watch,
  Wall Street's wild Wednesday, the expelled Swiss envoy, the pardoned
  turkeys, and Bangladesh's +36% garment wage.
- **23 short text stories** — from Poland's NATO missile plea to the
  Duterte trial's 100 witnesses.
- **Sidebar** — THE DAY IN NUMBERS, a WHERE IT HAPPENED map (12 places),
  a UTC timeline, and a DATE CHECK box with a HOW SURE legend.

Every fact was checked against Reuters, AP, BBC, CNN and the wires on
26 November 2026. Claims are marked ○ and the two older items on the page
(Andy Taylor died Mon 23 Nov; Shenzhou-24 launched Tue 25 Nov) are flagged
in the DATE CHECK box. See [SOURCES.md](SOURCES.md) for the verification
notes, including stories that were researched and dropped.

All illustrations are flat shapes drawn programmatically in `render.py` —
no photographs were downloaded or used.

## Files

| File | What it is |
| --- | --- |
| `entry.png` | The finished page, 1024 × 1024, 244 KB. |
| `main.py` | The entry point. Standard library only: it copies `entry.png` to the output directory. |
| `render.py` | The program that draws the page with Pillow. Run it to rebuild `entry.png`. |
| `SOURCES.md` | How every story was verified, and what was dropped. |

## How to run

```sh
# Rebuild the image (needs Pillow; deterministic — two runs are byte-identical)
python3 render.py

# Run the entry the way the grader does (standard library only)
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
# -> /tmp/out/entry.png, identical to the entry.png in this repo
```

## Verification

- `entry.png` is exactly 1024 × 1024 and under 1 MiB.
- `render.py` run twice produces byte-identical output (same SHA-256).
- `main.py` run as user `nobody`, from a read-only copy of the repo, with
  `python3 -S` and `cwd=/tmp`, produces output byte-identical to `entry.png`
  — twice.
- A programmatic wrap check confirms no headline, sub, text item, number
  label or timeline row overflows its allotted lines, and the finished page
  was visually inspected at 2× zoom for clipped text and contradictions.
