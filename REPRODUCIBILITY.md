# Current evidence and reproduction boundaries

## One safe command

Run `python -B scripts/verify_review.py` from this directory with Python 3.11+. It uses only the standard library, writes nothing, makes no network calls and does not recompute market outcomes or confidence intervals.

It verifies this edition's inventory and SHA-256 hashes; 71 bull event records in the 35/36 groups with 24/27 dates; their five pivot quantiles; counts and passage categories against the frozen location summaries; quoted full-EWMA probability points; and that all 1,392 native gaps in the saved 4,872-row family span zero under both saved block settings. It also checks local Markdown links. These are consistency checks on the **current final results**, not a pass carried over from an unrelated historical verifier.

## Six retained tables

| File under data/ | Meaning |
| --- | --- |
| derived_event_locations.csv | 71 genuine bull-side event records, date/N and derived distances only; no vendor prices |
| location_quantiles.csv | 32 MA5/MA10 summaries including near/far, all/A backgrounds and four outcome definitions |
| location_summary_all_N.csv | 464 final bull-side summaries across MA2–MA30; favorable and adverse locations retained |
| probability_points.csv | 696 saved landscape rows; near/far origin counts, success rates and uncertainty summaries |
| simultaneous_bands.csv | Complete 4,872-row final comparison family with 20-/60-session half-widths |
| exposure_counts.csv | 5,800 eligible-origin and success counts, including background complements and unknowns where available |

For locations, context 0=all and 1=A; origin_band 0=near and 1=far; outcomes 0/1/2/3 are strict-origin/strict-running-low/tolerant-origin/tolerant-running-low. Passage arrays are ordered: no passage within five minutes; marker before first passage; same close; marker after first passage. Non-overlap origins and raw origins are different populations.

For probability tables, S3 is the full-EWMA final definition. S0/S1/S2 are the frozen sensitivity bridge retained within the final multiple-comparison family: original sigma20 throughout; EWMA distance only; then EWMA reaction magnitude at unchanged origins. S3 also changes eligibility. These table identifiers are needed to interpret the final uncertainty family; they are not an invitation to read old experiment-round narratives. Contexts 0/1/2 are all/A/C; the exposure table additionally uses 3=non-C and 4=unknown. Period 0 is full; 1–4 are 2014–16, 2017–19, 2020–22, 2023–25. In the bands table, outcome and metric identify the saved estimate; half-widths are not standard errors.

## What this edition does not reproduce

No complete, portable final empirical pipeline has been certified. Some final calculations ran in interactive read-only memory sessions. This compact edition supplies their saved evidence and an honest verifier, not invented replacement implementation code. Historical scientific code and complete candidate v3 remain locally preserved outside this upload scope.

A genuine independent rebuild requires licensed source prices, reliable prior daily closes, session/eligibility definitions, original implementation recovery and the frozen resampling inputs. A fresh vendor download is not automatically equivalent. This edition contains no broker/downloader configuration and no market acquisition procedure; arrange any future data access through the provider's official licensing process. Source environment packages are not required for the artifact checks above.

## Selected implementation evidence

`code/reference_geometry.py` retains the original `decimal_cents` and `exact_live_geometry` function text; `code/session_clock.py` retains `session_minutes` and `clock_regions`. Source filenames, function line ranges and hashes are recorded in PROVENANCE.json. These selected earlier measurement utilities show exact-cent parsing, integer-sign live-reference geometry, close-stamped timestamp checks and session-length-aware clock regions. Imports/constants are retained and a provenance header is added; function bodies are not rewritten. They do not constitute or certify the final reaction detector, background construction or resampling pipeline. Their NumPy dependency is not needed for the standard-library review verifier; no package installation or full execution test was performed for this edition. The source project's declared NumPy lower bound was 1.26, not a newly certified environment lock.

## Mathematical source

`docs/early_model/typeset/main.tex` is an **edited model-background edition**, not an empirical program. It preserves choices, beliefs, payoff/FOC/SOC, fixed-point existence, complementarity, local stability, positive-action conditions, salience and CDF interpretation, with explicit qualifications. The retired measurement section is abbreviated; the full model reading remains in the v3 backup. The built-in desktop compiler returned success for this edited source. A standalone PDF has not been exported; the available compile tool does not export and the applicable desktop-automation rules prevent the UI workaround. No terminal TeX installation was assumed. Current empirical definitions are in MAINLINE_REVIEW.md and take precedence.
