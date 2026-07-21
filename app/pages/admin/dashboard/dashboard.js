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
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await createUser();
    });
}

// ============================================
// CREAR USUARIO (CORREGIDO)
// ============================================
async function createUser() {
    // ✅ Solo enviar los campos que el backend (InfoUser) acepta
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
            // ✅ MENSAJE DE ÉXITO CON CREDENCIALES
            const mensaje = `✅ Usuario creado exitosamente\n\n` +
                           `📧 Email: ${userData.email}\n` +
                           `🔑 Contraseña: ${userData.password}\n\n` +
                           `El usuario debe iniciar sesión para completar el formulario de vinculación.`;
            
            alert(mensaje);
            
            // ✅ LIMPIAR FORMULARIO
            document.getElementById('createUserForm').reset();
            
            // ✅ RECARGAR LISTA DE USUARIOS
            loadAdminDashboard();
            
            // ✅ OPCIÓN: Preguntar si desea redirigir al formulario de vinculación
            const redirigir = confirm(
                `¿Desea redirigir al usuario ${userData.email} al formulario de vinculación ahora?\n\n` +
                `Nota: El usuario deberá iniciar sesión con sus credenciales.`
            );
            
            if (redirigir) {
                // ✅ REDIRECCIÓN AL FORMULARIO DE VINCULACIÓN
                window.location.href = '/usuario';
            }
        } else {
            // ✅ MANEJO DE ERRORES
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
    
    try {
        const response = await fetch(`${API_URL}/admin/users`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (response.ok) {
            const data = await response.json();
            const users = data.message || [];
            
            if (users.length === 0) {
                container.innerHTML = '<h3 style="color: #1e3c72; margin: 20px 0;">📋 Usuarios Creados</h3><p style="color: #999; text-align: center; padding: 20px;">No hay usuarios creados aún</p>';
            } else {
                let html = '<h3 style="color: #1e3c72; margin: 20px 0;"> Usuarios Creados</h3>';
                users.forEach(user => {
                    const tipoUsuario = user.type_user_id === 1 ? 'Admin' : 
                                      user.type_user_id === 2 ? 'Normal' : 
                                      user.type_user_id === 3 ? 'Proveedor' : 'Cliente';
                    
                    html += `
                        <div class="user-item" style="padding: 10px; margin: 10px 0; background: #f1f5f9; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                            <div class="user-info">
                                <strong>${user.email}</strong>
                                <span style="margin-left: 10px; padding: 3px 8px; background: #2563eb; color: white; border-radius: 12px; font-size: 0.8rem;">${tipoUsuario}</span>
                                ${user.is_active ? '<span style="margin-left: 5px; padding: 3px 8px; background: #22c55e; color: white; border-radius: 12px; font-size: 0.8rem;">Activo</span>' : ''}
                            </div>
                        </div>
                    `;
                });
                container.innerHTML = html;
            }
        } else {
            container.innerHTML = '<h3 style="color: #1e3c72; margin: 20px 0;">📋 Usuarios Creados</h3><p style="color: #ef4444; text-align: center; padding: 20px;">Error al cargar usuarios</p>';
        }
    } catch (error) {
        console.error('Error cargando usuarios:', error);
        container.innerHTML = '<h3 style="color: #1e3c72; margin: 20px 0;">📋 Usuarios Creados</h3><p style="color: #ef4444; text-align: center; padding: 20px;">Error de conexión</p>';
    }
}

// ============================================
// CARGAR FORMULARIOS
// ============================================
async function loadForms() {
    const container = document.getElementById('formsList');
    
    try {
        const response = await fetch(`${API_URL}/submissions`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (response.ok) {
            const data = await response.json();
            const forms = data.submissions || [];
            
            if (forms.length === 0) {
                container.innerHTML = '<h3>📄 Formularios Recibidos</h3><p style="color: #999; text-align: center; padding: 20px;">No hay formularios recibidos aún</p>';
            } else {
                let html = '<h3>📄 Formularios Recibidos</h3>';
                forms.forEach(form => {
                    const fecha = form.created_at ? new Date(form.created_at).toLocaleDateString('es-CO') : 'N/A';
                    html += `
                        <div class="user-item" style="padding: 10px; margin: 10px 0; background: #f1f5f9; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                            <div class="user-info">
                                <strong>ID: ${form.id}</strong>
                                <span style="margin-left: 10px; padding: 3px 8px; background: #22c55e; color: white; border-radius: 12px; font-size: 0.8rem;">Estado: ${form.status || 'Pendiente'}</span>
                                <span style="margin-left: 10px; color: #64748b; font-size: 0.9rem;">${fecha}</span>
                            </div>
                        </div>
                    `;
                });
                container.innerHTML = html;
            }
        } else {
            container.innerHTML = '<h3>📄 Formularios Recibidos</h3><p style="color: #999; text-align: center; padding: 20px;">No hay formularios disponibles</p>';
        }
    } catch (error) {
        console.error('Error cargando formularios:', error);
        container.innerHTML = '<h3>📄 Formularios Recibidos</h3><p style="color: #999; text-align: center; padding: 20px;">Error al cargar</p>';
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