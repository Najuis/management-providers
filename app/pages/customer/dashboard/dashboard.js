// ============================================
// DASHBOARD DE CONFIRMACIÓN DE SOLICITUD
// ============================================
const STATUS_MAP = {
    'borrador': { text: 'Borrador', cls: 'badge-pending' },
    'pendiente_revision': { text: 'Pendiente de Revisión', cls: 'badge-pending' },
    'en_revision': { text: 'En Revisión', cls: 'badge-review' },
    'aprobado': { text: 'Aprobado', cls: 'badge-success' },
    'rechazado': { text: 'Rechazado', cls: 'badge-danger' },
    'completado': { text: 'Completado', cls: 'badge-success' }
};

document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
});

async function initDashboard() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    try {
        // 1. Perfil autenticado: el email de login
        const profileRes = await fetch('/api/user/profile', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!profileRes.ok) {
            window.location.href = '/login';
            return;
        }
        const profile = await profileRes.json();
        renderCredentials(profile);

        // 2. Datos reales de la solicitud desde la BD
        const id = new URLSearchParams(window.location.search).get('id');
        if (id) {
            const submission = await fetchSubmission(id, token);
            if (submission) {
                renderSummary(submission, profile);
                renderStatus(submission.status);
            } else {
                renderStatus('pendiente_revision');
            }
        }

        populateSignatureFields(submission);
    } catch (error) {
        console.error('Error al cargar el dashboard:', error);
        renderStatus('pendiente_revision');
    }
}

async function fetchSubmission(id, token) {
    try {
        const res = await fetch(`/api/submissions/${id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error(`Error ${res.status}`);
        return await res.json();
    } catch (error) {
        console.error('Error al cargar la solicitud:', error);
        return null;
    }
}

// ============================================
// CREDENCIALES DE ACCESO
// ============================================
function renderCredentials(profile) {
    document.getElementById('displayUsername').value = profile.email || '';
    document.getElementById('displayPassword').value = '••••••••';
    document.getElementById('passwordNote').textContent = 'Misma contraseña con la que iniciaste sesión.';
    const copyBtn = document.getElementById('copyPasswordBtn');
    if (copyBtn) copyBtn.style.display = 'none';
}

// ============================================
// RESUMEN DE LA INFORMACIÓN ENVIADA
// ============================================
function renderSummary(data, profile) {
    const nombre = data.razon_social || [data.nombres, data.apellidos].filter(Boolean).join(' ');
    const f = data.form_data || {};

    document.getElementById('summaryName').textContent = nombre || 'No disponible';
    document.getElementById('summaryDoc').textContent = data.numero_id || 'No disponible';
    document.getElementById('summaryType').textContent = data.tipo_persona === 'juridica' ? 'Persona Jurídica' : 'Persona Natural';
    document.getElementById('summaryEmail').textContent = profile.email || 'No disponible';
    document.getElementById('submissionId').textContent = data.id ?? 'N/A';
    document.getElementById('submissionDate').textContent = formatDate(data.submitted_at || data.created_at);
    document.getElementById('summaryCity').textContent = f.ciudad_nombre || 'No disponible';
    document.getElementById('summaryActivity').textContent = f.actividad_economica || data.codigo_ciiu || 'No disponible';
}

// ============================================
// ESTADO DE LA SOLICITUD
// ============================================
function renderStatus(status) {
    const badge = document.getElementById('statusBadge');
    if (!badge) return;
    const cfg = STATUS_MAP[status] || { text: status || 'No disponible', cls: 'badge-pending' };
    badge.textContent = cfg.text;
    badge.className = `badge ${cfg.cls}`;
}

// ============================================
// COMPLETAR CAMPOS DE FIRMA AUTOMÁTICAMENTE
// ============================================
function populateSignatureFields(submission) {
    const today = new Date();
    const months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

    const cityEl = document.getElementById('summaryCity');
    const nameEl = document.getElementById('summaryName');
    const docEl = document.getElementById('summaryDoc');

    document.getElementById('firmaCiudad').textContent = cityEl ? (cityEl.textContent || '_____________') : '_____________';
    document.getElementById('firmaNombre').textContent = nameEl ? (nameEl.textContent || '_________________________') : '_________________________';
    document.getElementById('firmaDocumento').textContent = docEl ? (docEl.textContent || '_________________________') : '_________________________';

    // Separar la firma según el tipo de cliente: Natural o Representante Legal
    const esJuridica = submission && submission.tipo_persona === 'juridica';
    const setText = (id, text) => {
        const el = document.getElementById(id);
        if (el) el.textContent = text;
    };

    setText('signatureTitle', esJuridica
        ? 'FIRMA DEL REPRESENTANTE LEGAL'
        : 'FIRMA PERSONA NATURAL CON ESTABLECIMIENTO DE COMERCIO');
    setText('signatureFirmaLabel', esJuridica ? 'Firma del representante legal:' : 'Firma:');
    setText('signatureNameLabel', esJuridica ? 'Razón social:' : 'Nombres y apellidos:');
    setText('signatureDocLabel', esJuridica ? 'NIT:' : 'No. de documento:');
}

// ============================================
// CARGAR FORMULARIO DE VINCULACIÓN FIRMADO
// ============================================
async function uploadSignedForm(input) {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('❌ No hay sesión activa. Inicia sesión nuevamente.');
        window.location.href = '/login';
        return;
    }
    if (!input.files || input.files.length === 0) return;

    const file = input.files[0];
    if (!/\.(pdf|jpe?g|png)$/i.test(file.name)) {
        alert('❌ Formato no permitido. Use PDF, JPG o PNG.');
        input.value = '';
        return;
    }
    if (file.size > 5 * 1024 * 1024) {
        alert('❌ El archivo excede el límite de 5MB.');
        input.value = '';
        return;
    }

    const id = new URLSearchParams(window.location.search).get('id');
    if (!id) {
        alert('❌ No se encontró la solicitud.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch(`/api/submissions/${id}/upload-form`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error en el servidor');
        }

        input.classList.add('uploaded');
        const msg = document.getElementById('uploadSuccessMessage');
        if (msg) msg.style.display = 'block';
    } catch (error) {
        console.error('Error al subir el formulario firmado:', error);
        alert(`❌ Error al subir el formulario firmado: ${error.message}`);
        input.value = '';
    }
}

// ============================================
// COPIAR AL PORTAPAPELES
// ============================================
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    element.select();
    element.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(element.value).then(() => {
        const button = element.nextElementSibling;
        const originalText = button.textContent;
        button.textContent = '¡Copiado!';
        button.style.background = 'var(--success)';

        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Error al copiar:', err);
        alert('No se pudo copiar al portapapeles');
    });
}

// ============================================
// FORMATEAR FECHA
// ============================================
function formatDate(dateString) {
    if (!dateString) return 'No disponible';

    const date = new Date(dateString);
    return date.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ============================================
// CERRAR SESIÓN
// ============================================
function logout() {
    if (confirm('¿Desea cerrar la sesión?')) {
        localStorage.clear();
        window.location.href = '/login';
    }
}

// ============================================
// EXPORTAR PARA USO GLOBAL
// ============================================
window.copyToClipboard = copyToClipboard;
window.logout = logout;
window.uploadSignedForm = uploadSignedForm;
