document.addEventListener('DOMContentLoaded', function() {
  const letters = document.querySelectorAll('.ripple-letter');
  const animationDuration = 300; // milliseconds per letter
  
  function startRippleAnimation() {
    letters.forEach((letter, index) => {
      // Delay each letter's animation based on its position
      setTimeout(() => {
        letter.style.animation = `ripple 0.6s ease`;
        
        // Remove animation after completion to allow it to be re-applied
        setTimeout(() => {
          letter.style.animation = '';
        }, 600);
      }, index * animationDuration);
    });
    
    // Calculate total animation time and start the next wave
    const totalDuration = letters.length * animationDuration + 1000; // Add extra delay before repeating
    setTimeout(startRippleAnimation, totalDuration);
  }
  
  // Start the initial animation
  startRippleAnimation();
}); 