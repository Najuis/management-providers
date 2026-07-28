// ============================================
// VARIABLES GLOBALES
// ============================================
const API_URL = window.location.origin + '/api';
const authToken = localStorage.getItem('token');

// ============================================
// VERIFICAR AUTENTICACIÓN
// ============================================
if (!authToken) {
    alert('Debes iniciar sesión primero');
    window.location.href = '/login';
}

// ============================================
// INICIALIZAR DASHBOARD
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    loadAdminDashboard();
    setupFormHandler();
});

// ============================================
// CONFIGURAR MANEJADOR DEL FORMULARIO
// ============================================
function setupFormHandler() {
    const form = document.getElementById('createUserForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await createUser();
        });
    }
}

// ============================================
// CREAR USUARIO
// ============================================
async function createUser() {
    const userData = {
        email: document.getElementById('newEmail').value,
        password: document.getElementById('newPassword').value,
        type_user_id: parseInt(document.getElementById('newTypeUser').value)
    };

    try {
        const response = await fetch(`${API_URL}/admin/user`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}` 
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            const mensaje = `✅ Usuario creado exitosamente\n\n` +
                           `📧 Email: ${userData.email}\n` +
                           `🔑 Contraseña: ${userData.password}\n\n` +
                           `El usuario debe iniciar sesión para completar el formulario de vinculación.`;
            
            alert(mensaje);
            document.getElementById('createUserForm').reset();
            loadAdminDashboard();
            
            const redirigir = confirm(
                `¿Desea redirigir al usuario ${userData.email} al formulario de vinculación ahora?\n\n` +
                `Nota: El usuario deberá iniciar sesión con sus credenciales.`
            );
            
            if (redirigir) {
                window.location.href = '/usuario';
            }
        } else {
            if (data.detail && data.detail.includes('email')) {
                alert('❌ El email ya está registrado. Usa otro email.');
            } else {
                alert('❌ ' + (data.detail || data.message || 'Error al crear usuario'));
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error de conexión con el servidor');
    }
}

// ============================================
// CARGAR DASHBOARD
// ============================================
async function loadAdminDashboard() {
    await loadUsers();
    await loadForms();
}

// ============================================
// CARGAR USUARIOS
// ============================================
async function loadUsers() {
    const container = document.getElementById('userList');
    if (!container) return;
    
    try {
        const response = await fetch(`${API_URL}/admin/users`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (response.ok) {
            const data = await response.json();
            const users = data.message || [];
            
            if (users.length === 0) {
                container.innerHTML = '<h3 style="color: var(--azul-medio); margin: 20px 0;">📋 Usuarios Creados</h3><p style="color: #999; text-align: center; padding: 20px;">No hay usuarios creados aún</p>';
            } else {
                let html = '<h3 style="color: var(--azul-medio); margin: 20px 0;">📋 Usuarios Creados</h3>';
                users.forEach(user => {
                    const tipoUsuario = user.type_user_id === 1 ? 'Admin' : 
                                      user.type_user_id === 2 ? 'Normal' : 
                                      user.type_user_id === 3 ? 'Proveedor' : 'Cliente';
                    
                    html += `
                        <div class="user-item" style="display: flex; justify-content: space-between; align-items: center;">
                            <div class="user-info">
                                <strong>${user.email}</strong>
                                <span class="badge ${user.type_user_id === 1 ? 'badge-admin' : 'badge-normal'}">${tipoUsuario}</span>
                                ${user.is_active ? '<span class="badge badge-activo">Activo</span>' : '<span class="badge badge-inactivo">Inactivo</span>'}
                            </div>
                        </div>
                    `;
                });
                container.innerHTML = html;
            }
        } else {
            container.innerHTML = '<h3 style="color: var(--azul-medio); margin: 20px 0;">📋 Usuarios Creados</h3><p style="color: #ef4444; text-align: center; padding: 20px;">Error al cargar usuarios</p>';
        }
    } catch (error) {
        console.error('Error cargando usuarios:', error);
        container.innerHTML = '<h3 style="color: var(--azul-medio); margin: 20px 0;">📋 Usuarios Creados</h3><p style="color: #ef4444; text-align: center; padding: 20px;">Error de conexión</p>';
    }
}

// ============================================
// CARGAR FORMULARIOS
// ============================================
async function loadForms() {
    const container = document.getElementById('formsList');
    if (!container) return;
    
    try {
        const response = await fetch(`${API_URL}/submissions`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (response.ok) {
            const data = await response.json();
            const forms = data.submissions || data.message || [];
            
            if (forms.length === 0) {
                container.innerHTML = '<h3 style="color: var(--azul-medio); margin: 20px 0;">📄 Formularios Recibidos</h3><p style="color: #999; text-align: center; padding: 20px;">No hay formularios recibidos aún</p>';
            } else {
                let html = '<h3 style="color: var(--azul-medio); margin: 20px 0;">📄 Formularios Recibidos</h3>';
                forms.forEach(form => {
                    const fecha = form.created_at ? new Date(form.created_at).toLocaleDateString('es-CO') : 'N/A';
                    html += `
                        <div class="user-item" style="display: flex; justify-content: space-between; align-items: center;">
                            <div class="user-info">
                                <strong>ID: ${form.id || 'N/A'}</strong>
                                <span class="badge badge-activo">Estado: ${form.status || 'Pendiente'}</span>
                                <span style="margin-left: 10px; color: #64748b; font-size: 0.9rem;">${fecha}</span>
                            </div>
                            <a href="/admin/validation" class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.85rem; text-decoration: none;">Validar</a>
                        </div>
                    `;
                });
                container.innerHTML = html;
            }
        } else {
            container.innerHTML = '<h3 style="color: var(--azul-medio); margin: 20px 0;">📄 Formularios Recibidos</h3><p style="color: #999; text-align: center; padding: 20px;">No hay formularios disponibles</p>';
        }
    } catch (error) {
        console.error('Error cargando formularios:', error);
        container.innerHTML = '<h3 style="color: var(--azul-medio); margin: 20px 0;">📄 Formularios Recibidos</h3><p style="color: #999; text-align: center; padding: 20px;">Error al cargar</p>';
    }
}

// ============================================
// CERRAR SESIÓN
// ============================================
function logout() {
    if (confirm('¿Confirmar cierre de sesión?')) {
        localStorage.removeItem('token');
        localStorage.removeItem('type_user');
        window.location.href = '/login';
    }
}