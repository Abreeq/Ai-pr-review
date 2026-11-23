
from core.llm import ask_gemini


def review_bugs(code):

    prompt = f"""
    You are a senior Python developer specializing
    in identifying software bugs.

    Analyze the following Python code.

    Look for:
    1. Logical errors
    2. Runtime errors
    3. Incorrect conditions
    4. Missing edge cases
    5. Potential crashes

    Rules:
    - Only report genuine potential issues.
    - Do not invent problems.
    - Explain why something is a problem.
    - Suggest how to fix it.

    Return your findings in this format:

    BUG:
    LINE:
    SEVERITY:
    EXPLANATION:
    SUGGESTED FIX:

    If no bugs are found, say:
    "No significant bugs found."

    CODE TO REVIEW:

    {code}
    """

    result = ask_gemini(prompt)

    return result
