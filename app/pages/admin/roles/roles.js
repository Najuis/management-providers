const API_URL = window.location.origin + '/api';
const authToken = localStorage.getItem('token');

if (!authToken) {
    alert('Debes iniciar sesión primero');
    window.location.href = '/login';
}

document.addEventListener('DOMContentLoaded', () => {
    loadAdmins();
});

function nombreRol(typeUserId) {
    switch (typeUserId) {
        case 1: return 'Admin';
        case 2: return 'Normal';
        case 3: return 'Proveedor';
        case 4: return 'Cliente';
        default: return 'Desconocido';
    }
}

async function loadAdmins() {
    const container = document.getElementById('adminList');
    const countBadge = document.getElementById('adminCount');
    if (!container) return;

    try {
        const response = await fetch(`${API_URL}/admin/admins`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (response.ok) {
            const data = await response.json();
            const admins = data.message || [];

            countBadge.textContent = admins.length;

            if (admins.length === 0) {
                container.innerHTML = '<p class="empty">No hay cuentas administradoras.</p>';
                return;
            }

            let html = '';
            admins.forEach(admin => {
                const id = admin.id_user || admin.id;
                const fecha = admin.created_at ? new Date(admin.created_at).toLocaleDateString('es-CO') : 'N/A';
                const rolActual = admin.type_user_id;
                const esAdmin = !!admin.is_admin;

                html += `
                    <div class="admin-item">
                        <div class="admin-top">
                            <div class="admin-meta">
                                <span>ID: ${id}</span>
                                <span>Registrado: ${fecha}</span>
                            </div>
                            ${admin.is_active ? '<span class="badge badge-activo">Activo</span>' : '<span class="badge badge-inactivo">Inactivo</span>'}
                        </div>
                        <div class="admin-top">
                            <strong>${admin.email}</strong>
                            <span class="badge badge-rol" id="rolBadge-${id}">${nombreRol(rolActual)}</span>
                        </div>
                        <div class="permissions-row">
                            <div class="permission-field">
                                <label>Rol:</label>
                                <select id="rolSelect-${id}">
                                    <option value="1" ${rolActual === 1 ? 'selected' : ''}>1 - Admin</option>
                                    <option value="2" ${rolActual === 2 ? 'selected' : ''}>2 - Normal</option>
                                    <option value="3" ${rolActual === 3 ? 'selected' : ''}>3 - Proveedor</option>
                                    <option value="4" ${rolActual === 4 ? 'selected' : ''}>4 - Cliente</option>
                                </select>
                            </div>
                            <div class="permission-field">
                                <label>Es administrador:</label>
                                <label class="switch">
                                    <input type="checkbox" id="adminToggle-${id}" ${esAdmin ? 'checked' : ''}>
                                    <span class="slider"></span>
                                </label>
                            </div>
                            <button class="btn-save" id="saveBtn-${id}" onclick="guardarPermisos(${id})">Guardar</button>
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
        } else if (response.status === 401 || response.status === 403) {
            alert('Sesión expirada o sin permisos. Inicia sesión nuevamente.');
            window.location.href = '/login';
        } else {
            container.innerHTML = '<p class="error">Error al cargar los administradores.</p>';
        }
    } catch (error) {
        console.error('Error cargando administradores:', error);
        container.innerHTML = '<p class="error">Error de conexión con el servidor.</p>';
    }
}

async function guardarPermisos(userId) {
    const rolSelect = document.getElementById(`rolSelect-${userId}`);
    const adminToggle = document.getElementById(`adminToggle-${userId}`);
    const saveBtn = document.getElementById(`saveBtn-${userId}`);

    if (!rolSelect || !adminToggle) return;

    const type_user_id = parseInt(rolSelect.value, 10);
    const is_admin = adminToggle.checked;

    if (!confirm(`¿Guardar rol "${type_user_id}" y ${is_admin ? 'conceder' : 'quitar'} permiso de administrador al usuario #${userId}?`)) return;

    saveBtn.disabled = true;
    saveBtn.textContent = 'Guardando...';

    try {
        const response = await fetch(`${API_URL}/admin/user/${userId}/permissions`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ type_user_id, is_admin })
        });

        const data = await response.json();
        if (response.ok) {
            alert(`✅ ${data.message}`);
            loadAdmins();
        } else {
            alert('❌ ' + (data.detail || 'Error al actualizar los permisos'));
            saveBtn.disabled = false;
            saveBtn.textContent = 'Guardar';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error de conexión con el servidor');
        saveBtn.disabled = false;
        saveBtn.textContent = 'Guardar';
    }
}
