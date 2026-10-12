# Research brief: UP Voter Pulse (per Assembly Constituency)

Goal: for ONE Uttar Pradesh Assembly Constituency (AC), find the Top 5 positives and Top 5 negatives
that voters there actually talk about, written in the voter's voice, ready for a survey.

## Rules (from UP_403_AC_Voter_Pulse_Template.pdf)
- Voter voice: each statement must read as something a voter in that AC would say aloud.
  Do: "नल लगे हैं, पर पानी नहीं आता"  Avoid: "JJM coverage gap".
- NO electoral data: no vote share, margins, caste arithmetic, party/candidate names' results.
  Focus on lived experience: water, roads, power, jobs, prices, farming (sugarcane dues, fertiliser,
  stray cattle), health, schools, safety, flooding, pollution, local projects.
- Short and in Hindi: one line, ~12 words, Devanagari.
- Ranked: 1 = highest vote impact, 5 = lowest.
- Evidenced: every item has a Basis with a REAL source URL you actually opened, naming the outlet.
- Inference flagged: if you could not find a source specific to this AC/district, prefix the Hindi
  and English statements with * and write "Inference: ..." in the basis. Never pass a guess off as fact.
- Local first: at least 3 of 5 negatives must be specific to the AC or its district (named village,
  town, road, mill, river, hospital, project, etc.). Positives should also be local where possible.
- Source priority: local Hindi media (Amar Ujala, Dainik Jagran, Hindustan / Live Hindustan, Navbharat
  Times, Patrika), then national ground reports (HT, TOI, Indian Express, The Hindu, Scroll, Gaon
  Connection, Down To Earth, The Wire, etc.), then government releases (PIB, UP govt, district NIC site,
  Lok Sabha/Rajya Sabha replies).
- Prefer recent sources (2024-2026). Note the date of each source.

## Accuracy (critical - the user said "do not make any mistake")
- First CONFIRM the AC number, official name, district and reserved status (SC/ST/none) from the
  Election Commission / Wikipedia "List of constituencies of the Uttar Pradesh Legislative Assembly".
- Only cite URLs you actually fetched and that actually support the claim. Never invent or guess a URL.
  If a fetch fails, do not cite it. Do not fabricate figures; quote numbers exactly as the source states.
- If a source is about the district, not the AC, say so in the basis ("district-level").
- Search in BOTH Hindi and English (e.g. "<AC name> समस्या", "<AC name> विधानसभा मुद्दे",
  "<town> सड़क / पानी / गन्ना भुगतान / जाम / बाढ़", "<AC name> problems", "<AC> development project").
  Do many searches (aim 15+). Use WebSearch mode "extended" for hard-to-find local facts.

## Output
Write exactly one JSON file at the path you are given, UTF-8, this shape:
{
  "ac_no": 1,
  "ac_name": "Behat",
  "ac_name_hindi": "बेहट",
  "reserved": "None" | "SC" | "ST",
  "district": "Saharanpur",
  "region": "Paschim UP",   // one of: Paschim UP, Rohilkhand, Braj, Awadh, Kanpur-Doab, Bundelkhand, Purvanchal
  "summary": "One English sentence: what dominates complaints and appreciation.",
  "identity_source": "URL confirming AC no/name/district",
  "positives": [
    {"rank": 1, "english": "...", "hindi": "...", "inference": false,
     "basis": "short fact as stated by source", "sources": [{"outlet": "Amar Ujala", "date": "2025-06-14", "url": "https://..."}]}
    // ... exactly 5, ranked
  ],
  "negatives": [ /* exactly 5, same shape; >=3 must be AC/district-specific */ ],
  "notes": "anything uncertain or worth a field check"
}
Validate it is valid JSON (e.g. python3 -c "import json;json.load(open('PATH'))") before finishing.
Reply with just: the file path, and a 2-line summary.

## Lessons from ACs 1-20 (apply from AC 21 on)
- Confirm every named place is INSIDE this AC before using it: use the AC's Wikipedia page "extent"
  (tehsils, kanungo circles, nagar panchayats), or a news report that names the vidhan sabha. Police
  station areas and tehsils do not equal AC boundaries. If unsure, say "AC membership unconfirmed" in basis.
- Never cite mirror/aggregator URLs if the original opens: spidertest.amarujala.com -> www.amarujala.com;
  Ground News / public.app / CropGPT -> find the original outlet. Read the article itself, not a headline.
- A positive must be something voters appreciate (a delivered benefit, a completed or started project,
  a fixed problem) - not a geography/heritage fact, a forecast, or an official announcement alone.
- Write as a voter speaks: no "विभाग का कहना है", no headline style, no full stops. Allegations stay
  allegations ("आरोप है"). Do not add facts the source does not state.
- Add "ac_specific_negatives": N (count only sourced, non-inference negatives whose place is confirmed
  inside the AC) at top level.
- Run python3 /home/user/UP-Seat-Issue-Mapping/scripts/check_ac.py <your file> and fix until it prints OK.
- Do not say "Draft (sourced)" yourself; just be honest in notes.
