from typing import Tuple, List


class RolePositionParser:
    def __init__(self, player_role: str):
        self.player_role = player_role
        self.hero_position, self.villain_positions = self._parse_role(player_role)

    def _parse_role(self, role: str) -> Tuple[str, List[str]]:
        if "_vs_" not in role:
            return role, []  # fallback

        parts = role.split("_vs_")
        hero = parts[0]
        villains = []

        # Handle 2-player and multiway roles
        if len(parts) == 2:
            villains = parts[1].split("_vs_") if "_vs_" in parts[1] else [parts[1]]

        return hero, villains

    def get_hero(self) -> str:
        return self.hero_position

    def get_villains(self) -> List[str]:
        return self.villain_positions