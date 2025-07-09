import argparse
import json
from pathlib import Path
from tqdm import tqdm

# ── CONFIG ─────────────────────────────────────────────────────────────────────
PARSED_DIR = Path("data/parsed")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_fold_actions(record):
    folds = []
    hand_id = record.get("hand_id")
    actions = record.get("actions", [])
    board = record.get("board", [])
    players = record.get("players", [])
    min_bet = record.get("min_bet")
    stakes = record.get("stakes")

    current_street = "preflop"
    street_headers = {
        "*** flop ***": "flop",
        "*** turn ***": "turn",
        "*** river ***": "river"
    }

    for action in actions:
        action_lower = action.lower()
        for header, street in street_headers.items():
            if header in action_lower:
                current_street = street
                break

        if "folds" in action_lower:
            for player in players:
                if action.startswith(player):
                    folds.append({
                        "hand_id": hand_id,
                        "street": current_street,
                        "board": board[:3] if current_street == "flop" else board[:4] if current_street == "turn" else board[:5] if current_street == "river" else [],
                        "hero": player,
                        "hero_hand": None,  # unknown when folded
                        "action_type": "fold",
                        "villains": [p for p in players if p != player],
                        "min_bet": min_bet,
                        "stakes": stakes
                    })
    return folds

# ── MAIN ───────────────────────────────────────────────────────────────────────
def build_fold_only_dataset(stake: str):
    stake_tag = f"NL{stake}"
    input_file = PARSED_DIR / f"hands_{stake_tag}.jsonl"
    output_file = OUTPUT_DIR / f"fold_only_dataset_{stake_tag}.jsonl"
    count = 0

    with open(input_file) as f_in, open(output_file, "w") as f_out:
        for line in tqdm(f_in, desc=f"Building fold-only dataset for {stake_tag}"):
            record = json.loads(line)
            fold_actions = extract_fold_actions(record)
            for fold in fold_actions:
                json.dump(fold, f_out)
                f_out.write("\n")
                count += 1

    print(f"✅ Saved {count} fold actions to: {output_file}")

# ── ENTRY POINT ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stake", type=str, required=True, help="Stake (e.g. 10 for NL10)")
    args = parser.parse_args()
    build_fold_only_dataset(args.stake)