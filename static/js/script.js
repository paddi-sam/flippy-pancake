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
        slide.style.top = '50%';

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
    nextBtn.addEventListener("click", () => {
        index = (index + 1) % document.querySelectorAll('.carousel-slide').length;
        updateCarousel();
    });
    prevBtn.addEventListener("click", () => {
        const total = document.querySelectorAll('.carousel-slide').length;
        index = (index - 1 + total) % total;
        updateCarousel();
    });
    updateCarousel();
}

const animElements = document.querySelectorAll('.slide-in-left');

if (animElements.length > 0) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('show');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

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

document.addEventListener("DOMContentLoaded", () => {
  const openBtn = document.getElementById("openmodal1");
  const closeBtn = document.getElementById("closemodal1");
  const modal1 = document.getElementById("modal1");

  if (modal1 && openBtn && closeBtn) {
    openBtn.addEventListener("click", (e) => {
      e.preventDefault();

      modal1.classList.add("opacity-100", "pointer-events-auto");
      modal1.classList.remove("opacity-0", "pointer-events-none");
    });

    closeBtn.addEventListener("click", () => {
      modal1.classList.add("opacity-0", "pointer-events-none");
      modal1.classList.remove("opacity-100", "pointer-events-auto");
    });

    modal1.addEventListener("click", (e) => {
      if (e.target === modal1) {
        modal1.classList.add("opacity-0", "pointer-events-none");
        modal1.classList.remove("opacity-100", "pointer-events-auto");
      }
    });

    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name');

    if (dropZone && fileInput && fileNameDisplay) {
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
  }
});

const openBtn2 = document.getElementById("openmodal2");
const closeBtn2 = document.getElementById("closemodal2");
const modal2 = document.getElementById("modal2");

if (modal2 && openBtn2 && closeBtn2) {
  openBtn2.addEventListener("click", (e) => {
    e.preventDefault();

    modal2.classList.remove("opacity-0", "pointer-events-none");
    modal2.classList.add("opacity-100", "pointer-events-auto");
  });

  closeBtn2.addEventListener("click", () => {
    modal2.classList.add("opacity-0", "pointer-events-none");
    modal2.classList.remove("opacity-100", "pointer-events-auto");
  });

  modal2.addEventListener("click", (e) => {
    if (e.target === modal2) {
      modal2.classList.add("opacity-0", "pointer-events-none");
      modal2.classList.remove("opacity-100", "pointer-events-auto");
    }
  });
}