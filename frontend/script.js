const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const summarizeBtn = document.getElementById("summarizeBtn");
const lengthSelect = document.getElementById("length");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const fileSummaries = document.getElementById("fileSummaries");
const improvementSuggestions = document.getElementById(
  "improvementSuggestions"
);

const API_BASE =
  window.localStorage.getItem("apiBase") ||
  "https://text-summarization-hdb9.onrender.com";
// const API_BASE =
//   window.localStorage.getItem("apiBase") || "http://127.0.0.1:5000";

let selectedFiles = [];

// Drag & Drop events
dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("dragover");
});
dropzone.addEventListener("dragleave", () =>
  dropzone.classList.remove("dragover")
);
dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("dragover");
  selectedFiles = Array.from(e.dataTransfer.files);
  if (selectedFiles.length > 0) {
    dropzone.querySelector("p").textContent = `Selected: ${selectedFiles
      .map((f) => f.name)
      .join(", ")}`;
  }
});

dropzone.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", () => {
  selectedFiles = Array.from(fileInput.files);
  if (selectedFiles.length > 0) {
    dropzone.querySelector("p").textContent = `Selected: ${selectedFiles
      .map((f) => f.name)
      .join(", ")}`;
  }
});

function formatBullets(text) {
  if (!text) return "<p>Not available.</p>";

  const lines = text
    .split(/\r?\n|•|-|\d+\./)
    .map((l) => l.trim())
    .filter(
      (l) =>
        l.length > 0 &&
        l.toLowerCase() !== "here are the combined outputs:" &&
        l !== "**" &&
        l !== "****"
    );

  if (lines.length === 0) return `<p>${text}</p>`;

  return `<ul>${lines.map((l) => `<li>${l}</li>`).join("")}</ul>`;
}

async function callSummarize() {
  if (selectedFiles.length === 0) {
    alert("Please choose at least one file.");
    return;
  }

  summarizeBtn.disabled = true;
  loading.classList.remove("hidden");
  result.classList.add("hidden");

  const form = new FormData();
  selectedFiles.forEach((file) => form.append("files", file));
  form.append("summary_type", lengthSelect.value);

  try {
    const res = await fetch(`${API_BASE}/api/analyze`, {
      method: "POST",
      body: form,
    });

    const data = await res.json();
    if (!res.ok || !data.ok) {
      throw new Error(data.error || "Something went wrong");
    }

    fileSummaries.innerHTML = "";
    data.files.forEach((f) => {
      const div = document.createElement("div");
      div.className = "file-summary";
      if (f.error) {
        div.innerHTML = `<h3>${f.name}</h3><p style="color:red">${f.error}</p>`;
      } else {
        div.innerHTML = `
          <h3>${f.name}</h3>
          <p><strong>Preview:</strong> ${f.text_preview}</p>
          <p><strong>${f.summary_type} summary:</strong></p>
          ${formatBullets(f.summary)}
          <p><strong>Improvement Suggestions:</strong></p>
          ${formatBullets(f.suggestions)}
        `;
      }
      fileSummaries.appendChild(div);
    });

    result.classList.remove("hidden");
  } catch (err) {
    alert(err.message);
  } finally {
    summarizeBtn.disabled = false;
    loading.classList.add("hidden");
  }
}

summarizeBtn.addEventListener("click", callSummarize);
