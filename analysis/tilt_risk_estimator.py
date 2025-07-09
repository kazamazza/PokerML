from models.poker_session import PokerSession
from typing import Literal


class TiltRiskEstimator:
    def __init__(self):
        pass

    def estimate(self, session: PokerSession) -> str:
        """
        Estimate the risk that the villain is currently tilted, based on profile and recent outcomes.
        """
        villain_profiles = session.villainProfiles
        risk_levels = []

        for villain_id, profile in villain_profiles.items():
            level = self._assess_individual_tilt(profile)
            risk_levels.append(level)

        if not risk_levels:
            return "low"

        # Take the highest observed tilt level
        return max(risk_levels, key=self._risk_score)

    def _assess_individual_tilt(self, profile: dict) -> Literal["low", "medium", "high"]:
        if profile.get("emotionalTiltLevel") == "tilted":
            return "high"
        recent_triggers = profile.get("recentHandResults", [])
        big_losses = [res for res in recent_triggers if res["outcome"] == "big_loss"]

        if len(big_losses) >= 2:
            return "high"
        if len(big_losses) == 1:
            return "medium"

        return "low"

    def _risk_score(self, level: str) -> int:
        return {"low": 0, "medium": 1, "high": 2}[level]