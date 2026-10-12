# Round 2: verify and strengthen one AC file

You are improving an existing draft. Read research/BRIEF.md first (all its rules still apply), then the
AC JSON file you are given. Edit ONLY that file, in place.

## Step 1 - Verify every cited source (do this first)
For each item with sources, WebFetch every URL and check that the page really supports the claim
(right place, right fact, numbers exactly as stated). Then:
- Supported -> keep. Fix outlet/date if wrong.
- Not supported, page dead, wrong place, or you cannot open it -> remove that source.
- Replace mirror/aggregator URLs with the original article where possible:
  spidertest.amarujala.com -> www.amarujala.com (same path; confirm it opens), Ground News / public.app /
  CropGPT / other aggregators -> find the original outlet's article. If you cannot, keep the aggregator
  only if it clearly states the fact, and say "(aggregator)" in basis.
- An item left with no supporting source must become inference (inference=true, * prefix) or be replaced.

## Step 2 - Strengthen
Use your searches on the gaps listed for your AC (given in your prompt), in this order:
1. Get at least 3 of 5 negatives specific to this AC (a named town/village/road/mill/drain/hospital that
   is INSIDE this AC). Confirm that each named place is actually in this AC (Wikipedia AC page, tehsil,
   or the news report naming the vidhan sabha). If a place is in a neighbouring AC, do not use it.
2. Replace * inference items with sourced ones where you can find a real source. Positives count too:
   look for completed local projects (roads, bridges, medical college, CHC, mill expansion, expressway,
   water tank, school) reported in local Hindi media.
3. Prefer 2024-2026 sources. A 2021-or-older source is acceptable only if the issue is shown to persist.
Re-rank 1-5 by likely vote impact after changes.

## Step 3 - Format (all mandatory)
- Every item with inference=true starts its "hindi" AND "english" with "*". Items with inference=false
  must NOT start with "*" and must have at least one source with a URL.
- Hindi statement: one line, at most 12-13 words, plain spoken Hindi as a voter would say it.
- Exactly 5 positives and 5 negatives, ranks 1..5.
- Add "round2": {"verified_sources": N, "removed_sources": N, "ac_specific_negatives": N,
  "changes": "short list of what changed"} at top level.
- Validate: python3 /home/user/UP-Seat-Issue-Mapping/scripts/check_ac.py <your file>  -> must print OK.

Never invent a URL, figure, place or date. If you run out of searches, stop, leave honest * flags, and
say so in notes. Reply with: file path, the check_ac.py output line, and a 2-line summary.
