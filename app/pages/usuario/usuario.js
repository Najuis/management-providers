document.addEventListener('DOMContentLoaded', () => {
    initializeUserForm();
});

function initializeUserForm() {
    loadUserProfile();
    loadReferenceData();
    bindFormEvents();
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
}

async function loadUserProfile() {
    try {
        const res = await fetch('/api/user/profile', { credentials: 'include' });
        if (!res.ok) throw new Error('No se pudo cargar el perfil');
        
        const profile = await res.json();
        document.getElementById('userGreeting').textContent = `Tercero: ${profile.name || profile.email}`;
        
        const userType = profile.type_user_id;
        applyUserTypeLayout(userType);
    } catch (error) {
        console.error(error);
        showMessage('Error al cargar perfil. Inicie sesión nuevamente.', 'error');
        setTimeout(() => window.location.href = '/login', 3000);
    }
}

function applyUserTypeLayout(typeId) {
    const naturalDiv = document.getElementById('naturalFields');
    const juridicaDiv = document.getElementById('juridicaFields');
    
    if (typeId === 1) {
        naturalDiv.classList.remove('hidden');
        setRequiredFields(naturalDiv, true);
    } else if (typeId === 2) {
        juridicaDiv.classList.remove('hidden');
        setRequiredFields(juridicaDiv, true);
        document.querySelectorAll('.juridica-only').forEach(el => el.classList.remove('hidden'));
    }
}

function setRequiredFields(container, required) {
    container.querySelectorAll('input, select, textarea').forEach(el => {
        if (required) el.setAttribute('required', '');
        else el.removeAttribute('required');
    });
}

async function loadReferenceData() {
    try {
        const [citiesRes, officesRes, ciiuRes, countriesRes] = await Promise.all([
            fetch('/api/cities'),
            fetch('/api/offices'),
            fetch('/api/ciiu'),
            fetch('/api/countries')
        ]);

        const [cities, offices, ciiu, countries] = await Promise.all([
            citiesRes.json(),
            officesRes.json(),
            ciiuRes.json(),
            countriesRes.json()
        ]);

        populateSelect('ciudad', cities.map(c => ({ value: c.codigo, text: c.nombre_municipio })));
        populateSelect('oficina', offices.map(o => ({ value: o.id, text: o.nombre_oficina || o.name })));
        populateSelect('codigoCIIU', ciiu.map(c => ({ value: c.codigo, text: `${c.codigo} - ${c.descripcion}` })));
        populateSelect('paisOrigen', countries.map(c => ({ value: c.codigo_iso, text: c.nombre_pais })));
        populateSelect('paisResidencia', countries.map(c => ({ value: c.codigo_iso, text: c.nombre_pais })));
    } catch (error) {
        console.error('Error cargando directorios:', error);
    }
}

function populateSelect(elementId, options) {
    const select = document.getElementById(elementId);
    if (!select) return;
    options.forEach(opt => {
        const el = document.createElement('option');
        el.value = opt.value;
        el.textContent = opt.text;
        select.appendChild(el);
    });
}

function bindFormEvents() {
    document.getElementById('vinculacionForm').addEventListener('submit', handleFormSubmit);
    
    document.getElementById('codigoCIIU').addEventListener('change', (e) => {
        const select = e.target;
        const text = select.options[select.selectedIndex].text;
        document.getElementById('actividadEconomica').value = text;
        calculateRisk();
    });

    ['paisOrigen', 'paisResidencia', 'ciudad'].forEach(id => {
        document.getElementById(id)?.addEventListener('change', calculateRisk);
    });
}

function calculateRisk() {
    const pais = document.getElementById('paisOrigen').value;
    const ciudad = document.getElementById('ciudad').value;
    const ciiu = document.getElementById('codigoCIIU').value;
    
    if (!pais || !ciudad || !ciiu) return;

    const riskAlert = document.getElementById('riskAlert');
    const eddSection = document.getElementById('eddSection');
    
    let riskScore = 0;
    if (['SY','SDN','KP','IR','CU','YE','HT','AF','GW'].includes(pais)) riskScore = 1;
    else if (['KY','SO','SS','VE','LY','CD','BI','IQ'].includes(pais)) riskScore = 0.75;
    else if (['CO','MX','PE','AR','CL'].includes(pais)) riskScore = 0.375;
    else riskScore = 0.125;

    let level = 'BAJO';
    let className = 'risk-low';
    if (riskScore >= 0.75) { level = 'EXTREMO'; className = 'risk-extreme'; eddSection.classList.remove('hidden'); }
    else if (riskScore >= 0.5) { level = 'ALTO'; className = 'risk-high'; eddSection.classList.remove('hidden'); }
    else if (riskScore >= 0.25) { level = 'MODERADO'; className = 'risk-moderate'; eddSection.classList.add('hidden'); }
    else { eddSection.classList.add('hidden'); }

    riskAlert.className = `risk-indicator ${className}`;
    riskAlert.textContent = `Nivel de Riesgo Estimado: ${level}. ${level === 'ALTO' || level === 'EXTREMO' ? 'Se requiere Debida Diligencia Ampliada.' : ''}`;
    riskAlert.classList.remove('hidden');
}

async function handleFormSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = document.getElementById('submitBtn');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Procesando solicitud...';

    try {
        const formData = new FormData(form);
        const sessionId = localStorage.getItem('user_session_id') || '';
        formData.append('session_id', sessionId);

        const res = await fetch('/api/submissions', {
            method: 'POST',
            body: formData
        });

        const result = await res.json();
        if (!res.ok) throw new Error(result.detail || 'Error al enviar');

        showMessage('Solicitud enviada exitosamente. Redirigiendo a confirmación...', 'success');
        setTimeout(() => {
            window.location.href = `/confirmacion?id=${result.submission_id}`;
        }, 2000);
    } catch (error) {
        console.error(error);
        showMessage(error.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Enviar Solicitud de Vinculación';
    }
}

function handleLogout() {
    fetch('/api/auth/logout', { method: 'POST', credentials: 'include' })
        .then(() => {
            localStorage.removeItem('user_session_id');
            window.location.href = '/login';
        })
        .catch(() => window.location.href = '/login');
}

function showMessage(text, type) {
    const container = document.getElementById('messageContainer');
    container.textContent = text;
    container.className = `message-container ${type}`;
}