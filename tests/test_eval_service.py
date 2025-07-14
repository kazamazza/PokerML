import pytest

from container import Container
from eval7_service import Eval7Service


@pytest.fixture
def container():
    return Container()


def test_eval_service_lazy_initialization_and_caching(container):
    # Before access, no Eval7Service should exist
    assert getattr(container, "_eval_service", None) is None

    # First access should create an Eval7Service
    svc1 = container.eval_service
    assert isinstance(svc1, Eval7Service)
    # And cache it on the private attribute
    assert getattr(container, "_eval_service") is svc1

    # Subsequent accesses return the same instance
    svc2 = container.eval_service
    assert svc2 is svc1