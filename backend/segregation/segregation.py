import google.generativeai as genai
from dotenv import load_dotenv
import json
import os
import time
load_dotenv()
# 🔐 Secure API key (set in terminal: export GOOGLE_API_KEY="your_key")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# for m in genai.list_models():
#     print(m.name)
# ✅ Correct Gemini model
model = genai.GenerativeModel("models/gemini-flash-latest")


# -------- CLEAN JSON FUNCTION -------- #
def clean_json(text):
    """
    Cleans Gemini output (removes ```json ``` wrappers)
    """
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return text


# -------- STRUCTURE ENFORCEMENT -------- #
def enforce_structure(gis):
    if "Grand Topics" not in gis:
        return {"Grand Topics": []}

    fixed_gt = []

    for gt in gis["Grand Topics"]:
        topics = gt.get("topics", [])

        # Ensure GT has at least one Topic
        if not topics:
            topics = [{
                "name": "General Topic",
                "subtopics": ["Overview"]
            }]

        fixed_topics = []

        for topic in topics:
            subtopics = topic.get("subtopics", [])

            # Ensure Topic has at least one Subtopic
            if not subtopics:
                subtopics = ["Overview"]

            # Limit size (optional but good)
            subtopics = subtopics[:5]

            fixed_topics.append({
                "name": topic.get("name", "Unnamed Topic"),
                "subtopics": subtopics
            })

        fixed_gt.append({
            "name": gt.get("name", "Unnamed Grand Topic"),
            "topics": fixed_topics
        })

    return {"Grand Topics": fixed_gt}


# -------- MAIN FUNCTION -------- #
def generate_gis(subject, text):
    try:
        if not subject:
            subject = "General Studies"

        prompt = f"""
        You are an expert curriculum designer.

        Subject: {subject}

        Content:
        {text[:1500]}

        Create a structured Global Index Sheet with exactly 3 levels:

        1. Grand Topics
        2. Topics
        3. Subtopics

        Rules:
        - Maintain clear hierarchy
        - Avoid duplicates
        - Be comprehensive but concise
        - Every Grand Topic must have at least one Topic
        - Every Topic must have at least one Subtopic

        Return ONLY valid JSON in this format:

        {{
          "Grand Topics": [
            {{
              "name": "",
              "topics": [
                {{
                  "name": "",
                  "subtopics": []
                }}
              ]
            }}
          ]
        }}
        """

        # 🔁 Retry logic for rate limits
        for attempt in range(3):
            try:
                response = model.generate_content(prompt)

                raw_output = response.text
                print("🔍 RAW GEMINI OUTPUT:\n", raw_output)

                cleaned = clean_json(raw_output)

                parsed = json.loads(cleaned)

                # ✅ Enforce structure rules
                parsed = enforce_structure(parsed)

                return parsed

            except Exception as e:
                print(f"⚠️ Retry {attempt+1} failed:", str(e))
                time.sleep(5)

        return {"error": "Failed after retries"}

    except Exception as e:
        print("🔥 ERROR IN GEMINI:", str(e))
        return {"error": str(e)}