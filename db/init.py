from db.session import engine
from db.models.hand_range import Base

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Database schema initialized.")