"""Structural checks for research/ac/AC-*.json against the template rules."""
import glob, json, re, sys

DEV = re.compile(r"[ऀ-ॿ]")
REGIONS = {"Paschim UP", "Rohilkhand", "Braj", "Awadh", "Kanpur-Doab", "Bundelkhand", "Purvanchal"}

def check(path):
    d = json.load(open(path, encoding="utf-8"))
    issues = []
    if d.get("region") not in REGIONS:
        issues.append(f"bad region {d.get('region')!r}")
    for side in ("positives", "negatives"):
        items = d.get(side, [])
        if len(items) != 5:
            issues.append(f"{side}: {len(items)} items")
        if [i.get("rank") for i in items] != [1, 2, 3, 4, 5]:
            issues.append(f"{side}: ranks not 1-5")
        for i in items:
            tag = f"{side[0].upper()}{i.get('rank')}"
            h = i.get("hindi", "")
            if not DEV.search(h):
                issues.append(f"{tag}: Hindi missing")
            if len(h.lstrip("*").split()) > 16:
                issues.append(f"{tag}: Hindi {len(h.split())} words")
            if i.get("inference"):
                if not h.startswith("*"):
                    issues.append(f"{tag}: inference without *")
            else:
                if h.startswith("*"):
                    issues.append(f"{tag}: * but inference=false")
                if not any(s.get("url", "").startswith("http") for s in i.get("sources", [])):
                    issues.append(f"{tag}: sourced item has no URL")
    inf = sum(i.get("inference", False) for s in ("positives", "negatives") for i in d.get(s, []))
    return d, inf, issues

for p in sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else "research/ac/AC-*.json")):
    d, inf, issues = check(p)
    print(f"AC-{d['ac_no']:03d} {d['ac_name']:<18} {d['district']:<14} inferences={inf}  " + ("; ".join(issues) or "OK"))
