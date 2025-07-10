import json
import os
from typing import Dict, List


class BoardTextureLoader:
    CONFIG_PATH = "/config/board_textures.json"

    @classmethod
    def load(cls) -> Dict[str, List[str]]:
        if not os.path.exists(cls.CONFIG_PATH):
            raise FileNotFoundError(f"❌ board_textures.json not found at: {cls.CONFIG_PATH}")

        with open(cls.CONFIG_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"❌ Failed to parse board_textures.json: {str(e)}")

        # Ensure values are always lists (normalize string-only entries)
        normalized: Dict[str, List[str]] = {}
        for key, value in data.items():
            if isinstance(value, str):
                normalized[key] = [value]
            elif isinstance(value, list):
                normalized[key] = value
            else:
                raise ValueError(f"⚠️ Unexpected board texture format under key '{key}': {value}")

        return normalized