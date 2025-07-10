from sqlalchemy import (
    Column, Integer, String, Float, JSON, UniqueConstraint
)
from db.base import Base


class HandRange(Base):
    __tablename__ = 'hand_ranges'

    id = Column(Integer, primary_key=True)
    player_role = Column(String(50), nullable=False)
    round = Column(String(10), nullable=False)
    board_cluster = Column(String(100), nullable=False)
    board = Column(String(20), nullable=False)

    # Villain profile metrics
    villain_type = Column(String(50), nullable=False, default='default')
    villain_aggression_factor = Column(Float)
    villain_vpip = Column(Float)
    villain_pfr = Column(Float)
    villain_tilt_level = Column(String(20))
    villain_overall_winrate = Column(Float)
    villain_bluff_frequency = Column(Float)
    villain_check_raise_frequency = Column(Float)
    villain_cold_call_frequency = Column(Float)
    villain_hero_bully_history = Column(Float)
    villain_hero_vs_villain_winrate = Column(Float)

    # The actual hand range
    hand_range = Column(JSON, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'player_role',
            'round',
            'board_cluster',
            'villain_type',
            'villain_aggression_factor',
            'villain_vpip',
            'villain_pfr',
            'villain_tilt_level',
            'villain_overall_winrate',
            'villain_bluff_frequency',
            'villain_check_raise_frequency',
            'villain_cold_call_frequency',
            'villain_hero_bully_history',
            'villain_hero_vs_villain_winrate',
            name='uq_hand_range_full_profile'
        ),
    )