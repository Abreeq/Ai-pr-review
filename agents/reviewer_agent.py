
from core.llm import ask_gemini


def aggregate_reviews(bug_report, security_report, quality_report):

    prompt = f"""
    You are a senior software engineer and lead PR reviewer.

    You have received code review reports from three
    specialized AI agents.

    Your task is to create one consolidated PR review.

    IMPORTANT RESPONSIBILITIES:

    1. Combine all findings.
    2. Remove duplicate findings.
    3. Preserve important technical details.
    4. Prioritize issues by severity.
    5. Do not invent new issues.
    6. Do not blindly trust agent findings.
    7. If findings are uncertain, mark them for manual verification.

    SEVERITY LEVELS:

    Critical: Serious security or correctness issue.
    High: Significant bug or vulnerability.
    Medium: Maintainability or moderate correctness issue.
    Low: Minor improvement.

    OUTPUT FORMAT:

    # Pull Request Review

    ## Overall Summary
    Summarize the code quality and major concerns.

    ## Critical Issues
    List critical findings.

    ## High Priority Issues
    List high priority findings.

    ## Medium Priority Issues
    List medium priority findings.

    ## Low Priority Suggestions
    List minor improvements.

    ## Final Recommendation

    Choose one:
    - APPROVE
    - REQUEST CHANGES
    - NEEDS MANUAL REVIEW

    Explain your recommendation.

    ----------------------------

    BUG AGENT REPORT:

    {bug_report}

    ----------------------------

    SECURITY AGENT REPORT:

    {security_report}

    ----------------------------

    QUALITY AGENT REPORT:

    {quality_report}
    """

    result = ask_gemini(prompt)

    return result
