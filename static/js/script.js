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
      el.classList.remove('gallery-item-1', 'gallery-item-2', 'gallery-item-3', 'gallery-item-4', 'gallery-item-5');
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

  useControls(){
    const triggers = [...galleryControlsContainer.childNodes];
    triggers.forEach(control => {
      control.addEventListener('click', e=> {
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
  const exampleCarousel = new Carousel(galleryContainer, galleryItems, galleryControls);
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

if (acc_button && dropdown) {
  acc_button.addEventListener("click", () => {
    dropdown.classList.toggle("show");
    dropdown.classList.toggle("active");
  });
}

setTimeout(() => {
  document.querySelectorAll('.flash-message-welcome').forEach(el => {
    el.classList.add('fade-out');
    setTimeout(() => el.remove(), 500);
  });
}, 3000);

document.addEventListener("DOMContentLoaded", () => {
  const openBtn = document.getElementById("openmodal");
  const closeBtn = document.getElementById("closemodal");
  const modal = document.getElementById("modal");

  console.log("Modal Debug:", {openBtn, closeBtn, modal});

  if (openBtn && modal) {
    openBtn.addEventListener("click", (e) => {
      e.preventDefault();
      console.log("Opening Modal...");
      modal.classList.add("open");
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        modal.classList.remove("open");
      });
    }
  }
});