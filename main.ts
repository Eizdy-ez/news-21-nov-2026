// Entry for make.fun news-image-20261121 (Node 22, standard library only).
// The front page is drawn by draw.py and shipped in this repository as
// entry.png; this program copies that file to the grader's output
// directory. It uses no network and writes the same bytes on every run,
// because a byte-for-byte copy cannot vary between runs.
//
// Run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// The image sums up Saturday 21 November 2026: the FBI's probe into a
// suspected hack of the NCIC crime database; the AI sell-off erasing
// the Nasdaq's 2026 gains; a 6.9 earthquake in Peru's Andes; COP31
// running overtime in Antalya; the UK-EU post-Brexit deal; and Trump
// weighing new strikes on Iran.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outputDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
const destination = join(outputDir, "entry.png");
copyFileSync(join(here, "entry.png"), destination);
