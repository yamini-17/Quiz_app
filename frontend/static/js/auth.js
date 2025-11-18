// auth.js - Unified Authentication (Login & Register)

function showAlert(message, type = 'error') {
    const alertContainer = document.getElementById('alert-container');
    const alertClass = type === 'success' ? 'alert-success' : 'alert-error';
    alertContainer.innerHTML = `<div class="alert ${alertClass}">${message}</div>`;
    setTimeout(() => { alertContainer.innerHTML = ''; }, 5000);
}

const BASE_URL = 'http://127.0.0.1:5000/api/auth';

// ---------------------- LOGIN ---------------------- //
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        if (!email || !password) return showAlert('Please fill in all fields');

        try {
            const response = await fetch(`${BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: "include", // ⭐ REQUIRED
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                showAlert(data.message || 'Login successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = data.user.role === 'admin' ? '/admin/dashboard' : '/dashboard';
                }, 1000);
            } else {
                showAlert(data.message || 'Invalid email or password.');
            }
        } catch (err) {
            console.error('Login error:', err);
            showAlert('Cannot connect to server. Make sure backend is running.');
        }
    });
}

// ---------------------- REGISTER ---------------------- //
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (!username || !email || !password || !confirmPassword)
            return showAlert('Please fill in all fields');

        if (username.length < 3) return showAlert('Username must be at least 3 characters');
        if (!email.includes('@') || !email.includes('.')) return showAlert('Invalid email');
        if (password.length < 6) return showAlert('Password must be at least 6 characters');
        if (password !== confirmPassword) return showAlert('Passwords do not match');

        try {
            const response = await fetch(`${BASE_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: "include", // ⭐ REQUIRED
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();

            if (response.ok) {
                showAlert(data.message || 'Registration successful! Redirecting to login...', 'success');
                setTimeout(() => { window.location.href = '/login'; }, 2000);
            } else {
                showAlert(data.message || 'Registration failed. Try again.');
            }
        } catch (err) {
            console.error('Registration error:', err);
            showAlert('Cannot connect to server. Make sure backend is running.');
        }
    });
}
