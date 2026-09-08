import os
import time
from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD API KEY
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found.\n"
        "Create a .env file in the same folder as research.py\n"
        "and add:\n\n"
        "GEMINI_API_KEY=your_api_key"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.6-flash"


# ============================================================
# LLM FUNCTION WITH RETRY
# ============================================================

def ask_llm(prompt, retries=3):

    for attempt in range(1, retries + 1):

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            if response and response.text:
                return response.text.strip()

            return "No response generated."

        except Exception as e:

            error_message = str(e)

            print(
                f"\nAttempt {attempt}/{retries} failed."
            )

            print(error_message)

            # Retry temporary server errors
            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < retries:

                    print(
                        "Gemini is temporarily busy. "
                        "Retrying in 5 seconds..."
                    )

                    time.sleep(5)

                else:

                    return (
                        "ERROR: Gemini service is currently unavailable "
                        "after multiple attempts."
                    )

            else:

                return f"ERROR: {error_message}"

    return "ERROR: Unable to generate response."


# ============================================================
# STEP 1: PLANNING AGENT
# ============================================================

def create_research_plan(topic):

    print("\n" + "=" * 70)
    print("STEP 1: RESEARCH PLANNING")
    print("=" * 70)

    prompt = f"""
You are a Research Planning Agent.

Topic:
{topic}

Create a research plan containing 5 important sections.

For every section provide:

1. Section title
2. Research focus
3. Important questions

Do not write the final report.

Return only the research plan.
"""

    plan = ask_llm(prompt)

    print(plan)

    return plan


# ============================================================
# STEP 2: CONTENT GENERATION
# ============================================================

def generate_content(topic, plan):

    print("\n" + "=" * 70)
    print("STEP 2: CONTENT GENERATION")
    print("=" * 70)

    prompt = f"""
You are a Content Generation Agent.

Topic:
{topic}

Research Plan:
{plan}

Using the research plan, create a detailed first draft.

Requirements:

- Follow every section.
- Explain concepts clearly.
- Use an academic style.
- Include examples where useful.
- Avoid unnecessary repetition.
- Maintain logical organization.
- Provide useful and informative explanations.

Do not discuss the planning process.

Return only the research content.
"""

    content = ask_llm(prompt)

    print(content)

    return content


# ============================================================
# STEP 3: REFLECTION AGENT
# ============================================================

def reflect_on_content(topic, content):

    print("\n" + "=" * 70)
    print("STEP 3: REFLECTION")
    print("=" * 70)

    prompt = f"""
You are a Reflection Agent.

Topic:
{topic}

Generated Content:
{content}

Review the content critically.

Evaluate:

1. Accuracy
2. Completeness
3. Relevance
4. Structure
5. Clarity
6. Missing information
7. Repetition
8. Weak explanations

Return:

QUALITY SCORE: X/10

STRENGTHS:
- ...

WEAKNESSES:
- ...

MISSING INFORMATION:
- ...

IMPROVEMENTS:
- ...
"""

    reflection = ask_llm(prompt)

    print(reflection)

    return reflection


# ============================================================
# STEP 4: REVISION AGENT
# ============================================================

def revise_content(topic, content, reflection):

    print("\n" + "=" * 70)
    print("STEP 4: CONTENT REVISION")
    print("=" * 70)

    prompt = f"""
You are a Revision Agent.

Topic:
{topic}

Original Content:
{content}

Reflection Report:
{reflection}

Improve the content according to the reflection.

Requirements:

- Fix weaknesses.
- Add missing information.
- Improve clarity.
- Remove repetition.
- Improve organization.
- Maintain academic quality.
- Produce a complete final version.

Do not mention the reflection process.

Return only the improved content.
"""

    revised_content = ask_llm(prompt)

    print(revised_content)

    return revised_content


# ============================================================
# STEP 5: FINAL REVIEW
# ============================================================

def final_review(topic, content):

    print("\n" + "=" * 70)
    print("STEP 5: FINAL QUALITY REVIEW")
    print("=" * 70)

    prompt = f"""
You are a Final Quality Assurance Agent.

Topic:
{topic}

Final Content:
{content}

Evaluate the final content.

Check:

- Completeness
- Accuracy
- Clarity
- Relevance
- Organization
- Academic quality

Return:

FINAL QUALITY SCORE: X/10

FINAL ASSESSMENT:
Provide a short assessment.

If the content is acceptable, write:

READY FOR USE
"""

    review = ask_llm(prompt)

    print(review)

    return review


# ============================================================
# MAIN AGENT WORKFLOW
# ============================================================

def deep_research_agent(topic):

    print("\n")
    print("=" * 70)
    print("          DEEP RESEARCH AGENT WORKFLOW")
    print("=" * 70)

    print("\nTopic:", topic)

    # --------------------------------------------------------
    # PLANNING
    # --------------------------------------------------------

    plan = create_research_plan(topic)

    if plan.startswith("ERROR:"):

        print("\nPlanning failed.")
        return

    time.sleep(2)

    # --------------------------------------------------------
    # CONTENT GENERATION
    # --------------------------------------------------------

    content = generate_content(topic, plan)

    if content.startswith("ERROR:"):

        print("\nContent generation failed.")
        print(
            "\nThis is usually a temporary Gemini 503 error."
        )
        print(
            "Run the program again after a short wait."
        )

        return

    time.sleep(2)

    # --------------------------------------------------------
    # REFLECTION
    # --------------------------------------------------------

    reflection = reflect_on_content(topic, content)

    if reflection.startswith("ERROR:"):

        print("\nReflection failed.")
        return

    time.sleep(2)

    # --------------------------------------------------------
    # REVISION
    # --------------------------------------------------------

    revised_content = revise_content(
        topic,
        content,
        reflection
    )

    if revised_content.startswith("ERROR:"):

        print("\nRevision failed.")
        return

    time.sleep(2)

    # --------------------------------------------------------
    # FINAL REVIEW
    # --------------------------------------------------------

    final_review_result = final_review(
        topic,
        revised_content
    )

    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("                 FINAL REPORT")
    print("=" * 70)

    print("\nTOPIC")
    print("-" * 70)
    print(topic)

    print("\nFINAL CONTENT")
    print("-" * 70)
    print(revised_content)

    print("\nFINAL QUALITY REVIEW")
    print("-" * 70)
    print(final_review_result)

    print("\n")
    print("=" * 70)
    print("        DEEP RESEARCH WORKFLOW COMPLETED")
    print("=" * 70)


# ============================================================
# PROGRAM START
# ============================================================

def main():

    print("\nDeep Research Agent")
    print("-------------------")

    topic = input(
        "\nEnter the topic you want to research: "
    ).strip()

    if not topic:

        print("Please enter a valid topic.")
        return

    deep_research_agent(topic)


if __name__ == "__main__":
    main()