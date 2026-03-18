import google.generativeai as genai
from dotenv import load_dotenv
import json
import os
import time

# Load env variables
load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Model
model = genai.GenerativeModel("models/gemini-flash-latest")


# -------- CLEAN JSON -------- #
def clean_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return text


# -------- NORMALIZE KEYS (VERY IMPORTANT) -------- #
def normalize_keys(gis):
    normalized = {"Grand Topics": []}

    for gt in gis.get("Grand Topics", []):
        gt_name = gt.get("name") or gt.get("title") or "Unnamed Grand Topic"

        topics = gt.get("topics") or gt.get("Topics") or []

        norm_topics = []

        for topic in topics:
            t_name = topic.get("name") or topic.get("title") or "Unnamed Topic"

            subtopics = topic.get("subtopics") or topic.get("Subtopics") or []

            norm_topics.append({
                "name": t_name,
                "subtopics": subtopics
            })

        normalized["Grand Topics"].append({
            "name": gt_name,
            "topics": norm_topics
        })

    return normalized


# -------- STRUCTURE ENFORCEMENT -------- #
def enforce_structure(gis):
    if "Grand Topics" not in gis:
        return {"Grand Topics": []}

    fixed_gt = []

    for gt in gis["Grand Topics"]:
        topics = gt.get("topics", [])

        if not topics:
            topics = [{
                "name": "General Topic",
                "subtopics": ["Overview"]
            }]

        fixed_topics = []

        for topic in topics:
            subtopics = topic.get("subtopics", [])

            if not subtopics:
                subtopics = ["Overview"]

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


# -------- CODING SYSTEM -------- #
def add_topic_codes(gis):
    gt_counter = 1

    for gt in gis.get("Grand Topics", []):
        gt_code = f"GT{gt_counter}"
        gt["code"] = gt_code

        t_counter = 1

        for topic in gt.get("topics", []):
            t_code = f"{gt_code}.T{t_counter}"
            topic["code"] = t_code

            s_counter = 1
            new_subtopics = []

            for sub in topic.get("subtopics", []):
                s_code = f"{t_code}.S{s_counter}"

                new_subtopics.append({
                    "name": sub,
                    "code": s_code
                })

                s_counter += 1

            topic["subtopics"] = new_subtopics
            t_counter += 1

        gt_counter += 1

    return gis


# -------- TAGGING -------- #
def add_tags_and_difficulty(gis, subject):
    try:
        prompt = f"""
        You are an expert educator.

        Given this structured syllabus:

        {json.dumps(gis, indent=2)}

        Add:
        - difficulty (Beginner / Intermediate / Advanced)
        - blooms_level (Remember, Understand, Apply, Analyze, Evaluate, Create)

        Rules:
        - Do NOT change structure
        - Add tags to topics and subtopics

        Return ONLY valid JSON.
        """

        response = model.generate_content(prompt)

        cleaned = clean_json(response.text)

        return json.loads(cleaned)

    except Exception as e:
        print("⚠️ Tagging failed:", e)
        return gis


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

        Create a structured Global Index Sheet with:

        1. Grand Topics
        2. Topics
        3. Subtopics

        Rules:
        - Maintain hierarchy
        - Avoid duplicates
        - Every GT must have topics
        - Every topic must have subtopics

        Return ONLY valid JSON.
        """

        for attempt in range(3):
            try:
                response = model.generate_content(prompt)

                raw = response.text
                print("🔍 RAW OUTPUT:\n", raw)

                cleaned = clean_json(raw)

                parsed = json.loads(cleaned)

                # 🔥 CRITICAL PIPELINE
                parsed = normalize_keys(parsed)
                parsed = enforce_structure(parsed)
                parsed = add_topic_codes(parsed)

                if "error" not in parsed:
                    parsed = add_tags_and_difficulty(parsed, subject)

                return parsed

            except Exception as e:
                print(f"⚠️ Retry {attempt+1}:", e)
                time.sleep(5)

        return {"error": "Failed after retries"}

    except Exception as e:
        print("🔥 ERROR:", e)
        return {"error": str(e)}