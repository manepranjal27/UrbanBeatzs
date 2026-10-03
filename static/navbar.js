// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarLinks = document.querySelector('.navbar-links');
    
    if (navbarToggle && navbarLinks) {
        navbarToggle.addEventListener('click', function() {
            navbarLinks.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (navbarLinks.classList.contains('active') && 
            !navbarLinks.contains(e.target) && 
            !navbarToggle.contains(e.target)) {
            navbarLinks.classList.remove('active');
        }
    });
});
