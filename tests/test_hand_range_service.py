import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base
from db.models.hand_range import HandRange
from models.board_texture import BoardTexture
from models.poker_ml_input import VillainProfile
from models.poker_session import PlayerRole, PokerSession
from services.hand_range_service import HandRangeService
from types import SimpleNamespace


@pytest.fixture(scope="module")
def in_memory_session():
    # Spin up an in‐memory SQLite and create the hand_ranges table
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()
    engine.dispose()

@pytest.fixture
def service(in_memory_session):
    return HandRangeService(db_session=in_memory_session)

@pytest.fixture
def board_texture():
    # minimal BoardTexture stub
    return BoardTexture(
        structure="uncoordinated",
        suit_texture="rainbow",
        suits={},
        is_paired=False,
        is_two_tone=False,
        is_monotone=False,
        is_connected=False,
        has_flush_draw=False,
        has_backdoor_flush_draw=False,
        has_straight_draw=False,
        is_flush_possible=False,
        is_straight_possible=False,
        has_backdoor_straight_draw=False,
        high_card_rank=0,
        board_class="empty",
        rank_cluster="low",
        texture_blocker_influence_score=0.0,
        coordination_density_score=0.0,
        board_cluster_id=0
    )

def test_exact_match_returns_seeded_range(service, in_memory_session, board_texture):
    # clean slate
    in_memory_session.query(HandRange).delete()
    in_memory_session.commit()

    # seed one exact row
    row = HandRange(
        player_role=PlayerRole.BTN_vs_BB.value,
        round="flop",
        board="AsKsQs",
        board_cluster="As-Ks-Qs:uncoordinated:rainbow",
        villain_type="default",
        villain_aggression_factor=None,
        villain_vpip=None,
        villain_pfr=None,
        villain_tilt_level=None,
        villain_overall_winrate=None,
        villain_bluff_frequency=None,
        villain_check_raise_frequency=None,
        villain_cold_call_frequency=None,
        villain_hero_bully_history=None,
        villain_hero_vs_villain_winrate=None,
        hand_range=["AA", "KK"]
    )
    in_memory_session.add(row)
    in_memory_session.commit()

    result = service.get_range(
        player_role=PlayerRole.BTN_vs_BB,
        round="flop",
        board="AsKsQs",
        board_cluster="As-Ks-Qs:uncoordinated:rainbow",
        board_texture=board_texture,
        villain_profile={"villain_profile_type": "default"}
    )
    # should pick up our seeded hand_range
    assert result[PlayerRole.BTN_vs_BB.value] == ["AA", "KK"]

def test_default_fallback_when_no_rows(service, in_memory_session, board_texture):
    # remove all rows
    in_memory_session.query(HandRange).delete()
    in_memory_session.commit()

    result = service.get_range(
        player_role=PlayerRole.BTN_vs_BB,
        round="turn",
        board="2h3d4s",
        board_cluster="2-h-3-d-4-s:uncoordinated:rainbow",
        board_texture=board_texture,
        villain_profile={}  # empty → villain_type defaults to "default"
    )
    # default tight range
    assert result[PlayerRole.BTN_vs_BB.value] == ["AA", "KK", "QQ", "AKs", "AQs", "KQs"]
