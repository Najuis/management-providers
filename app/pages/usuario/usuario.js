// Datos de oficinas y CIIU (se cargarán desde el backend)
let oficinasData = [];
let ciiuData = [];
let ciudadesData = [];

document.addEventListener('DOMContentLoaded', () => {
    console.log('📝 Formulario de usuario cargado');
    initializeUserForm();
});

function initializeUserForm() {
    // 1. Cargar fecha actual automáticamente
    const fechaInput = document.getElementById('fecha');
    if (fechaInput) {
        fechaInput.valueAsDate = new Date();
    }
    
    // 2. Intentar cargar el perfil, pero NO redirigir si falla
    loadUserProfile().catch(err => {
        console.warn('⚠️ No se pudo cargar el perfil, pero continuamos:', err);
    });
    
    // 3. Cargar datos de referencia
    loadReferenceData();
    loadOficinas();
    loadCIIU();
    
    // 4. Bind de eventos
    bindFormEvents();
    
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
}

async function loadUserProfile() {
    try {
        const token = localStorage.getItem('token');
        const greetingEl = document.getElementById('userGreeting');
        
        if (!token) {
            console.warn('⚠️ No hay token almacenado');
            if (greetingEl) greetingEl.textContent = 'Usuario no autenticado';
            return; // NO redirigir
        }
        
        console.log('📡 Cargando perfil de usuario...');
        const res = await fetch('/api/user/profile', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (res.status === 401) {
            console.error('❌ Token inválido o expirado');
            if (greetingEl) greetingEl.textContent = 'Sesión expirada (Inicie sesión nuevamente)';
            return; // NO redirigir automáticamente
        }
        
        if (!res.ok) {
            throw new Error(`Error ${res.status}: ${res.statusText}`);
        }
        
        const profile = await res.json();
        console.log('✅ Perfil cargado:', profile);
        
        if (greetingEl) {
            const nombre = profile.name || profile.email?.split('@')[0] || 'Usuario';
            greetingEl.textContent = `Tercero: ${nombre}`;
        }
        
        localStorage.setItem('current_user_id', profile.id_user);
        localStorage.setItem('current_user_type', profile.type_user_id);
        
        applyUserTypeLayout(profile.type_user_id);
        
    } catch (error) {
        console.error('💥 Error en loadUserProfile:', error);
        const greetingEl = document.getElementById('userGreeting');
        if (greetingEl) {
            greetingEl.textContent = 'Perfil no disponible';
        }
    }
}

function applyUserTypeLayout(typeId) {
    console.log('🎨 Aplicando layout para typeId:', typeId);
    // Aquí puedes agregar lógica si necesitas mostrar/ocultar campos según el tipo de usuario
}

// Función para manejar el cambio de Tipo de Cliente (Mayoreo/Institucional)
function onTipoClienteChange() {
    const tipoCliente = document.getElementById('tipoCliente').value;
    const naturalFields = document.getElementById('personaNaturalFields');
    const juridicaFields = document.getElementById('personaJuridicaFields');
    
    if (tipoCliente === 'Mayoreo') {
        // Mayoreo puede ser natural o jurídica, mostramos ambas o la que elija el usuario
        if (naturalFields) naturalFields.style.display = 'block';
        if (juridicaFields) juridicaFields.style.display = 'block';
    } else if (tipoCliente === 'Institucional') {
        // Institucional es siempre Persona Jurídica
        if (naturalFields) naturalFields.style.display = 'none';
        if (juridicaFields) juridicaFields.style.display = 'block';
    }
}

async function loadReferenceData() {
    try {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        
        const [citiesRes, countriesRes] = await Promise.all([
            fetch('/api/cities', { headers }),
            fetch('/api/countries', { headers })
        ]);

        ciudadesData = (await citiesRes.json()).message || [];
        const countriesData = (await countriesRes.json()).message || [];
        
        // Llenar select de ciudades
        const ciudadSelect = document.getElementById('ciudad');
        if (ciudadSelect) {
            ciudadSelect.innerHTML = '<option value="">Seleccione...</option>';
            ciudadesData.forEach(c => {
                const option = document.createElement('option');
                option.value = c.id_city || c.codigo;
                option.textContent = c.name || c.nombre_municipio || c.ciudad;
                ciudadSelect.appendChild(option);
            });
        }
        
        // Llenar select de países
        const paisOrigenSelect = document.getElementById('paisOrigen');
        const paisResidenciaSelect = document.getElementById('paisResidencia');
        
        if (paisOrigenSelect) {
            paisOrigenSelect.innerHTML = '<option value="">Seleccione...</option>';
            countriesData.forEach(c => {
                const option = document.createElement('option');
                option.value = c.id_country || c.codigo_iso;
                option.textContent = c.country_name || c.nombre_pais;
                paisOrigenSelect.appendChild(option);
            });
        }
        
        if (paisResidenciaSelect) {
            paisResidenciaSelect.innerHTML = '<option value="">Seleccione...</option>';
            countriesData.forEach(c => {
                const option = document.createElement('option');
                option.value = c.id_country || c.codigo_iso;
                option.textContent = c.country_name || c.nombre_pais;
                paisResidenciaSelect.appendChild(option);
            });
        }
        
    } catch (error) {
        console.error('💥 Error cargando directorios:', error);
    }
}

async function loadOficinas() {
    try {
        const response = await fetch('/api/oficinas');
        if (response.ok) {
            const data = await response.json();
            oficinasData = data || [];
            
            const ciudadSelect = document.getElementById('ciudad');
            if (ciudadSelect) {
                ciudadSelect.addEventListener('change', onCiudadChange);
            }
        }
    } catch (error) {
        console.error('Error cargando oficinas:', error);
    }
}

async function loadCIIU() {
    try {
        const response = await fetch('/api/ciiu');
        if (response.ok) {
            const data = await response.json();
            ciiuData = data || [];
            
            const ciiuSelect = document.getElementById('codigoCIIU');
            if (ciiuSelect) {
                ciiuSelect.innerHTML = '<option value="">Seleccione...</option>';
                ciiuData.forEach(c => {
                    const option = document.createElement('option');
                    option.value = c.codigo || c.Codigo_CIIU;
                    option.textContent = `${c.codigo || c.Codigo_CIIU} - ${c.descripcion || c.Descripcion_CIIU}`;
                    option.dataset.descripcion = c.descripcion || c.Descripcion_CIIU;
                    ciiuSelect.appendChild(option);
                });
                ciiuSelect.addEventListener('change', onCIIUChange);
            }
        }
    } catch (error) {
        console.error('Error cargando CIIU:', error);
    }
}

function onCiudadChange() {
    const ciudadId = document.getElementById('ciudad').value;
    const sucursalSelect = document.getElementById('sucursal');
    
    if (!sucursalSelect) return;
    
    sucursalSelect.innerHTML = '<option value="">Seleccione...</option>';
    
    const oficinasFiltradas = oficinasData.filter(o => 
        (o.ciudad_id === parseInt(ciudadId)) || 
        (o.ciudad && o.ciudad.toLowerCase().includes(ciudadesData.find(c => c.id_city == ciudadId)?.name?.toLowerCase() || ''))
    );
    
    oficinasFiltradas.forEach(o => {
        const option = document.createElement('option');
        option.value = o.id_office || o.id;
        option.textContent = o.nombre || o.office_name || o.NOMBRE;
        sucursalSelect.appendChild(option);
    });
}

function onCIIUChange() {
    const select = document.getElementById('codigoCIIU');
    if (!select) return;
    
    const selectedOption = select.options[select.selectedIndex];
    const descripcion = selectedOption.dataset.descripcion || selectedOption.text.split(' - ')[1] || '';
    
    const actividadInput = document.getElementById('actividadEconomica');
    if (actividadInput) {
        actividadInput.value = descripcion;
    }
    calculateRisk();
}

function calculateRisk() {
    const pais = document.getElementById('paisOrigen')?.value;
    const riskAlert = document.getElementById('riskAlert');
    if (!pais || !riskAlert) return;

    let riskScore = 0.25;
    const highRisk = ['VE', 'SY', 'SDN', 'KP', 'IR', 'CU', 'YE', 'HT', 'AF', 'GW'];
    const mediumRisk = ['KY', 'SO', 'SS', 'LY', 'CD', 'BI', 'IQ'];
    
    if (highRisk.includes(pais)) riskScore = 1;
    else if (mediumRisk.includes(pais)) riskScore = 0.75;
    else if (pais === 'CO') riskScore = 0.25;
    else riskScore = 0.5;
    
    let level = 'BAJO';
    let className = 'risk-low';
    
    if (riskScore >= 0.75) { level = 'EXTREMO'; className = 'risk-extreme'; }
    else if (riskScore >= 0.5) { level = 'ALTO'; className = 'risk-high'; }
    else if (riskScore >= 0.25) { level = 'MODERADO'; className = 'risk-moderate'; }
    
    riskAlert.className = `risk-alert ${className}`;
    riskAlert.textContent = `Nivel de Riesgo Estimado: ${level}`;
    riskAlert.style.display = 'block';
}

function bindFormEvents() {
    const form = document.getElementById('vinculacionForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('.btn-submit');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Procesando...';

    try {
        const token = localStorage.getItem('token');
        const formData = new FormData(form);
        
        const payload = {
            fecha: document.getElementById('fecha').value,
            tipo_cliente: document.getElementById('tipoCliente').value,
            tipo_vinculacion: document.getElementById('tipoVinculacion').value,
            ciudad_id: parseInt(document.getElementById('ciudad').value) || 0,
            sucursal_id: parseInt(document.getElementById('sucursal').value) || 0,
            
            tipo_persona: document.getElementById('tipoCliente').value === 'Institucional' ? 'juridica' : 'natural',
            nombres: document.getElementById('nombres')?.value || '',
            apellidos: document.getElementById('apellidos')?.value || '',
            razon_social: document.getElementById('razonSocial')?.value || document.getElementById('razonSocialNatural')?.value || '',
            nit: document.getElementById('nit')?.value || '',
            tipo_id: document.getElementById('tipoDocNatural')?.value || document.getElementById('tipoDocRep')?.value || '',
            numero_id: document.getElementById('numeroDocNatural')?.value || document.getElementById('nit')?.value || '',
            
            codigo_ciiu: document.getElementById('codigoCIIU').value,
            actividad_economica: document.getElementById('actividadEconomica').value,
            pais_origen_id: document.getElementById('paisOrigen').value,
            pais_residencia_id: document.getElementById('paisResidencia').value,
            zona: document.getElementById('zona').value,
            
            regimen_tributario: document.getElementById('regimenTributario').value,
            total_ingresos: parseFloat(document.getElementById('totalIngresos').value) || 0,
            total_egresos: parseFloat(document.getElementById('totalEgresos').value) || 0,
            total_activos: parseFloat(document.getElementById('totalActivos').value) || 0,
            total_patrimonio: parseFloat(document.getElementById('totalPatrimonio').value) || 0,
            
            banco: document.getElementById('nombreBanco').value,
            titular_cuenta: document.getElementById('nombreTitular').value,
            tipo_cuenta: document.getElementById('tipoCuenta').value,
            numero_cuenta: document.getElementById('numeroCuenta').value,
            
            aut_datos: document.getElementById('authDatos').checked,
            aut_laft: document.getElementById('authLAFT').checked,
            aut_anticorrupcion: document.getElementById('authAnticorrupcion').checked,
            aut_transparencia: document.getElementById('authTransparencia').checked,
            
            subcontratistas: document.querySelector('input[name="subcontratistas"]:checked')?.value || 'No',
            entidades_publicas: document.querySelector('input[name="entidadesPublicas"]:checked')?.value || 'No',
            propiedad_estatal: document.querySelector('input[name="propiedadEstatal"]:checked')?.value || 'No',
            licencias: document.querySelector('input[name="licencias"]:checked')?.value || 'No'
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
        
        if (!res.ok) {
            throw new Error(result.detail || 'Error al enviar la solicitud');
        }

        showMessage('✅ Solicitud enviada exitosamente. Redirigiendo...', 'success');
        setTimeout(() => {
            window.location.href = `/admin/confirmacion?id=${result.id_submission || 1}`;
        }, 2000);
    } catch (error) {
        console.error('💥 Error:', error);
        showMessage(error.message || 'Error al enviar el formulario', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Enviar Solicitud de Vinculación';
    }
}

function handleLogout() {
    console.log('🚪 Cerrando sesión...');
    localStorage.clear();
    window.location.href = '/login';
}

function showMessage(text, type) {
    const container = document.getElementById('messageContainer');
    if (container) {
        container.textContent = text;
        container.className = `message-container ${type}`;
        container.style.display = 'block';
    } else {
        alert(text);
    }
}