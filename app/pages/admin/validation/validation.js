(function() {
    'use strict';

    const API_BASE = '/api';
    let state = {
        submissions: [],
        currentId: null,
        filters: {
            status: '',
            risk: '',
            dateFrom: '',
            dateTo: '',
            search: ''
        }
    };

    function init() {
        loadSubmissions();
        bindEvents();
    }

    function bindEvents() {
        document.getElementById('applyFilters').addEventListener('click', applyFilters);
        document.getElementById('resetFilters').addEventListener('click', resetFilters);
        document.getElementById('closeModal').addEventListener('click', closeModal);
        document.getElementById('cancelValidation').addEventListener('click', closeModal);
        document.getElementById('saveValidation').addEventListener('click', saveValidation);
        document.getElementById('validationStatus').addEventListener('change', updateVigenciaOptions);
    }

    async function loadSubmissions() {
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '<tr><td colspan="7" class="loading-state">Cargando solicitudes...</td></tr>';

        try {
            const params = new URLSearchParams(state.filters);
            const res = await fetch(`${API_BASE}/submissions?${params.toString()}`);
            if (!res.ok) throw new Error('Error al cargar solicitudes');
            
            state.submissions = await res.json();
            renderTable(state.submissions);
        } catch (error) {
            console.error(error);
            tbody.innerHTML = `<tr><td colspan="7" class="loading-state" style="color: var(--danger)">Error al cargar datos. Verifique la API.</td></tr>`;
        }
    }

    function renderTable(data) {
        const tbody = document.getElementById('tableBody');
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="loading-state">No se encontraron solicitudes.</td></tr>';
            return;
        }

        tbody.innerHTML = data.map(sub => `
            <tr>
                <td>${sub.id}</td>
                <td>${sub.personal_data?.razonSocial || sub.personal_data?.nombres || 'Sin nombre'}</td>
                <td>${sub.form_type === 'natural' ? 'Natural' : 'Jurídica'}</td>
                <td><span class="badge badge-${sub.risk_assessment?.nivel_riesgo?.toLowerCase()}">${sub.risk_assessment?.nivel_riesgo || 'N/A'}</span></td>
                <td><span class="badge badge-${sub.status?.toLowerCase()}">${sub.status || 'Pendiente'}</span></td>
                <td>${formatDate(sub.created_at)}</td>
                <td><button class="btn-action" onclick="window.ValidationManager.openValidation('${sub.id}')">Validar</button></td>
            </tr>
        `).join('');
    }

    function applyFilters() {
        state.filters.status = document.getElementById('filterStatus').value;
        state.filters.risk = document.getElementById('filterRisk').value;
        state.filters.dateFrom = document.getElementById('filterDateFrom').value;
        state.filters.dateTo = document.getElementById('filterDateTo').value;
        state.filters.search = document.getElementById('filterSearch').value.trim();
        loadSubmissions();
    }

    function resetFilters() {
        document.getElementById('filterStatus').value = '';
        document.getElementById('filterRisk').value = '';
        document.getElementById('filterDateFrom').value = '';
        document.getElementById('filterDateTo').value = '';
        document.getElementById('filterSearch').value = '';
        state.filters = { status: '', risk: '', dateFrom: '', dateTo: '', search: '' };
        loadSubmissions();
    }

    async function openValidation(id) {
        state.currentId = id;
        document.getElementById('validationModal').classList.remove('hidden');
        document.getElementById('modalTitle').textContent = `Validación: ${id}`;
        document.getElementById('tableBody').closest('.table-container').style.pointerEvents = 'none';

        try {
            const res = await fetch(`${API_BASE}/submissions/${id}`);
            if (!res.ok) throw new Error('No se pudo cargar el detalle');
            
            const data = await res.json();
            populateModal(data);
        } catch (error) {
            console.error(error);
            alert('Error al cargar los detalles de la solicitud');
            closeModal();
        }
    }

    function populateModal(data) {
        document.getElementById('detailType').textContent = data.form_type === 'natural' ? 'Persona Natural' : 'Persona Jurídica';
        document.getElementById('detailClient').textContent = data.client_type || 'N/A';
        document.getElementById('detailName').textContent = data.personal_data?.razonSocial || data.personal_data?.nombres || 'N/A';
        document.getElementById('detailDoc').textContent = data.personal_data?.nit || data.personal_data?.numeroIdentificacion || 'N/A';
        document.getElementById('detailEmail').textContent = data.personal_data?.correoElectronico || 'N/A';
        
        const risk = data.risk_assessment?.nivel_riesgo || 'MODERADO';
        const riskBadge = document.getElementById('detailRisk');
        riskBadge.textContent = risk;
        riskBadge.className = `badge badge-${risk.toLowerCase()}`;
        
        document.getElementById('detailCountry').textContent = data.risk_assessment?.paisRiesgo || 'N/A';
        document.getElementById('detailCity').textContent = data.risk_assessment?.ciudadRiesgo || 'N/A';
        document.getElementById('detailCIIU').textContent = data.risk_assessment?.codigoCIIU || 'N/A';

        renderDocuments(data.documents_status || []);
        toggleEDD(risk);
    }

    function renderDocuments(docs) {
        const container = document.getElementById('documentsList');
        if (!docs.length) {
            container.innerHTML = '<p style="color: var(--text-muted); font-size: 0.85rem;">No se adjuntaron documentos.</p>';
            return;
        }

        const today = new Date();
        container.innerHTML = docs.map(doc => {
            const expiryDate = doc.expiry_date ? new Date(doc.expiry_date) : null;
            let warning = '';
            if (expiryDate) {
                const daysDiff = Math.ceil((today - expiryDate) / (1000 * 60 * 60 * 24));
                if (daysDiff > 30) warning = '<span class="doc-warning">Expirado (>30 días)</span>';
            }
            return `
                <div class="doc-item">
                    <span>${doc.document_type} (${doc.file_name})</span>
                    ${warning}
                </div>
            `;
        }).join('');
    }

    function toggleEDD(risk) {
        const eddSection = document.getElementById('eddSection');
        if (risk === 'ALTO' || risk === 'EXTREMO') {
            eddSection.classList.remove('hidden');
        } else {
            eddSection.classList.add('hidden');
        }
    }

    function updateVigenciaOptions() {
        // Opcional: habilitar/deshabilitar vigencia según estado
    }

    function closeModal() {
        document.getElementById('validationModal').classList.add('hidden');
        state.currentId = null;
        document.getElementById('tableBody').closest('.table-container').style.pointerEvents = 'auto';
        clearForm();
    }

    function clearForm() {
        document.getElementById('chkDocsValid').checked = false;
        document.getElementById('chkListsVerified').checked = false;
        document.getElementById('listsDate').value = '';
        document.getElementById('validationStatus').value = '';
        document.getElementById('validationVigencia').value = '';
        document.getElementById('validationObservations').value = '';
        document.getElementById('eddStructure').value = '';
        document.getElementById('eddManagement').value = '';
        document.getElementById('eddGovRelation').value = '';
        document.querySelectorAll('input[name="eddCompliance"]').forEach(r => r.checked = false);
    }

    async function saveValidation() {
        const status = document.getElementById('validationStatus').value;
        const vigencia = document.getElementById('validationVigencia').value;
        const observations = document.getElementById('validationObservations').value.trim();
        const docsValid = document.getElementById('chkDocsValid').checked;
        const listsVerified = document.getElementById('chkListsVerified').checked;
        const listsDate = document.getElementById('listsDate').value;

        if (!status || !vigencia || !observations) {
            alert('Por favor complete los campos obligatorios de decisión administrativa.');
            return;
        }
        if (!docsValid || !listsVerified || !listsDate) {
            alert('Debe confirmar la validez documental y la verificación en listas restrictivas con fecha.');
            return;
        }

        const payload = {
            status: status,
            vigencia: vigencia,
            observations: observations,
            documentos_validados: docsValid,
            listas_restrictivas_verificadas: listsVerified,
            fecha_consulta_listas: listsDate,
            edd: {
                estructura: document.getElementById('eddStructure').value,
                gerencia: document.getElementById('eddManagement').value,
                relacion_gov: document.getElementById('eddGovRelation').value,
                programa_cumplimiento: document.querySelector('input[name="eddCompliance"]:checked')?.value || 'no'
            }
        };

        try {
            const res = await fetch(`${API_BASE}/submissions/${state.currentId}/validate`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                const errorData = await res.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Error al guardar validación');
            }

            alert('Validación guardada exitosamente.');
            closeModal();
            loadSubmissions();
        } catch (error) {
            console.error(error);
            alert('Error al guardar: ' + error.message);
        }
    }

    function formatDate(dateStr) {
        if (!dateStr) return '-';
        return new Date(dateStr).toLocaleDateString('es-CO');
    }

    // Exponer métodos necesarios al alcance global para onclick en tabla
    window.ValidationManager = { openValidation };

    // Inicializar
    document.addEventListener('DOMContentLoaded', init);
})();