document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.querySelectorAll('.password-toggle');

    togglePassword.forEach(toggle => {
        toggle.onclick = function () {
            const inputGroup = this.parentElement;
            const passwordField = inputGroup.querySelector('input[type="password"], input[type="text"]');
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            this.textContent = type === 'password' ? 'visibility_off' : 'visibility';
        };
    });
});

