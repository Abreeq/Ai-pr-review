
from core.orchestrator import review_code


sample_code = """
API_KEY = "my-secret-key"

def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)


def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return db.execute(query)
"""


print("===================================")
print("       AI MULTI-AGENT PR REVIEW")
print("===================================")

final_report = review_code(sample_code)

print("\n========== FINAL PR REVIEW ==========\n")

if final_report:
    print(final_report)
else:
    print("Review could not be completed.")
