document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');
    const submitButton = document.getElementById('submitButton');

    errorMessage.textContent = '';
    submitButton.classList.add('loading');
    submitButton.disabled = true;

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Login exitoso:', data);

            if (data.access_token) {
                localStorage.setItem('token', data.access_token);
            }
            window.location.href = '/pages/admin/index.html';
        } else {
            errorMessage.textContent = data.detail || 'Credenciales inválidas. Inténtalo de nuevo.';
            showErrorAnimation();
        }
    } catch (error) {
        console.error('Error de red:', error);
        errorMessage.textContent = 'Error de conexión. Por favor revisa tu internet.';
    } finally {
        submitButton.classList.remove('loading');
        submitButton.disabled = false;
    }
});

function showErrorAnimation() {
    const card = document.querySelector('.login-card');
    card.style.animation = 'none';
    card.offsetHeight;
    card.style.animation = 'shake 0.4s ease-in-out';
}

const style = document.createElement('style');
style.textContent = `
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-8px); }
    50% { transform: translateX(8px); }
    75% { transform: translateX(-4px); }
}
`;
document.head.appendChild(style);
