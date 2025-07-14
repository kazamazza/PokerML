from typing import Dict, Any
from sqlalchemy.orm import Session
from db.models.hand_range import HandRange
from models.board_texture import BoardTexture
from models.poker_session import PokerSession, PlayerRole


class HandRangeService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_range(
        self,
        player_role: PlayerRole,
        round: str,
        board: str,
        board_cluster: str,
        board_texture: BoardTexture,
        villain_profile: Dict[str, Any]
    ) -> Dict[str, list]:
        """
        Attempts to fetch a hand range based on full villain profile and board info.
        Fallbacks: exact match → cluster → similarity → default.
        """
        if isinstance(player_role, PlayerRole):
            player_role = player_role.value
        print("▶️ get_range called with:", player_role, round, board_cluster)
        query_filters = dict(
            player_role=player_role,
            round=round,
            villain_type=villain_profile.get("villain_profile_type", "default"),
            villain_aggression_factor=villain_profile.get("villain_aggression_factor"),
            villain_vpip=villain_profile.get("villain_vpip"),
            villain_pfr=villain_profile.get("villain_pfr"),
            villain_tilt_level=villain_profile.get("villain_emotional_tilt_level"),
            villain_overall_winrate=villain_profile.get("villain_overall_winrate"),
            villain_bluff_frequency=villain_profile.get("villain_bluff_frequency"),
            villain_check_raise_frequency=villain_profile.get("villain_check_raise_freq"),
            villain_cold_call_frequency=villain_profile.get("villain_cold_call_frequency"),
            villain_hero_bully_history=villain_profile.get("villain_hero_bully_history"),
            villain_hero_vs_villain_winrate=villain_profile.get("hero_vs_villain_winrate"),
        )

        # 🟢 Exact match on board
        exact = self.db.query(HandRange).filter_by(board=board, **query_filters).first()
        # Exact match
        if exact:
            return {player_role: exact.hand_range}  # type: ignore

        # 🟡 Fallback: Cluster key only
        cluster = self.db.query(HandRange).filter_by(board_cluster=board_cluster, **query_filters).first()
        if cluster:
            print("⚠️ No exact match. Using board cluster fallback.")
            return {player_role: cluster.hand_range}  # type: ignore

        # 🔵 Fallback: Similar board texture structure/suit
        structure = board_texture.structure
        suit_texture = board_texture.suit_texture
        similar = (
            self.db.query(HandRange)
            .filter(
                HandRange.player_role == player_role,
                HandRange.round == round,
                HandRange.board_cluster.like(f"%{structure}%"),
                HandRange.board_cluster.like(f"%{suit_texture}%"),
                HandRange.villain_type == query_filters["villain_type"]
            )
            .first()
        )
        if similar:
            print("⚠️ No cluster match. Using texture similarity fallback.")
            return {player_role: similar.hand_range}  # type: ignore

        # 🔴 Final fallback: Default strong hands
        print("❌ No hand range found. Returning tight default range.")
        return {player_role: ["AA", "KK", "QQ", "AKs", "AQs", "KQs"]}


    def get_hand_range_from_session(self, session: PokerSession) -> Dict[str, list]:
        player_role = session.player_role
        round = session.calculations.street
        board = session.calculations.normalized_board
        board_cluster = session.calculations.board_cluster_key
        board_texture = session.calculations.board_texture

        # 🟢 Choose the most active villain
        sorted_villains = sorted(
            session.villain_profiles.values(),
            key=lambda vp: vp.hands_observed,
            reverse=True
        )
        villain_profile = sorted_villains[0].dict() if sorted_villains else {}

        return self.get_range(
            player_role=player_role,
            round=round,
            board=board,
            board_cluster=board_cluster,
            board_texture=board_texture,
            villain_profile=villain_profile
        )