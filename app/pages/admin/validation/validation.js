(function() {
    'use strict';

    const API_BASE = '/api';
    const authToken = localStorage.getItem('token');

    if (!authToken) {
        alert('Debes iniciar sesión primero');
        window.location.href = '/login';
    }

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

    const headers = () => ({
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
    });

    function init() {
        loadSubmissions();
        bindEvents();
    }

    function bindEvents() {
        document.getElementById('applyFilters').addEventListener('click', applyFilters);
        document.getElementById('resetFilters').addEventListener('click', resetFilters);
        document.getElementById('exportExcel').addEventListener('click', exportToExcel);
        document.getElementById('closeModal').addEventListener('click', closeModal);
        document.getElementById('cancelValidation').addEventListener('click', closeModal);
        document.getElementById('saveValidation').addEventListener('click', saveValidation);
        document.getElementById('validationStatus').addEventListener('change', updateVigenciaOptions);
        document.getElementById('logoutBtn').addEventListener('click', logout);
    }

    async function loadSubmissions() {
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '<tr><td colspan="7" class="loading-state">Cargando solicitudes...</td></tr>';

        try {
            const params = new URLSearchParams();
            if (state.filters.status) params.set('status_filter', state.filters.status);
            if (state.filters.risk) params.set('risk', state.filters.risk);
            if (state.filters.dateFrom) params.set('date_from', state.filters.dateFrom);
            if (state.filters.dateTo) params.set('date_to', state.filters.dateTo);
            if (state.filters.search) params.set('search', state.filters.search);

            const qs = params.toString();
            const res = await fetch(`${API_BASE}/submissions${qs ? `?${qs}` : ''}`, { headers: headers() });
            if (!res.ok) throw new Error('Error al cargar solicitudes');

            const data = await res.json();
            const list = data.submissions || data.message || [];
            state.submissions = filterLocal(list);
            renderTable(state.submissions);
        } catch (error) {
            console.error(error);
            tbody.innerHTML = `<tr><td colspan="7" class="loading-state" style="color: var(--danger)">Error al cargar datos. Verifique la API.</td></tr>`;
        }
    }

    // Filtros adicionales que la API no soporta (fechas y búsqueda por texto)
    function filterLocal(list) {
        const { dateFrom, dateTo, search } = state.filters;
        return list.filter(sub => {
            if (dateFrom && sub.created_at && new Date(sub.created_at) < new Date(dateFrom)) return false;
            if (dateTo && sub.created_at && new Date(sub.created_at) > new Date(dateTo + 'T23:59:59')) return false;
            if (search) {
                const haystack = [
                    sub.nombre, sub.nombres, sub.razon_social,
                    sub.numero_id, String(sub.id), sub.codigo_ciiu, sub.oficina
                ].filter(Boolean).join(' ').toLowerCase();
                if (!haystack.includes(search.toLowerCase())) return false;
            }
            return true;
        });
    }

    const STATUS_TEXT = {
        'borrador': 'Borrador',
        'pendiente_revision': 'Pendiente de Revisión',
        'en_revision': 'En Revisión',
        'aprobado': 'Aprobado',
        'rechazado': 'Rechazado',
        'completado': 'Completado'
    };

    const RISK_TEXT = {
        'bajo': 'BAJO', 'medio': 'MEDIO', 'moderado': 'MODERADO',
        'alto': 'ALTO', 'extremo': 'EXTREMO'
    };

    function renderTable(data) {
        const tbody = document.getElementById('tableBody');
        if (!data.length) {
            tbody.innerHTML = '<tr><td colspan="7" class="loading-state">No se encontraron solicitudes.</td></tr>';
            return;
        }

        tbody.innerHTML = data.map(sub => {
            const nombre = sub.nombre || sub.razon_social ||
                [sub.nombres, sub.apellidos].filter(Boolean).join(' ') || 'Sin nombre';
            const tipo = sub.tipo_persona === 'juridica' ? 'Jurídica' : 'Natural';
            const riesgo = sub.risk_level ? RISK_TEXT[sub.risk_level.toLowerCase()] || sub.risk_level : 'N/A';
            const estado = STATUS_TEXT[sub.status] || sub.status || 'Pendiente';
            const riesgoCls = (sub.risk_level || 'sin').toLowerCase();
            const estadoCls = (sub.status || 'pendiente').toLowerCase();

            return `
                <tr>
                    <td>${sub.id}</td>
                    <td>${nombre}</td>
                    <td>${tipo}</td>
                    <td><span class="badge badge-${riesgoCls}">${riesgo}</span></td>
                    <td><span class="badge badge-${estadoCls}">${estado}</span></td>
                    <td>${formatDate(sub.created_at)}</td>
                    <td><button class="btn-action" onclick="window.ValidationManager.openValidation(${sub.id})">Validar</button></td>
                </tr>
            `;
        }).join('');
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
            const res = await fetch(`${API_BASE}/submissions/${id}`, { headers: headers() });
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
        const esJuridica = data.tipo_persona === 'juridica';
        const nombre = data.nombre || data.razon_social ||
            [data.nombres, data.apellidos].filter(Boolean).join(' ') || 'N/A';
        const f = data.form_data || {};

        document.getElementById('detailType').textContent = esJuridica ? 'Persona Jurídica' : 'Persona Natural';
        document.getElementById('detailClient').textContent = data.tipo_cliente || 'N/A';
        document.getElementById('detailName').textContent = nombre;
        document.getElementById('detailDoc').textContent = data.numero_id || 'N/A';
        document.getElementById('detailEmail').textContent = f.email || f.correo_natural || data.email || 'N/A';

        const risk = (data.risk_level || 'MODERADO').toUpperCase();
        const riskBadge = document.getElementById('detailRisk');
        riskBadge.textContent = RISK_TEXT[risk.toLowerCase()] || risk;
        riskBadge.className = `badge badge-${risk.toLowerCase()}`;

        document.getElementById('detailCountry').textContent = f.pais_origen_nombre || data.pais_origen_id || 'N/A';
        document.getElementById('detailCity').textContent = f.ciudad_nombre || f.ciudad_natural || f.ciudad_juridica || 'N/A';
        document.getElementById('detailCIIU').textContent = data.codigo_ciiu || f.codigo_ciiu || 'N/A';

        renderDocuments(data.documents || []);
        toggleEDD(risk);
    }

    function renderDocuments(docs) {
        const container = document.getElementById('documentsList');
        if (!docs.length) {
            container.innerHTML = '<p style="color: var(--text-muted); font-size: 0.85rem;">No se adjuntaron documentos.</p>';
            return;
        }

        container.innerHTML = docs.map(doc => {
            const fileName = doc.file_name || doc.document_type || 'Documento';
            return `
                <div class="doc-item">
                    <span>${doc.document_type} (${fileName})</span>
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

        // Mapear estado del select al valor esperado por la API
        const action = status === 'aprobado' ? 'APROBADO' :
                       status === 'rechazado' ? 'RECHAZADO' : 'APROBADO';

        const params = new URLSearchParams();
        params.set('action', action);
        if (observations) params.set('comments', observations);

        try {
            const res = await fetch(`${API_BASE}/submissions/${state.currentId}/validate?${params.toString()}`, {
                method: 'PUT',
                headers: headers()
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

    // ============================================
    // EXPORTAR A EXCEL (CSV con separador ; compatible con Excel es-CO)
    // ============================================
    function exportToExcel() {
        const data = state.submissions;
        if (!data.length) {
            alert('No hay datos para exportar.');
            return;
        }

        const f = (obj, key) => {
            const v = obj && obj[key];
            return v === null || v === undefined ? '' : v;
        };

        // Cabeceras
        const headers = [
            'ID Solicitud', 'Fecha', 'Tipo de Persona', 'Tipo de Cliente', 'Tipo de Vinculación',
            'Nombre / Razón Social', 'Nombres', 'Apellidos', 'NIT / Documento', 'Tipo Documento',
            'Oficina / Sucursal', 'Ciudad', 'Código CIIU', 'Actividad Económica',
            'Correo', 'Teléfono', 'Régimen Tributario',
            'Total Ingresos', 'Total Egresos', 'Total Activos', 'Total Pasivos', 'Total Patrimonio',
            'Representante Legal', 'NIT Representante', 'Tipo Sociedad',
            'Beneficiarios', 'Accionistas', 'Riesgo', 'Estado'
        ];

        const rows = data.map(sub => {
            const fd = sub.form_data || {};
            const nombre = sub.nombre || [sub.nombres, sub.apellidos].filter(Boolean).join(' ');
            const beneficiarios = (fd.beneficiarios || [])
                .map(b => `${b.nombre} (${b.numero_doc || ''})`).join(' | ');
            const accionistas = (fd.accionistas || [])
                .map(a => `${a.nombre} ${a.participacion ? a.participacion + '%' : ''}`).join(' | ');

            return [
                f(sub, 'id'),
                sub.created_at ? new Date(sub.created_at).toLocaleString('es-CO') : '',
                sub.tipo_persona === 'juridica' ? 'Jurídica' : 'Natural',
                f(sub, 'tipo_cliente'),
                f(sub, 'tipo_vinculacion'),
                nombre,
                f(sub, 'nombres'),
                f(sub, 'apellidos'),
                f(sub, 'numero_id'),
                f(sub, 'tipo_id'),
                f(sub, 'oficina'),
                f(fd, 'ciudad_nombre') || f(fd, 'ciudad_natural') || f(fd, 'ciudad_juridica'),
                f(sub, 'codigo_ciiu'),
                f(fd, 'actividad_economica'),
                f(fd, 'email') || f(fd, 'correo_natural'),
                f(fd, 'telefono_natural'),
                f(sub, 'regimen_tributario'),
                f(sub, 'total_ingresos'),
                f(sub, 'total_egresos'),
                f(fd, 'total_activos'),
                f(fd, 'total_pasivos'),
                f(fd, 'total_patrimonio'),
                f(fd, 'representante_legal'),
                f(fd, 'numero_doc_rep'),
                f(fd, 'tipo_sociedad'),
                beneficiarios,
                accionistas,
                sub.risk_level ? RISK_TEXT[sub.risk_level.toLowerCase()] || sub.risk_level : 'N/A',
                STATUS_TEXT[sub.status] || sub.status || 'Pendiente'
            ];
        });

        const escapeCell = cell => {
            const s = String(cell === null || cell === undefined ? '' : cell);
            return /[";\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
        };

        const csv = '\uFEFF' + [headers, ...rows]
            .map(row => row.map(escapeCell).join(';'))
            .join('\r\n');

        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        const hoy = new Date().toISOString().slice(0, 10);
        a.href = url;
        a.download = `vinculaciones_${hoy}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    function logout() {
        if (confirm('¿Confirmar cierre de sesión?')) {
            localStorage.clear();
            window.location.href = '/login';
        }
    }

    // Exponer métodos necesarios al alcance global para onclick en tabla
    window.ValidationManager = { openValidation };

    // Inicializar
    document.addEventListener('DOMContentLoaded', init);
})();