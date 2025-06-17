document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');
  const signupLink = document.getElementById('signup-link');
  const backToLogin = document.getElementById('back-to-login');
  const passwordInput = signupForm?.querySelector('input[name="password"]');
  const strengthMsg = document.getElementById('strengthMsg');

  // Only run if both forms exist
  if (loginForm && signupForm) {
    signupLink?.addEventListener('click', function (e) {
      e.preventDefault();
      loginForm.classList.remove('active');
      signupForm.classList.add('active');
    });

    backToLogin?.addEventListener('click', function (e) {
      e.preventDefault();
      signupForm.classList.remove('active');
      loginForm.classList.add('active');
    });

    passwordInput?.addEventListener('input', function () {
      const val = passwordInput.value;
      let message = '';

      if (val.length < 8) {
        message = '❌ At least 8 characters';
      } else if (!/[A-Z]/.test(val)) {
        message = '❌ Include 1 uppercase letter';
      } else if (!/[0-9]/.test(val)) {
        message = '❌ Include 1 number';
      } else if (!/[!@#$%^&*]/.test(val)) {
        message = '❌ Include 1 special character';
      } else {
        message = '✅ Strong password';
      }

      strengthMsg.textContent = message;
    });
  
  const mobileInput = document.getElementById('mobile_number');
mobileInput?.addEventListener('input', () => {
  const val = mobileInput.value;
  const isValid = /^[6-9]\d{9}$/.test(val); // Indian mobile number pattern

  mobileInput.style.borderColor = isValid ? 'green' : 'red';
});
  }
});