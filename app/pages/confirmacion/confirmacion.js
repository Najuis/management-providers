document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const submissionId = urlParams.get('id');
    
    if (!submissionId) {
        document.getElementById('summaryContent').innerHTML = '<p class="error">Error: ID de solicitud no proporcionado.</p>';
        return;
    }

    document.getElementById('submissionId').textContent = submissionId;
    loadSubmissionData(submissionId);
});

async function loadSubmissionData(id) {
    try {
        const res = await fetch(`/api/submissions/${id}`);
        if (!res.ok) throw new Error('No se pudo cargar la solicitud');
        
        const data = await res.json();
        renderSummary(data);
        renderStatus(data);
        
        document.getElementById('displayUsername').value = data.credentials?.username || `tercero_${id.substring(0,6)}`;
        document.getElementById('displayPassword').value = data.credentials?.temp_password || `TempPass_${id.substring(0,4)}`;
        
    } catch (error) {
        console.error(error);
        document.getElementById('summaryContent').innerHTML = '<p class="error">Error al cargar los datos. Contacte al administrador.</p>';
    }
}

function renderSummary(data) {
    const container = document.getElementById('summaryContent');
    const p = data.personal_data || {};
    const f = data.financial_data || {};
    const r = data.risk_assessment || {};
    
    let html = `
        <div class="summary-section">
            <h3>Informacion General</h3>
            <div class="data-row"><strong>Tipo:</strong> ${data.form_type === 'natural' ? 'Persona Natural' : 'Persona Juridica'}</div>
            <div class="data-row"><strong>Cliente:</strong> ${data.client_type}</div>
            <div class="data-row"><strong>Nombre/Razon:</strong> ${p.razonSocial || p.nombres || 'N/A'}</div>
            <div class="data-row"><strong>ID:</strong> ${p.numeroIdentificacion || p.nit || 'N/A'}</div>
        </div>
        <div class="summary-section">
            <h3>Datos Financieros</h3>
            <div class="data-row"><strong>Ingresos:</strong> ${formatCurrency(f.totalIngresos)}</div>
            <div class="data-row"><strong>Egresos:</strong> ${formatCurrency(f.totalEgresos)}</div>
        </div>
        <div class="summary-section">
            <h3>Evaluacion de Riesgo</h3>
            <div class="data-row"><strong>Pais:</strong> ${r.paisRiesgo || 'N/A'}</div>
            <div class="data-row"><strong>Ciudad:</strong> ${r.ciudadRiesgo || 'N/A'}</div>
            <div class="data-row"><strong>CIIU:</strong> ${r.codigoCIIU || 'N/A'}</div>
        </div>
    `;
    container.innerHTML = html;
}

function renderStatus(data) {
    const riskBadge = document.getElementById('riskBadge');
    const risk = data.risk_assessment?.nivel_riesgo || 'MODERADO';
    
    riskBadge.textContent = risk;
    riskBadge.className = `badge badge-${risk.toLowerCase()}`;
}

function formatCurrency(value) {
    if (!value) return '$0';
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value);
}

function copyCredentials() {
    const user = document.getElementById('displayUsername').value;
    const pass = document.getElementById('displayPassword').value;
    const text = `Usuario: ${user}\nContraseña: ${pass}`;
    
    navigator.clipboard.writeText(text).then(() => {
        alert('Credenciales copiadas al portapapeles');
    }).catch(() => {
        alert('Error al copiar. Por favor seleccione y copie manualmente.');
    });
}