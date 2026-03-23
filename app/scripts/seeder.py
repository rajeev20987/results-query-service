from app.db.connection import SessionLocal, engine
from app.db.models import Base, TestResult

# Create tables if not exists
Base.metadata.create_all(bind=engine)

# Sample dummy records
dummy_results = [
    {"name": "Login test - valid credentials", "status": "passed", "suite": "login-tests"},
    {"name": "Login test - invalid password", "status": "failed", "suite": "login-tests"},
    {"name": "Checkout test - add to cart", "status": "passed", "suite": "checkout-tests"},
    {"name": "Checkout test - payment declined", "status": "failed", "suite": "checkout-tests"},
    {"name": "Profile update test", "status": "passed", "suite": "profile-tests"},
]

# Open DB session
db = SessionLocal()

try:
    for r in dummy_results:
        db.add(TestResult(**r))
    db.commit()
    print("Dummy data inserted successfully!")
finally:
    db.close()