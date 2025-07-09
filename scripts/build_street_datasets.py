import argparse
import json
from pathlib import Path
from tqdm import tqdm

# ── CONFIG ─────────────────────────────────────────────────────────────────────
PARSED_DIR = Path("data/parsed")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STREETS = ["preflop", "flop", "turn", "river"]

# ── HELPERS ────────────────────────────────────────────────────────────────────
def extract_hero(record):
    for player, cards in record.get("hole_cards_by_player", {}).items():
        if cards:
            return player
    return None

def extract_board_for_street(board, street):
    if street == "flop":
        return board[:3] if len(board) >= 3 else None
    elif street == "turn":
        return board[:4] if len(board) >= 4 else None
    elif street == "river":
        return board[:5] if len(board) == 5 else None
    return []

def extract_action_for_street(actions, hero, street):
    for action in actions:
        if action.startswith(hero) and f"{street}" in action.lower():
            # Explicitly tagged street (rare)
            return action
        elif action.startswith(hero):
            if street == "preflop" and "raises" in action or "calls" in action or "folds" in action:
                return action
            elif street == "flop" and "*** FLOP ***" in action:
                return None  # skip headers
            elif street == "turn" and "*** TURN ***" in action:
                return None
            elif street == "river" and "*** RIVER ***" in action:
                return None
    # fallback: return any post-street action
    for action in actions:
        if action.startswith(hero):
            if street == "flop" and "*** FLOP ***" not in action:
                return action
            elif street == "turn" and "*** TURN ***" not in action:
                return action
            elif street == "river" and "*** RIVER ***" not in action:
                return action
    return None

# ── MAIN ───────────────────────────────────────────────────────────────────────
def build_all_datasets(stake: str):
    stake_tag = f"NL{stake}"
    input_file = PARSED_DIR / f"hands_{stake_tag}.jsonl"
    out_files = {
        street: (OUTPUT_DIR / f"{street}_dataset_{stake_tag}.jsonl", 0) for street in STREETS
    }

    # Open all files for writing
    writers = {s: open(f[0], "w") for s, f in out_files.items()}

    with open(input_file) as f:
        for line in tqdm(f, desc=f"Building datasets for {stake_tag}"):
            record = json.loads(line)
            hero = extract_hero(record)
            if not hero:
                continue

            hero_hand = record.get("hole_cards_by_player", {}).get(hero)
            if not hero_hand:
                continue

            for street in STREETS:
                if street == "preflop":
                    board = []
                else:
                    board = extract_board_for_street(record["board"], street)
                    if not board:
                        continue

                action = extract_action_for_street(record["actions"], hero, street)
                if not action:
                    continue

                out_record = {
                    "hand_id": record["hand_id"],
                    "street": street,
                    "hero_hand": hero_hand,
                    "board": board,
                    "stakes": record["stakes"],
                    "min_bet": record["min_bet"],
                    "hero": hero,
                    "villains": [p for p in record["players"] if p != hero],
                    "action_line": action,
                }

                json.dump(out_record, writers[street])
                writers[street].write("\n")
                out_files[street] = (out_files[street][0], out_files[street][1] + 1)

    # Close all files and print summary
    for street, (file_path, count) in out_files.items():
        writers[street].close()
        print(f"✅ Saved {count} hands to: {file_path}")

# ── ENTRY POINT ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stake", type=str, required=True, help="Stake (e.g. 10 for NL10)")
    args = parser.parse_args()
    build_all_datasets(args.stake)