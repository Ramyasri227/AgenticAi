"""
Image Retrieval / Visual QA System
----------------------------------

A simple multimodal pipeline using Gemini.

Pipeline:

Image
  ↓
Image Loading
  ↓
Gemini Vision Model
  ↓
Image Understanding
  ↓
User Question
  ↓
Visual Question Answer
"""

import os
from dotenv import load_dotenv
from google import genai
from PIL import Image


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found.\n"
        "Create a .env file and add:\n\n"
        "GEMINI_API_KEY=your_api_key"
    )


# ============================================================
# 2. CREATE GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.6-flash"


# ============================================================
# 3. LOAD IMAGE
# ============================================================

def load_image(image_path):

    try:

        image = Image.open(image_path)

        print("\nImage loaded successfully.")
        print("Image size:", image.size)
        print("Image format:", image.format)

        return image

    except FileNotFoundError:

        print("\nERROR: Image file not found.")
        return None

    except Exception as e:

        print("\nERROR loading image:", e)
        return None


# ============================================================
# 4. IMAGE DESCRIPTION
# ============================================================

def describe_image(image):

    prompt = """
Analyze this image carefully.

Provide:

1. A short description of the image.
2. Important objects visible.
3. People or animals if present.
4. Environment or background.
5. Important activities.
6. Any visible text.
7. Overall context.

Do not guess information that cannot be clearly observed.
"""

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=[image, prompt]
        )

        return response.text.strip()

    except Exception as e:

        return f"ERROR: {e}"


# ============================================================
# 5. VISUAL QUESTION ANSWERING
# ============================================================

def answer_question(image, question):

    prompt = f"""
You are a Visual Question Answering Agent.

Analyze the provided image and answer the user's question.

USER QUESTION:
{question}

Rules:

- Answer using information visible in the image.
- Be concise and clear.
- Do not invent information.
- If the answer cannot be determined from the image,
  say that it cannot be determined from the image.
"""

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=[image, prompt]
        )

        return response.text.strip()

    except Exception as e:

        return f"ERROR: {e}"


# ============================================================
# 6. MULTIPLE QUESTIONS
# ============================================================

def visual_qa_session(image):

    print("\n")
    print("=" * 70)
    print("              VISUAL QUESTION ANSWERING")
    print("=" * 70)

    print("\nYou can ask questions about the image.")
    print("Type 'exit' to finish.\n")

    while True:

        question = input("Ask a question: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            print("Please enter a question.")
            continue

        answer = answer_question(
            image,
            question
        )

        print("\nAnswer:")
        print(answer)
        print("-" * 70)


# ============================================================
# 7. MAIN MULTIMODAL PIPELINE
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("          IMAGE RETRIEVAL / VISUAL QA SYSTEM")
    print("=" * 70)

    # --------------------------------------------------------
    # IMAGE INPUT
    # --------------------------------------------------------

    image_path = input(
        "\nEnter the image path: "
    ).strip()

    if not image_path:

        print("Image path cannot be empty.")
        return

    # --------------------------------------------------------
    # LOAD IMAGE
    # --------------------------------------------------------

    image = load_image(image_path)

    if image is None:
        return

    # --------------------------------------------------------
    # IMAGE UNDERSTANDING
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("STEP 1: IMAGE UNDERSTANDING")
    print("=" * 70)

    description = describe_image(image)

    print("\nImage Analysis:")
    print(description)

    # --------------------------------------------------------
    # VISUAL QA
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("STEP 2: VISUAL QUESTION ANSWERING")
    print("=" * 70)

    visual_qa_session(image)

    # --------------------------------------------------------
    # END
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("              PIPELINE COMPLETED")
    print("=" * 70)


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()