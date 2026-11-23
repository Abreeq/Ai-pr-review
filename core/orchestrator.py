
from concurrent.futures import ThreadPoolExecutor

from agents.bug_agent import review_bugs
from agents.security_agent import review_security
from agents.quality_agent import review_quality
from agents.reviewer_agent import aggregate_reviews


def review_code(code):

    print("\nStarting Multi-Agent Code Review...\n")

    with ThreadPoolExecutor(max_workers=3) as executor:

        bug_future = executor.submit(review_bugs, code)
        security_future = executor.submit(review_security, code)
        quality_future = executor.submit(review_quality, code)

        print("Three agents are reviewing the code...\n")

        bug_report = bug_future.result()
        security_report = security_future.result()
        quality_report = quality_future.result()

    print("All specialist agents completed!")

    print("\nStarting Lead Reviewer Agent...\n")

    final_report = aggregate_reviews(
        bug_report,
        security_report,
        quality_report
    )

    return final_report
