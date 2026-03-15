/**
 * AI Code Reviewer - Frontend JavaScript
 */

const codeTextarea = document.getElementById("code-textarea");
const fileInput = document.getElementById("file-input");
const fileDropZone = document.getElementById("file-drop-zone");
const fileList = document.getElementById("file-list");
const analyzeBtn = document.getElementById("analyze-btn");
const resetBtn = document.getElementById("reset-btn");
const exportBtn = document.getElementById("export-btn");

const uploadSection = document.querySelector(".upload-section");
const resultsSection = document.getElementById("results-section");
const loadingState = document.getElementById("loading-state");
const resultsContent = document.getElementById("results-content");
const filesContainer = document.getElementById("files-container");

const tabButtons = document.querySelectorAll(".tab-button");
const tabContents = document.querySelectorAll(".tab-content");
const themeToggle = document.getElementById("theme-toggle");
const themeToggleIcon = document.getElementById("theme-toggle-icon");
const themeToggleText = document.getElementById("theme-toggle-text");
const overallGrade = document.getElementById("overall-grade");
const overallProgress = document.getElementById("overall-progress");
const severityFilters = document.querySelectorAll(".severity-filter");
const countAll = document.getElementById("count-all");
const countCritical = document.getElementById("count-critical");
const countWarning = document.getElementById("count-warning");
const countSuggestion = document.getElementById("count-suggestion");
const filteredEmptyState = document.getElementById("filtered-empty-state");

const activeMode = document.getElementById("active-mode");
const selectedFileCount = document.getElementById("selected-file-count");
const inlineMessage = document.getElementById("inline-message");

let selectedFiles = [];
let currentTheme = "dark";
let activeSeverityFilter = "ALL";

function applyTheme(theme) {
  const isLight = theme === "light";
  document.body.classList.toggle("light-theme", isLight);

  currentTheme = theme;
  if (themeToggleIcon) {
    themeToggleIcon.textContent = isLight ? "☀️" : "🌙";
  }
  if (themeToggleText) {
    themeToggleText.textContent = isLight ? "Light" : "Dark";
  }
  if (themeToggle) {
    themeToggle.setAttribute(
      "aria-label",
      isLight ? "Switch to dark theme" : "Switch to light theme",
    );
  }
}

function loadThemePreference() {
  const savedTheme = localStorage.getItem("ai-reviewer-theme");
  if (savedTheme === "light" || savedTheme === "dark") {
    applyTheme(savedTheme);
    return;
  }

  applyTheme("dark");
}

function toggleTheme() {
  const nextTheme = currentTheme === "light" ? "dark" : "light";
  applyTheme(nextTheme);
  localStorage.setItem("ai-reviewer-theme", nextTheme);
}

function setInlineMessage(message = "", type = "info") {
  if (!inlineMessage) {
    return;
  }
  inlineMessage.textContent = message;
  inlineMessage.dataset.type = message ? type : "";
}

function updateModeLabel(modeText) {
  if (activeMode) {
    activeMode.textContent = modeText;
  }
}

function updateSelectedFileCount() {
  if (selectedFileCount) {
    selectedFileCount.textContent = String(selectedFiles.length);
  }
}

function createElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) {
    element.className = className;
  }
  if (typeof text === "string") {
    element.textContent = text;
  }
  return element;
}

function getScoreGrade(score) {
  if (score >= 9) return "A+";
  if (score >= 8) return "A";
  if (score >= 7) return "B";
  if (score >= 6) return "C";
  if (score >= 5) return "D";
  return "F";
}

function setActiveSeverityFilter(filter) {
  activeSeverityFilter = filter;
  severityFilters.forEach((button) => {
    button.classList.toggle("active", button.dataset.filter === filter);
  });
}

function updateFilterCounts(data) {
  if (countAll) {
    countAll.textContent = String(data.total_issues);
  }
  if (countCritical) {
    countCritical.textContent = String(data.critical_count);
  }
  if (countWarning) {
    countWarning.textContent = String(data.warning_count);
  }
  if (countSuggestion) {
    countSuggestion.textContent = String(data.suggestion_count);
  }
}

function updateTabState(button) {
  const tabId = button.id.replace("tab-", "");

  tabButtons.forEach((btn) => btn.classList.remove("active"));
  tabContents.forEach((content) => content.classList.remove("active"));

  button.classList.add("active");
  document.getElementById(`${tabId}-tab`).classList.add("active");

  updateModeLabel(tabId === "paste" ? "Paste Code" : "Upload Files");
  setInlineMessage("");
}

tabButtons.forEach((button) => {
  button.addEventListener("click", () => updateTabState(button));
});

if (themeToggle) {
  themeToggle.addEventListener("click", toggleTheme);
}

severityFilters.forEach((button) => {
  button.addEventListener("click", () => {
    setActiveSeverityFilter(button.dataset.filter);
    applyIssueVisibilityFilter();
  });
});

if (fileDropZone && fileInput) {
  fileDropZone.addEventListener("click", () => fileInput.click());
}

if (fileInput) {
  fileInput.addEventListener("change", (event) => {
    handleFiles(event.target.files);
  });
}

if (fileDropZone) {
  fileDropZone.addEventListener("dragover", (event) => {
    event.preventDefault();
    fileDropZone.classList.add("drag-over");
  });
}

if (fileDropZone) {
  fileDropZone.addEventListener("dragleave", () => {
    fileDropZone.classList.remove("drag-over");
  });
}

if (fileDropZone) {
  fileDropZone.addEventListener("drop", (event) => {
    event.preventDefault();
    fileDropZone.classList.remove("drag-over");
    handleFiles(event.dataTransfer.files);
  });
}

function handleFiles(files) {
  selectedFiles = Array.from(files);
  updateFileList();
  updateSelectedFileCount();

  if (selectedFiles.length > 0) {
    setInlineMessage(
      `${selectedFiles.length} file(s) ready for review.`,
      "info",
    );
  } else {
    setInlineMessage("");
  }
}

function updateFileList() {
  fileList.innerHTML = "";

  selectedFiles.forEach((file, index) => {
    const fileItem = createElement("div", "file-item");

    const fileInfo = createElement("div");
    fileInfo.appendChild(createElement("div", "file-item-name", file.name));
    fileInfo.appendChild(
      createElement("div", "file-item-size", formatFileSize(file.size)),
    );

    const removeBtn = createElement("button", "file-item-remove", "✕");
    removeBtn.type = "button";
    removeBtn.setAttribute("aria-label", `Remove ${file.name}`);
    removeBtn.addEventListener("click", () => removeFile(index));

    fileItem.append(fileInfo, removeBtn);
    fileList.appendChild(fileItem);
  });
}

function removeFile(index) {
  selectedFiles.splice(index, 1);
  updateFileList();
  updateSelectedFileCount();

  if (selectedFiles.length === 0) {
    setInlineMessage("No files selected. Upload files or paste code.", "info");
  } else {
    setInlineMessage(
      `${selectedFiles.length} file(s) ready for review.`,
      "info",
    );
  }
}

function formatFileSize(bytes) {
  if (bytes === 0) {
    return "0 Bytes";
  }

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${Math.round((bytes / Math.pow(k, i)) * 100) / 100} ${sizes[i]}`;
}

analyzeBtn.addEventListener("click", analyzeCode);

async function analyzeCode() {
  const codeText = codeTextarea.value.trim();

  if (!codeText && selectedFiles.length === 0) {
    setInlineMessage(
      "Please provide code to analyze (paste or upload files).",
      "error",
    );
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";
  setInlineMessage("Running analysis...", "info");

  try {
    const formData = new FormData();

    if (codeText) {
      formData.append("code", codeText);
    }

    selectedFiles.forEach((file) => {
      formData.append("files", file);
    });

    resultsSection.classList.remove("hidden");
    loadingState.classList.remove("hidden");
    resultsContent.classList.add("hidden");

    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });

    console.log("Sending analysis request...", {
      hasCode: !!codeText,
      fileCount: selectedFiles.length,
    });

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

    const response = await fetch("/api/analyze", {
      method: "POST",
      body: formData,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    console.log("Response received:", response.status);

    if (!response.ok) {
      let errorMsg = `Server error (${response.status})`;
      try {
        const error = await response.json();
        errorMsg = error.error || errorMsg;
      } catch (e) {
        // If response body isn't JSON, use status message
        errorMsg = `${response.status}: ${response.statusText}`;
      }
      throw new Error(errorMsg);
    }

    const result = await response.json();

    console.log("Analysis result:", result);

    if (!result.success) {
      throw new Error(result.error || "Analysis failed - no data returned");
    }

    if (!result.data) {
      throw new Error("No analysis data received from server");
    }

    displayResults(result.data);
    setInlineMessage("Analysis completed successfully.", "success");
  } catch (error) {
    console.error("Analysis error:", error);
    if (error.name === "AbortError") {
      setInlineMessage(
        "Error: Request timed out. The server took too long to respond. Please try again with a smaller file.",
        "error",
      );
    } else {
      setInlineMessage(`Error: ${error.message}`, "error");
    }
    resultsSection.classList.add("hidden");
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Review Code";
  }
}

function displayResults(data) {
  if (loadingState) {
    loadingState.classList.add("hidden");
  }
  if (resultsContent) {
    resultsContent.classList.remove("hidden");
  }

  const overallScoreEl = document.getElementById("overall-score");
  const totalIssuesEl = document.getElementById("total-issues");
  const criticalCountEl = document.getElementById("critical-count");
  const warningCountEl = document.getElementById("warning-count");
  const suggestionCountEl = document.getElementById("suggestion-count");

  if (overallScoreEl) {
    overallScoreEl.textContent = String(data.overall_score);
  }
  if (totalIssuesEl) {
    totalIssuesEl.textContent = String(data.total_issues);
  }
  if (criticalCountEl) {
    criticalCountEl.textContent = String(data.critical_count);
  }
  if (warningCountEl) {
    warningCountEl.textContent = String(data.warning_count);
  }
  if (suggestionCountEl) {
    suggestionCountEl.textContent = String(data.suggestion_count);
  }

  if (overallGrade) {
    overallGrade.textContent = `Grade ${getScoreGrade(data.overall_score)}`;
  }
  if (overallProgress) {
    overallProgress.style.width = `${Math.max(0, Math.min(100, data.overall_score * 10))}%`;
  }
  updateFilterCounts(data);

  const score = data.overall_score;
  let message = "";

  if (score >= 8.5) {
    message = "Excellent work! Your code looks great.";
  } else if (score >= 7) {
    message = "Good job! A few improvements recommended.";
  } else if (score >= 5) {
    message = "Code needs attention. Review the issues below.";
  } else {
    message =
      "Multiple issues detected. Prioritize critical and warning items.";
  }

  const scoreMessageEl = document.getElementById("score-message");
  if (scoreMessageEl) {
    scoreMessageEl.textContent = message;
  }

  if (!filesContainer) {
    return;
  }

  filesContainer.innerHTML = "";

  Object.entries(data.files).forEach(([filename, fileData]) => {
    filesContainer.appendChild(createFileCard(filename, fileData));
  });

  applyIssueVisibilityFilter();
}

function applyIssueVisibilityFilter() {
  const fileCards = filesContainer.querySelectorAll(".file-card");
  let visibleCardCount = 0;

  fileCards.forEach((fileCard) => {
    const issues = fileCard.querySelectorAll(".issue-item");
    let visibleIssueCount = 0;

    issues.forEach((issue) => {
      const severity = issue
        .querySelector(".issue-badge")
        ?.textContent?.trim()
        .toUpperCase();
      const shouldShow =
        activeSeverityFilter === "ALL" || severity === activeSeverityFilter;

      issue.style.display = shouldShow ? "flex" : "none";
      if (shouldShow) {
        visibleIssueCount += 1;
      }
    });

    const noIssues = fileCard.querySelector(".no-issues");
    if (noIssues) {
      noIssues.style.display =
        activeSeverityFilter === "ALL" ? "block" : "none";
    }

    if (issues.length > 0) {
      fileCard.style.display = visibleIssueCount > 0 ? "block" : "none";
      if (visibleIssueCount > 0) {
        visibleCardCount += 1;
      }
    } else if (activeSeverityFilter === "ALL") {
      visibleCardCount += 1;
    }
  });

  if (filteredEmptyState) {
    filteredEmptyState.classList.toggle("hidden", visibleCardCount > 0);
  }
}

function createFileCard(filename, fileData) {
  const card = createElement("div", "file-card");

  const header = createElement("div", "file-card-header");
  header.appendChild(createElement("div", "file-name", `📄 ${filename}`));
  header.appendChild(
    createElement("div", "file-score", `${fileData.score}/10`),
  );
  card.appendChild(header);

  if (fileData.issues.length === 0) {
    card.appendChild(createElement("div", "no-issues", "✓ No issues found!"));
    return card;
  }

  const issuesList = createElement("div", "issues-list");

  const sortedIssues = [...fileData.issues].sort((a, b) => {
    const severityOrder = { CRITICAL: 0, WARNING: 1, SUGGESTION: 2 };
    return severityOrder[a.severity] - severityOrder[b.severity];
  });

  sortedIssues.forEach((issue) => {
    const issueItem = createElement(
      "div",
      `issue-item ${issue.severity.toLowerCase()}`,
    );

    const issueContent = createElement("div", "issue-content");
    issueContent.appendChild(createElement("div", "issue-type", issue.type));
    issueContent.appendChild(
      createElement("div", "issue-message", issue.message),
    );
    issueContent.appendChild(
      createElement("div", "issue-line", `Line ${issue.line}`),
    );

    issueItem.appendChild(issueContent);
    issueItem.appendChild(createElement("div", "issue-badge", issue.severity));
    issuesList.appendChild(issueItem);
  });

  card.appendChild(issuesList);
  return card;
}

if (resetBtn) {
  resetBtn.addEventListener("click", () => {
    if (codeTextarea) {
      codeTextarea.value = "";
    }
    selectedFiles = [];
    if (fileInput) {
      fileInput.value = "";
    }
    if (fileList) {
      fileList.innerHTML = "";
    }
    if (resultsSection) {
      resultsSection.classList.add("hidden");
    }
    updateSelectedFileCount();
    setInlineMessage("Ready for a new review.", "info");
    if (uploadSection) {
      uploadSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
}

if (exportBtn) {
  exportBtn.addEventListener("click", () => {
    const resultsText = generateResultsText();
    downloadAsFile(resultsText, "code-review-results.txt");
    setInlineMessage("Results exported.", "success");
  });
}

function generateResultsText() {
  const score = document.getElementById("overall-score")?.textContent || "0";
  const totalIssues =
    document.getElementById("total-issues")?.textContent || "0";
  const criticalCount =
    document.getElementById("critical-count")?.textContent || "0";
  const warningCount =
    document.getElementById("warning-count")?.textContent || "0";
  const suggestionCount =
    document.getElementById("suggestion-count")?.textContent || "0";

  let text = "AI CODE REVIEW RESULTS\n";
  text += "=".repeat(50) + "\n\n";
  text += `Overall Score: ${score}/10\n`;
  text += `Total Issues: ${totalIssues}\n`;
  text += `Critical: ${criticalCount} | Warnings: ${warningCount} | Suggestions: ${suggestionCount}\n\n`;

  const fileCards = document.querySelectorAll(".file-card");
  fileCards.forEach((card) => {
    const filename = card.querySelector(".file-name")?.textContent || "Unknown";
    const fileScore = card.querySelector(".file-score")?.textContent || "-";
    const issues = card.querySelectorAll(".issue-item");

    text += "-".repeat(50) + "\n";
    text += `${filename} - Score: ${fileScore}\n`;
    text += "-".repeat(50) + "\n";

    if (issues.length === 0) {
      text += "No issues found!\n";
    } else {
      issues.forEach((issue) => {
        const type = issue.querySelector(".issue-type")?.textContent || "Issue";
        const message =
          issue.querySelector(".issue-message")?.textContent || "No details";
        const line =
          issue.querySelector(".issue-line")?.textContent || "Line ?";
        const severity =
          issue.querySelector(".issue-badge")?.textContent || "UNKNOWN";

        text += `[${severity}] ${type}\n`;
        text += `  ${message}\n`;
        text += `  ${line}\n\n`;
      });
    }

    text += "\n";
  });

  text += "\nGenerated by AI Code Reviewer\n";
  text += `${new Date().toLocaleString()}\n`;

  return text;
}

function downloadAsFile(content, filename) {
  const element = document.createElement("a");
  element.setAttribute(
    "href",
    `data:text/plain;charset=utf-8,${encodeURIComponent(content)}`,
  );
  element.setAttribute("download", filename);
  element.style.display = "none";
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
}

if (analyzeBtn) {
  analyzeBtn.addEventListener("click", analyzeCode);
}

document.addEventListener("DOMContentLoaded", () => {
  loadThemePreference();
  updateModeLabel("Paste Code");
  updateSelectedFileCount();
  setActiveSeverityFilter("ALL");
  setInlineMessage("Paste code or upload files to begin.", "info");

  document.addEventListener("keydown", (event) => {
    const isAnalyzeShortcut =
      (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "enter";
    if (isAnalyzeShortcut) {
      event.preventDefault();
      analyzeCode();
    }
  });
});
