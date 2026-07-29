// ============================================
// VARIABLES GLOBALES
// ============================================
let submissionData = null;

// ============================================
// INICIALIZACIÓN
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ Página de confirmación cargada');
    loadSubmissionData();
    setTimeout(populateSignatureFields, 500); // Esperar a que se carguen los datos
});

// ============================================
// CARGAR DATOS DE LA SOLICITUD
// ============================================
async function loadSubmissionData() {
    try {
        // Obtener datos del localStorage (guardados al enviar el formulario)
        const savedData = localStorage.getItem('lastSubmission');
        
        if (savedData) {
            submissionData = JSON.parse(savedData);
            populateDashboard(submissionData);
        } else {
            // Si no hay datos en localStorage, mostrar datos de ejemplo
            showDemoData();
        }
    } catch (error) {
        console.error('Error al cargar datos:', error);
        showDemoData();
    }
}

// ============================================
// LLENAR EL DASHBOARD CON DATOS
// ============================================
function populateDashboard(data) {
    // Credenciales
    document.getElementById('displayUsername').value = data.email || 'usuario@ejemplo.com';
    document.getElementById('displayPassword').value = data.tempPassword || 'Temp123!';
    
    // Resumen
    document.getElementById('summaryName').textContent = data.nombre || data.razonSocial || 'No disponible';
    document.getElementById('summaryDoc').textContent = data.nit || data.numeroDocumento || 'No disponible';
    document.getElementById('summaryType').textContent = data.tipoCliente === 'Natural' ? 'Persona Natural' : 'Persona Jurídica';
    document.getElementById('summaryEmail').textContent = data.email || 'No disponible';
    
    // Detalles
    document.getElementById('submissionId').textContent = data.id || 'N/A';
    document.getElementById('submissionDate').textContent = formatDate(data.fechaEnvio || new Date());
    document.getElementById('summaryCity').textContent = data.ciudad || 'No disponible';
    document.getElementById('summaryActivity').textContent = data.actividadEconomica || 'No disponible';
}

// ============================================
// MOSTRAR DATOS DE DEMOSTRACIÓN
// ============================================
function showDemoData() {
    const demoData = {
        email: 'usuario@ejemplo.com',
        tempPassword: 'Temp123!',
        nombre: 'Empresa Demo S.A.S',
        razonSocial: 'Empresa Demo S.A.S',
        nit: '900.123.456-7',
        tipoCliente: 'Juridica',
        id: 'SOL-2024-001',
        fechaEnvio: new Date().toISOString(),
        ciudad: 'Bogotá',
        actividadEconomica: 'Comercio al por mayor'
    };
    
    populateDashboard(demoData);
}

// ============================================
// COPIAR AL PORTAPAPELES
// ============================================
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    element.select();
    element.setSelectionRange(0, 99999); // Para móviles
    
    navigator.clipboard.writeText(element.value).then(() => {
        // Cambiar texto del botón temporalmente
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
// COMPLETAR DATOS DE FIRMA AUTOMÁTICAMENTE
// ============================================
function populateSignatureFields() {
    const today = new Date();
    const months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    
    // Ciudad (puedes obtenerla del resumen)
    const city = document.getElementById('summaryCity').textContent || '_____________';
    document.getElementById('firmaCiudad').textContent = city;
    
    // Fecha actual
    const day = today.getDate();
    const month = months[today.getMonth()];
    const year = today.getFullYear();
    
    // Nombre (puedes obtenerlo del resumen)
    const name = document.getElementById('summaryName').textContent || '_________________________';
    document.getElementById('firmaNombre').textContent = name;
    
    // Documento (puedes obtenerlo del resumen)
    const doc = document.getElementById('summaryDoc').textContent || '_________________________';
    document.getElementById('firmaDocumento').textContent = doc;
}

// ============================================
// EXPORTAR PARA USO GLOBAL
// ============================================
window.copyToClipboard = copyToClipboard;
window.logout = logout;