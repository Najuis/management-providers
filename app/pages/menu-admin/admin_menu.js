document.addEventListener('DOMContentLoaded', () => {
    initializeAdminMenu();
});

function initializeAdminMenu() {
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
    validateAdminSession();
}

function navigateTo(route) {
    if (!validateAdminSession()) return;
    window.location.href = route;
}

function validateAdminSession() {
    const session = JSON.parse(localStorage.getItem('admin_session') || '{}');
    if (!session.is_authenticated) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

function handleLogout() {
    if (confirm('¿Confirmar cierre de sesión de administrador?')) {
        localStorage.removeItem('admin_session');
        window.location.href = '/';
    }
}