import argparse
import json
import re
from pathlib import Path

from hand_schema import HandHistory

# ── CONFIG ─────────────────────────────────────────────────────────────────────
HAND_SPLIT_RE = re.compile(r"(?=^PokerStars Hand #\d+)", re.MULTILINE)
HOLE_CARDS_RE = re.compile(r"Dealt to (.+?) \[([2-9TJQKA][cdhs]) ([2-9TJQKA][cdhs])\]")
SHOWDOWN_RE = re.compile(r"^(.+?): shows \[([2-9TJQKA][cdhs]) ([2-9TJQKA][cdhs])\]")
ACTION_LINE_RE = re.compile(r"^(.+?): (.+)$")

FLOP_RE = re.compile(r"\*\*\* FLOP \*\*\* \[([^\]]+)\]")
TURN_RE = re.compile(r"\*\*\* TURN \*\*\* \[[^\]]+\] \[([^\]]+)\]")
RIVER_RE = re.compile(r"\*\*\* RIVER \*\*\* \[[^\]]+\] \[([^\]]+)\]")

# ── HELPERS ────────────────────────────────────────────────────────────────────
def determine_street(board_cards: list[str]) -> str:
    if len(board_cards) == 5:
        return "river"
    elif len(board_cards) == 4:
        return "turn"
    elif len(board_cards) == 3:
        return "flop"
    return "preflop"

def extract_board(lines: list[str]) -> list[str]:
    board = []
    for line in lines:
        if (m := FLOP_RE.search(line)):
            board += m.group(1).split()
        if (m := TURN_RE.search(line)):
            board.append(m.group(1))
        if (m := RIVER_RE.search(line)):
            board.append(m.group(1))
    return board

def parse_hand_block(text: str, stake_label: str) -> dict:
    lines = text.strip().splitlines()
    hand = {
        "hand_id": None,
        "street": "preflop",
        "hole_cards_by_player": {},
        "board": [],
        "actions": [],
        "players": [],
        "winnings": [],
        "min_bet": 0.10,
        "stakes": stake_label,
    }

    for line in lines:
        if line.startswith("PokerStars Hand #"):
            hand["hand_id"] = line.split("#")[1].split(":")[0]
            break

    for line in lines:
        if (m := HOLE_CARDS_RE.search(line)):
            player, card1, card2 = m.group(1), m.group(2), m.group(3)
            hand["hole_cards_by_player"][player.strip()] = [card1, card2]

    for line in lines:
        if (m := SHOWDOWN_RE.match(line)):
            player, card1, card2 = m.group(1), m.group(2), m.group(3)
            if player.strip() not in hand["hole_cards_by_player"]:
                hand["hole_cards_by_player"][player.strip()] = [card1, card2]

    hand["board"] = extract_board(lines)
    hand["street"] = determine_street(hand["board"])

    for line in lines:
        if (m := ACTION_LINE_RE.match(line)):
            player, action = m.group(1).strip(), m.group(2).strip()
            hand["actions"].append(f"{player} {action}")
            if player not in hand["players"]:
                hand["players"].append(player)

    # ✅ Return normalized dict via schema
    return HandHistory(**hand).dict()

# ── MAIN ───────────────────────────────────────────────────────────────────────
def parse_all_hands(stake: int):
    stake_label = f"NL{stake}"
    raw_dir = Path(f"data/raw/{stake_label}")
    out_dir = Path("data/parsed")
    out_file = out_dir / f"hands_{stake_label}.jsonl"
    out_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    with out_file.open("w") as out_f:
        for txt_file in raw_dir.rglob("*.txt"):
            content = txt_file.read_text(errors="ignore")
            blocks = HAND_SPLIT_RE.split(content)
            for block in blocks:
                if not block.strip():
                    continue
                parsed = parse_hand_block(block, stake_label)
                json.dump(parsed, out_f)
                out_f.write("\n")
                total += 1

    print(f"✅ Parsed {total} hands to: {out_file}")

# ── ENTRY POINT ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stake", type=int, required=True, help="Stake in big blind cents, e.g. 10 for NL10")
    args = parser.parse_args()
    parse_all_hands(args.stake)