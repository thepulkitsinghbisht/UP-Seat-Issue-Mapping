"""Compile research/ac/AC-*.json into the template table (Markdown) and a survey CSV.

Formatting only: every statement, basis and source comes from the JSON files unchanged.
"""
import csv, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lo, hi = (int(a) for a in (sys.argv[1:3] or (1, 20)))
tag = f"AC{lo:03d}-{hi:03d}"

acs = []
for p in sorted(glob.glob(os.path.join(ROOT, "research", "ac", "AC-*.json"))):
    d = json.load(open(p, encoding="utf-8"))
    if lo <= d["ac_no"] <= hi:
        acs.append(d)


def n_inf(d):
    return sum(i["inference"] for s in ("positives", "negatives") for i in d[s])


def local_negs(d):
    return d.get("round2", {}).get("ac_specific_negatives", d.get("ac_specific_negatives"))


def status(d):
    loc = local_negs(d)
    if n_inf(d) == 0 and loc is not None and loc >= 3:
        return "Draft (sourced)"
    return "Draft (field check)"


def cell(items):
    return " ".join(f"{i['rank']}) {i['hindi']}" for i in items)


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def links(item):
    out = []
    for s in item.get("sources", []):
        label = s.get("outlet") or "source"
        if s.get("date"):
            label += f", {s['date']}"
        out.append(f"[{esc(label)}]({s['url']})")
    return "; ".join(out)


md = [f"# UP Voter Pulse: ACs {lo} to {hi}", ""]
md += [
    "Five positives and five negatives per Assembly Constituency, in the voter's voice, built to the "
    "rules in `UP_403_AC_Voter_Pulse_Template.pdf`. Research by Haiku agents in two rounds: a first "
    "pass, then a round that opened every cited link, removed sources that did not support their "
    "claim or were about places outside the AC, and filled gaps.",
    "",
    "`*` = inference, not backed by a source; verify in the field before use.",
    "",
    "## Status",
    "",
    "| AC No | AC name | District | Unsourced (*) of 10 | AC-specific negatives (agent count) | Status |",
    "|---|---|---|---|---|---|",
]
for d in acs:
    loc = local_negs(d)
    md.append(f"| {d['ac_no']} | {d['ac_name']} | {d['district']} | {n_inf(d)} | "
              f"{'n/a' if loc is None else loc} | {status(d)} |")

md += ["", "## AC template table", "",
       "| AC No | AC name | District | Region | Top 5 positives (सकारात्मक) | Top 5 negatives (नकारात्मक) | Status |",
       "|---|---|---|---|---|---|---|"]
for d in acs:
    name = d["ac_name"] + (f" ({d['reserved']})" if d["reserved"] not in ("None", None, "") else "")
    md.append(f"| {d['ac_no']} | {esc(name)} | {d['district']} | {d['region']} | "
              f"{esc(cell(d['positives']))} | {esc(cell(d['negatives']))} | {status(d)} |")

md += ["", "## AC detail", ""]
for d in acs:
    md += [f"### {d['ac_no']}. {d['ac_name']} ({d['ac_name_hindi']}), {d['district']}", "",
           esc(d["summary"]), ""]
    for side, title in (("positives", "Positives"), ("negatives", "Negatives")):
        md += [f"**{title}**", "", "| # | Voter says (English) | Survey statement (Hindi) | Basis |",
               "|---|---|---|---|"]
        for i in d[side]:
            basis = esc(i["basis"])
            src = links(i)
            md.append(f"| {i['rank']} | {esc(i['english'])} | {esc(i['hindi'])} | "
                      f"{basis}{' (' + src + ')' if src else ''} |")
        md.append("")
    if d.get("notes"):
        md += [f"**Field-check notes:** {esc(d['notes'])}", ""]

md_path = os.path.join(ROOT, "research", f"UP_AC_Voter_Pulse_{tag}.md")
open(md_path, "w", encoding="utf-8").write("\n".join(md) + "\n")

csv_path = os.path.join(ROOT, "research", f"survey_items_{tag}.csv")
with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ac_no", "ac_name", "district", "type", "rank", "statement_hindi", "statement_english",
                "inference", "basis", "source_urls"])
    for d in acs:
        for side, kind in (("positives", "positive"), ("negatives", "negative")):
            for i in d[side]:
                w.writerow([d["ac_no"], d["ac_name"], d["district"], kind, i["rank"], i["hindi"],
                            i["english"], "yes" if i["inference"] else "no", i["basis"],
                            " ".join(s["url"] for s in i.get("sources", []))])

print(md_path)
print(csv_path)
