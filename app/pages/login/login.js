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

        //si el login es exitoso, redirige al dashboard
        if (response.ok) {
            console.log('Login exitoso:', data);
            // guardar token y tipo de usuario en localStorage
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('type_user', data.type_user);

            // Redireccionar según el tipo de usuario
            if (data.type_user === 1) {
                window.location.href = "/admin/dashboard";
            } else if (data.type_user === 2) {
                window.location.href = "/admin/form";
            } else {
                // Redirección por defecto
                window.location.href = "/admin/dashboard";
            }
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
