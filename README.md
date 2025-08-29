# 📄 Document Summary Assistant  

An AI-powered web application that takes **documents (PDFs & images)**, extracts text with **OCR / parsing**, and generates **smart summaries** along with **improvement suggestions**.  

## 🌐 Live Demo  
🔗 **URL**: [https://text-sumarization.netlify.app](https://text-sumarization.netlify.app)  
> Backend deployed on **Render** and frontend on **Netlify**.  

## 🔎 Approach  
The Document Summary Assistant was developed to solve the challenge of extracting key insights from unstructured documents like PDFs and scanned images. The project combines text extraction, natural language processing, and a user-friendly interface to deliver quick, useful summaries. The workflow begins with file upload, where users can provide PDFs or images through a drag-and-drop interface. The backend first checks the file type and applies the appropriate extraction method. For PDFs, the application uses pdfplumber to parse text accurately. For image-based documents, Optical Character Recognition (OCR) is performed using Tesseract (pytesseract in Python) to convert visual text into machine-readable format.
Once text is extracted, it is split into manageable chunks and sent to the Groq LLM API for analysis. The model generates summaries of different lengths—short, medium, or long—depending on user preference. Additionally, the AI provides improvement suggestions to enhance readability, conciseness, and engagement.
The frontend, built with HTML, CSS, and JavaScript, presents the results in a clean, responsive design. The backend is deployed on Render using Docker, while the frontend is hosted on Netlify. Together, the system demonstrates problem-solving, clean code practices, and real-world usability within the given assessment constraints.
## ⚡ Features  
- 📂 Upload PDFs & images (drag & drop / file picker)  
- 📑 Text extraction (OCR + PDF parsing)  
- ✍️ AI Summaries (short / medium / long)  
- 💡 Improvement Suggestions from AI  
- 🔒 CORS Handling for local + production  
- 🎨 Modern UI with responsive design  

## 🗂 Project Structure
```
document-summary-assistant/
├─ backend/
│ ├─ app.py # Flask backend with API endpoints
│ ├─ requirements.txt # Python dependencies
│ ├─ Dockerfile # Dockerfile for containerized deployment
│ └─ .env.example # Example environment variables
├─ frontend/
│ ├─ index.html # Frontend UI
│ ├─ script.js # Frontend logic (file upload, API calls)
│ └─ styles.css # Styling for the UI
```

## 🛠 Tech Stack  
- **Backend**: Python, Flask, pdfplumber, pytesseract, Pillow, dotenv, Groq API  
- **Frontend**: HTML, CSS, JavaScript  
- **OCR**: Tesseract  
- **Deployment**: Render (backend), Netlify (frontend)  
- **Containerization**: Docker  

## 🚀 Getting Started (Local)  

### Clone the repo  
```bash
git clone https://github.com/your-username/document-summary-assistant.git
cd document-summary-assistant
```
### Install Tesseract
## Ubuntu/Debian
```bash
sudo apt-get update && sudo apt-get install -y tesseract-ocr
```
### macOS (Homebrew)
```bash
brew install tesseract
```
## Windows 
- Download from Tesseract GitHub
- Add path (e.g. C:\Program Files\Tesseract-OCR\tesseract.exe) to PATH or set in .env.
## Backend Setup
``` bash
cd backend
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
```
Edit .env with your API keys, then run:
``` bash
python app.py
```
## ➡ Backend runs at: http://127.0.0.1:5000
## Frontend Setup
- Open frontend/index.html in your browser.
- In script.js, set API_BASE to your backend URL:
``` js
// const API_BASE = "http://127.0.0.1:5000";
// const API_BASE = "https://your-backend.onrender.com";
```
## 🧪 API
POST /api/summarize
Form-Data
- files: one or more PDFs or images
- summary_type: short | medium | long
## Response Example
``` json
{
  "ok": true,
  "files": [
    {
      "name": "FileName.pdf",
      "text_preview": "First 500 chars...",
      "summary_type": "medium",
      "summary": "• bullet points",
      "suggestions": "• improvements"
    }
  ]
}
```
## ✍️ Assignment Requirements

This project fulfills the Document Summary Assistant technical assessment:

- ✅ Document Upload (PDFs, images)

- ✅ Text Extraction (PDF parsing + OCR)

- ✅ Summarization (short / medium / long)

- ✅ Improvement Suggestions

- ✅ Clean UI/UX, responsive

- ✅ Hosted on Netlify + Render

- ✅ Code quality + documentation

## 📸Screenshots
<img width="1919" height="752" alt="image" src="https://github.com/user-attachments/assets/ec0f915f-e903-4bd5-b401-ce5f6dbde801" />
<img width="1919" height="777" alt="image" src="https://github.com/user-attachments/assets/08fda4a7-cefe-477f-b806-02cc06e993a9" />
<img width="1011" height="743" alt="image" src="https://github.com/user-attachments/assets/6a3880c5-93a1-4979-a3c8-a07170cd67d5" />


## 🙌 Acknowledgements

- Tesseract OCR

- Groq LLM

- pdfplumber

- Pillow

- Flask + CORS

- Docker + Render + Netlify
