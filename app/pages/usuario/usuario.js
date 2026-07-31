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
// FORMATO DE NÚMEROS (Puntos de miles, coma decimal)
// ============================================
function formatearNumero(input) {
    // Si está vacío, salir
    let valor = input.value.trim();
    if (valor === '') {
        input.value = '';
        return;
    }

    // 1. Normalizar separador decimal: un punto seguido de 1-2 dígitos al final se trata como decimal
    valor = valor.replace(/\.(?=\d{1,2}$)/, ',');

    // 2. Quitar puntos de miles restantes
    valor = valor.replace(/\./g, '');

    // 3. Eliminar cualquier carácter que no sea dígito o coma
    valor = valor.replace(/[^0-9,]/g, '');

    // 4. Máximo una coma (primera), separando entero y decimales
    const partes = valor.split(',');
    let entero = partes[0];
    let decimales = partes.slice(1).join('').slice(0, 2);

    // 5. Quitar ceros a la izquierda innecesarios
    entero = entero.replace(/^0+(?=\d)/, '');

    // 6. Formatear parte entera con puntos de miles
    entero = entero.replace(/\B(?=(\d{3})+(?!\d))/g, '.');

    input.value = partes.length > 1 ? entero + ',' + decimales : entero;
}

// ============================================
// PARSEO DE NÚMEROS CON FORMATO COLOMBIANO (1.500,50)
// ============================================
function parsearNumero(valor) {
    if (!valor) return 0;
    return parseFloat(String(valor).replace(/\./g, '').replace(/,/g, '.')) || 0;
}

// ============================================
// CÁLCULO AUTOMÁTICO DE PATRIMONIO NETO
// ============================================
function calcularPatrimonio() {
    const inputActivo = document.getElementById('totalActivos');
    const inputPasivo = document.getElementById('totalPasivos');
    const inputPatrimonio = document.getElementById('totalPatrimonio');

    // 1. Formatear entradas con puntos de miles y coma decimal
    formatearNumero(inputActivo);
    formatearNumero(inputPasivo);

    // 2. Convertir a float (si está vacío, es 0)
    const activo = parsearNumero(inputActivo.value);
    const pasivo = parsearNumero(inputPasivo.value);

    // 3. Calcular Patrimonio Neto = Activo - Pasivo
    const patrimonio = activo - pasivo;

    // 4. Formatear el resultado (formato colombiano con máx. 2 decimales)
    if (inputActivo.value === '' && inputPasivo.value === '') {
        inputPatrimonio.value = '';
    } else {
        inputPatrimonio.value = patrimonio.toLocaleString('es-CO', { maximumFractionDigits: 2 });
    }
}

// ============================================
// REGLAS DE FORMATO POR CAMPO
// ============================================
// tipo: letras (solo letras/espacios) | alfanumerico | entero | moneda | porcentaje | correo | url | fecha
const FORMATO_REGLA = {
    // --- Persona natural ---
    nombres: { tipo: 'letras', max: 80 },
    apellidos: { tipo: 'letras', max: 80 },
    numeroDocNatural: { tipo: 'entero', max: 15 },
    fechaNacimiento: { tipo: 'fecha' },
    fechaExpNatural: { tipo: 'fecha' },
    direccionNatural: { tipo: 'alfanumerico', max: 200 },
    ciudadNatural: { tipo: 'letras', max: 80 },
    DepartamentoNatural: { tipo: 'letras', max: 80 },
    correoNatural: { tipo: 'correo', max: 150 },
    telefonoNatural: { tipo: 'entero', max: 10 },
    razonSocialNatural: { tipo: 'alfanumerico', max: 200 },
    nitNatural: { tipo: 'entero', max: 15 },

    // --- Persona jurídica ---
    razonSocial: { tipo: 'alfanumerico', max: 200 },
    nit: { tipo: 'entero', max: 12 },
    digitoVerificacion: { tipo: 'entero', max: 1 },
    fechaConstitucion: { tipo: 'fecha' },
    otroSociedad: { tipo: 'alfanumerico', max: 100 },
    direccionJuridica: { tipo: 'alfanumerico', max: 200 },
    municipioJuridica: { tipo: 'alfanumerico', max: 120 },
    paginaWeb: { tipo: 'url', max: 200 },

    // --- Representantes legales ---
    representanteLegal: { tipo: 'letras', max: 120 },
    numeroDocRep: { tipo: 'entero', max: 15 },
    representanteSuplente: { tipo: 'letras', max: 120 },
    numeroDocSuplente: { tipo: 'entero', max: 15 },

    // --- Beneficiarios finales ---
    bf1_nombre: { tipo: 'letras', max: 80 },
    bf1_numeroDoc: { tipo: 'entero', max: 15 },
    bf2_nombre: { tipo: 'letras', max: 80 },
    bf2_numeroDoc: { tipo: 'entero', max: 15 },
    bf3_nombre: { tipo: 'letras', max: 80 },
    bf3_numeroDoc: { tipo: 'entero', max: 15 },

    // --- Composición accionaria ---
    ca1Nombre: { tipo: 'alfanumerico', max: 120 },
    ca1Participacion: { tipo: 'porcentaje', max: 6 },
    ca1NumeroDoc: { tipo: 'entero', max: 15 },
    ca1Direccion: { tipo: 'alfanumerico', max: 200 },
    ca1Telefono: { tipo: 'entero', max: 10 },
    ca2Nombre: { tipo: 'alfanumerico', max: 120 },
    ca2Participacion: { tipo: 'porcentaje', max: 6 },
    ca2NumeroDoc: { tipo: 'entero', max: 15 },
    ca2Direccion: { tipo: 'alfanumerico', max: 200 },
    ca2Telefono: { tipo: 'entero', max: 10 },
    ca3Nombre: { tipo: 'alfanumerico', max: 120 },
    ca3Participacion: { tipo: 'porcentaje', max: 6 },
    ca3NumeroDoc: { tipo: 'entero', max: 15 },
    ca3Direccion: { tipo: 'alfanumerico', max: 200 },
    ca3Telefono: { tipo: 'entero', max: 10 },
    ca4Nombre: { tipo: 'alfanumerico', max: 120 },
    ca4Participacion: { tipo: 'porcentaje', max: 6 },
    ca4NumeroDoc: { tipo: 'entero', max: 15 },
    ca4Direccion: { tipo: 'alfanumerico', max: 200 },
    ca4Telefono: { tipo: 'entero', max: 10 },
    ca5Nombre: { tipo: 'alfanumerico', max: 120 },
    ca5Participacion: { tipo: 'porcentaje', max: 6 },
    ca5NumeroDoc: { tipo: 'entero', max: 15 },
    ca5Direccion: { tipo: 'alfanumerico', max: 200 },
    ca5Telefono: { tipo: 'entero', max: 10 },

    // --- Referencias bancarias ---
    nombreBanco1: { tipo: 'alfanumerico', max: 100 },
    nombreTitular1: { tipo: 'letras', max: 120 },
    numeroCuenta1: { tipo: 'entero', max: 30 },
    nombreBanco2: { tipo: 'alfanumerico', max: 100 },
    nombreTitular2: { tipo: 'letras', max: 120 },
    numeroCuenta2: { tipo: 'entero', max: 30 },

    // --- Referencias comerciales ---
    refCom1Empresa: { tipo: 'alfanumerico', max: 150 },
    refCom1Contacto: { tipo: 'letras', max: 80 },
    refCom1Telefono: { tipo: 'entero', max: 10 },
    refCom1Correo: { tipo: 'correo', max: 150 },
    refCom2Empresa: { tipo: 'alfanumerico', max: 150 },
    refCom2Contacto: { tipo: 'letras', max: 80 },
    refCom2Telefono: { tipo: 'entero', max: 10 },
    refCom2Correo: { tipo: 'correo', max: 150 },

    // --- Financiero ---
    totalIngresos: { tipo: 'moneda', max: 18 },
    totalEgresos: { tipo: 'moneda', max: 18 },
    totalActivos: { tipo: 'moneda', max: 18 },
    totalPasivos: { tipo: 'moneda', max: 18 },

    // --- PEP ---
    cargoPEP: { tipo: 'alfanumerico', max: 120 },
    entidadPEP: { tipo: 'alfanumerico', max: 150 },
    fechaPEP: { tipo: 'fecha' }
};

const ETIQUETAS_CAMPO = {
    nombres: 'Nombres',
    apellidos: 'Apellidos',
    numeroDocNatural: 'Número de documento',
    fechaNacimiento: 'Fecha de nacimiento',
    fechaExpNatural: 'Fecha de expedición del documento',
    direccionNatural: 'Dirección',
    ciudadNatural: 'Ciudad',
    DepartamentoNatural: 'Departamento',
    correoNatural: 'Correo electrónico',
    telefonoNatural: 'Teléfono',
    razonSocialNatural: 'Razón social (establecimiento)',
    nitNatural: 'NIT del establecimiento',
    razonSocial: 'Razón social',
    nit: 'NIT',
    digitoVerificacion: 'Dígito de verificación',
    fechaConstitucion: 'Fecha de constitución',
    otroSociedad: 'Otro tipo de sociedad',
    direccionJuridica: 'Dirección',
    municipioJuridica: 'Municipio',
    paginaWeb: 'Página web',
    representanteLegal: 'Representante legal',
    numeroDocRep: 'Documento representante legal',
    representanteSuplente: 'Representante suplente',
    numeroDocSuplente: 'Documento representante suplente',
    bf1_nombre: 'Beneficiario final 1 - nombre',
    bf1_numeroDoc: 'Beneficiario final 1 - documento',
    bf2_nombre: 'Beneficiario final 2 - nombre',
    bf2_numeroDoc: 'Beneficiario final 2 - documento',
    bf3_nombre: 'Beneficiario final 3 - nombre',
    bf3_numeroDoc: 'Beneficiario final 3 - documento',
    ca1Nombre: 'Accionista 1 - nombre',
    ca1Participacion: 'Accionista 1 - participación',
    ca1NumeroDoc: 'Accionista 1 - documento',
    ca1Direccion: 'Accionista 1 - dirección',
    ca1Telefono: 'Accionista 1 - teléfono',
    ca2Nombre: 'Accionista 2 - nombre',
    ca2Participacion: 'Accionista 2 - participación',
    ca2NumeroDoc: 'Accionista 2 - documento',
    ca2Direccion: 'Accionista 2 - dirección',
    ca2Telefono: 'Accionista 2 - teléfono',
    ca3Nombre: 'Accionista 3 - nombre',
    ca3Participacion: 'Accionista 3 - participación',
    ca3NumeroDoc: 'Accionista 3 - documento',
    ca3Direccion: 'Accionista 3 - dirección',
    ca3Telefono: 'Accionista 3 - teléfono',
    ca4Nombre: 'Accionista 4 - nombre',
    ca4Participacion: 'Accionista 4 - participación',
    ca4NumeroDoc: 'Accionista 4 - documento',
    ca4Direccion: 'Accionista 4 - dirección',
    ca4Telefono: 'Accionista 4 - teléfono',
    ca5Nombre: 'Accionista 5 - nombre',
    ca5Participacion: 'Accionista 5 - participación',
    ca5NumeroDoc: 'Accionista 5 - documento',
    ca5Direccion: 'Accionista 5 - dirección',
    ca5Telefono: 'Accionista 5 - teléfono',
    nombreBanco1: 'Banco referencia 1',
    nombreTitular1: 'Titular cuenta 1',
    numeroCuenta1: 'Número de cuenta 1',
    nombreBanco2: 'Banco referencia 2',
    nombreTitular2: 'Titular cuenta 2',
    numeroCuenta2: 'Número de cuenta 2',
    refCom1Empresa: 'Referencia comercial 1 - empresa',
    refCom1Contacto: 'Referencia comercial 1 - contacto',
    refCom1Telefono: 'Referencia comercial 1 - teléfono',
    refCom1Correo: 'Referencia comercial 1 - correo',
    refCom2Empresa: 'Referencia comercial 2 - empresa',
    refCom2Contacto: 'Referencia comercial 2 - contacto',
    refCom2Telefono: 'Referencia comercial 2 - teléfono',
    refCom2Correo: 'Referencia comercial 2 - correo',
    totalIngresos: 'Total ingresos',
    totalEgresos: 'Total egresos',
    totalActivos: 'Total activos',
    totalPasivos: 'Total pasivos',
    cargoPEP: 'Cargo desempeñado',
    entidadPEP: 'Entidad',
    fechaPEP: 'Fecha vinculación/desvinculación'
};

const REGEX_LETRAS = /^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' ]+$/;
const REGEX_ALFANUMERICO = /^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ .,#()-]+$/;
const REGEX_ENTERO = /^\d+$/;
const REGEX_CORREO = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const REGEX_URL = /^https?:\/\/.+\.\S+/;

// ============================================
// SANITIZACIÓN EN VIVO SEGÚN EL TIPO DE CAMPO
// ============================================
function bindInputFormats() {
    for (const [id, regla] of Object.entries(FORMATO_REGLA)) {
        const el = document.getElementById(id);
        if (!el) continue;

        el.addEventListener('input', () => {
            let valor = el.value;

            switch (regla.tipo) {
                case 'letras':
                    el.value = valor.replace(/[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ' ]/g, '');
                    break;
                case 'alfanumerico':
                    el.value = valor.replace(/[^A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ .,#()-]/g, '');
                    break;
                case 'entero':
                    el.value = valor.replace(/[^0-9]/g, '');
                    break;
                case 'moneda':
                case 'porcentaje':
                    formatearNumero(el);
                    break;
                default:
                    break;
            }

            if (regla.max && el.value.length > regla.max) {
                el.value = el.value.slice(0, regla.max);
            }
        });
    }
}

// ============================================
// VALIDACIÓN DE FORMATOS AL ENVIAR
// ============================================
function validarFormatos() {
    const get = id => document.getElementById(id);
    const errores = [];

    for (const [id, regla] of Object.entries(FORMATO_REGLA)) {
        const el = get(id);
        if (!el) continue;
        const valor = el.value.trim();
        if (valor === '') continue;

        const etiqueta = ETIQUETAS_CAMPO[id] || id;

        if (regla.max && valor.length > regla.max) {
            errores.push(`${etiqueta}: máximo ${regla.max} caracteres`);
            continue;
        }

        switch (regla.tipo) {
            case 'letras':
                if (!REGEX_LETRAS.test(valor)) {
                    errores.push(`${etiqueta}: solo se permiten letras y espacios`);
                }
                break;
            case 'alfanumerico':
                if (!REGEX_ALFANUMERICO.test(valor)) {
                    errores.push(`${etiqueta}: solo se permiten letras, números y los caracteres . , # ( ) -`);
                }
                break;
            case 'entero':
                if (!REGEX_ENTERO.test(valor)) {
                    errores.push(`${etiqueta}: debe ser un número entero`);
                }
                break;
            case 'correo':
                if (!REGEX_CORREO.test(valor)) {
                    errores.push(`${etiqueta}: formato de correo no válido`);
                }
                break;
            case 'url':
                if (!REGEX_URL.test(valor)) {
                    errores.push(`${etiqueta}: debe ser una URL válida (ej. https://www.ejemplo.com)`);
                }
                break;
            case 'porcentaje': {
                const n = parsearNumero(valor);
                if (isNaN(n) || n < 0 || n > 100) {
                    errores.push(`${etiqueta}: debe estar entre 0 y 100`);
                }
                break;
            }
            case 'moneda': {
                const n = parsearNumero(valor);
                if (isNaN(n) || n < 0) {
                    errores.push(`${etiqueta}: valor monetario no válido`);
                }
                break;
            }
            case 'fecha':
                if (!/^\d{4}-\d{2}-\d{2}$/.test(valor)) {
                    errores.push(`${etiqueta}: formato de fecha no válido`);
                }
                break;
            default:
                break;
        }
    }

    return errores;
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
            if (ciudadSelect) {
                ciudadSelect.addEventListener('change', onCiudadChange);
                // Si ya hay una ciudad seleccionada (restauración/autofill), llenar las sucursales
                if (ciudadSelect.value) {
                    onCiudadChange();
                }
            }
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

    bindInputFormats();
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
// ENVIAR FORMULARIO - CREA SOLICITUD EN BD Y REDIRIGE
// ============================================
async function handleFormSubmit(e) {
    e.preventDefault();

    const token = localStorage.getItem('token');
    if (!token) {
        alert('❌ No hay sesión activa. Inicia sesión nuevamente.');
        window.location.href = '/login';
        return;
    }

    // Validación Frontend: Persona Natural no puede ser Gran Contribuyente
    const tipoCliente = document.getElementById('tipoCliente').value;
    const regimenTributario = document.getElementById('regimenTributario');

    if (tipoCliente === 'Natural' && regimenTributario.value === 'Gran Contribuyente') {
        alert('❌ El régimen "Gran Contribuyente" no está disponible para Persona Natural con Establecimiento de Comercio.');
        return;
    }

    // Validar casilla de Aceptación Final (obligatoria para enviar)
    const aceptacionFinal = document.getElementById('authAceptacionFinal');
    if (aceptacionFinal && !aceptacionFinal.checked) {
        alert('❌ Debes marcar la casilla de Aceptación Final para enviar el formulario.');
        return;
    }

    // Validación de campos obligatorios (el formulario usa novalidate)
    const campoFaltante = validateRequiredFields(tipoCliente);
    if (campoFaltante) {
        alert(`❌ Campo obligatorio pendiente: ${campoFaltante}. Completa todos los campos antes de enviar.`);
        return;
    }

    // Validación de formatos por campo (caracteres, longitudes, decimales)
    const erroresFormato = validarFormatos();
    if (erroresFormato.length) {
        alert(`❌ Revisa el formato de los siguientes campos:\n\n• ${erroresFormato.join('\n• ')}`);
        return;
    }

    // Validación de consistencia matemática antes de enviar
    const totalActivos = parsearNumero(document.getElementById('totalActivos').value);
    const totalPasivos = parsearNumero(document.getElementById('totalPasivos').value);
    const totalPatrimonio = parsearNumero(document.getElementById('totalPatrimonio').value);
    if (Math.abs(totalPatrimonio - (totalActivos - totalPasivos)) > 0.01) {
        alert(`⚠️ Error de integridad: El Patrimonio Neto (${totalPatrimonio}) no coincide con el cálculo de Activo (${totalActivos}) - Pasivo (${totalPasivos}) = ${totalActivos - totalPasivos}`);
        return;
    }

    const payload = buildSubmissionPayload(tipoCliente, totalActivos, totalPasivos, totalPatrimonio);

    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Enviando...';
    submitBtn.disabled = true;

    try {
        const response = await fetch('/api/submissions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error en el servidor');
        }

        const result = await response.json();
        window.location.href = `/customer/dashboard?id=${result.id}`;
    } catch (error) {
        console.error('Error al enviar la solicitud:', error);
        alert(`❌ Error al procesar la solicitud: ${error.message}`);
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

function validateRequiredFields(tipoCliente) {
    const get = id => document.getElementById(id);
    const esJuridica = tipoCliente === 'Juridica';

    const requeridos = [
        { id: 'fecha', label: 'Fecha' },
        { id: 'tipoVinculacion', label: 'Tipo de vinculación' },
        { id: 'ciudad', label: 'Ciudad' },
        { id: 'sucursal', label: 'Oficina/Sucursal' },
        { id: 'codigoCIIU', label: 'Código CIIU' },
        { id: 'regimenTributario', label: 'Régimen tributario' },
        { id: 'totalIngresos', label: 'Total ingresos' },
        { id: 'totalEgresos', label: 'Total egresos' },
        { id: 'totalActivos', label: 'Total activos' },
        { id: 'totalPasivos', label: 'Total pasivos' }
    ];

    if (esJuridica) {
        requeridos.push(
            { id: 'razonSocial', label: 'Razón social' },
            { id: 'nit', label: 'NIT' },
            { id: 'tipoSociedad', label: 'Tipo de sociedad' }
        );
    } else {
        requeridos.push(
            { id: 'nombres', label: 'Nombres' },
            { id: 'apellidos', label: 'Apellidos' },
            { id: 'tipoDocNatural', label: 'Tipo de documento' },
            { id: 'numeroDocNatural', label: 'Número de documento' },
            { id: 'correoNatural', label: 'Correo electrónico' }
        );
    }

    for (const campo of requeridos) {
        const el = get(campo.id);
        if (!el || !el.value || el.value.trim() === '') {
            return campo.label;
        }
    }

    if (esJuridica) {
        const tipoSociedad = get('tipoSociedad').value;
        if (tipoSociedad === 'Otro') {
            const otro = get('otroSociedad');
            if (!otro || !otro.value.trim()) return 'Especifique el tipo de sociedad';
        }
    }

    const autorizaciones = [
        { id: 'authDatos', label: 'Autorización de datos' },
        { id: 'authLAFT', label: 'Autorización LA/FT' },
        { id: 'authAnticorrupcion', label: 'Autorización anticorrupción' },
        { id: 'authTransparencia', label: 'Autorización de transparencia' }
    ];
    for (const auth of autorizaciones) {
        const el = get(auth.id);
        if (el && !el.checked) return auth.label;
    }

    return null;
}

function buildSubmissionPayload(tipoCliente, totalActivos, totalPasivos, totalPatrimonio) {
    const get = id => document.getElementById(id);
    const esJuridica = tipoCliente === 'Juridica';

    const ciudadSelect = get('ciudad');
    const sucursalSelect = get('sucursal');
    const regimenSelect = get('regimenTributario');

    return {
        fecha: get('fecha').value || null,
        tipo_cliente: tipoCliente,
        tipo_vinculacion: get('tipoVinculacion').value || null,
        ciudad_id: parseInt(ciudadSelect.value) || null,
        oficina: sucursalSelect.options[sucursalSelect.selectedIndex]?.text || sucursalSelect.value || null,
        tipo_persona: esJuridica ? 'juridica' : 'natural',
        nombres: get('nombres')?.value || null,
        apellidos: get('apellidos')?.value || null,
        razon_social: esJuridica ? get('razonSocial').value : null,
        tipo_id: esJuridica ? 'NIT' : (get('tipoDocNatural').value || null),
        numero_id: esJuridica ? get('nit').value : get('numeroDocNatural').value,
        fecha_expedicion: esJuridica
            ? (get('fechaConstitucion').value || null)
            : (get('fechaExpNatural').value || null),
        estructura_juridica: esJuridica
            ? (get('tipoSociedad').value === 'Otro' ? get('otroSociedad').value : (get('tipoSociedad').value || null))
            : null,
        codigo_ciiu: get('codigoCIIU').value || null,
        regimen_tributario: regimenSelect.value || null,
        total_ingresos: parsearNumero(get('totalIngresos').value) || null,
        total_egresos: parsearNumero(get('totalEgresos').value) || null,
        aut_datos: get('authDatos').checked,
        aut_laft: get('authLAFT').checked,
        aut_anticorrupcion: get('authAnticorrupcion').checked,
        aut_etica: get('authTransparencia').checked,
        // Datos extra para el resumen del dashboard
        email: get('correoNatural').value || '',
        ciudad_nombre: ciudadSelect.options[ciudadSelect.selectedIndex]?.text || '',
        actividad_economica: get('actividadEconomica').value || '',
        total_activos: totalActivos,
        total_pasivos: totalPasivos,
        total_patrimonio: totalPatrimonio
    };
}

function handleLogout() {
    localStorage.clear();
    window.location.href = '/login';
}