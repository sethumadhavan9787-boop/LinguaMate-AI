// LinguaMate AI - Central Interactive Script

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initSidebarToggle();
  initReportModal();
});

// Theme Management
function initTheme() {
  const savedTheme = localStorage.getItem("linguamate_theme") || "light";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeIcon(savedTheme);

  const toggleBtn = document.getElementById("themeToggleBtn");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme") || "light";
      const nextTheme = current === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", nextTheme);
      localStorage.setItem("linguamate_theme", nextTheme);
      updateThemeIcon(nextTheme);
    });
  }
}

function updateThemeIcon(theme) {
  const icon = document.getElementById("themeIcon");
  if (icon) {
    icon.className = theme === "dark" ? "bi bi-sun-fill" : "bi bi-moon-stars-fill";
  }
}

// Sidebar toggle for smaller screens
function initSidebarToggle() {
  const toggleBtn = document.getElementById("sidebarToggleBtn");
  const sidebar = document.querySelector(".app-sidebar");
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", () => {
      sidebar.classList.toggle("show");
    });
  }
}

// Copy text utility with toast / visual feedback
function copyToClipboard(text, btnElement) {
  navigator.clipboard.writeText(text).then(() => {
    const originalHtml = btnElement.innerHTML;
    btnElement.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i> Copied!';
    setTimeout(() => {
      btnElement.innerHTML = originalHtml;
    }, 2000);
  }).catch(() => {
    alert("Could not copy text to clipboard.");
  });
}

// Toggle vocabulary favorite
async function toggleWordFavorite(wordId, btnElement) {
  try {
    const res = await fetch("/vocabulary/favorite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: wordId })
    });
    const data = await res.json();
    if (data.success) {
      const icon = btnElement.querySelector("i");
      if (icon) {
        if (data.is_favorite) {
          icon.className = "bi bi-star-fill text-warning";
        } else {
          icon.className = "bi bi-star text-muted";
        }
      }
    }
  } catch (err) {
    console.error("Failed to toggle favorite:", err);
  }
}

// Toggle lesson completion
async function toggleLessonCompletion(dayNumber, btnElement) {
  try {
    const res = await fetch(`/lessons/${dayNumber}/toggle`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    const data = await res.json();
    if (data.success) {
      if (data.completed) {
        btnElement.classList.replace("btn-outline-success", "btn-success");
        btnElement.innerHTML = '<i class="bi bi-check-circle-fill me-1"></i> Completed';
      } else {
        btnElement.classList.replace("btn-success", "btn-outline-success");
        btnElement.innerHTML = '<i class="bi bi-circle me-1"></i> Mark as Complete';
      }
    }
  } catch (err) {
    console.error("Error toggling completion:", err);
  }
}

// Responsible AI report modal handling
function initReportModal() {
  const form = document.getElementById("reportAiForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const module = document.getElementById("reportModule").value;
      const inputText = document.getElementById("reportInputText").value;
      const aiResponse = document.getElementById("reportAiResponse").value;
      const issueCategory = document.getElementById("reportIssueCategory").value;
      const userNotes = document.getElementById("reportUserNotes").value;

      try {
        const res = await fetch("/responsible-ai/report", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            module,
            input_text: inputText,
            ai_response: aiResponse,
            issue_category: issueCategory,
            user_notes: userNotes
          })
        });
        const data = await res.json();
        if (data.success) {
          alert(data.message);
          form.reset();
          const modalEl = document.getElementById("reportAiModal");
          const modal = bootstrap.Modal.getInstance(modalEl);
          if (modal) modal.hide();
        }
      } catch (err) {
        alert("Failed to submit report. Please try again.");
      }
    });
  }
}

function openReportModal(module = "General", inputText = "", aiResponse = "") {
  document.getElementById("reportModule").value = module;
  document.getElementById("reportInputText").value = inputText;
  document.getElementById("reportAiResponse").value = aiResponse;
  const modal = new bootstrap.Modal(document.getElementById("reportAiModal"));
  modal.show();
}
