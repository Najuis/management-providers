document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Inicializando formulario de usuario...');
    initializeUserForm();
});

function initializeUserForm() {
    loadUserProfile();
    loadReferenceData();
    bindFormEvents();
    
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
}

async function loadUserProfile() {
    try {
        // 1. Verificar si el token existe
        const token = localStorage.getItem('token');
        console.log('🔑 Token encontrado:', token ? 'SÍ' : 'NO');
        
        if (!token) {
            console.warn('⚠️ No hay token. Redirigiendo al login...');
            window.location.href = '/login';
            return;
        }

        // 2. Hacer la petición con el token
        console.log('📡 Solicitando perfil al backend...');
        const res = await fetch('/api/user/profile', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        console.log('📥 Respuesta del perfil:', res.status, res.statusText);

        if (res.status === 401) {
            console.error('❌ Token inválido o expirado (401).');
            localStorage.removeItem('token');
            window.location.href = '/login';
            return;
        }

        if (!res.ok) {
            throw new Error(`Error ${res.status}: ${res.statusText}`);
        }
        
        const profile = await res.json();
        console.log('✅ Perfil cargado:', profile);
        
        // 3. Actualizar la interfaz
        const nombre = profile.name || profile.email.split('@')[0];
        const greetingEl = document.getElementById('userGreeting');
        if (greetingEl) {
            greetingEl.textContent = `Tercero: ${nombre}`;
        }
        
        localStorage.setItem('current_user_id', profile.id_user);
        localStorage.setItem('current_user_type', profile.type_user_id);
        
        applyUserTypeLayout(profile.type_user_id);
        
    } catch (error) {
        console.error('💥 Error crítico en loadUserProfile:', error);
        showMessage('Error al cargar perfil. Inicie sesión nuevamente.', 'error');
        setTimeout(() => {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }, 3000);
    }
}

function applyUserTypeLayout(typeId) {
    console.log('🎨 Aplicando layout para tipo de usuario:', typeId);
    const naturalDiv = document.getElementById('naturalFields');
    const juridicaDiv = document.getElementById('juridicaFields');
    
    if (typeId === 1) {
        if (naturalDiv) {
            naturalDiv.classList.remove('hidden');
            setRequiredFields(naturalDiv, true);
        }
    } else if (typeId === 2) {
        if (juridicaDiv) {
            juridicaDiv.classList.remove('hidden');
            setRequiredFields(juridicaDiv, true);
        }
        document.querySelectorAll('.juridica-only').forEach(el => {
            if (el) el.classList.remove('hidden');
        });
    }
}

function setRequiredFields(container, required) {
    if (!container) return;
    container.querySelectorAll('input, select, textarea').forEach(el => {
        if (required) el.setAttribute('required', '');
        else el.removeAttribute('required');
    });
}

async function loadReferenceData() {
    try {
        console.log('📚 Cargando datos de referencia...');
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        
        const [citiesRes, officesRes, ciiuRes, countriesRes] = await Promise.all([
            fetch('/api/cities', { headers }),
            fetch('/api/offices', { headers }),
            fetch('/api/ciiu', { headers }),
            fetch('/api/countries', { headers })
        ]);

        const citiesData = (await citiesRes.json()).message || [];
        const officesData = (await officesRes.json()).message || [];
        const ciiuData = (await ciiuRes.json()).message || (await ciiuRes.json()) || [];
        const countriesData = (await countriesRes.json()).message || [];

        console.log('📊 Datos cargados:', { 
            ciudades: citiesData.length, 
            oficinas: officesData.length, 
            ciiu: ciiuData.length, 
            paises: countriesData.length 
        });

        populateSelect('ciudad', citiesData.map(c => ({ value: c.id_city || c.codigo, text: c.name || c.nombre_municipio })));
        populateSelect('oficina', officesData.map(o => ({ value: o.id_office || o.id, text: o.office_name || o.nombre_oficina || o.name })));
        populateSelect('codigoCIIU', ciiuData.map(c => ({ value: c.codigo, text: `${c.codigo} - ${c.descripcion}` })));
        populateSelect('paisOrigen', countriesData.map(c => ({ value: c.id_country || c.codigo_iso, text: c.country_name || c.nombre_pais })));
        populateSelect('paisResidencia', countriesData.map(c => ({ value: c.id_country || c.codigo_iso, text: c.country_name || c.nombre_pais })));
    } catch (error) {
        console.error('💥 Error cargando directorios:', error);
    }
}

function populateSelect(elementId, options) {
    const select = document.getElementById(elementId);
    if (!select) return;
    
    while (select.options.length > 1) {
        select.remove(1);
    }

    options.forEach(opt => {
        const el = document.createElement('option');
        el.value = opt.value;
        el.textContent = opt.text;
        select.appendChild(el);
    });
}

function bindFormEvents() {
    const form = document.getElementById('vinculacionForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
    
    const ciiuSelect = document.getElementById('codigoCIIU');
    if (ciiuSelect) {
        ciiuSelect.addEventListener('change', (e) => {
            const text = e.target.options[e.target.selectedIndex].text;
            const actividadInput = document.getElementById('actividadEconomica');
            if (actividadInput) actividadInput.value = text;
            calculateRisk();
        });
    }

    ['paisOrigen', 'paisResidencia', 'ciudad'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', calculateRisk);
    });
}

function calculateRisk() {
    const pais = document.getElementById('paisOrigen')?.value;
    const ciudad = document.getElementById('ciudad')?.value;
    const ciiu = document.getElementById('codigoCIIU')?.value;
    
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
    
    if (riskScore >= 0.75) { level = 'EXTREMO'; className = 'risk-extreme'; if(eddSection) eddSection.classList.remove('hidden'); }
    else if (riskScore >= 0.5) { level = 'ALTO'; className = 'risk-high'; if(eddSection) eddSection.classList.remove('hidden'); }
    else if (riskScore >= 0.25) { level = 'MODERADO'; className = 'risk-moderate'; if(eddSection) eddSection.classList.add('hidden'); }
    else { if(eddSection) eddSection.classList.add('hidden'); }

    if (riskAlert) {
        riskAlert.className = `risk-indicator ${className}`;
        riskAlert.textContent = `Nivel de Riesgo Estimado: ${level}. ${level === 'ALTO' || level === 'EXTREMO' ? 'Se requiere Debida Diligencia Ampliada.' : ''}`;
        riskAlert.classList.remove('hidden');
    }
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
        const token = localStorage.getItem('token');
        const formData = new FormData(form);
        const jsonData = Object.fromEntries(formData.entries());

        const payload = {
            fecha: jsonData.fecha || new Date().toISOString().split('T')[0],
            tipo_cliente: jsonData.tipoCliente || 'Nuevo',
            tipo_vinculacion: jsonData.tipoVinculacion || 'Proveedor',
            ciudad_id: parseInt(jsonData.ciudad) || 0,
            oficina: jsonData.oficina || 'Principal',
            tipo_persona: form.querySelector('input[name="tipoPersona"]:checked')?.value || 'natural',
            nombres: jsonData.nombres || '',
            apellidos: jsonData.apellidos || '',
            razon_social: jsonData.razonSocial || '',
            tipo_id: jsonData.tipoIdNatural || jsonData.tipoId || 'CC',
            numero_id: jsonData.numeroDocNatural || jsonData.numeroId || jsonData.nit || '',
            fecha_expedicion: jsonData.fechaExpNatural || jsonData.fechaExpedicion || null,
            estructura_juridica: jsonData.estructuraJuridica || '',
            codigo_ciiu: jsonData.codigoCIIU || '',
            pais_origen_id: parseInt(jsonData.paisOrigen) || 0,
            pais_residencia_id: parseInt(jsonData.paisResidencia) || 0,
            zona: jsonData.zona || 'Nacional',
            regimen_tributario: jsonData.regimenTributario || 'Común',
            total_ingresos: parseFloat(jsonData.totalIngresos) || 0,
            total_egresos: parseFloat(jsonData.totalEgresos) || 0,
            aut_datos: jsonData.aut_datos === 'on',
            aut_laft: jsonData.aut_laft === 'on',
            aut_anticorrupcion: jsonData.aut_anticorrupcion === 'on',
            aut_etica: jsonData.aut_etica === 'on'
        };

        console.log('📤 Enviando payload:', payload);

        const res = await fetch('/api/submissions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await res.json();
        console.log('📥 Respuesta del envío:', res.status, result);
        
        if (!res.ok) {
            throw new Error(result.detail || 'Error al enviar la solicitud');
        }

        showMessage('Solicitud enviada exitosamente. Redirigiendo a confirmación...', 'success');
        setTimeout(() => {
            window.location.href = `/admin/confirmacion?id=${result.submission_id}`;
        }, 2000);
    } catch (error) {
        console.error('💥 Error en handleFormSubmit:', error);
        showMessage(error.message || 'Ocurrió un error al enviar el formulario', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Enviar Solicitud de Vinculación';
    }
}

function handleLogout() {
    console.log('🚪 Cerrando sesión...');
    localStorage.removeItem('token');
    localStorage.removeItem('type_user');
    localStorage.removeItem('user_session_id');
    localStorage.removeItem('current_user_id');
    localStorage.removeItem('current_user_type');
    window.location.href = '/login';
}

function showMessage(text, type) {
    const container = document.getElementById('messageContainer');
    if (container) {
        container.textContent = text;
        container.className = `message-container ${type}`;
    } else {
        alert(text);
    }
}