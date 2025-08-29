# Document Summary Assistant

A minimal PDF/Image → Text → Summary web app for technical assessment.

## Features
- Upload **PDF** or **image** (`.png/.jpg/.jpeg`)
- Extract text:
  - PDFs via `pdfplumber`
  - Images via **OCR** (`pytesseract`)
- Summarize with Hugging Face Transformers (DistilBART, fallback to T5)
- Choose summary length: **short**, **medium**, **long**
- Clean, mobile-friendly UI
- Simple Flask backend API

> NOTE: You must have the **Tesseract OCR** system binary installed for image OCR to work.  
> On Ubuntu: `sudo apt-get install tesseract-ocr`  
> On macOS (Homebrew): `brew install tesseract`

## Tech Stack
- Backend: **Flask**, `pdfplumber`, `pytesseract`, `transformers`, `torch`
- Frontend: HTML/CSS/JS (no framework)
- Deploy: Render/Heroku (backend), Netlify/Vercel (frontend)

## Local Development

### 1) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
The API will run at `http://localhost:8000`.

### 2) Frontend (static)
Open `frontend/index.html` in a Live Server (VS Code) or any static host.  
If your backend runs elsewhere, set custom base URL in the browser console:
```js
localStorage.setItem("apiBase","https://your-backend.onrender.com")
```

## API
`POST /api/summarize` multipart form:
- `file` — the document (PDF or image)
- `length` — `short|medium|long` (default: `medium`)

Response:
```json
{
  "summary": "...",
  "key_points": ["..."],
  "length": "medium",
  "chars_in": 12345
}
```

## Deploy Tips
- **Backend**: Use Render/Heroku. Add a `Procfile` (`web: python app.py`). Ensure `tesseract-ocr` is available (Render supports apt packages via render-build scripts; on Heroku, use a buildpack).
- **Frontend**: Drag-drop `frontend/` to Netlify, or deploy via Vercel (as static). Point it at the backend URL.

## 200-word Approach (example)
This app extracts text from PDFs with `pdfplumber` and from images via Tesseract OCR. Extracted text is normalized and chunked to keep model input sizes small. We use the Hugging Face Transformers summarization pipeline with DistilBART for quality and speed, with an automatic fallback to T5 on environments where DistilBART cannot load. The server exposes a single `/api/summarize` endpoint that accepts a file and an optional target summary length (short/medium/long). For large documents, the service summarizes page-wise chunks and then summarizes the combined result again to preserve coherence. The frontend is a clean, mobile-friendly HTML/CSS/JS interface with drag-and-drop upload, a length selector, and clear loading states. Errors are handled gracefully (unsupported file types, no text detected, upstream model failures). The solution is intentionally minimal, dependency-light, and easy to deploy: the backend can be hosted on Render or Heroku, and the frontend on Netlify or Vercel. The codebase follows a simple structure, enabling quick review and extension (e.g., adding highlight styles, history, or authentication).

## License
MIT
