import argparse
import json
from pathlib import Path

# ── CONFIG ─────────────────────────────────────────────────────────────────────
PARSED_DIR = Path("data/parsed")
FILTERED_DIR = Path("data/filtered")


# ── MAIN ───────────────────────────────────────────────────────────────────────
def filter_by_street(stake: str):
    stake_tag = f"NL{stake}"
    infile = PARSED_DIR / f"hands_{stake_tag}.jsonl"
    if not infile.exists():
        raise FileNotFoundError(f"❌ Missing input file: {infile}")

    FILTERED_DIR.mkdir(parents=True, exist_ok=True)

    street_outfiles = {
        "preflop": (FILTERED_DIR / f"hands_{stake_tag}_preflop.jsonl").open("w"),
        "flop": (FILTERED_DIR / f"hands_{stake_tag}_flop.jsonl").open("w"),
        "turn": (FILTERED_DIR / f"hands_{stake_tag}_turn.jsonl").open("w"),
        "river": (FILTERED_DIR / f"hands_{stake_tag}_river.jsonl").open("w"),
    }

    count_by_street = {"preflop": 0, "flop": 0, "turn": 0, "river": 0}

    with infile.open() as in_f:
        for line in in_f:
            record = json.loads(line)
            street = record.get("street")
            if street in street_outfiles:
                json.dump(record, street_outfiles[street])
                street_outfiles[street].write("\n")
                count_by_street[street] += 1

    for fh in street_outfiles.values():
        fh.close()

    print("✅ Filtered hands by street:")
    for street, count in count_by_street.items():
        print(f"  {street}: {count} hands")


# ── ENTRY POINT ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stake", type=str, required=True, help="e.g. 10 for NL10")
    args = parser.parse_args()
    filter_by_street(args.stake)