import random
from app.db.connection import SessionLocal, engine
from app.db.models import Base, TestResult

# Create tables if not exists
Base.metadata.create_all(bind=engine)


# ✅ Generate 1000 dummy results
def generate_dummy_results(n=1000):
    actions = ["Login", "Checkout", "Payment", "Profile", "Search", "Signup"]
    scenarios = [
        "valid credentials",
        "invalid password",
        "add to cart",
        "payment declined",
        "update info",
        "empty input",
        "timeout",
        "edge case",
        "large data",
        "special characters"
    ]
    suites = ["login-tests", "checkout-tests", "profile-tests", "search-tests"]

    results = []

    for i in range(1, n + 1):
        status = "passed" if i <= int(n * 0.93) else "failed"

        results.append({
            "name": f"{random.choice(actions)} test - {random.choice(scenarios)}",
            "status": status,
            "suite": random.choice(suites),
            "confidence": round(random.uniform(0.7, 0.99), 2),
            "avg_execution_time": round(random.uniform(0.5, 3.0), 2),
        })

    random.shuffle(results)  # mix passed/failed
    return results


dummy_results = generate_dummy_results()


# Open DB session
db = SessionLocal()

try:
    db.bulk_insert_mappings(TestResult, dummy_results)  # ✅ faster than loop
    db.commit()
    print(f"{len(dummy_results)} dummy records inserted successfully!")
finally:
    db.close()