from db.session import engine
from db.base import Base
from models.hand_range import HandRange

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Database schema initialized.")