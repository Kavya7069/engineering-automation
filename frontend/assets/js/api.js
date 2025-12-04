const API_BASE = 'http://localhost:8000/api';

class WorkflowAPI {
    static async callCSVProcessing(file, operation) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('operation', operation);
        
        return fetch(`${API_BASE}/workflows/csv-processing`, {
            method: 'POST',
            body: formData
        });
    }

    static async callFileConversion(sourceFormat, targetFormat, data) {
        return fetch(`${API_BASE}/workflows/file-conversion`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                source_format: sourceFormat,
                target_format: targetFormat,
                data: data
            })
        });
    }

    static async callAPIIntegration(endpoint, method, params) {
        return fetch(`${API_BASE}/workflows/api-integration`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                endpoint: endpoint,
                method: method,
                params: params
            })
        });
    }

    static async callReportGeneration(title, data, format) {
        return fetch(`${API_BASE}/workflows/report-generation`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                data: data,
                format: format
            })
        });
    }

    static async getHistory() {
        return fetch(`${API_BASE}/workflows/history`);
    }

    static async getHealth() {
        return fetch(`${API_BASE}/health`);
    }
}
