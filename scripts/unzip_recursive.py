import os
import zipfile
import argparse

def extract_all_zips(zip_path: str, dest_dir: str):
    queue = [zip_path]
    os.makedirs(dest_dir, exist_ok=True)

    while queue:
        current_zip = queue.pop()
        with zipfile.ZipFile(current_zip, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)

        # Cleanup queue and relocate .txt files
        for root, _, files in os.walk(dest_dir):
            for file in files:
                full_path = os.path.join(root, file)

                if file.endswith(".zip"):
                    queue.append(full_path)
                elif file.endswith(".txt") and os.path.dirname(full_path) != dest_dir:
                    os.rename(full_path, os.path.join(dest_dir, os.path.basename(full_path)))

    # Delete all .zip files after processing
    for root, _, files in os.walk(dest_dir):
        for file in files:
            if file.endswith(".zip"):
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f"❌ Failed to delete zip: {file} — {e}")

    print(f"✅ Extracted all .txt and cleaned up zips in: {dest_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True, help="Path to top-level .zip file")
    parser.add_argument("--stake", required=True, help="Numeric stake, e.g., 10 for NL10")

    args = parser.parse_args()
    stake_dir = f"data/raw/NL{args.stake}"
    extract_all_zips(args.zip, stake_dir)