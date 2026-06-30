document.addEventListener('DOMContentLoaded', () => {
    initializeAdminMenu();
});

function initializeAdminMenu() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
    
    // ✅ NO validar sesión al cargar - solo al hacer clic en las tarjetas
    console.log('✅ Menú administrativo cargado correctamente');
}

function navigateTo(route) {
    // Validar sesión solo cuando el usuario hace clic en una tarjeta
    const session = JSON.parse(localStorage.getItem('admin_session') || '{}');
    if (!session.is_authenticated) {
        alert('Debes iniciar sesión primero');
        window.location.href = '/';
        return;
    }
    window.location.href = route;
}

function handleLogout() {
    if (confirm('¿Confirmar cierre de sesión?')) {
        localStorage.removeItem('admin_session');
        localStorage.removeItem('token');
        window.location.href = '/';
    }
}