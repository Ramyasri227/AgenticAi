"""
Reasoning Model Benchmarking
----------------------------

Compare outputs across different prompting strategies.

Strategies:
1. Zero-Shot
2. Few-Shot
3. Step-by-Step
4. Structured Prompt

The same question is given to the model using each strategy.

The program compares:
- Answer
- Response length
- Basic correctness
- Overall performance

"""

import os
import time
from dotenv import load_dotenv
from google import genai


# ============================================================
# 1. LOAD API KEY
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found.\n\n"
        "Create a .env file and add:\n"
        "GEMINI_API_KEY=your_api_key"
    )


# ============================================================
# 2. GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.6-flash"


# ============================================================
# 3. ASK MODEL
# ============================================================

def ask_model(prompt):

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            if response and response.text:
                return response.text.strip()

            return "No response generated."

        except Exception as e:

            error = str(e)

            print(
                f"\nAttempt {attempt + 1}/3 failed: {error}"
            )

            if (
                "503" in error
                or "UNAVAILABLE" in error
            ):

                if attempt < 2:

                    print(
                        "Model temporarily unavailable. "
                        "Retrying..."
                    )

                    time.sleep(5)

                else:

                    return "ERROR: Model unavailable."

            else:

                return f"ERROR: {error}"

    return "ERROR: Request failed."


# ============================================================
# 4. ZERO-SHOT PROMPT
# ============================================================

def zero_shot(question):

    prompt = f"""
Answer the following question.

Question:
{question}
"""

    return ask_model(prompt)


# ============================================================
# 5. FEW-SHOT PROMPT
# ============================================================

def few_shot(question):

    prompt = f"""
You are a reasoning assistant.

Here are examples of how to solve problems.

Example 1:

Question:
If a car travels 60 km in 2 hours, what is its average speed?

Answer:
Average speed = Distance / Time
= 60 / 2
= 30 km/h

Example 2:

Question:
A product costs 100 and has a 20% discount.
What is the final price?

Answer:
Discount = 20% of 100 = 20
Final price = 100 - 20 = 80

Now solve this problem using the same approach.

Question:
{question}

Provide the answer and explain the calculation.
"""

    return ask_model(prompt)


# ============================================================
# 6. STEP-BY-STEP PROMPT
# ============================================================

def step_by_step(question):

    prompt = f"""
Solve the following problem systematically.

Question:
{question}

Use this process:

1. Identify the information given.
2. Identify what needs to be calculated.
3. Select the appropriate method or formula.
4. Perform the calculation.
5. Verify the result.
6. Provide the final answer.

Give a clear solution.
"""

    return ask_model(prompt)


# ============================================================
# 7. STRUCTURED PROMPT
# ============================================================

def structured_prompt(question):

    prompt = f"""
Solve the following problem.

Question:
{question}

Return the answer using exactly this structure:

GIVEN:
List the important information.

METHOD:
Explain the method or formula.

CALCULATION:
Show the calculation.

VERIFICATION:
Check whether the result is reasonable.

FINAL ANSWER:
Give the final answer clearly.

Do not include unnecessary information.
"""

    return ask_model(prompt)


# ============================================================
# 8. EVALUATE RESPONSE
# ============================================================

def evaluate_response(response, expected_answer):

    if response.startswith("ERROR"):
        return 0

    response_lower = response.lower()
    expected_lower = expected_answer.lower()

    # Simple correctness check
    if expected_lower in response_lower:
        correctness = 10
    else:
        correctness = 5

    # Response length score
    length = len(response)

    if 50 <= length <= 1500:
        clarity = 10
    elif length < 50:
        clarity = 5
    else:
        clarity = 7

    # Final score
    score = (correctness + clarity) / 2

    return score


# ============================================================
# 9. DISPLAY RESULT
# ============================================================

def display_result(name, response, score):

    print("\n")
    print("=" * 70)
    print(name)
    print("=" * 70)

    print("\nResponse:")
    print(response)

    print("\nResponse Length:", len(response), "characters")

    print("Benchmark Score:", f"{score:.2f}/10")


# ============================================================
# 10. MAIN BENCHMARK
# ============================================================

def run_benchmark(question, expected_answer):

    print("\n")
    print("=" * 70)
    print("           REASONING MODEL BENCHMARK")
    print("=" * 70)

    print("\nQuestion:")
    print(question)

    print("\nExpected Answer:")
    print(expected_answer)

    # --------------------------------------------------------
    # ZERO SHOT
    # --------------------------------------------------------

    print("\nRunning Zero-Shot strategy...")

    zero_result = zero_shot(question)

    zero_score = evaluate_response(
        zero_result,
        expected_answer
    )

    display_result(
        "1. ZERO-SHOT PROMPT",
        zero_result,
        zero_score
    )

    time.sleep(2)

    # --------------------------------------------------------
    # FEW SHOT
    # --------------------------------------------------------

    print("\nRunning Few-Shot strategy...")

    few_result = few_shot(question)

    few_score = evaluate_response(
        few_result,
        expected_answer
    )

    display_result(
        "2. FEW-SHOT PROMPT",
        few_result,
        few_score
    )

    time.sleep(2)

    # --------------------------------------------------------
    # STEP BY STEP
    # --------------------------------------------------------

    print("\nRunning Step-by-Step strategy...")

    step_result = step_by_step(question)

    step_score = evaluate_response(
        step_result,
        expected_answer
    )

    display_result(
        "3. STEP-BY-STEP PROMPT",
        step_result,
        step_score
    )

    time.sleep(2)

    # --------------------------------------------------------
    # STRUCTURED
    # --------------------------------------------------------

    print("\nRunning Structured Prompt strategy...")

    structured_result = structured_prompt(question)

    structured_score = evaluate_response(
        structured_result,
        expected_answer
    )

    display_result(
        "4. STRUCTURED PROMPT",
        structured_result,
        structured_score
    )

    # ========================================================
    # FINAL COMPARISON
    # ========================================================

    print("\n")
    print("=" * 70)
    print("                 BENCHMARK SUMMARY")
    print("=" * 70)

    results = [
        ("Zero-Shot", zero_score),
        ("Few-Shot", few_score),
        ("Step-by-Step", step_score),
        ("Structured", structured_score)
    ]

    print(
        f"\n{'Strategy':<25} {'Score':<10}"
    )

    print("-" * 40)

    for name, score in results:

        print(
            f"{name:<25} {score:.2f}/10"
        )

    # Find best strategy
    best_strategy = max(
        results,
        key=lambda x: x[1]
    )

    print("\nBest Performing Strategy:")
    print(
        f"{best_strategy[0]} "
        f"({best_strategy[1]:.2f}/10)"
    )

    print("\n")
    print("=" * 70)
    print("              BENCHMARK COMPLETED")
    print("=" * 70)


# ============================================================
# 11. MAIN PROGRAM
# ============================================================

def main():

    print("\nReasoning Model Benchmarking")
    print("----------------------------")

    print(
        "\nEnter a reasoning problem."
    )

    question = input(
        "\nQuestion: "
    ).strip()

    if not question:

        print("Question cannot be empty.")
        return

    print(
        "\nEnter the expected answer."
    )

    expected_answer = input(
        "Expected Answer: "
    ).strip()

    if not expected_answer:

        print("Expected answer cannot be empty.")
        return

    run_benchmark(
        question,
        expected_answer
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()