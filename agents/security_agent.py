
from core.llm import ask_gemini


def review_security(code):

    prompt = f"""
    You are a senior application security engineer.

    Review the following Python code for security issues.

    Look for:
    1. SQL injection vulnerabilities
    2. Hardcoded passwords or API keys
    3. Unsafe user input handling
    4. Authentication weaknesses
    5. Authorization problems
    6. Insecure data processing

    Rules:
    - Only report issues supported by the code.
    - Do not invent vulnerabilities.
    - Explain the potential security impact.
    - Suggest a secure solution.

    Return findings in this format:

    VULNERABILITY:
    LINE:
    SEVERITY:
    EXPLANATION:
    SUGGESTED FIX:

    If no issues are found, say:
    "No significant security issues found."

    CODE TO REVIEW:

    {code}
    """

    result = ask_gemini(prompt)

    return result
