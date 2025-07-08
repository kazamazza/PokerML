import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import json
import pandas as pd
from tqdm import tqdm
from features.feature_extractor import FeatureExtractor

# ── CONFIG ───────────────────────────────────────────────
STREETS = ["preflop", "flop", "turn", "river"]
INPUT_DIR = Path("data/processed")
BASE_OUTPUT_DIR = Path("data/features")

# ── MAIN ─────────────────────────────────────────────────
def build_feature_datasets(stake: str):
    extractor = FeatureExtractor()
    stake_tag = f"NL{stake}"

    for street in STREETS:
        input_file = INPUT_DIR / f"{street}_dataset_{stake_tag}.jsonl"
        output_dir = BASE_OUTPUT_DIR / stake_tag / street
        output_dir.mkdir(parents=True, exist_ok=True)

        features_file = output_dir / "features.csv"
        labels_file = output_dir / "labels.csv"

        if not input_file.exists():
            print(f"⚠️ Skipping {street} — file not found: {input_file}")
            continue

        features = []
        labels = []

        with open(input_file) as f:
            for line in tqdm(f, desc=f"Extracting features: {street}"):
                record = json.loads(line)
                result = extractor.extract(record, street=street)
                if result:
                    x, y = result
                    features.append(x)
                    labels.append(y)

        if features:
            pd.DataFrame(features).to_csv(features_file, index=False)
            pd.Series(labels, name="label").to_csv(labels_file, index=False)
            print(f"✅ Saved {len(features)} examples for {street} at {stake_tag}")
        else:
            print(f"⚠️ No valid examples found for {street} at {stake_tag}")

# ── ENTRY POINT ──────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stake", type=str, required=True, help="e.g. 10 for NL10")
    args = parser.parse_args()
    build_feature_datasets(args.stake)