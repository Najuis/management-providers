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
        console.error('💥 Error en loadUserProfile:', error);
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
    pepFields.style.display = showFields ? 'block' : 'none'; // ✅ Se eliminó la 's' suelta que había aquí
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const tipoCliente = document.getElementById('tipoCliente').value;
    const regimenTributario = document.getElementById('regimenTributario');
    
    if (tipoCliente === 'Natural' && regimenTributario && regimenTributario.value === 'Gran Contribuyente') {
        alert('❌ El régimen "Gran Contribuyente" no está disponible para Persona Natural con Establecimiento de Comercio.');
        return;
    }
    
    console.log('✅ Formulario validado correctamente. Preparando envío...');
    alert('✅ Formulario enviado exitosamente (Función de backend en desarrollo)');
}

function handleLogout() {
    localStorage.clear();
    window.location.href = '/login';
}