document.addEventListener('DOMContentLoaded', () => {
    initializeForm();
});

function initializeForm() {
    loadReferenceData();
    setupToggleLogic();
    setupRiskMonitoring();
    document.getElementById('vinculacionForm').addEventListener('submit', handleFormSubmission);
}

async function loadReferenceData() {
    try {
        const [citiesRes, countriesRes, ciiuRes] = await Promise.all([
            fetch('/api/city'),
            fetch('/api/country'),
            fetch('/api/ciiu')
        ]);

        const [cities, countries, ciiu] = await Promise.all([
            citiesRes.json(),
            countriesRes.json(),
            ciiuRes.json()
        ]);

        populateSelect('ciudad', (cities.message || []).map(c => ({ value: c.id_city, text: c.name })));
        populateSelect('paisOrigen', (countries.message || []).map(c => ({ value: c.id_country, text: c.country_name })));
        populateSelect('paisResidencia', (countries.message || []).map(c => ({ value: c.id_country, text: c.country_name })));
        
        // CIIU de ejemplo si no existe el endpoint
        const ciiuData = ciiu.message || [
            { codigo: "0111", descripcion: "Cultivo de cereales" },
            { codigo: "4711", descripcion: "Comercio al por menor" }
        ];
        populateSelect('codigoCIIU', ciiuData.map(c => ({ value: c.codigo, text: `${c.codigo} - ${c.descripcion}` })));
    } catch (error) {
        console.error('Error cargando datos de referencia:', error);
    }
}

function populateSelect(elementId, options) {
    const select = document.getElementById(elementId);
    if (!select) return;
    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt.value;
        option.textContent = opt.text;
        select.appendChild(option);
    });
}

function setupToggleLogic() {
    const radios = document.querySelectorAll('input[name="tipoPersona"]');
    radios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            const isJuridica = e.target.value === 'juridica';
            document.querySelectorAll('.natural-only').forEach(el => el.classList.toggle('hidden', isJuridica));
            document.querySelectorAll('.juridica-only').forEach(el => el.classList.toggle('hidden', !isJuridica));
            
            const tipoId = document.getElementById('tipoId');
            if (isJuridica) {
                tipoId.value = 'NIT';
                tipoId.disabled = true;
            } else {
                tipoId.disabled = false;
                tipoId.value = 'CC';
            }
        });
    });
}

function setupRiskMonitoring() {
    ['paisOrigen', 'ciudad', 'codigoCIIU'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', calculateRisk);
    });
}

function calculateRisk() {
    const pais = document.getElementById('paisOrigen').value;
    const ciudad = document.getElementById('ciudad').value;
    const ciiu = document.getElementById('codigoCIIU').value;

    if (!pais || !ciudad || !ciiu) {
        document.getElementById('riskAlert').style.display = 'none';
        return;
    }

    const riskLevels = { pais: 0.375, ciudad: 0.5, ciiu: 0.25 };
    const totalRisk = (riskLevels.pais + riskLevels.ciudad + riskLevels.ciiu) / 3;

    const alertBox = document.getElementById('riskAlert');
    let level = 'BAJO';
    if (totalRisk >= 0.75) level = 'EXTREMO';
    else if (totalRisk >= 0.5) level = 'ALTO';
    else if (totalRisk >= 0.25) level = 'MODERADO';

    alertBox.style.display = 'flex';
    alertBox.className = `alert-box ${level === 'EXTREMO' || level === 'ALTO' ? 'alert-warning' : 'alert-success'}`;
    alertBox.textContent = `Nivel de Riesgo Estimado: ${level} (Requiere ${level === 'EXTREMO' || level === 'ALTO' ? 'diligencia ampliada' : 'revisión estándar'})`;
}

async function handleFormSubmission(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Procesando...';
    submitBtn.disabled = true;

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    data.person_type = form.querySelector('input[name="tipoPersona"]:checked').value;
    data.submitted_at = new Date().toISOString();

    try {
        const response = await fetch('/api/submissions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error en el servidor');
        }

        const result = await response.json();
        window.location.href = `/admin/confirmacion?id=${result.submission_id}`;
    } catch (error) {
        console.error('Error al enviar:', error);
        alert(`Error al procesar la solicitud: ${error.message}`);
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}