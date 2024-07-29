// Animation function
document.addEventListener("DOMContentLoaded", function() {
    const homeText = "Our Innovativeness is the secret for our Uniqueness";
    const home_title = $(".home-title");
    let index = 0;
  
    function homeTitle() {
      if (index < homeText.length) {
        home_title.append(homeText[index]);
        index++;
        setTimeout(homeTitle, 30);
      }
    }
  
    homeTitle();
  
    const vis_img = document.querySelector(".vision1");
    const mis_img = document.querySelector(".mission");
    const keyframes = [
      { transform: "scale(0)", opacity: 0 },
      { transform: "scale(1)", opacity: 1 },
    ];
    const optns = { duration: 2000, easing: "ease-in-out" };
    
    vis_img.animate(keyframes, optns);
    mis_img.animate(keyframes, optns);
    
    // Animation on Company Profile Summary Section
    const boxes = document.querySelectorAll(".prof-item");
    const section = document.querySelector(".comp-profile");
    const banner = document.querySelector('.home-banner');
  
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateBoxes();
        }
      });
    });
    
    observer.observe(section);
    
    function animateBoxes() {
      let index = 0;
      const interval = setInterval(() => {
        if (index < boxes.length) {
          boxes[index].style.opacity = 1;
          boxes[index].classList.add("animate");
          index++;
        } else  {
          clearInterval(interval);
          boxes.forEach(box => box.classList.remove("animate"));
        }
      }, 500);
    }
  
    // <!-- Beginning of rotate 360 deg once it is in view  -->
    // const banner = document.querySelector('.home-banner');
  
    // Function to check if an element is in view
    function isInViewport(element) {
      const rect = element.getBoundingClientRect();
      return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
      );
    }
  
    // Function to handle rotation
    function handleRotation() {
      if (isInViewport(banner)) {
        banner.style.animation = 'spin 2s linear';
      } else {
        banner.style.animation = 'none';
      }
    }
  
    // Add event listener for scrolling
    window.addEventListener('scroll', handleRotation);
  
    // Initial check on page load
    handleRotation();
    // <!-- End of rotate 360 deg -->
  
  
    // <!-- Beginning of slide in from the left once it is in view  -->
    const slideRIght = document.querySelector('.slided');
  
    function slideRightIfVisible() {
      if (isInViewport(slideRIght)) {
        slideRIght.style.animation = 'moveright 1s forwards';
      } else {
        slideRIght.style.animation = 'none';
      }
    }
    
    // Listen for scroll events
    window.addEventListener('scroll', slideRightIfVisible);
    
    // Initially check if object is in view
    slideRightIfVisible();
    // <!-- End of slide in from the left -->
  
    // <!-- Beginning of slide in from the right once it is in view  -->
    banner.style.animation = 'moveright 1s forwards';
    banner.style.position = 'relative';
    // <!-- End of slide in from the right -->
});