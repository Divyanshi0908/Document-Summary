import os
import io
import pdfplumber
import pytesseract
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")
client  = Groq(api_key=os.getenv("OPEN_API_KEY"))

# Flask app
app = Flask(__name__)

# for local developement. 
# CORS(app)

# for production 
CORS(app, resources={r"/api/*": {"origins": "https://text-sumarization.netlify.app"}})


ALLOWED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}
ALLOWED_PDF_EXTS = {".pdf"}


def file_ext(filename: str) -> str:
    return os.path.splitext(filename.lower())[1]


def extract_text_from_pdf(fileobj: io.BytesIO) -> str:
    text_parts = []
    with pdfplumber.open(fileobj) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts).strip()


def extract_text_from_image(fileobj: io.BytesIO) -> str:
    try:
        image = Image.open(fileobj).convert("RGB")
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"Error in image extraction: {str(e)}")
        raise


def chunk_text(text: str, max_chars: int = 8000) -> list:
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

def summarize_and_suggest_chunks(text: str, summary_type: str) -> dict:
    """
    Summarize + Suggest improvements for large text in chunks.
    Returns dict: {"summary": ..., "suggestions": ...}
    """
    chunks = chunk_text(text)
    partial_summaries = []
    partial_suggestions = []

    for idx, chunk in enumerate(chunks, 1):
        prompt = f"""
You are an assistant that provides two outputs for the text below:
1. A {summary_type} summary in clear bullet points (•).
2. 3–5 improvement suggestions in bullet points (•).

Return the result in this strict format:

Summary:
• point 1
• point 2

Improvement Suggestions:
• suggestion 1
• suggestion 2

---

Text chunk {idx}:
{chunk}
"""
        try:
            resp = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=800
            )
            output = resp.choices[0].message.content.strip()

            # Parse into sections
            summary, suggestions = "", ""
            if "Improvement Suggestions:" in output:
                parts = output.split("Improvement Suggestions:")
                summary = parts[0].replace("Summary:", "").strip()
                suggestions = parts[1].strip()
            else:
                summary = output.strip()

        except Exception as e:
            summary = f"[Error summarizing chunk {idx}: {str(e)}]"
            suggestions = ""

        partial_summaries.append(summary)
        if suggestions:
            partial_suggestions.append(suggestions)

    # Combine into final summary + suggestions
    combined_prompt = f"""
Combine the following into clean, final outputs.

Final {summary_type} Summary (bullet points only):
{chr(10).join(partial_summaries)}

Final Improvement Suggestions (merge, remove duplicates, keep 3–7 bullet points):
{chr(10).join(partial_suggestions)}

Return in this format:

Summary:
• point 1
• point 2

Improvement Suggestions:
• suggestion 1
• suggestion 2
"""
    try:
        final_resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": combined_prompt}],
            temperature=0.5,
            max_tokens=1000
        )
        final_output = final_resp.choices[0].message.content.strip()

        summary, suggestions = "", ""
        if "Improvement Suggestions:" in final_output:
            parts = final_output.split("Improvement Suggestions:")
            summary = parts[0].replace("Summary:", "").strip()
            suggestions = parts[1].strip()
        else:
            summary = final_output.strip()

        return {
            "summary": summary,
            "suggestions": suggestions
        }

    except Exception:
        return {
            "summary": "\n".join(partial_summaries),
            "suggestions": "\n".join(partial_suggestions)
        }



def analyze_text(text: str, summary_type: str) -> dict:
    if not text.strip():
        return {"summary": "", "suggestions": ""}
    return summarize_and_suggest_chunks(text, summary_type)


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "status": "healthy"})


@app.post("/api/analyze")
def analyze():
    if "files" not in request.files:
        return jsonify({"ok": False, "error": "No files provided"}), 400

    files = request.files.getlist("files")
    if not files:
        return jsonify({"ok": False, "error": "Empty file list"}), 400

    summary_type = request.form.get("summary_type", "short").lower()
    if summary_type not in ["short", "medium", "long"]:
        summary_type = "short"

    results = []

    for f in files:
        name = getattr(f, "filename", "upload")
        ext = file_ext(name)
        try:
            raw = f.read()
            buf = io.BytesIO(raw)
            text = ""

            if ext in ALLOWED_PDF_EXTS:
                buf.seek(0)
                text = extract_text_from_pdf(buf)
            elif ext in ALLOWED_IMAGE_EXTS:
                buf.seek(0)
                text = extract_text_from_image(buf)
            else:
                try:
                    buf.seek(0)
                    text = extract_text_from_pdf(buf)
                    if not text.strip():
                        raise Exception("Empty PDF text; fallback to OCR")
                except Exception:
                    buf = io.BytesIO(raw)
                    text = extract_text_from_image(buf)

            result = analyze_text(text, summary_type)

            preview = text[:500].replace("\n", " ")
            if len(text) > 500:
                preview += " ..."

            results.append({
                "name": name,
                "text_preview": preview,
                "summary_type": summary_type,
                "summary": result["summary"],
                "suggestions": result["suggestions"],
            })
        except Exception as e:
            results.append({
                "name": name,
                "error": f"Failed to process: {e}"
            })

    return jsonify({
        "ok": True,
        "files": results
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
