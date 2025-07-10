from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models.hand_range import HandRange
from services.hand_range_estimator import HandRangeEstimator


def check_and_generate():
    db: Session = SessionLocal()
    count = db.query(HandRange).count()

    if count == 0:
        print("🟡 No hand ranges found. Generating...")
        estimator = HandRangeEstimator()
        all_ranges = estimator.generate_preflop() + estimator.generate_postflop()
        for item in all_ranges:
            db.add(HandRange(**item))
        db.commit()
        print(f"✅ Inserted {len(all_ranges)} hand ranges.")
    else:
        print(f"✅ Hand range table already has {count} entries.")

if __name__ == "__main__":
    check_and_generate()