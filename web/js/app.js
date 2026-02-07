/**
 * 🍭 Fililico - Main Application
 * Logique frontend pour l'interface Kawaii
 */

// State
const state = {
  files: [], // Maintenant contient des objets {path, name, size, type}
  selectedFileIndex: null,
  isProcessing: false,
  mascotState: "idle",
  userSetOutputFolder: false,
};

// DOM Elements
const elements = {
  dropZone: document.getElementById("dropZone"),
  fileInput: document.getElementById("fileInput"),
  fileList: document.getElementById("fileList"),
  previewContainer: document.getElementById("previewContainer"),
  previewPlaceholder: document.getElementById("previewPlaceholder"),
  previewImage: document.getElementById("previewImage"),
  resultsSection: document.getElementById("resultsSection"),
  resultsList: document.getElementById("resultsList"),
  watermarkText: document.getElementById("watermarkText"),
  opacitySlider: document.getElementById("opacitySlider"),
  opacityValue: document.getElementById("opacityValue"),
  outputFolder: document.getElementById("outputFolder"),
  processBtn: document.getElementById("processBtn"),
  progressSection: document.getElementById("progressSection"),
  progressFill: document.getElementById("progressFill"),
  progressText: document.getElementById("progressText"),
  fileCount: document.getElementById("fileCount"),
  mascot: document.getElementById("mascot"),
};

// Mascot states - images mapping
const mascotImages = {
  idle: "assets/images/stamp_1.png",
  drag: "assets/images/stamp_2.png",
  processing: "assets/images/stamp_3.png",
  done: "assets/images/stamp_4.png",
};

// ═══════════════════════════════════════════════════════════════
// MASCOT MANAGEMENT
// ═══════════════════════════════════════════════════════════════

function setMascotState(newState) {
  if (state.mascotState === newState) return;

  state.mascotState = newState;
  const mascot = elements.mascot;

  // Remove all state classes
  mascot.classList.remove("idle", "drag", "processing", "done");

  // Add new state class
  mascot.classList.add(newState);

  // Update image
  mascot.src = mascotImages[newState] || mascotImages.idle;
}

// ═══════════════════════════════════════════════════════════════
// DRAG & DROP
// ═══════════════════════════════════════════════════════════════

function initDragDrop() {
  const dropZone = elements.dropZone;

  // Click to select - use Python file picker for real paths
  dropZone.addEventListener("click", async () => {
    if (typeof eel !== "undefined") {
      try {
        const files = await eel.select_files()();
        if (files && files.length > 0) {
          handleFilesFromPython(files);
        }
      } catch (e) {
        console.error("File selection error:", e);
        showNotification("Erreur lors de la sélection", "error");
      }
    } else {
      // Fallback pour dev sans Eel
      elements.fileInput.click();
    }
  });

  // File input change (fallback)
  elements.fileInput.addEventListener("change", (e) => {
    // Note: Browser files don't have real paths
    showNotification("Utilisez le clic pour sélectionner avec les vrais chemins", "info");
  });

  // Drag events
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
    setMascotState("drag");
  });

  dropZone.addEventListener("dragleave", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    setMascotState("idle");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    setMascotState("idle");

    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  });
}

// ═══════════════════════════════════════════════════════════════
// FILE HANDLING
// ═══════════════════════════════════════════════════════════════

const SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".pdf"];

function isSupported(file) {
  const ext = "." + file.name.split(".").pop().toLowerCase();
  return SUPPORTED_EXTENSIONS.includes(ext);
}

function getFileIcon(fileName) {
  const ext = fileName.split(".").pop().toLowerCase();
  const icons = {
    png: "🖼️",
    jpg: "🖼️",
    jpeg: "🖼️",
    bmp: "🖼️",
    gif: "🖼️",
    pdf: "📄",
  };
  return icons[ext] || "📁";
}

function formatFileSize(bytes) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
}

/**
 * Gère les fichiers venant du sélecteur Python (avec vrais chemins)
 */
async function handleFilesFromPython(filePaths) {
  if (filePaths.length === 0) {
    showNotification("Aucun fichier sélectionné !", "error");
    return;
  }

  // Créer des objets fichier avec les chemins complets
  const newFiles = filePaths.map((path) => {
    const name = path.split(/[\\/]/).pop(); // Extraire le nom du fichier
    return {
      path: path,
      name: name,
      size: 0, // On ne connaît pas la taille, pas grave
      type: getFileType(name),
    };
  });

  // Add to state
  state.files.push(...newFiles);

  // Auto-set output folder from first file's directory
  if (!state.userSetOutputFolder && newFiles.length > 0) {
    try {
      const folder = await eel.get_file_directory(newFiles[0].path)();
      if (folder) {
        elements.outputFolder.value = folder;
      }
    } catch (e) {
      console.warn("Could not get file directory:", e);
    }
  }

  // Update UI
  updateFileList();
  updateFileCount();
  updateProcessButton();

  // Select first file if none selected
  if (state.selectedFileIndex === null && state.files.length > 0) {
    selectFile(0);
  }

  showNotification(`${newFiles.length} fichier(s) ajouté(s) !`, "success");
}

function getFileType(fileName) {
  const ext = fileName.split(".").pop().toLowerCase();
  const types = {
    png: "image/png",
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    bmp: "image/bmp",
    gif: "image/gif",
    pdf: "application/pdf",
  };
  return types[ext] || "application/octet-stream";
}

async function handleFiles(files) {
  const supportedFiles = files.filter(isSupported);

  if (supportedFiles.length === 0) {
    showNotification("Aucun fichier supporté trouvé !", "error");
    return;
  }

  // Add to state
  state.files.push(...supportedFiles);

  // Auto-set output folder if not manually set by user
  if (!state.userSetOutputFolder && supportedFiles.length > 0) {
    const firstFile = supportedFiles[0];
    // Get the directory of the first file via Eel or fallback
    if (typeof eel !== "undefined" && firstFile.path) {
      try {
        const folder = await eel.get_file_directory(firstFile.path)();
        if (folder) {
          elements.outputFolder.value = folder;
        }
      } catch (e) {
        console.warn("Could not get file directory:", e);
      }
    }
  }

  // Update UI
  updateFileList();
  updateFileCount();
  updateProcessButton();

  // Select first file if none selected
  if (state.selectedFileIndex === null && state.files.length > 0) {
    selectFile(0);
  }

  // Show notification
  showNotification(
    `${supportedFiles.length} fichier(s) ajouté(s) !`,
    "success",
  );
}

function updateFileList() {
  const fileList = elements.fileList;

  if (state.files.length === 0) {
    fileList.classList.add("hidden");
    return;
  }

  fileList.classList.remove("hidden");
  fileList.innerHTML = "";

  state.files.forEach((file, index) => {
    const item = document.createElement("div");
    item.className = "file-item slide-in";
    item.style.animationDelay = `${index * 50}ms`;

    item.innerHTML = `
      <span class="file-item-icon">${getFileIcon(file.name)}</span>
      <span class="file-item-name">${file.name}</span>
      <span class="file-item-size">${formatFileSize(file.size)}</span>
      <button class="file-item-remove" data-index="${index}" title="Retirer">✕</button>
    `;

    // Click to select
    item.addEventListener("click", (e) => {
      if (!e.target.classList.contains("file-item-remove")) {
        selectFile(index);
      }
    });

    fileList.appendChild(item);
  });

  // Add remove listeners
  fileList.querySelectorAll(".file-item-remove").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      removeFile(parseInt(btn.dataset.index));
    });
  });
}

function selectFile(index) {
  state.selectedFileIndex = index;
  const file = state.files[index];

  // Update UI selection
  elements.fileList.querySelectorAll(".file-item").forEach((item, i) => {
    item.style.borderColor =
      i === index ? "var(--bubblegum-pink)" : "var(--magic-berry-light)";
  });

  // Generate preview
  generatePreview(file);
}

function removeFile(index) {
  state.files.splice(index, 1);

  // Adjust selection
  if (state.selectedFileIndex === index) {
    state.selectedFileIndex =
      state.files.length > 0 ? Math.min(index, state.files.length - 1) : null;
  } else if (state.selectedFileIndex > index) {
    state.selectedFileIndex--;
  }

  updateFileList();
  updateFileCount();
  updateProcessButton();

  // Update preview
  if (state.selectedFileIndex !== null) {
    selectFile(state.selectedFileIndex);
  } else {
    clearPreview();
  }
}

function updateFileCount() {
  elements.fileCount.textContent = state.files.length;
}

function updateProcessButton() {
  elements.processBtn.disabled = state.files.length === 0 || state.isProcessing;
}

// ═══════════════════════════════════════════════════════════════
// PREVIEW
// ═══════════════════════════════════════════════════════════════

async function generatePreview(file) {
  const isPdf = file.name.toLowerCase().endsWith(".pdf");

  if (isPdf) {
    // PDF preview - just show icon
    elements.previewPlaceholder.innerHTML = `
      <span class="preview-placeholder-icon">📄</span>
      <span>${file.name}</span>
      <span style="font-size: 0.875rem; color: var(--magic-berry);">
        Aperçu PDF non disponible
      </span>
    `;
    elements.previewPlaceholder.classList.remove("hidden");
    elements.previewImage.classList.add("hidden");
  } else {
    // Image preview - use Eel to get base64 from real path
    if (typeof eel !== "undefined" && file.path) {
      try {
        const base64 = await eel.get_image_preview(file.path)();
        if (base64) {
          elements.previewImage.src = base64;
          elements.previewImage.classList.remove("hidden");
          elements.previewPlaceholder.classList.add("hidden");
        } else {
          showPreviewError(file.name);
        }
      } catch (e) {
        console.error("Preview error:", e);
        showPreviewError(file.name);
      }
    } else {
      showPreviewError(file.name);
    }
  }
}

function showPreviewError(fileName) {
  elements.previewPlaceholder.innerHTML = `
    <span class="preview-placeholder-icon">🖼️</span>
    <span>${fileName}</span>
    <span style="font-size: 0.875rem; color: var(--magic-berry);">
      Aperçu non disponible
    </span>
  `;
  elements.previewPlaceholder.classList.remove("hidden");
  elements.previewImage.classList.add("hidden");
}

function clearPreview() {
  elements.previewPlaceholder.innerHTML = `
    <span class="preview-placeholder-icon">🖼️</span>
    <span>Sélectionnez un fichier pour voir l'aperçu</span>
  `;
  elements.previewPlaceholder.classList.remove("hidden");
  elements.previewImage.classList.add("hidden");
}

// ═══════════════════════════════════════════════════════════════
// PROCESSING (Eel Integration Point)
// ═══════════════════════════════════════════════════════════════

async function processFiles() {
  if (state.files.length === 0 || state.isProcessing) return;

  state.isProcessing = true;
  setMascotState("processing");
  updateProcessButton();

  // Show progress
  elements.progressSection.classList.remove("hidden");
  elements.resultsSection.classList.add("hidden");
  elements.resultsList.innerHTML = "";

  const results = [];
  const total = state.files.length;

  for (let i = 0; i < total; i++) {
    const file = state.files[i];
    const progress = ((i + 1) / total) * 100;

    // Update progress
    elements.progressFill.style.width = `${progress}%`;
    elements.progressText.textContent = `Traitement de ${file.name}... (${i + 1}/${total})`;

    try {
      // Call Eel function (or simulate)
      let result;
      if (typeof eel !== "undefined") {
        // Real Eel call
        result = await eel.process_file(
          file.path,
          elements.watermarkText.value,
          parseInt(elements.opacitySlider.value) / 100,
          elements.outputFolder.value || null,
        )();
      } else {
        // Simulation for testing
        await sleep(500);
        result = {
          success: true,
          input: file.name,
          output: file.name.replace(/(\.[^.]+)$/, "_watermarked$1"),
        };
      }

      results.push(result);
    } catch (error) {
      results.push({
        success: false,
        input: file.name,
        error: error.message || "Erreur inconnue",
      });
    }
  }

  // Complete
  state.isProcessing = false;
  setMascotState("done");
  showResults(results);
  updateProcessButton();

  // Reset mascot after delay
  setTimeout(() => {
    if (!state.isProcessing) {
      setMascotState("idle");
    }
  }, 3000);
}

function showResults(results) {
  elements.progressSection.classList.add("hidden");
  elements.resultsSection.classList.remove("hidden");
  elements.resultsList.innerHTML = "";

  const successCount = results.filter((r) => r.success).length;
  const totalCount = results.length;

  results.forEach((result, index) => {
    const item = document.createElement("div");
    item.className = `result-item ${result.success ? "success" : "error"} slide-in`;
    item.style.animationDelay = `${index * 100}ms`;

    item.innerHTML = `
      <span class="result-icon">${result.success ? "✅" : "❌"}</span>
      <div style="flex: 1;">
        <span style="font-weight: 600;">${result.input}</span>
        ${
          result.success
            ? `<span style="display: block; font-size: 0.875rem; color: var(--minty-fresh);">
               → ${result.output}
             </span>`
            : `<span style="display: block; font-size: 0.875rem; color: var(--bubblegum-pink);">
               ${result.error}
             </span>`
        }
      </div>
    `;

    elements.resultsList.appendChild(item);
  });

  // Show notification
  if (successCount === totalCount) {
    showNotification(
      `${totalCount} fichier(s) traité(s) avec succès ! ✨`,
      "success",
    );
  } else {
    showNotification(
      `${successCount}/${totalCount} fichier(s) traité(s)`,
      successCount > 0 ? "warning" : "error",
    );
  }

  // Clear files after processing
  state.files = [];
  state.selectedFileIndex = null;
  updateFileList();
  updateFileCount();
  clearPreview();
}

// ═══════════════════════════════════════════════════════════════
// NOTIFICATIONS
// ═══════════════════════════════════════════════════════════════

function showNotification(message, type = "info") {
  // Create notification
  const notification = document.createElement("div");
  notification.className = "notification fade-in";
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 16px 24px;
    border-radius: 16px;
    font-weight: 600;
    z-index: 1000;
    backdrop-filter: blur(10px);
    animation: slideIn 0.3s ease;
  `;

  const colors = {
    success: {
      bg: "rgba(52, 211, 153, 0.9)",
      text: "white",
    },
    error: {
      bg: "rgba(244, 114, 182, 0.9)",
      text: "white",
    },
    warning: {
      bg: "rgba(251, 191, 36, 0.9)",
      text: "#4c1d95",
    },
    info: {
      bg: "rgba(167, 139, 250, 0.9)",
      text: "white",
    },
  };

  const color = colors[type] || colors.info;
  notification.style.background = color.bg;
  notification.style.color = color.text;
  notification.textContent = message;

  document.body.appendChild(notification);

  // Remove after delay
  setTimeout(() => {
    notification.style.animation = "fadeOut 0.3s ease forwards";
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// ═══════════════════════════════════════════════════════════════
// UTILITIES
// ═══════════════════════════════════════════════════════════════

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ═══════════════════════════════════════════════════════════════
// OPACITY SLIDER
// ═══════════════════════════════════════════════════════════════

function initOpacitySlider() {
  elements.opacitySlider.addEventListener("input", (e) => {
    elements.opacityValue.textContent = e.target.value;
  });
}

// ═══════════════════════════════════════════════════════════════
// OUTPUT FOLDER PICKER
// ═══════════════════════════════════════════════════════════════

function initOutputFolderPicker() {
  const outputFolderInput = elements.outputFolder;
  const browseBtn = document.getElementById("browseOutputBtn");
  
  if (browseBtn) {
    browseBtn.addEventListener("click", async () => {
      if (typeof eel !== "undefined") {
        try {
          const folder = await eel.select_output_folder(
            outputFolderInput.value || null
          )();
          if (folder) {
            outputFolderInput.value = folder;
            state.userSetOutputFolder = true;
            showNotification("Dossier de destination défini !", "success");
          }
        } catch (e) {
          console.error("Folder selection error:", e);
          showNotification("Erreur lors de la sélection du dossier", "error");
        }
      } else {
        // Fallback pour le dev sans Eel
        showNotification("Sélection de dossier disponible uniquement dans l'app", "info");
      }
    });
  }

  // Mark as user-set if they manually type in the field
  outputFolderInput.addEventListener("input", () => {
    state.userSetOutputFolder = true;
  });
}

// ═══════════════════════════════════════════════════════════════
// PROCESS BUTTON
// ═══════════════════════════════════════════════════════════════

function initProcessButton() {
  elements.processBtn.addEventListener("click", processFiles);
}

// ═══════════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════════

function init() {
  initDragDrop();
  initOpacitySlider();
  initOutputFolderPicker();
  initProcessButton();

  console.log("🍭 Fililico initialized!");
}

// Start app
document.addEventListener("DOMContentLoaded", init);
