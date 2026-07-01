// ============================================
// CONFIGURACIÓN GLOBAL
// ============================================
const API_URL = window.location.origin + '/api';
let authToken = localStorage.getItem('token');
let currentSubmissionId = null;

// Verificar autenticación
if (!authToken) {
    console.warn('No hay token de autenticación');
    window.location.href = '/';
}

// ============================================
// INICIALIZACIÓN
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    loadSubmissions();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('btn-refresh').addEventListener('click', loadSubmissions);
    document.getElementById('status-filter').addEventListener('change', loadSubmissions);
    
    document.getElementById('btn-approve').addEventListener('click', () => processValidation('APROBADO'));
    document.getElementById('btn-reject').addEventListener('click', () => processValidation('RECHAZADO'));
    
    // Cerrar modal al hacer clic fuera
    document.getElementById('review-modal').addEventListener('click', (e) => {
        if (e.target.id === 'review-modal') {
            closeModal();
        }
    });
}

// ============================================
// CARGAR SOLICITUDES (LISTA) valida cion del modo de filtrado Frmula ri Mila===========================================
async function loadSubmissions() {
    const statusFilter = document.getElementById('status-filter').value;
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '<tr><td colspan="6" class="loading">Cargando solicitudes...</td></tr>';

    try {
        // Construir URL con filtros
        let url = `${API_URL}/submissions`;
        const params = new URLSearchParams();
        
        if (statusFilter !== 'all') {
            params.append('status', statusFilter);
        }
        
        if (params.toString()) {
            url += `?${params.toString()}`;
        }

        const response = await fetch(url, {
            headers: { 
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                alert('Sesión expirada. Redirigiendo al login...');
                localStorage.removeItem('token');
                window.location.href = '/';
                return;
            }
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        renderTable(data.submissions || data || []);
        
    } catch (error) {
        console.error('Error al cargar solicitudes:', error);
        tbody.innerHTML = `<tr><td colspan="6" style="color:red; text-align:center; padding:20px;">
            Error cargando solicitudes: ${error.message}<br>
            <small>Verifica que el servidor esté corriendo y los endpoints existan.</small>
        </td></tr>`;
    }
}

// ============================================
// RENDERIZAR TABLA
// ============================================
function renderTable(submissions) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    if (!submissions || submissions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:20px; color:#7f8c8d;">No hay solicitudes encontradas.</td></tr>';
        return;
    }

    submissions.forEach(sub => {
        const tr = document.createElement('tr');
        
        // Formatear fecha
        const fecha = sub.submitted_at || sub.created_at;
        const fechaFormateada = fecha ? new Date(fecha).toLocaleDateString('es-CO') : 'N/A';
        
        // Nombre del usuario
        const nombre = sub.nombres && sub.apellidos 
            ? `${sub.nombres} ${sub.apellidos}`
            : sub.razon_social || `Usuario ID: ${sub.user_id || 'N/A'}`;
        
        // Badges con clases correctas
        const statusBadge = getStatusBadge(sub.status);
        const riskBadge = getRiskBadge(sub.risk_level);
        
        tr.innerHTML = `
            <td><strong>#${sub.id}</strong></td>
            <td>${nombre}</td>
            <td>${fechaFormateada}</td>
            <td>${riskBadge}</td>
            <td>${statusBadge}</td>
            <td>
                <button class="btn-action" onclick="openReviewModal(${sub.id})">
                    <i class="fas fa-eye"></i> Revisar
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    }); // ✅ CORREGIDO: Cerrar forEach correctamente
} // ✅ CORREGIDO: Cerrar función renderTable

// ============================================
// FUNCIONES AUXILIARES PARA BADGES
// ============================================
function getStatusBadge(status) {
    if (!status) return '<span class="badge badge-pendiente">Desconocido</span>';
    
    const statusMap = {
        'borrador': { class: 'badge-pendiente', text: 'Borrador' },
        'pendiente_revision': { class: 'badge-pendiente', text: 'Pendiente' },
        'en_revision': { class: 'badge-pendiente', text: 'En Revisión' },
        'aprobado': { class: 'badge-aprobado', text: 'Aprobado' },
        'rechazado': { class: 'badge-rechazado', text: 'Rechazado' },
        'completado': { class: 'badge-aprobado', text: 'Completado' }
    };
    
    const config = statusMap[status.toLowerCase()] || { class: 'badge-pendiente', text: status };
    return `<span class="badge ${config.class}">${config.text}</span>`;
}

function getRiskBadge(riskLevel) {
    if (!riskLevel) return '<span class="badge badge-bajo">No evaluado</span>';
    
    const riskMap = {
        'bajo': { class: 'badge-bajo', text: 'Bajo' },
        'medio': { class: 'badge-medio', text: 'Medio' },
        'alto': { class: 'badge-alto', text: 'Alto' },
        'extremo': { class: 'badge-extremo', text: 'Extremo' }
    };
    
    const config = riskMap[riskLevel.toLowerCase()] || { class: 'badge-bajo', text: riskLevel };
    return `<span class="badge ${config.class}">${config.text}</span>`;
}

// ============================================
// MODAL DE REVISIÓN
// ============================================
window.openReviewModal = async (id) => {
    currentSubmissionId = id;
    const modal = document.getElementById('review-modal');
    document.getElementById('modal-submission-id').textContent = id;
    
    // Limpiar campos
    document.getElementById('audit-comments').value = '';
    document.getElementById('documents-list').innerHTML = '<p style="color:#7f8c8d;">Cargando documentos...</p>';
    document.getElementById('applicant-details').innerHTML = '<p style="color:#7f8c8d;">Cargando detalles...</p>';
    document.getElementById('pdf-viewer').src = '';
    document.getElementById('direct-pdf-link').href = '#';

    modal.classList.remove('hidden');

    try {
        // Cargar detalles específicos
        const response = await fetch(`${API_URL}/submissions/${id}`, {
            headers: { 
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Renderizar detalles del solicitante
        renderApplicantDetails(data);
        
        // Renderizar documentos
        renderDocumentsList(data.documents || []);
        
        // Cargar PDF en iframe
        const pdfUrl = `${API_URL}/submissions/${id}/download-pdf`;
        document.getElementById('pdf-viewer').src = pdfUrl;
        document.getElementById('direct-pdf-link').href = pdfUrl;
        
    } catch (error) {
        console.error('Error al cargar detalles:', error);
        document.getElementById('applicant-details').innerHTML = `
            <p style="color:red;">Error cargando detalles: ${error.message}</p>
        `;
    }
};

function renderApplicantDetails(submission) {
    const detailsDiv = document.getElementById('applicant-details');
    
    const isNatural = submission.tipo_persona === 'natural';
    const nombre = isNatural 
        ? `${submission.nombres || ''} ${submission.apellidos || ''}`.trim()
        : submission.razon_social || 'N/A';
    
    detailsDiv.innerHTML = `
        <p><strong>Nombre/Razón Social:</strong> ${nombre}</p>
        <p><strong>Tipo de Persona:</strong> ${isNatural ? 'Natural' : 'Jurídica'}</p>
        <p><strong>Tipo de ID:</strong> ${submission.tipo_id || 'N/A'}</p>
        <p><strong>Número de ID:</strong> ${submission.numero_id || 'N/A'}</p>
        <p><strong>Código CIIU:</strong> ${submission.codigo_ciiu || 'N/A'}</p>
        <p><strong>Régimen Tributario:</strong> ${submission.regimen_tributario || 'N/A'}</p>
        <p><strong>Nivel de Riesgo:</strong> ${getRiskBadge(submission.risk_level)}</p>
        <p><strong>Estado Actual:</strong> ${getStatusBadge(submission.status)}</p>
        <p><strong>Fecha de Envío:</strong> ${submission.submitted_at ? new Date(submission.submitted_at).toLocaleString('es-CO') : 'No enviada'}</p>
        ${submission.observations ? `<p><strong>Observaciones:</strong> ${submission.observations}</p>` : ''}
    `;
}

function renderDocumentsList(documents) {
    const docsDiv = document.getElementById('documents-list');
    
    if (!documents || documents.length === 0) {
        docsDiv.innerHTML = '<p style="color:#7f8c8d;">No hay documentos adjuntos</p>';
        return;
    }
    
    docsDiv.innerHTML = documents.map(doc => `
        <a href="${doc.file_path}" target="_blank" download style="display:block; margin-bottom:8px; padding:10px; background:white; border:1px solid #dcdde1; border-radius:5px; text-decoration:none; color:#3498db; transition:all 0.2s;">
            <i class="fas fa-file-pdf"></i> ${doc.file_name}
            <span style="float:right;"><i class="fas fa-download"></i></span>
        </a>
    `).join('');
}

window.closeModal = () => {
    document.getElementById('review-modal').classList.add('hidden');
    currentSubmissionId = null;
};

// ============================================
// PROCESAR VALIDACIÓN (APROBAR/RECHAZAR)
// ============================================
async function processValidation(action) {
    if (!currentSubmissionId) {
        alert('No hay solicitud seleccionada');
        return;
    }
    
    const comments = document.getElementById('audit-comments').value.trim();
    
    if (!comments) {
        alert('Por favor, escribe tus observaciones antes de continuar');
        return;
    }
    
    const confirmMsg = action === 'APROBADO' 
        ? '¿Estás seguro de APROBAR esta solicitud?' 
        : '¿Estás seguro de RECHAZAR esta solicitud?';
    
    if (!confirm(confirmMsg)) return;

    try {
        // Enviar como query parameters (como espera el backend)
        const url = `${API_URL}/submissions/${currentSubmissionId}/validate?action=${action}&comments=${encodeURIComponent(comments)}`;
        
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.message || `Solicitud ${action.toLowerCase()} exitosamente.`);
            closeModal();
            loadSubmissions(); // Recargar tabla
        } else {
            const err = await response.json();
            alert(`Error: ${err.detail || 'Error al procesar la validación'}`);
        }
    } catch (error) {
        alert('Error de conexión al validar.');
        console.error('Error en validación:', error);
    }
}