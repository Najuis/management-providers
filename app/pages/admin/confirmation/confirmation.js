const API_URL = window.location.origin + '/api';
const authToken = localStorage.getItem('token');

if (!authToken) {
    alert('Debes iniciar sesión primero');
    window.location.href = '/login';
}

document.addEventListener('DOMContentLoaded', () => {
    loadUsers();
});

async function loadUsers() {
    const container = document.getElementById('userList');
    const countBadge = document.getElementById('userCount');
    if (!container) return;

    try {
        const response = await fetch(`${API_URL}/admin/users`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (response.ok) {
            const data = await response.json();
            const users = data.message || [];

            countBadge.textContent = users.length;

            if (users.length === 0) {
                container.innerHTML = '<p class="empty">No hay usuarios creados aún.</p>';
                return;
            }

            let html = '';
            users.forEach(user => {
                const tipoUsuario = user.type_user_id === 1 ? 'Admin' :
                                   user.type_user_id === 2 ? 'Normal' :
                                   user.type_user_id === 3 ? 'Proveedor' : 'Cliente';

                const fecha = user.created_at ? new Date(user.created_at).toLocaleDateString('es-CO') : 'N/A';
                const esAdmin = user.type_user_id === 1;
                const botonEstado = user.is_active
                    ? `<button class="btn-action btn-inactivo" onclick="cambiarEstado(${user.id_user || user.id}, false)" ${esAdmin ? 'disabled title="No se puede desactivar al administrador"' : ''}>Desactivar</button>`
                    : `<button class="btn-action btn-activar" onclick="cambiarEstado(${user.id_user || user.id}, true)">Activar</button>`;

                html += `
                    <div class="user-item">
                        <div class="user-info">
                            <strong>${user.email}</strong>
                            <span class="badge badge-rol">${tipoUsuario}</span>
                            ${user.is_active ? '<span class="badge badge-activo">Activo</span>' : '<span class="badge badge-inactivo">Inactivo</span>'}
                        </div>
                        <div class="user-meta">
                            <span>ID: ${user.id_user || user.id || 'N/A'}</span>
                            <span>Registrado: ${fecha}</span>
                        </div>
                        <div class="user-actions">
                            ${botonEstado}
                            <button class="btn-action btn-password" onclick="resetPassword(${user.id_user || user.id})">Resetear Clave</button>
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
        } else if (response.status === 401) {
            alert('Sesión expirada. Inicia sesión nuevamente.');
            window.location.href = '/login';
        } else {
            container.innerHTML = '<p class="error">Error al cargar usuarios.</p>';
        }
    } catch (error) {
        console.error('Error cargando usuarios:', error);
        container.innerHTML = '<p class="error">Error de conexión con el servidor.</p>';
    }
}

async function cambiarEstado(userId, activar) {
    const accion = activar ? 'activar' : 'desactivar';
    if (!confirm(`¿Seguro que deseas ${accion} el usuario #${userId}?`)) return;

    try {
        const response = await fetch(`${API_URL}/admin/user/${userId}/state`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ is_active: activar })
        });

        const data = await response.json();
        if (response.ok) {
            alert(`✅ ${data.message}`);
            loadUsers();
        } else {
            alert('❌ ' + (data.detail || 'Error al cambiar el estado del usuario'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error de conexión con el servidor');
    }
}

async function resetPassword(userId) {
    const password = prompt(`Ingresa la nueva contraseña para el usuario #${userId} (mín. 8 caracteres, una mayúscula y un número):`);
    if (!password) return;

    try {
        const response = await fetch(`${API_URL}/admin/user/${userId}/password`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ password })
        });

        const data = await response.json();
        if (response.ok) {
            alert(`✅ ${data.message}`);
        } else {
            alert('❌ ' + (data.detail || 'Error al actualizar la contraseña'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error de conexión con el servidor');
    }
}
