const galleryContainer = document.querySelector('.gallery-container');
const galleryControlsContainer = document.querySelector('.gallery-controls');
const galleryControls = ['previous', 'next']
const galleryItems=document.querySelectorAll('.gallery-item')

class Carousel {

  constructor(container, items, controls){
    this.carouselContainer = container;
    this.carouselControls = controls;
    this.carouselArray = [...items];
  }

  updateGallery(){
    this.carouselArray.forEach(el => {
      el.classList.remove('gallery-item-1');
      el.classList.remove('gallery-item-2');
      el.classList.remove('gallery-item-3');
      el.classList.remove('gallery-item-4');
      el.classList.remove('gallery-item-5');
    });

    this.carouselArray.slice(0, 5).forEach((el , i) => {
      el.classList.add(`gallery-item-${i+1}`);
    });
  }

  setCurrentState(direction){
    if (direction.classList.contains('gallery-controls-previous')){
      this.carouselArray.unshift(this.carouselArray.pop());
    } else {
      this.carouselArray.push(this.carouselArray.shift());
    }
    this.updateGallery();
  }

  setControls() {
    this.carouselControls.forEach(control => {
      galleryControlsContainer.appendChild(document.createElement('button')).className = `gallery-controls-${control}`;
      document.querySelector(`.gallery-controls-${control}`).innerText = control;
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
      this.setCurrentState(prevButton);
    }

    if (e.key === 'ArrowRight') {
      const nextButton = document.querySelector('.gallery-controls-next');
      this.setCurrentState(nextButton);
    }
  });
}}

const exampleCarousel = new Carousel(galleryContainer, galleryItems, galleryControls);

exampleCarousel.setControls();
exampleCarousel.useControls();
exampleCarousel.useKeyboard();

const elements = document.querySelectorAll('.slide-in-left');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show');
      observer.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.2
});

elements.forEach(el => observer.observe(el));

const button = document.getElementById("account-button");
const menu = document.querySelector(".account-drop-down");

button.addEventListener("click", () => {
  menu.classList.toggle("active");
});

const acc_button = document.getElementById("account-button");
const dropdown = document.querySelector(".account-drop-down");

acc_button.addEventListener("click", () => {
  dropdown.classList.toggle("show");
});

setTimeout(() => {
  document.querySelectorAll('.flash-message-welcome').forEach(el => {
    el.classList.add('fade-out');

    setTimeout(() => {
      el.remove();
    }, 500);
  });
}, 3000);