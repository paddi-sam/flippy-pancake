console.log("JS is loaded");

const track = document.getElementById("track");
const nextBtn = document.getElementById("next");
const prevBtn = document.getElementById("prev");

let index = 0;

function updateCarousel() {
    if (!track) return;
    const slides = document.querySelectorAll('.carousel-slide');
    const total = slides.length;
    
    slides.forEach((slide, i) => {
        slide.style.transition = 'all 0.3s';
        slide.style.top = '60%';

        let offset = i - index;
        if (offset > total / 2) offset -= total;
        if (offset < -total / 2) offset += total;

        if (offset === 0) {
            slide.style.left = '50%';
            slide.style.transform = 'translate(-50%, -50%) scale(1)';
            slide.style.zIndex = '30';
            slide.style.opacity = '1';
        } else if (Math.round(offset) === -1) {
          //left
            slide.style.left = '25%';
            slide.style.transform = 'translate(-50%, -50%) scale(0.8)';
            slide.style.zIndex = '20';
            slide.style.opacity = '0.4';
        } else if (Math.round(offset) === 1) {
          //right
            slide.style.left = '75%';
            slide.style.transform = 'translate(-50%, -50%) scale(0.8)';
            slide.style.zIndex = '20';
            slide.style.opacity = '0.4';
        } else {
            slide.style.left = '50%';
            slide.style.transform = 'translate(-50%, -50%) scale(0.5)';
            slide.style.zIndex = '10';
            slide.style.opacity = '0';
        }
    });
}

if (track && nextBtn && prevBtn) {
    const slides = document.querySelectorAll('.carousel-slide');

    function goNext() {
        index = (index + 1) % slides.length;
        updateCarousel();
    }

    function goPrev() {
        index = (index - 1 + slides.length) % slides.length;
        updateCarousel();
    }

    nextBtn.addEventListener("click", goNext);
    prevBtn.addEventListener("click", goPrev);

    // Arrow key support
    document.addEventListener("keydown", (e) => {
        if (e.key === "ArrowRight") {
            goNext();
        } else if (e.key === "ArrowLeft") {
            goPrev();
        }
    });

    updateCarousel();
}

const animElements = document.querySelectorAll('.slide-in-left');

if (animElements.length > 0) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.remove("opacity-0", "-translate-x-[1200px]");
        entry.target.classList.add("opacity-100", "translate-x-0");
      }
    });
  }, { threshold: 0 });

  animElements.forEach(el => observer.observe(el));
}

const acc_button = document.getElementById("account-button");
const dropdown = document.querySelector(".account-drop-down");

let dropdownOpen = false;

if (acc_button && dropdown) {
  acc_button.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdownOpen = !dropdownOpen;

    dropdown.classList.toggle("opacity-0", !dropdownOpen);
    dropdown.classList.toggle("-translate-y-10", !dropdownOpen);
    dropdown.classList.toggle("pointer-events-none", !dropdownOpen);

    dropdown.classList.toggle("opacity-100", dropdownOpen);
    dropdown.classList.toggle("translate-y-0", dropdownOpen);
    dropdown.classList.toggle("pointer-events-auto", dropdownOpen);
  });

  document.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target) && !acc_button.contains(e.target)) {
      dropdownOpen = false;

      dropdown.classList.add(
        "opacity-0",
        "-translate-y-10",
        "pointer-events-none"
      );

      dropdown.classList.remove(
        "opacity-100",
        "translate-y-0",
        "pointer-events-auto"
      );
    }
  });
}


setTimeout(() => {
  document.querySelectorAll('.flash-message-welcome').forEach(el => {
    el.classList.add('fade-out');
    setTimeout(() => el.remove(), 500);
  });
}, 3000);

function setupFileUpload({ dropZone, fileInput, fileNameDisplay }) {
  if (!dropZone || !fileInput || !fileNameDisplay) return;

  dropZone.addEventListener('click', () => fileInput.click());

  dropZone.addEventListener('dragover', (e) => e.preventDefault());

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    handleFile(e.dataTransfer.files[0]);
  });

  fileInput.addEventListener('change', () =>
    handleFile(fileInput.files[0])
  );

  function handleFile(file) {
    if (!file) return;

    fileNameDisplay.textContent = file.name;


    const formData = new FormData();
    formData.append('image', file);

    fetch('/upload', { method: 'POST', body: formData });
  }
}

function setupModal({ modalId, openId, closeId }) {
  const modal = document.getElementById(modalId);
  const openBtn = document.getElementById(openId);
  const closeBtn = document.getElementById(closeId);

  if (!modal || !openBtn || !closeBtn) return;

  openBtn.addEventListener("click", (e) => {
    e.preventDefault();
    modal.classList.remove("opacity-0", "pointer-events-none");
    modal.classList.add("opacity-100", "pointer-events-auto");
  });

  function closeModal() {
    modal.classList.add("opacity-0", "pointer-events-none");
    modal.classList.remove("opacity-100", "pointer-events-auto");
  }

  closeBtn.addEventListener("click", closeModal);

  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupModal({
    modalId: "modal1",
    openId: "openmodal1",
    closeId: "closemodal1"
  });

  setupModal({
    modalId: "modal2",
    openId: "openmodal2",
    closeId: "closemodal2"
  });

  setupModal({
    modalId: "modal3",
    openId: "openmodal3",
    closeId: "closemodal3"
  });

    setupModal({
    modalId: "modal4",
    openId: "openmodal4",
    closeId: "closemodal4"
  });
});