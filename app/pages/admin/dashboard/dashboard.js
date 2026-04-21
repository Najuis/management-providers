async function loadAdminDashboard() {
    try {
        const usersResponse = await fetch(`${API_URL}/usuarios/`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const usersData = await usersResponse.json();
        if (usersData.success || Array.isArray(usersData)) {
            renderUserList(usersData.data || usersData);
        }
    } catch (error) { console.error('Error cargando usuarios:', error); }

    try {
        const formsResponse = await fetch(`${API_URL}/formularios/`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const formsData = await formsResponse.json();
        if (formsData.success || Array.isArray(formsData.data)) {
            renderFormsList(formsData.data || formsData);
        }
    } catch (error) { console.error('Error cargando formularios:', error); }
}

function renderUserList(users) {
    const container = document.getElementById('userList');
    let html = '<h3 style="color: #1e3c72; margin: 20px 0;">📋 Usuarios Creados</h3>';
    const userUsers = users.filter(u => u.role === 'user');
    if (userUsers.length === 0) {
        html += '<p style="color: #999;">No hay usuarios creados aún</p>';
    } else {
        userUsers.forEach(user => {
            html += `
                <div class="user-item">
                    <div class="user-info">
                        <strong>${user.username}</strong>
                        <span class="badge">${user.tipo_persona === 'natural' ? '👤 Natural' : '🏢 Jurídica'}</span>
                        <span class="badge badge-warning">${user.tipo_servicio}</span>
                        <span class="badge badge-success">${user.estado}</span>
                    </div>
                    <button class="btn btn-danger btn-sm" onclick="deleteUser(${user.id})">🗑️ Eliminar</button>
                </div>`;
        });
    }
    container.innerHTML = html;
}

function renderFormsList(forms) {
    const container = document.getElementById('formsList');
    let html = '<h3 style="color: #1e3c72; margin: 20px 0;">📄 Formularios Recibidos</h3>';
    if (!forms || forms.length === 0) {
        html += '<p style="color: #999;">No hay formularios recibidos aún</p>';
    } else {
        forms.forEach(form => {
            html += `
                <div class="user-item">
                    <div class="user-info">
                        <strong>ID: ${form.id}</strong>
                        <span class="badge">Estado: ${form.estado}</span>
                        <span>${form.created_at ? new Date(form.created_at).toLocaleDateString() : ''}</span>
                    </div>
                    <div>
                        <button class="btn btn-success btn-sm" onclick="approveForm(${form.id}, true)">✅ Aprobar</button>
                        <button class="btn btn-danger btn-sm"  onclick="approveForm(${form.id}, false)">❌ Rechazar</button>
                    </div>
                </div>`;
        });
    }
    container.innerHTML = html;
}

document.getElementById('createUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const userData = {
        username: document.getElementById('newUsername').value,
        password: document.getElementById('newPassword').value,
        email: document.getElementById('newEmail').value,
        tipo_persona: document.getElementById('newTipoPersona').value,
        tipo_vinculacion: document.getElementById('newTipoVinculacion').value,
        tipo_servicio: document.getElementById('newTipoServicio').value
    };
    try {
        const response = await fetch(`${API_URL}/usuarios/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${authToken}` },
            body: JSON.stringify(userData)
        });
        const data = await response.json();
        if (data.success) {
            alert(`✅ Usuario creado exitosamente\n\n👤 Usuario: ${userData.username}\n🔑 Contraseña: ${userData.password}`);
            document.getElementById('createUserForm').reset();
            loadAdminDashboard();
        } else {
            alert('❌ ' + (data.detail || data.message || 'Error al crear usuario'));
        }
    } catch (error) { alert('❌ Error de conexión con el servidor'); }
});

async function deleteUser(id) {
    if (!confirm('¿Estás seguro de eliminar este usuario?')) return;
    try {
        const response = await fetch(`${API_URL}/usuarios/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const data = await response.json();
        if (data.success) { loadAdminDashboard(); }
        else { alert('❌ ' + (data.detail || data.message || 'Error al eliminar')); }
    } catch (error) { alert('❌ Error de conexión'); }
}

async function approveForm(id, aprueba) {
    if (!confirm(`¿${aprueba ? 'Aprobar' : 'Rechazar'} este formulario?`)) return;
    try {
        const response = await fetch(`${API_URL}/formularios/${id}/aprobar?aprueba=${aprueba}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const data = await response.json();
        if (data.success) { alert(data.message); loadAdminDashboard(); }
        else { alert('❌ ' + (data.detail || data.message || 'Error')); }
    } catch (error) { alert('❌ Error de conexión'); }
}
