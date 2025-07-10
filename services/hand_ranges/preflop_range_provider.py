from typing import Dict, List

class PreflopRangeProvider:
    ranges: Dict[str, List[str]] = {
        "BTN_vs_BB": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs", "KQs", "QJs"],
        "UTG_vs_BB": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs"],
        "CO_vs_BB": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "AQs", "KQs"],
        "SB_vs_BB": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "AQs", "AJs"],
        "MP_vs_BB": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "AQs"],
        "BTN_vs_SB_vs_BB": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs", "KQs"],
        "HeadsUp": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "AQs", "KQs"],
        "Multiway": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs"],
        "ThreeBetPot": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs", "KQs"],
        "SRP_vs_Limper": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs", "AJs"],
        "UTG_vs_CO": ["AA", "KK", "QQ", "JJ", "AKs", "AQs"],
        "MP_vs_BTN": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs", "KQs"],
        "CO_vs_BTN": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "KQs", "QJs"],
        "SB_vs_UTG": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs"],
        "BB_vs_SB": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "AQs", "KJs"],
        "BTN_vs_CO": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs", "KQs", "QJs"]
    }

    @classmethod
    def get_range(cls, role: str) -> List[str]:
        return cls.ranges.get(role, ["AA", "KK"])

    @classmethod
    def supported_roles(cls) -> List[str]:
        return list(cls.ranges.keys())