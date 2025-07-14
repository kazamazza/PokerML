from analysis.session_context_analyzer import SessionContextAnalyzer
from board_analyzer import BoardAnalyzer
from models.poker_ml_input import PsychologicalContext
from models.poker_session import PokerSession


class PsychologicalContextBuilder:
    def __init__(
        self,
        session_context_analyzer: SessionContextAnalyzer,
        board_analyzer: BoardAnalyzer
    ):
        self.session_ctx = session_context_analyzer
        self.board_analyzer = board_analyzer

    def build(self, session: PokerSession) -> PsychologicalContext:
        session_metrics = self.session_ctx.analyze(session)

        return PsychologicalContext(
            hero_recent_big_loss_flag=session_metrics.get("hero_recent_big_loss_flag"),
            multiway_aggression_score=session_metrics.get("multiway_aggression_score"),
            board_cluster_key=self.board_analyzer.get_cluster_id(session.board),
        )