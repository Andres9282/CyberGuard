// script.js - CyberGuard Dashboard (Versión Integrada)
class CyberGuardDashboard {
    constructor() {
        this.currentPage = 'dashboard';
        this.currentCase = null;
        this.cases = [];
        this.autoRefreshInterval = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.startAutoRefresh();
        this.updateCurrentTime();
    }

    setupEventListeners() {
        // Navegación del sidebar
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', () => {
                const page = item.dataset.page;
                this.showPage(page);
            });
        });

        // Actualizar hora cada minuto
        setInterval(() => this.updateCurrentTime(), 60000);

        // Cerrar modal al hacer clic fuera
        document.getElementById('reportModal').addEventListener('click', (e) => {
            if (e.target === document.getElementById('reportModal')) {
                this.closeReport();
            }
        });
    }

    async loadInitialData() {
        await Promise.all([
            this.loadSystemStatus(),
            this.loadCases()
        ]);
    }

    async loadSystemStatus() {
        try {
            const response = await fetch('/api/status');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            this.updateSystemStatus(data);
        } catch (error) {
            console.error('Error loading system status:', error);
            this.updateSystemStatus({
                status: 'ERROR',
                message: 'Error de conexión con el servidor'
            });
        }
    }

    async loadCases() {
        try {
            const response = await fetch('/api/cases');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            // Si la respuesta es un array, usarlo directamente
            // Si es un objeto con propiedad cases, usar esa propiedad
            this.cases = Array.isArray(data) ? data : (data.cases || []);
            this.renderCases();
            this.updateIncidentsCount();
        } catch (error) {
            console.error('Error loading cases:', error);
            this.cases = [];
            this.renderCases();
            this.updateIncidentsCount();
        }
    }

    async loadCaseDetail(caseId) {
        try {
            const response = await fetch(`/api/cases/${caseId}`);
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('Caso no encontrado');
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const caseData = await response.json();
            
            if (caseData.error) {
                throw new Error(caseData.error);
            }

            this.currentCase = caseData;
            this.showCaseDetail(caseData);
        } catch (error) {
            console.error('Error loading case detail:', error);
            alert('Error cargando detalles del caso: ' + error.message);
        }
    }

    updateSystemStatus(statusData) {
        // Actualizar sidebar
        const statusDot = document.getElementById('sidebarStatusDot');
        const statusText = document.getElementById('sidebarStatusText');
        const lastUpdate = document.getElementById('lastUpdate');
        
        statusDot.className = 'status-dot ' + this.getStatusClass(statusData.status);
        statusText.textContent = this.getStatusText(statusData.status);
        lastUpdate.textContent = 'Actualizado: ' + new Date().toLocaleTimeString();

        // Actualizar estado principal
        document.getElementById('systemStatusValue').textContent = this.getStatusText(statusData.status);
        document.getElementById('systemStatusDescription').textContent = statusData.message || '';
    }

    renderCases() {
        this.renderRecentIncidents();
        this.renderAllIncidents();
        this.updateActiveIncidentsCount();
    }

    renderRecentIncidents() {
        const container = document.getElementById('recentIncidents');
        const recentCases = this.cases.slice(0, 5);

        if (recentCases.length === 0) {
            container.innerHTML = `
                <div class="no-data">
                    <i class="fas fa-check-circle"></i>
                    <span>No hay incidentes recientes</span>
                </div>
            `;
            return;
        }

        container.innerHTML = recentCases.map(caseItem => `
            <div class="incident-item" onclick="dashboard.loadCaseDetail(${caseItem.id})">
                <div class="incident-header">
                    <div class="incident-title">${this.escapeHtml(caseItem.proceso || 'Proceso desconocido')}</div>
                    <div class="incident-badge ${this.getSeverityClass(caseItem.gravedad)}">
                        ${this.getSeverityText(caseItem.gravedad)}
                    </div>
                </div>
                <div class="incident-details">
                    <div class="incident-detail">
                        <i class="fas fa-calendar"></i>
                        ${this.formatDate(caseItem.fecha)}
                    </div>
                    <div class="incident-detail">
                        <i class="fas fa-globe"></i>
                        ${this.escapeHtml(caseItem.ip || 'N/A')}
                    </div>
                    <div class="incident-detail">
                        <i class="fas fa-bug"></i>
                        ${this.escapeHtml(caseItem.tipo_ataque || 'Amenaza desconocida')}
                    </div>
                </div>
            </div>
        `).join('');
    }

    renderAllIncidents() {
        const container = document.getElementById('allIncidents');

        if (this.cases.length === 0) {
            container.innerHTML = `
                <div class="no-data">
                    <i class="fas fa-search"></i>
                    <span>No se encontraron incidentes</span>
                </div>
            `;
            return;
        }

        container.innerHTML = this.cases.map(caseItem => `
            <div class="incident-card" onclick="dashboard.loadCaseDetail(${caseItem.id})">
                <div class="incident-card-header">
                    <div class="incident-card-id">Caso #${caseItem.id}</div>
                    <div class="incident-card-severity ${this.getSeverityClass(caseItem.gravedad)}">
                        ${this.getSeverityText(caseItem.gravedad)}
                    </div>
                </div>
                <div class="incident-card-details">
                    <div class="incident-detail-item">
                        <div class="incident-detail-label">Fecha</div>
                        <div class="incident-detail-value">${this.formatDateTime(caseItem.fecha)}</div>
                    </div>
                    <div class="incident-detail-item">
                        <div class="incident-detail-label">Proceso</div>
                        <div class="incident-detail-value">${this.escapeHtml(caseItem.proceso || 'N/A')}</div>
                    </div>
                    <div class="incident-detail-item">
                        <div class="incident-detail-label">IP</div>
                        <div class="incident-detail-value">${this.escapeHtml(caseItem.ip || 'N/A')}</div>
                    </div>
                    <div class="incident-detail-item">
                        <div class="incident-detail-label">Tipo</div>
                        <div class="incident-detail-value">${this.escapeHtml(caseItem.tipo_ataque || 'Desconocido')}</div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    showCaseDetail(caseData) {
        this.currentCase = caseData;
        document.getElementById('caseIdHeader').textContent = caseData.id;
        
        const content = document.getElementById('caseDetailContent');
        content.innerHTML = this.generateCaseDetailHTML(caseData);
        
        this.showPage('case-detail');
    }

    generateCaseDetailHTML(caseData) {
        return `
            <div class="detail-section">
                <h3>Resumen del Ataque</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">Fecha y Hora</div>
                        <div class="detail-value">${this.formatDateTime(caseData.fecha)}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Gravedad</div>
                        <div class="detail-value">
                            <span class="incident-badge ${this.getSeverityClass(caseData.gravedad)}">
                                ${this.getSeverityText(caseData.gravedad)}
                            </span>
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Tipo de Ataque</div>
                        <div class="detail-value">${this.escapeHtml(caseData.tipo_ataque || 'Desconocido')}</div>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>Proceso Identificado</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">Nombre del Proceso</div>
                        <div class="detail-value">${this.escapeHtml(caseData.proceso || 'N/A')}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">PID</div>
                        <div class="detail-value">${caseData.pid || 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Ruta de Ejecución</div>
                        <div class="detail-value">${this.escapeHtml(caseData.ruta_proceso || 'N/A')}</div>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>Conexión de Red</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">IP Remota</div>
                        <div class="detail-value">${this.escapeHtml(caseData.ip || 'N/A')}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Puerto</div>
                        <div class="detail-value">${caseData.puerto || 'N/A'}</div>
                    </div>
                </div>
            </div>

            ${caseData.archivos_afectados && caseData.archivos_afectados.length > 0 ? `
            <div class="detail-section">
                <h3>Archivos Afectados</h3>
                <div class="detail-grid">
                    ${caseData.archivos_afectados.map(file => `
                        <div class="detail-item">
                            <div class="detail-label">Archivo</div>
                            <div class="detail-value">${this.escapeHtml(file.ruta)}</div>
                            <div class="detail-label">Hash</div>
                            <div class="detail-value" style="font-family: monospace; font-size: 11px;">${this.escapeHtml(file.hash)}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}

            <div class="detail-section">
                <h3>Acciones Tomadas</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">Proceso Terminado</div>
                        <div class="detail-value">${caseData.proceso_terminado ? '✅ SÍ' : '❌ NO'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">IP Bloqueada</div>
                        <div class="detail-value">${caseData.ip_bloqueada ? '✅ SÍ' : '❌ NO'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Usuario Deshabilitado</div>
                        <div class="detail-value">${caseData.usuario_deshabilitado ? '✅ SÍ' : '❌ NO'}</div>
                    </div>
                </div>
            </div>

            <button class="btn btn-primary" onclick="dashboard.generateReport()" style="margin-top: 24px;">
                <i class="fas fa-file-pdf"></i>
                Generar Informe para Fiscalía
            </button>
        `;
    }

    showPage(pageName) {
        // Ocultar todas las páginas
        document.querySelectorAll('.page-content').forEach(page => {
            page.classList.remove('active');
        });

        // Remover activo de todos los items de navegación
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });

        // Mostrar página seleccionada
        const targetPage = document.getElementById(`${pageName}-page`);
        if (targetPage) {
            targetPage.classList.add('active');
            this.currentPage = pageName;
        }

        // Activar item de navegación correspondiente
        const navItem = document.querySelector(`[data-page="${pageName}"]`);
        if (navItem) {
            navItem.classList.add('active');
        }

        // Actualizar título de página
        this.updatePageTitle(pageName);
        
        // Recargar datos si es necesario
        if (pageName === 'dashboard' || pageName === 'incidents') {
            this.loadCases();
        }
    }

    updatePageTitle(pageName) {
        const titles = {
            'dashboard': 'Dashboard de Seguridad',
            'incidents': 'Gestión de Incidentes',
            'reports': 'Reportes Forenses',
            'evidence': 'Evidencias Recolectadas',
            'case-detail': 'Detalle del Incidente'
        };

        const descriptions = {
            'dashboard': 'Monitoreo en tiempo real del sistema',
            'incidents': 'Historial y gestión de incidentes de seguridad',
            'reports': 'Generación y visualización de reportes',
            'evidence': 'Evidencias digitales recolectadas automáticamente',
            'case-detail': 'Análisis detallado del incidente'
        };

        document.getElementById('pageTitle').textContent = titles[pageName] || 'CyberGuard SV';
        document.getElementById('pageDescription').textContent = descriptions[pageName] || '';
    }

    updateIncidentsCount() {
        const count = this.cases.length;
        document.getElementById('incidentsCount').textContent = count;
    }

    updateActiveIncidentsCount() {
        const activeCount = this.cases.filter(caseItem => {
            const severity = (caseItem.gravedad || '').toLowerCase();
            return severity.includes('crítico') || severity.includes('critical') || 
                   severity.includes('alto') || severity.includes('high');
        }).length;
        document.getElementById('activeIncidentsCount').textContent = activeCount;
    }

    updateCurrentTime() {
        const now = new Date();
        document.getElementById('currentTime').textContent = now.toLocaleTimeString();
    }

    generateReport() {
        if (this.currentCase) {
            this.showReportModal(this.currentCase);
        } else {
            alert('Por favor, selecciona un incidente primero');
        }
    }

    showReportModal(caseData) {
        document.getElementById('reportContent').innerHTML = this.generateReportContent(caseData);
        document.getElementById('reportModal').style.display = 'flex';
    }

    generateReportContent(caseData) {
        return `
            <div class="detail-section">
                <h3>INFORME DE INCIDENTE - CYBERGUARD SV</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">Número de Caso</div>
                        <div class="detail-value">${caseData.id}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Fecha y Hora de Detección</div>
                        <div class="detail-value">${this.formatDateTime(caseData.fecha)}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Gravedad</div>
                        <div class="detail-value">${this.getSeverityText(caseData.gravedad)}</div>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>INFORMACIÓN TÉCNICA</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">Proceso Malicioso</div>
                        <div class="detail-value">${this.escapeHtml(caseData.proceso || 'N/A')}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">IP Remota</div>
                        <div class="detail-value">${this.escapeHtml(caseData.ip || 'N/A')}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Tipo de Ataque</div>
                        <div class="detail-value">${this.escapeHtml(caseData.tipo_ataque || 'Desconocido')}</div>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>MEDIDAS DE MITIGACIÓN</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">Proceso Terminado</div>
                        <div class="detail-value">${caseData.proceso_terminado ? 'SÍ' : 'NO'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">IP Bloqueada</div>
                        <div class="detail-value">${caseData.ip_bloqueada ? 'SÍ' : 'NO'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Usuario Deshabilitado</div>
                        <div class="detail-value">${caseData.usuario_deshabilitado ? 'SÍ' : 'NO'}</div>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>EVIDENCIAS PRESERVADAS</h3>
                <ul class="evidence-list">
                    <li class="evidence-item">Logs del sistema con timestamp del incidente</li>
                    <li class="evidence-item">Hashes criptográficos de archivos afectados</li>
                    <li class="evidence-item">Información de procesos maliciosos</li>
                    <li class="evidence-item">Registros de conexiones de red</li>
                    ${caseData.archivos_afectados && caseData.archivos_afectados.length > 0 ? 
                      '<li class="evidence-item">Archivos afectados preservados para análisis forense</li>' : ''}
                </ul>
            </div>

            <div class="timestamp" style="margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border-color); font-size: 12px; color: var(--light-gray);">
                Informe generado el: ${new Date().toLocaleString()}<br>
                Sistema CyberGuard SV - Plataforma de detección de ransomware
            </div>
        `;
    }

    closeReport() {
        document.getElementById('reportModal').style.display = 'none';
    }

    startAutoRefresh() {
        // Actualizar cada 3 segundos para ver ataques en tiempo real
        this.autoRefreshInterval = setInterval(() => {
            this.loadSystemStatus();
            if (this.currentPage === 'dashboard' || this.currentPage === 'incidents') {
                this.loadCases();
            }
        }, 3000);
    }

    // Helper methods
    getStatusClass(status) {
        const statusMap = {
            'NORMAL': 'safe',
            'ESCUDO': 'warning', 
            'ATAQUE': 'danger',
            'ERROR': 'danger'
        };
        return statusMap[status] || 'warning';
    }

    getStatusText(status) {
        const textMap = {
            'NORMAL': 'Sistema Normal',
            'ESCUDO': 'Modo Protección',
            'ATAQUE': 'Ataque Detectado!',
            'ERROR': 'Error de Conexión'
        };
        return textMap[status] || 'Conectando...';
    }

    getSeverityClass(gravedad) {
        const level = (gravedad || '').toLowerCase();
        if (level.includes('crítico') || level.includes('critical')) return 'badge-critical';
        if (level.includes('alto') || level.includes('high')) return 'badge-high';
        if (level.includes('medio') || level.includes('medium')) return 'badge-medium';
        return 'badge-low';
    }

    getSeverityText(gravedad) {
        const level = (gravedad || '').toLowerCase();
        if (level.includes('crítico') || level.includes('critical')) return 'CRÍTICO';
        if (level.includes('alto') || level.includes('high')) return 'ALTO';
        if (level.includes('medio') || level.includes('medium')) return 'MEDIO';
        return 'BAJO';
    }

    formatDate(dateString) {
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString();
        } catch {
            return 'Fecha inválida';
        }
    }

    formatDateTime(dateString) {
        try {
            const date = new Date(dateString);
            return date.toLocaleString();
        } catch {
            return 'Fecha inválida';
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Funciones globales
async function triggerScan() {
    try {
        const response = await fetch('/api/scan', { method: 'POST' });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        alert('✅ Escaneo de seguridad iniciado correctamente');
        dashboard.loadCases();
        dashboard.loadSystemStatus();
    } catch (error) {
        console.error('Error triggering scan:', error);
        alert('❌ Error iniciando escaneo: ' + error.message);
    }
}

function showPage(pageName) {
    dashboard.showPage(pageName);
}

function closeReport() {
    dashboard.closeReport();
}

function printReport() {
    if (dashboard.currentCase) {
        // Descargar PDF directamente
        window.open(`/api/report/${dashboard.currentCase.id}/pdf`, '_blank');
    } else {
        alert('Por favor, selecciona un incidente primero');
    }
}

function exportIncidents() {
    alert('📊 Función de exportación de incidentes activada');
}

function generateIncidentReport() {
    if (dashboard.currentCase) {
        dashboard.generateReport();
    } else {
        alert('Por favor, selecciona un incidente primero');
    }
}

function generateActivityReport() {
    alert('📈 Generando reporte de actividad del sistema...');
}

// Inicializar dashboard cuando la página cargue
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new CyberGuardDashboard();
});