from analysis.aggression_stats_analyzer import AggressionStatsAnalyzer
from analysis.cbet_stats_analyzer import CBetStatsAnalyzer
from analysis.fold_to_cbet_stats_analyzer import FoldToCBetStatsAnalyzer
from analysis.showdown_stats_analyzer import ShowdownStatsAnalyzer
from features.preflop_stats_analyzer import PreflopStatsAnalyzer
from models.villain_action_history import VillainActionHistory


class ActionHistoryAnalyzer:
    def __init__(self):
        self.analyzers = [
            PreflopStatsAnalyzer(),
            CBetStatsAnalyzer(),
            AggressionStatsAnalyzer(),
            FoldToCBetStatsAnalyzer(),
            ShowdownStatsAnalyzer()
        ]

    def analyze(self, history: VillainActionHistory) -> dict:
        result = {}
        for analyzer in self.analyzers:
            result.update(analyzer.analyze(history))
        return result