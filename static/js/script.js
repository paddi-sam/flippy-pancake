console.log("JS is loaded");

const galleryContainer = document.querySelector('.gallery-container');
const galleryControlsContainer = document.querySelector('.gallery-controls');
const galleryControls = ['previous', 'next'];
const galleryItems = document.querySelectorAll('.gallery-item');
class Carousel {
  constructor(container, items, controls) {
    this.carouselContainer = container;
    this.carouselControls = controls;
    this.carouselArray = [...items];
  }

  updateGallery() {
    this.carouselArray.forEach(el => {
      el.classList.remove(
        'gallery-item-1',
        'gallery-item-2',
        'gallery-item-3',
        'gallery-item-4',
        'gallery-item-5'
      );
    });

    this.carouselArray.slice(0, 5).forEach((el, i) => {
      el.classList.add(`gallery-item-${i + 1}`);
    });
  }

  setCurrentState(direction) {
    if (direction.classList.contains('gallery-controls-previous')) {
      this.carouselArray.unshift(this.carouselArray.pop());
    } else {
      this.carouselArray.push(this.carouselArray.shift());
    }
    this.updateGallery();
  }

  setControls() {
    this.carouselControls.forEach(control => {
      const btn = document.createElement('button');
      btn.className = `gallery-controls-${control}`;
      btn.innerText = control;
      galleryControlsContainer.appendChild(btn);
    });
  }

  useControls() {
    const triggers = [...galleryControlsContainer.childNodes];

    triggers.forEach(control => {
      control.addEventListener('click', e => {
        e.preventDefault();
        this.setCurrentState(control);
      });
    });
  }

  useKeyboard() {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        const prevButton = document.querySelector('.gallery-controls-previous');
        if (prevButton) this.setCurrentState(prevButton);
      }
      if (e.key === 'ArrowRight') {
        const nextButton = document.querySelector('.gallery-controls-next');
        if (nextButton) this.setCurrentState(nextButton);
      }
    });
  }
}

if (galleryContainer && galleryControlsContainer && galleryItems.length > 0) {
  const exampleCarousel = new Carousel(
    galleryContainer,
    galleryItems,
    galleryControls
  );

  exampleCarousel.setControls();
  exampleCarousel.useControls();
  exampleCarousel.useKeyboard();
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

  // close on outside click
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

  if (!modal1 || !openBtn || !closeBtn) {
    console.log("Modal elements missing");
    return;
  }

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