// ============================================
// VARIABLES GLOBALES
// ============================================
let oficinasData = [];
let ciiuData = [];
let ciudadesData = [];

// ============================================
// INICIALIZACIÓN
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    console.log('📝 Formulario de usuario cargado');
    initializeUserForm();
});

function initializeUserForm() {
    const fechaInput = document.getElementById('fecha');
    if (fechaInput && !fechaInput.value) {
        const hoy = new Date();
        const yyyy = hoy.getFullYear();
        const mm = String(hoy.getMonth() + 1).padStart(2, '0');
        const dd = String(hoy.getDate()).padStart(2, '0');
        fechaInput.value = `${yyyy}-${mm}-${dd}`;
    }
    
    loadUserProfile();
    loadReferenceData();
    loadOficinas();
    loadCIIU();
    bindFormEvents();
    onTipoClienteChange();
    
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
}

// ============================================
// FUNCIÓN showTab
// ============================================
function showTab(tabNumber) {
    console.log('📑 Cambiando a pestaña:', tabNumber);
    
    document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    
    const selectedSection = document.getElementById(`section${tabNumber}`);
    if (selectedSection) selectedSection.classList.add('active');
    
    const selectedTab = document.querySelectorAll('.tab')[tabNumber - 1];
    if (selectedTab) selectedTab.classList.add('active');
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================
// FUNCIÓN onTipoClienteChange - ✅ CORREGIDA
// ============================================
function onTipoClienteChange() {
    const tipoCliente = document.getElementById('tipoCliente').value;
    const personaNaturalFields = document.getElementById('personaNaturalFields');
    const personaJuridicaFields = document.getElementById('personaJuridicaFields');
    const regimenTributario = document.getElementById('regimenTributario');
    
    console.log('🔄 Tipo de cliente cambiado a:', tipoCliente);
    
    // 1. Mostrar/ocultar campos de identificación
    if (tipoCliente === 'Natural') {
        if (personaNaturalFields) personaNaturalFields.style.display = 'block';
        if (personaJuridicaFields) personaJuridicaFields.style.display = 'none';
    } else if (tipoCliente === 'Juridica') {
        if (personaNaturalFields) personaNaturalFields.style.display = 'none';
        if (personaJuridicaFields) personaJuridicaFields.style.display = 'block';
    } else {
        if (personaNaturalFields) personaNaturalFields.style.display = 'none';
        if (personaJuridicaFields) personaJuridicaFields.style.display = 'none';
    }
    
    // 2. Controlar la opción "Gran Contribuyente"
    if (regimenTributario) {
        const granContribuyenteOption = regimenTributario.querySelector('option[value="Gran Contribuyente"]');
        
        if (tipoCliente === 'Juridica') {
            if (granContribuyenteOption) {
                granContribuyenteOption.style.display = 'block';
                granContribuyenteOption.disabled = false;
            }
        } else {
            if (granContribuyenteOption) {
                granContribuyenteOption.style.display = 'none';
                granContribuyenteOption.disabled = true;
                if (regimenTributario.value === 'Gran Contribuyente') {
                    regimenTributario.value = '';
                }
            }
        }
    }

    // 3. Documentos 8, 9 y 10: solo para Persona Jurídica
    const esJuridica = tipoCliente === 'Juridica';
    document.querySelectorAll('.documentos-juridica').forEach(group => {
        group.style.display = esJuridica ? '' : 'none';
    });

    // 4. Texto del documento 3 según el tipo de cliente
    const docIdentidadLabel = document.getElementById('docIdentidadLabel');
    if (docIdentidadLabel) {
        docIdentidadLabel.textContent = esJuridica
            ? '3. Copia de documento de identidad del representante legal *'
            : '3. Copia de documento de identidad *';
    }
}

// ============================================
// FUNCIÓN checkOtroSociedad
// ============================================
function checkOtroSociedad() {
    const tipoSociedad = document.getElementById('tipoSociedad').value;
    const otroGroup = document.getElementById('otroSociedadGroup');
    const otroInput = document.getElementById('otroSociedad');
    
    if (tipoSociedad === 'Otro') {
        if (otroGroup) otroGroup.style.display = 'block';
        if (otroInput) otroInput.required = true;
    } else {
        if (otroGroup) otroGroup.style.display = 'none';
        if (otroInput) otroInput.required = false;
    }
}

// ============================================
// FUNCIÓN checkFileUpload
// ============================================
function checkFileUpload(input) {
    if (input.files && input.files.length > 0) {
        input.classList.add('uploaded');
    } else {
        input.classList.remove('uploaded');
    }
}

// ============================================
// VALIDACIÓN DE CAMPOS NUMÉRICOS (Regex ^[0-9]+$)
// ============================================
function validarSoloNumeros(input) {
    // Elimina cualquier carácter que no sea dígito
    input.value = input.value.replace(/[^0-9]/g, '');
}

// ============================================
// VALIDACIÓN DINÁMICA DE DOCUMENTO REPRESENTANTE LEGAL
// ============================================
function validarFormatoDocumentoRep() {
    const tipoDoc = document.getElementById('tipoDocRep').value;
    const inputDoc = document.getElementById('numeroDocRep');
    
    // Si es Pasaporte o PTP, podría requerir letras, si es CC/TI/CE, solo números.
    if (['CC', 'TI', 'CE'].includes(tipoDoc)) {
        inputDoc.setAttribute('inputmode', 'numeric');
        inputDoc.setAttribute('pattern', '[0-9]*');
    } else {
        inputDoc.setAttribute('inputmode', 'text');
    }
}

// ============================================
// FORMATO DE NÚMEROS (Separador de miles)
// ============================================
function formatearNumero(input) {
    // Remover formato previo
    let valor = input.value.replace(/\./g, '').replace(/,/g, '');
    
    // Si está vacío, salir
    if (valor === '') {
        input.value = '';
        return;
    }
    
    // Validar que solo sean números
    valor = valor.replace(/[^0-9]/g, '');
    
    // Formatear con puntos de miles
    const numero = parseInt(valor);
    if (!isNaN(numero)) {
        input.value = numero.toLocaleString('es-CO');
    }
}

// ============================================
// CÁLCULO AUTOMÁTICO DE PATRIMONIO NETO
// ============================================
function calcularPatrimonio() {
    const inputActivo = document.getElementById('totalActivos');
    const inputPasivo = document.getElementById('totalPasivos');
    const inputPatrimonio = document.getElementById('totalPatrimonio');

    // 1. Limpiar formato para obtener el número puro (quitar puntos y comas)
    const activoStr = inputActivo.value.replace(/\./g, '').replace(/,/g, '');
    const pasivoStr = inputPasivo.value.replace(/\./g, '').replace(/,/g, '');

    // 2. Validar que solo queden números (seguridad extra)
    inputActivo.value = inputActivo.value.replace(/[^0-9.,]/g, '');
    inputPasivo.value = inputPasivo.value.replace(/[^0-9.,]/g, '');

    // 3. Convertir a float (si está vacío, es 0)
    const activo = parseFloat(activoStr) || 0;
    const pasivo = parseFloat(pasivoStr) || 0;

    // 4. Calcular Patrimonio Neto = Activo - Pasivo
    const patrimonio = activo - pasivo;

    // 5. Formatear el resultado para mostrarlo al usuario (formato colombiano)
    // Si ambos están vacíos, dejar vacío. Si hay cálculo, mostrar con separadores de miles.
    if (inputActivo.value === '' && inputPasivo.value === '') {
        inputPatrimonio.value = '';
    } else {
        inputPatrimonio.value = patrimonio.toLocaleString('es-CO');
    }
}

// ============================================
// PERFIL DE USUARIO
// ============================================
async function loadUserProfile() {
    try {
        const token = localStorage.getItem('token');
        const greetingEl = document.getElementById('userGreeting');
        
        if (!token) {
            if (greetingEl) greetingEl.textContent = 'Usuario no autenticado';
            return;
        }
        
        const res = await fetch('/api/user/profile', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
        });
        
        if (res.status === 401) {
            if (greetingEl) greetingEl.textContent = 'Sesión expirada';
            return;
        }
        
        if (!res.ok) throw new Error(`Error ${res.status}`);
        const profile = await res.json();
        
        if (greetingEl) {
            const nombre = profile.name || profile.email?.split('@')[0] || 'Usuario';
            greetingEl.textContent = `Tercero: ${nombre}`;
        }
        
        localStorage.setItem('current_user_id', profile.id_user);
        localStorage.setItem('current_user_type', profile.type_user_id);
    } catch (error) {
        console.error(' Error en loadUserProfile:', error);
    }
}

// ============================================
// CARGAR DATOS
// ============================================
async function loadReferenceData() {
    try {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const citiesRes = await fetch('/api/cities', { headers });
        const citiesJson = await citiesRes.json();
        ciudadesData = citiesJson.message || citiesJson || [];
        
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
    } catch (error) {
        console.error('💥 Error cargando directorios:', error);
    }
}

async function loadOficinas() {
    try {
        const response = await fetch('/api/offices');
        if (response.ok) {
            const data = await response.json();
            oficinasData = Array.isArray(data) ? data : (data.message || []);
            const ciudadSelect = document.getElementById('ciudad');
            if (ciudadSelect) ciudadSelect.addEventListener('change', onCiudadChange);
        }
    } catch (error) {
        console.error('💥 Error cargando oficinas:', error);
    }
}

async function loadCIIU() {
    try {
        const response = await fetch('/api/ciiu');
        if (response.ok) {
            const data = await response.json();
            ciiuData = Array.isArray(data) ? data : (data.message || []);
            const ciiuSelect = document.getElementById('codigoCIIU');
            if (ciiuSelect) {
                ciiuSelect.innerHTML = '<option value="">Seleccione...</option>';
                ciiuData.forEach(c => {
                    const option = document.createElement('option');
                    const codigo = c.codigo || c.Codigo_CIIU || c.codigo_ciiu;
                    const descripcion = c.descripcion || c.Descripcion_CIIU || c.descripcion_ciiu;
                    option.value = codigo;
                    option.textContent = `${codigo} - ${descripcion}`;
                    option.dataset.descripcion = descripcion;
                    ciiuSelect.appendChild(option);
                });
                ciiuSelect.addEventListener('change', onCIIUChange);
            }
        }
    } catch (error) {
        console.error('💥 Error cargando CIIU:', error);
    }
}

// ============================================
// EVENTOS DE CAMBIO
// ============================================
function onCiudadChange() {
    const ciudadSelect = document.getElementById('ciudad');
    const sucursalSelect = document.getElementById('sucursal');
    if (!ciudadSelect || !sucursalSelect) return;
    
    const ciudadId = ciudadSelect.value;
    const ciudadObj = ciudadesData.find(c => (c.id_city || c.codigo) == ciudadId);
    const ciudadNombre = ciudadObj ? (ciudadObj.name || ciudadObj.nombre_municipio || ciudadObj.ciudad).toLowerCase() : '';
    
    sucursalSelect.innerHTML = '<option value="">Seleccione...</option>';
    oficinasData.filter(o => {
        const oficinaCiudad = (o.ciudad || '').toLowerCase();
        return oficinaCiudad.includes(ciudadNombre) || ciudadNombre.includes(oficinaCiudad);
    }).forEach(o => {
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
    const descripcion = selectedOption.dataset.descripcion || selectedOption.text.split(' - ').slice(1).join(' - ') || '';
    const actividadInput = document.getElementById('actividadEconomica');
    if (actividadInput) actividadInput.value = descripcion;
}

// ============================================
// BIND DE EVENTOS Y VALIDACIÓN
// ============================================
function bindFormEvents() {
    const form = document.getElementById('vinculacionForm');
    if (form) form.addEventListener('submit', handleFormSubmit);
    
    document.querySelectorAll('input[name="manejaRecursosPublicos"], input[name="ejercePoderPublico"], input[name="reconocimientoPublico"], input[name="vinculoPEP"]').forEach(radio => {
        radio.addEventListener('change', checkPEP);
    });
}

function checkPEP() {
    const pepFields = document.getElementById('pepFields');
    if (!pepFields) return;
    const radios = document.querySelectorAll('input[name="manejaRecursosPublicos"]:checked, input[name="ejercePoderPublico"]:checked, input[name="reconocimientoPublico"]:checked, input[name="vinculoPEP"]:checked');
    let showFields = false;
    radios.forEach(radio => { if (radio.value === 'Si') showFields = true; });
    pepFields.style.display = showFields ? 'block' : 'none';
}

// ============================================
// ENVIAR FORMULARIO - ACTUALIZADA CON VALIDACIÓN Y REDIRECCIÓN
// ============================================
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Validación Frontend: Persona Natural no puede ser Gran Contribuyente
    const tipoCliente = document.getElementById('tipoCliente').value;
    const regimenTributario = document.getElementById('regimenTributario');
    
    if (tipoCliente === 'Natural' && regimenTributario.value === 'Gran Contribuyente') {
        alert('❌ El régimen "Gran Contribuyente" no está disponible para Persona Natural con Establecimiento de Comercio.');
        return;
    }
    
    // Recopilar datos financieros limpios (sin puntos) para el backend
    const formData = {
        total_activos: parseFloat(document.getElementById('totalActivos').value.replace(/\./g, '')) || 0,
        total_pasivos: parseFloat(document.getElementById('totalPasivos').value.replace(/\./g, '')) || 0,
        total_patrimonio: parseFloat(document.getElementById('totalPatrimonio').value.replace(/\./g, '')) || 0,
        beneficiario_1: document.getElementById('beneficiario1').value,
        beneficiario_2: document.getElementById('beneficiario2').value,
        beneficiario_3: document.getElementById('beneficiario3').value
    };

    // Validación de consistencia matemática antes de enviar
    const patrimonioCalculado = formData.total_activos - formData.total_pasivos;
    if (Math.abs(formData.total_patrimonio - patrimonioCalculado) > 0.01) {
        alert(`⚠️ Error de integridad: El Patrimonio Neto (${formData.total_patrimonio}) no coincide con el cálculo de Activo (${formData.total_activos}) - Pasivo (${formData.total_pasivos}) = ${patrimonioCalculado}`);
        return;
    }

    console.log('✅ Datos validados y listos para envío:', formData);
    alert('✅ Formulario enviado exitosamente. Redirigiendo...');
    
    // Guardar datos en localStorage para la página de confirmación
    localStorage.setItem('lastSubmission', JSON.stringify({
        email: document.getElementById('correoNatural').value || 'usuario@ejemplo.com',
        tempPassword: 'Temp123!',
        nombre: document.getElementById('razonSocial').value || document.getElementById('nombres').value,
        nit: document.getElementById('nit').value || document.getElementById('numeroDocNatural').value,
        tipoCliente: tipoCliente,
        id: 'SOL-' + Date.now(),
        fechaEnvio: new Date().toISOString(),
        ciudad: document.getElementById('ciudad').options[document.getElementById('ciudad').selectedIndex]?.text || 'No disponible',
        actividadEconomica: document.getElementById('actividadEconomica').value || 'No disponible',
        nivelRiesgo: 'MODERADO'
    }));
    
    // Redirección solicitada
    window.location.href = '/customer/dashboard';
}

function handleLogout() {
    localStorage.clear();
    window.location.href = '/login';
}