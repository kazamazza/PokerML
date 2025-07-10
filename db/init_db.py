from db.session import engine
from models.hand_range import Base


def init_db():
    Base.metadata.create_all(bind=engine)