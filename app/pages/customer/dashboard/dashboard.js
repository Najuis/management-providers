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
                renderFullForm(submission);
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
// FORMULARIO COMPLETO PARA IMPRIMIR
// ============================================
function renderFullForm(submission) {
    const container = document.getElementById('fullFormContent');
    if (!container) return;
    const f = (submission && submission.form_data) || {};
    const esJuridica = submission && submission.tipo_persona === 'juridica';

    const siNo = v => (v ? 'SÍ' : 'NO');
    const texto = v => (v === null || v === undefined || v === '' ? 'N/A' : v);
    const espe = (id, label, fn) => {
        const v = f[id];
        if (v === null || v === undefined || v === '' || (Array.isArray(v) && v.length === 0)) return '';
        const valor = fn ? fn(v) : v;
        return `<div class="ff-row"><span class="ff-label">${label}:</span><span class="ff-value">${texto(valor)}</span></div>`;
    };

    const money = v => {
        const n = parseFloat(v);
        if (isNaN(n)) return v;
        return n.toLocaleString('es-CO', { maximumFractionDigits: 2 });
    };

    const block = (title, inner) =>
        `<div class="ff-block"><h4>${title}</h4><div class="ff-grid">${inner}</div></div>`;

    let html = '';

    // 1. Información general
    html += block('1. Información General',
        espe('fecha', 'Fecha', v => v.split('T')[0]) +
        espe('tipo_cliente', 'Tipo de cliente', v => v === 'Juridica' ? 'Persona Jurídica' : 'Persona Natural') +
        espe('tipo_vinculacion', 'Tipo de vinculación') +
        espe('ciudad_nombre', 'Ciudad') +
        espe('oficina', 'Oficina/Sucursal'));

    // 2. Identificación
    if (esJuridica) {
        html += block('2. Información de Identificación (Persona Jurídica)',
            espe('razon_social', 'Razón social') +
            espe('nit', 'NIT') +
            espe('digito_verificacion', 'Dígito de verificación') +
            espe('fecha_constitucion', 'Fecha de constitución') +
            espe('tipo_sociedad', 'Tipo de sociedad') +
            espe('otro_tipo_sociedad', 'Otro tipo de sociedad') +
            espe('direccion_juridica', 'Dirección') +
            espe('ciudad_juridica', 'Ciudad') +
            espe('departamento_juridica', 'Departamento') +
            espe('pagina_web', 'Página web'));
    } else {
        html += block('2. Información de Identificación (Persona Natural)',
            espe('nombres', 'Nombres') +
            espe('apellidos', 'Apellidos') +
            espe('tipo_doc_natural', 'Tipo de documento') +
            espe('numero_doc_natural', 'Número de documento') +
            espe('fecha_nacimiento', 'Fecha de nacimiento') +
            espe('fecha_exp_natural', 'Fecha de expedición') +
            espe('direccion_natural', 'Dirección') +
            espe('ciudad_natural', 'Ciudad') +
            espe('departamento_natural', 'Departamento') +
            espe('correo_natural', 'Correo electrónico') +
            espe('telefono_natural', 'Teléfono/Celular') +
            espe('nombre_establecimiento', 'Nombre del establecimiento comercial') +
            espe('nit_establecimiento', 'NIT del establecimiento'));
    }

    // 3. Representantes legales (solo jurídica)
    if (esJuridica) {
        html += block('3. Representantes Legales',
            espe('representante_legal', 'Representante legal') +
            espe('tipo_doc_rep', 'Tipo de documento del representante') +
            espe('numero_doc_rep', 'Número de documento del representante') +
            espe('representante_suplente', 'Representante suplente') +
            espe('tipo_doc_suplente', 'Tipo de documento del suplente') +
            espe('numero_doc_suplente', 'Número de documento del suplente'));
    }

    // 4. Beneficiarios finales
    const bf = (f.beneficiarios || []).map((b, i) =>
        `<h5>Beneficiario final ${i + 1}</h5>` +
        `<div class="ff-row"><span class="ff-label">Nombre:</span><span class="ff-value">${texto(b.nombre)}</span></div>` +
        `<div class="ff-row"><span class="ff-label">Tipo de documento:</span><span class="ff-value">${texto(b.tipo_doc)}</span></div>` +
        `<div class="ff-row"><span class="ff-label">Número de documento:</span><span class="ff-value">${texto(b.numero_doc)}</span></div>`
    ).join('');
    if (bf) html += block('4. Beneficiarios Finales', bf);

    // 5. Composición accionaria
    const acc = (f.accionistas || []).map(a =>
        `<h5>Accionista ${a.numero}</h5>` +
        `<div class="ff-row"><span class="ff-label">Nombre o razón social:</span><span class="ff-value">${texto(a.nombre)}</span></div>` +
        `<div class="ff-row"><span class="ff-label">Participación:</span><span class="ff-value">${texto(a.participacion)}%</span></div>` +
        `<div class="ff-row"><span class="ff-label">Tipo de documento:</span><span class="ff-value">${texto(a.tipo_doc)}</span></div>` +
        `<div class="ff-row"><span class="ff-label">Número de documento:</span><span class="ff-value">${texto(a.numero_doc)}</span></div>` +
        `<div class="ff-row"><span class="ff-label">Dirección:</span><span class="ff-value">${texto(a.direccion)}</span></div>` +
        `<div class="ff-row"><span class="ff-label">Teléfono:</span><span class="ff-value">${texto(a.telefono)}</span></div>`
    ).join('');
    if (acc) html += block('5. Composición Accionaria', acc);

    // 6. Actividad económica
    html += block('6. Actividad Económica',
        espe('codigo_ciiu', 'Código CIIU') +
        espe('actividad_economica', 'Actividad económica'));

    // 7. Referencias bancarias
    const banc1 = espe('banco1_nombre', 'Banco') + espe('banco1_titular', 'Titular') +
        espe('banco1_tipo_cuenta', 'Tipo de cuenta') + espe('banco1_numero', 'Número de cuenta');
    const banc2 = espe('banco2_nombre', 'Banco') + espe('banco2_titular', 'Titular') +
        espe('banco2_tipo_cuenta', 'Tipo de cuenta') + espe('banco2_numero', 'Número de cuenta');
    html += block('7. Referencias Bancarias',
        (banc1 ? `<h5>Referencia bancaria 1</h5>${banc1}` : '') +
        (banc2 ? `<h5>Referencia bancaria 2</h5>${banc2}` : ''));

    // 8. Referencias comerciales
    const rc1 = espe('refcom1_empresa', 'Empresa') + espe('refcom1_contacto', 'Contacto') +
        espe('refcom1_telefono', 'Teléfono') + espe('refcom1_correo', 'Correo');
    const rc2 = espe('refcom2_empresa', 'Empresa') + espe('refcom2_contacto', 'Contacto') +
        espe('refcom2_telefono', 'Teléfono') + espe('refcom2_correo', 'Correo');
    html += block('8. Referencias Comerciales',
        (rc1 ? `<h5>Referencia comercial 1</h5>${rc1}` : '') +
        (rc2 ? `<h5>Referencia comercial 2</h5>${rc2}` : ''));

    // 9. Información financiera y tributaria
    html += block('9. Información Financiera y Tributaria',
        espe('regimen_tributario', 'Régimen tributario') +
        espe('total_ingresos', 'Total ingresos', money) +
        espe('total_egresos', 'Total egresos', money) +
        espe('total_activos', 'Total activos', money) +
        espe('total_pasivos', 'Total pasivos', money) +
        espe('total_patrimonio', 'Total patrimonio neto', money));

    // 10. Declaración PEP
    html += block('10. Declaración de Personas Expuestas Políticamente (PEP)',
        espe('maneja_recursos_publicos', '¿Maneja recursos públicos?', v => v === 'Si' ? 'SÍ' : v === 'No' ? 'NO' : v) +
        espe('ejerce_poder_publico', '¿Ejerce poder público?', v => v === 'Si' ? 'SÍ' : v === 'No' ? 'NO' : v) +
        espe('reconocimiento_publico', '¿Tiene reconocimiento público?', v => v === 'Si' ? 'SÍ' : v === 'No' ? 'NO' : v) +
        espe('vinculo_pep', '¿Vínculo con una PEP?', v => v === 'Si' ? 'SÍ' : v === 'No' ? 'NO' : v) +
        espe('cargo_pep', 'Cargo desempeñado') +
        espe('entidad_pep', 'Entidad') +
        espe('fecha_pep', 'Fecha de vinculación/desvinculación'));

    // 11. Autorizaciones
    html += block('11. Autorizaciones y Declaraciones',
        espe('aut_datos', 'Autorización de datos', siNo) +
        espe('aut_laft', 'Autorización LA/FT', siNo) +
        espe('aut_anticorrupcion', 'Autorización anticorrupción', siNo) +
        espe('aut_conflicto_interes', 'Autorización conflicto de interés', siNo) +
        espe('aut_transparencia', 'Autorización de transparencia', siNo) +
        espe('aut_origen_recursos', 'Autorización origen de recursos', siNo) +
        espe('aut_listas_restrictivas', 'Autorización listas restrictivas', siNo) +
        espe('aut_aceptacion', 'Aceptación final', siNo));

    container.innerHTML = html || '<p class="info-text">No se encontraron datos del formulario.</p>';
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
        ? 'REPRESENTANTE LEGAL'
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
    if (!/\.pdf$/i.test(file.name)) {
        alert('❌ Solo se permiten archivos en formato PDF.');
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
