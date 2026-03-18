from flask import Blueprint, request, jsonify
from validation.extract import extract_text, is_relevant

allroute = Blueprint("allroute", __name__)

@allroute.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    subject = request.form.get("subject", "")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    content = file.read()

    text = extract_text(file.filename, content)

    if not text.strip():
        return jsonify({"error": "No text extracted"}), 400

    relevant, score = is_relevant(subject, text)

    if not relevant:
        return jsonify({
            "status": "irrelevant",
            "score": float(score)
        })
    
    return jsonify({
        "status": "relevant",
        "score": float(score),
        "text_preview": text[:500]
    })