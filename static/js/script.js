// console.log("JS loaded");
// script.js

// Smooth scroll for anchor links (if added later)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Button ripple effect on click
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', function (e) {
        const circle = document.createElement('span');
        circle.classList.add('ripple');
        this.appendChild(circle);

        const diameter = Math.max(this.clientWidth, this.clientHeight);
        const radius = diameter / 2;

        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${e.clientX - this.getBoundingClientRect().left - radius}px`;
        circle.style.top = `${e.clientY - this.getBoundingClientRect().top - radius}px`;

        setTimeout(() => circle.remove(), 600);
    });
});

// Show random mental health quote popup every 30 seconds
const quotes = [
    "You are not alone.",
    "Healing is not linear.",
    "It’s okay to rest.",
    "One day at a time.",
    "You are enough.",
    "Asking for help is strength.",
    "Healing takes time, and that’s okay.",
    "Your mental health is a priority.",
    "It's okay to ask for help.",
    "Be kind to your mind.",
    "Every day is a fresh start.",
    "Progress, not perfection."
];

// Function to show loading overlay with a random quote
function createOverlayElement(quoteText) {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';

    const quote = document.createElement('div');
    quote.className = 'loading-quote';
    quote.innerText = quoteText;

    overlay.appendChild(quote);
    return overlay;
}

// Intercept clicks on disorder/resource links to show quote
document.querySelectorAll('.resource-link, .disorder-link, a[href^="/finder/"]').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();  // Stop immediate navigation
        const url = this.href;
        const quoteText = quotes[Math.floor(Math.random() * quotes.length)];

        // Save to sessionStorage to know we should show overlay on next page
        sessionStorage.setItem('showOverlay', 'true');
        sessionStorage.setItem('quoteText', quoteText);

        // Navigate after short delay (optional: show local preview if desired)
        window.location.href = url;
    });
});

// On load, check if overlay needs to be shown (then faded out)
window.addEventListener('load', () => {
    const shouldShow = sessionStorage.getItem('showOverlay');
    const quoteText = sessionStorage.getItem('quoteText');

    if (shouldShow === 'true' && quoteText) {
        const overlay = createOverlayElement(quoteText);
        document.body.appendChild(overlay);

        // Fade out after load
        setTimeout(() => {
            overlay.classList.add('fade-out');
            setTimeout(() => overlay.remove(), 500);  // Match CSS transition time
        }, 1500); // wait a bit before fade

        // Clean up storage
        sessionStorage.removeItem('showOverlay');
        sessionStorage.removeItem('quoteText');
    }
});
