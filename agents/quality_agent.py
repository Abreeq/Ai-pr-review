
from core.llm import ask_gemini


def review_quality(code):

    prompt = f"""
    You are a senior Python software engineer
    specializing in code quality and maintainability.

    Review the following Python code.

    Look for:
    1. Poor variable and function naming
    2. Unnecessary code duplication
    3. Functions that do too many things
    4. Unnecessary complexity
    5. Poor code organization
    6. Missing useful documentation

    Rules:
    - Follow Python best practices.
    - Only suggest meaningful improvements.
    - Do not report personal style preferences as bugs.
    - Explain why each improvement matters.
    - Suggest better alternatives.

    Return findings in this format:

    ISSUE:
    LINE:
    IMPORTANCE:
    EXPLANATION:
    SUGGESTED IMPROVEMENT:

    If no significant improvements are needed, say:
    "Code quality looks good."

    CODE TO REVIEW:

    {code}
    """

    result = ask_gemini(prompt)

    return result
