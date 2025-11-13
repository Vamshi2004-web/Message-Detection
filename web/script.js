// script.js

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contact-form');
  
    form.addEventListener('submit', function (event) {
      event.preventDefault(); // Prevents the default form submission behavior
  
      // Add your login logic here, e.g., validate the username and password
      // If validation passes, you can redirect the user to a dashboard or another page
      // For demonstration purposes, let's just log a message to the console
      console.log('Login successful!');
    });
  
    // Registration link
    const registrationLink = document.querySelector('.bottom-links a[href="registration.html"]');
    if (registrationLink) {
      registrationLink.addEventListener('click', function (event) {
        event.preventDefault();
        window.location.href = 'registration.html'; // Redirect to the registration page
      });
    }
  
    // Forgot Password link
    const forgotPasswordLink = document.querySelector('.bottom-links a[href="forgot-password.html"]');
    if (forgotPasswordLink) {
      forgotPasswordLink.addEventListener('click', function (event) {
        event.preventDefault();
        window.location.href = 'forgot-password.html'; // Redirect to the forgot password page
      });
    }
  });
  