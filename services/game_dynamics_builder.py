from analysis.action_history_analyzer import ActionHistoryAnalyzer
from models.poker_ml_input import GameDynamics, BetAction
from models.poker_session import PokerSession


class GameDynamicsBuilder:
    def __init__(self, action_history_analyzer: ActionHistoryAnalyzer):
        self.analyzer = action_history_analyzer

    def build(self, session: PokerSession) -> GameDynamics:
        stats = self.analyzer.analyze(session)  # You can reuse per-villain logic here
        bet_history = [
            BetAction(player=a.player, action=a.action, size=a.amount or 0.0)
            for a in session.action_history
            if a.action in {"bet", "raise", "call", "3bet", "shove"}
        ]

        return GameDynamics(
            bet_history=bet_history,
            hero_tilt_state=stats.get("hero_tilt_state"),
            session_heat=stats.get("session_heat")
        )