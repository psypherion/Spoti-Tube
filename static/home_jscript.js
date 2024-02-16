// home_jscript.js

document.addEventListener('DOMContentLoaded', function () {
    // Add event listener for Google Login button
    document.getElementById('googleLogin').addEventListener('click', function () {
      // Redirect to the index file or set the appropriate URL
      window.location.href = '/google_login';
    });
  
    // Add event listener for Guest Login button
    document.getElementById('guestLogin').addEventListener('click', function () {
      // Redirect to the index file or set the appropriate URL
      window.location.href = '/guest_login';
    });
  });
  