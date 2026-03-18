** AI Powered Global Index Sheet (GIS) Generator

-> Overview

This project converts unstructured educational content (PDF, DOCX, TXT) into a structured **Global Index Sheet (GIS)** using AI.

The system organizes content into:

* **Grand Topics**
* **Topics**
* **Subtopics**

and enhances them with:

* Topic Codes
* Difficulty Levels
* Bloom’s Taxonomy
* Source Traceability

---

-> Features

* 📂 File Upload (Drag & Drop)
* 📄 Multi-format Support (PDF, DOCX, TXT)
* 🤖 AI-powered Topic Extraction (Gemini)
* 🧠 Intelligent Deduplication & Hierarchy
* 🏷 Topic Coding System (GT → T → S)
* 📊 Difficulty Classification
* 🎓 Bloom’s Taxonomy Tagging
* 🔍 Source Traceability (Snippet + Confidence)
* ⚡ Relevance Detection (AI-based)
* 🌐 Full-stack Deployment (Frontend + Backend)

---

-> Tech Stack

-> Frontend

* React.js
* Vite
* CSS

-> Backend

* Flask (Python)
* Flask-CORS

-> AI / NLP

* Google Gemini API

-> Document Processing

* PyPDF2 (PDF)
* python-docx (DOCX)
* Pillow (Image handling)

-> Deployment

* Backend: Render
* Frontend: Vercel

---

-> System Architecture

```text
User Upload
   ↓
Text Extraction
   ↓
Relevance Check (AI)
   ↓
LLM Processing (Gemini)
   ↓
Post-processing (Validation + Deduplication)
   ↓
Topic Coding + Tagging
   ↓
Source Traceability
   ↓
Frontend Display
```

---

-> Live Demo

* 🌐 Frontend: https://your-vercel-link
* 🔗 Backend API: https://globalindexsheet.onrender.com

---

-> Project Structure

```
GlobalIndexSheet/
 ├── backend/
 │   ├── main.py
 │   ├── routes/
 │   ├── validation/
 │   ├── segregation/
 │   ├── requirements.txt
 │
 ├── frontend/
 │   ├── src/
 │   ├── components/
 │   ├── css/
 │
 └── README.md
```

---

-> How to Run Locally

-> Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

---

-> Frontend

```bash
cd frontend
npm install
npm run dev
```

---

-> Environment Variables

Create a `.env` file in backend:

```env
GOOGLE_API_KEY=your_api_key_here
```

---

-> AI Capabilities

The system uses LLMs to:

* Extract key concepts
* Build hierarchical structure
* Remove duplicate topics
* Add educational tags
* Map topics to source content

---

-> Challenges & Solutions

| Challenge               | Solution                                        |
| ----------------------- | ----------------------------------------------- |
| Inconsistent LLM output | Added normalization layer                       |
| Invalid JSON responses  | Implemented cleaning logic                      |
| High memory usage       | Replaced local models with Gemini               |
| Deployment issues       | Used environment variables + lightweight design |

---

-> Future Improvements
Tree-based visualization
Search & filtering
Export GIS (PDF/CSV)
Multi-document analysis

---

-> Author

**Sai Rohan Tanuku**

---

## ⭐ Key Insight

> This system combines generative AI with rule-based validation to ensure both flexibility and reliability.
