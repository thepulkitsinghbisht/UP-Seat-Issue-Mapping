# Round 3: voter-voice wording pass (no new research)

For each AC JSON file you are given, review the 10 statements ("hindi" and "english") against
research/BRIEF.md. Edit ONLY the "hindi", "english" and "notes" fields. Do NOT change sources, basis,
inference flags or ranks, and do NOT add facts that the basis does not state.

Fix any statement that:
- is not something a voter would say aloud (e.g. "विभाग का कहना है...", news-headline style, official
  claims, full stops/headline punctuation) -> rewrite in first-person or plain spoken voter voice,
  keeping exactly the fact in the basis.
- is a "positive" that is not appreciation (a forecast like "crushing is expected to start", a
  geography/heritage fact) -> reword as what the voter appreciates, staying true to the basis; if that
  is impossible, leave it and add to notes: "P<rank> weak positive: <why>".
- mentions party names, vote, election, caste -> remove that part. Praise or criticism of a local
  official's work is allowed only if the basis supports it.
- Hindi longer than 13 words -> shorten. Keep the leading "*" on inference items; no "*" on others.
- English is not a faithful translation of the Hindi -> fix the English.

After editing each file run: python3 /home/user/UP-Seat-Issue-Mapping/scripts/check_ac.py <file>
(must print OK). Reply with one line per AC listing what you changed (or "no change").
