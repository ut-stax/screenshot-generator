document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("captureForm");
  const urlInput = document.getElementById("urlInput");
  const captureBtn = document.getElementById("captureBtn");
  const btnSpinner = document.getElementById("btnSpinner");
  const btnText = document.getElementById("btnText");
  const urlFeedback = document.getElementById("urlFeedback");
  const previewImage = document.getElementById("previewImage");
  const retakeBtn = document.getElementById("retakeBtn");

  function isValidURL(url) {
    try {
      const u = new URL(url);
      return u.protocol === "http:" || u.protocol === "https:";
    } catch (err) {
      return false;
    }
  }

  form.addEventListener("submit", function (e) {
    const raw = urlInput.value.trim();
    const value = raw === "" ? "" : (raw.startsWith("http") ? raw : ("https://" + raw));

    if (!isValidURL(value)) {
      e.preventDefault();
      urlInput.classList.add("is-invalid");
      urlFeedback.style.display = "block";
      urlFeedback.textContent = "Please enter a valid URL (e.g., https://example.com).";
      urlInput.focus();
      return;
    }

    urlInput.classList.remove("is-invalid");
    urlFeedback.style.display = "none";

    btnSpinner.style.display = "inline-block";
    btnText.textContent = "Capturing...";
    captureBtn.disabled = true;
  });

  if (previewImage) {
    if (previewImage.complete) {
      previewImage.classList.add("img-loaded");
    } else {
      previewImage.addEventListener("load", function () {
        previewImage.classList.add("img-loaded");
      });
      previewImage.addEventListener("error", function () {
      });
    }
  }

  if (retakeBtn) {
    retakeBtn.addEventListener("click", function (ev) {
      ev.preventDefault();
      window.location = "/";
    });
  }
});
