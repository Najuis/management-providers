document.addEventListener('DOMContentLoaded', () => {
    console.log('🔐 Login page loaded');
});

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
        console.log('📤 Enviando login...', { email });
        
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        console.log('📥 Respuesta del login:', response.status, data);

        if (response.ok) {
            console.log('✅ Login exitoso');
            console.log('🔑 Token:', data.access_token ? 'RECIBIDO' : 'NO RECIBIDO');
            console.log('👤 Type User:', data.type_user);
            console.log('👤 Is Admin:', data.is_admin);
            
            // Guardar token y tipo de usuario
            if (data.access_token) {
                localStorage.setItem('token', data.access_token);
            }
            if (data.type_user !== undefined) {
                localStorage.setItem('type_user', String(data.type_user));
            }
            if (data.is_admin !== undefined) {
                localStorage.setItem('is_admin', String(data.is_admin));
            }
            
            // ✅ REDIRECCIÓN CORREGIDA - VERIFICAR AMBAS CONDICIONES
            const userType = Number(data.type_user);
            const isAdmin = data.is_admin === true || data.is_admin === "true" || data.is_admin === 1;
            
            console.log('🔄 Evaluando redirección...');
            console.log('   userType:', userType);
            console.log('   isAdmin:', isAdmin);
            
            // Lógica CORRECTA:
            // - Si type_user_id = 1 O is_admin = true → Admin Dashboard
            // - Si type_user_id = 2, 3, 4 → Usuario Formulario
            
            if (userType === 1 || isAdmin) {
                console.log('👉 Redirigiendo a ADMINISTRADOR: /admin/dashboard');
                window.location.href = "/admin/dashboard";
            } else if (userType === 2 || userType === 3 || userType === 4) {
                console.log(' Redirigiendo a USUARIO: /usuario');
                window.location.href = "/usuario";
            } else {
                console.log('️ Redirección por defecto a: /login');
                window.location.href = "/login";
            }
        } else {
            console.error('❌ Error en login:', data);
            errorMessage.textContent = data.detail || 'Credenciales inválidas. Inténtalo de nuevo.';
            showErrorAnimation();
        }
    } catch (error) {
        console.error('💥 Error de red:', error);
        errorMessage.textContent = 'Error de conexión. Por favor revisa tu internet.';
    } finally {
        submitButton.classList.remove('loading');
        submitButton.disabled = false;
    }
});

function showErrorAnimation() {
    const card = document.querySelector('.login-card');
    if (card) {
        card.style.animation = 'none';
        card.offsetHeight;
        card.style.animation = 'shake 0.4s ease-in-out';
    }
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