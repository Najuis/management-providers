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
    // Cargar fecha actual
    const fechaInput = document.getElementById('fecha');
    if (fechaInput && !fechaInput.value) {
        const hoy = new Date();
        const yyyy = hoy.getFullYear();
        const mm = String(hoy.getMonth() + 1).padStart(2, '0');
        const dd = String(hoy.getDate()).padStart(2, '0');
        fechaInput.value = `${yyyy}-${mm}-${dd}`;
    }
    
    // Cargar perfil
    loadUserProfile();
    
    // Cargar datos
    loadReferenceData();
    loadOficinas();
    loadCIIU();
    
    // Bind events
    bindFormEvents();
    
    // Logout
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
}

// ============================================
// FUNCIÓN showTab - CRÍTICA PARA LAS PESTAÑAS
// ============================================
function showTab(tabNumber) {
    console.log('📑 Cambiando a pestaña:', tabNumber);
    
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    const selectedSection = document.getElementById(`section${tabNumber}`);
    if (selectedSection) {
        selectedSection.classList.add('active');
    }
    
    const selectedTab = document.querySelectorAll('.tab')[tabNumber - 1];
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================
// FUNCIÓN onTipoClienteChange - CRÍTICA
// ============================================
function onTipoClienteChange() {
    const tipoCliente = document.getElementById('tipoCliente').value;
    const personaNaturalFields = document.getElementById('personaNaturalFields');
    const personaJuridicaFields = document.getElementById('personaJuridicaFields');
    
    console.log('🔄 Tipo de cliente cambiado a:', tipoCliente);
    
    if (tipoCliente === 'Mayoreo') {
        if (personaNaturalFields) personaNaturalFields.style.display = 'block';
        if (personaJuridicaFields) personaJuridicaFields.style.display = 'none';
    } else if (tipoCliente === 'Institucional') {
        if (personaNaturalFields) personaNaturalFields.style.display = 'none';
        if (personaJuridicaFields) personaJuridicaFields.style.display = 'block';
    } else {
        if (personaNaturalFields) personaNaturalFields.style.display = 'none';
        if (personaJuridicaFields) personaJuridicaFields.style.display = 'none';
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
            console.warn('⚠️ No hay token');
            if (greetingEl) greetingEl.textContent = 'Usuario no autenticado';
            return;
        }
        
        const res = await fetch('/api/user/profile', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (res.status === 401) {
            console.error('❌ Token inválido');
            if (greetingEl) greetingEl.textContent = 'Sesión expirada';
            return;
        }
        
        if (!res.ok) throw new Error(`Error ${res.status}`);
        
        const profile = await res.json();
        console.log('✅ Perfil cargado:', profile);
        
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
// CARGAR CIUDADES Y PAÍSES
// ============================================
async function loadReferenceData() {
    try {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        
        const [citiesRes, countriesRes] = await Promise.all([
            fetch('/api/cities', { headers }),
            fetch('/api/countries', { headers })
        ]);

        const citiesJson = await citiesRes.json();
        const countriesJson = await countriesRes.json();
        
        ciudadesData = citiesJson.message || citiesJson || [];
        const paisesData = countriesJson.message || countriesJson || [];
        
        console.log(`📊 ${ciudadesData.length} ciudades cargadas`);
        
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
        console.error(' Error cargando directorios:', error);
    }
}

// ============================================
// CARGAR OFICINAS
// ============================================
async function loadOficinas() {
    try {
        console.log('🏢 Cargando oficinas...');
        const response = await fetch('/api/offices');
        
        if (response.ok) {
            const data = await response.json();
            oficinasData = Array.isArray(data) ? data : (data.message || []);
            console.log(`✅ ${oficinasData.length} oficinas cargadas`);
            
            const ciudadSelect = document.getElementById('ciudad');
            if (ciudadSelect) {
                ciudadSelect.addEventListener('change', onCiudadChange);
            }
        } else {
            console.error('❌ Error al cargar oficinas:', response.status);
        }
    } catch (error) {
        console.error('💥 Error cargando oficinas:', error);
    }
}

// ============================================
// CARGAR CIIU
// ============================================
async function loadCIIU() {
    try {
        console.log('📋 Cargando CIIU...');
        const response = await fetch('/api/ciiu');
        
        if (response.ok) {
            const data = await response.json();
            ciiuData = Array.isArray(data) ? data : (data.message || []);
            console.log(`✅ ${ciiuData.length} códigos CIIU cargados`);
            
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
        } else {
            console.error('❌ Error al cargar CIIU:', response.status);
        }
    } catch (error) {
        console.error('💥 Error cargando CIIU:', error);
    }
}

// ============================================
// CAMBIO DE CIUDAD
// ============================================
function onCiudadChange() {
    const ciudadSelect = document.getElementById('ciudad');
    const sucursalSelect = document.getElementById('sucursal');
    
    if (!ciudadSelect || !sucursalSelect) return;
    
    const ciudadId = ciudadSelect.value;
    const ciudadObj = ciudadesData.find(c => (c.id_city || c.codigo) == ciudadId);
    const ciudadNombre = ciudadObj ? (ciudadObj.name || ciudadObj.nombre_municipio || ciudadObj.ciudad).toLowerCase() : '';
    
    console.log(`🔍 Ciudad seleccionada: ${ciudadNombre}`);
    
    sucursalSelect.innerHTML = '<option value="">Seleccione...</option>';
    
    const oficinasFiltradas = oficinasData.filter(o => {
        const oficinaCiudad = (o.ciudad || '').toLowerCase();
        return oficinaCiudad.includes(ciudadNombre) || ciudadNombre.includes(oficinaCiudad);
    });
    
    console.log(`🏪 ${oficinasFiltradas.length} sucursales encontradas`);
    
    oficinasFiltradas.forEach(o => {
        const option = document.createElement('option');
        option.value = o.id_office || o.id;
        option.textContent = o.nombre || o.office_name || o.NOMBRE;
        sucursalSelect.appendChild(option);
    });
}

// ============================================
// CAMBIO DE CIIU
// ============================================
function onCIIUChange() {
    const select = document.getElementById('codigoCIIU');
    if (!select) return;
    
    const selectedOption = select.options[select.selectedIndex];
    const descripcion = selectedOption.dataset.descripcion || 
                       selectedOption.text.split(' - ').slice(1).join(' - ') || '';
    
    const actividadInput = document.getElementById('actividadEconomica');
    if (actividadInput) {
        actividadInput.value = descripcion;
    }
}

// ============================================
// BIND DE EVENTOS
// ============================================
function bindFormEvents() {
    const form = document.getElementById('vinculacionForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
    
    // Eventos para PEP
    const pepRadios = document.querySelectorAll('input[name="manejaRecursosPublicos"], input[name="ejercePoderPublico"], input[name="reconocimientoPublico"], input[name="vinculoPEP"]');
    pepRadios.forEach(radio => {
        radio.addEventListener('change', checkPEP);
    });
}

// ============================================
// VERIFICAR PEP
// ============================================
function checkPEP() {
    const pepFields = document.getElementById('pepFields');
    if (!pepFields) return;
    
    const radios = document.querySelectorAll('input[name="manejaRecursosPublicos"]:checked, input[name="ejercePoderPublico"]:checked, input[name="reconocimientoPublico"]:checked, input[name="vinculoPEP"]:checked');
    
    let showFields = false;
    radios.forEach(radio => {
        if (radio.value === 'Si') showFields = true;
    });
    
    pepFields.style.display = showFields ? 'block' : 'none';
}

// ============================================
// ENVIAR FORMULARIO
// ============================================
async function handleFormSubmit(e) {
    e.preventDefault();
    alert('Formulario enviado (función en desarrollo)');
}

// ============================================
// CERRAR SESIÓN
// ============================================
function handleLogout() {
    console.log('🚪 Cerrando sesión...');
    localStorage.clear();
    window.location.href = '/login';
}