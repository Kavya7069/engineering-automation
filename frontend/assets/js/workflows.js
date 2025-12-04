
let currentWorkflow = null;
let executionHistory = [];

function selectWorkflow(workflowType) {
    currentWorkflow = workflowType;
    document.getElementById('noWorkflowSelected').classList.add('hidden');
    document.getElementById('workflowForm').classList.remove('hidden');
    
    document.querySelectorAll('[id$="_form"]').forEach(el => {
        el.classList.remove('active');
    });
    document.getElementById(`${workflowType}_form`).classList.add('active');
}

async function executeWorkflow(workflowType) {
    const button = event.target;
    button.disabled = true;
    
    try {
        let response;
        
        switch(workflowType) {
            case 'csv_processing':
                const fileInput = document.getElementById('csvFile');
                if (!fileInput.files.length) {
                    showError('Please select a CSV file');
                    button.disabled = false;
                    return;
                }
                showLoading(button);
                response = await WorkflowAPI.callCSVProcessing(
                    fileInput.files[0],
                    document.getElementById('csvOperation').value
                );
                break;

            case 'file_conversion':
                showLoading(button);
                response = await WorkflowAPI.callFileConversion(
                    document.getElementById('sourceFormat').value,
                    document.getElementById('targetFormat').value,
                    document.getElementById('conversionData').value
                );
                break;

            case 'api_integration':
                showLoading(button);
                response = await WorkflowAPI.callAPIIntegration(
                    document.getElementById('apiEndpoint').value,
                    document.getElementById('apiMethod').value,
                    JSON.parse(document.getElementById('apiParams').value || '{}')
                );
                break;

            case 'report_generation':
                showLoading(button);
                response = await WorkflowAPI.callReportGeneration(
                    document.getElementById('reportTitle').value,
                    JSON.parse(document.getElementById('reportData').value || '{}'),
                    document.getElementById('reportFormat').value
                );
                break;
        }

        const result = await response.json();

        if (response.ok) {
            displayOutput(result, 'success');
            addToHistory(workflowType, 'completed', result);
        } else {
            showError(result.detail || 'Workflow execution failed');
            addToHistory(workflowType, 'failed', result);
        }
    } catch (error) {
        showError(`Error: ${error.message}`);
        addToHistory(workflowType, 'error', { error: error.message });
    } finally {
        button.disabled = false;
        button.innerHTML = button.getAttribute('data-original-text') || 'Execute Workflow';
    }
}

function showLoading(button) {
    button.setAttribute('data-original-text', button.innerHTML);
    button.innerHTML = '<div class="loading-spinner"></div>Processing...';
    button.disabled = true;
}

function displayOutput(data, status) {
    document.getElementById('workflowOutput').classList.remove('hidden');
    const output = document.getElementById('outputContent');
    output.textContent = JSON.stringify(data, null, 2);

    const statusMsg = document.getElementById('statusMessage');
    statusMsg.classList.remove('hidden', 'error-message', 'success-message');
    if (status === 'success') {
        statusMsg.classList.add('success-message');
        statusMsg.textContent = '✓ Workflow executed successfully';
    } else {
        statusMsg.classList.add('error-message');
        statusMsg.textContent = '✗ Workflow execution failed';
    }
}

function showError(message) {
    document.getElementById('workflowOutput').classList.remove('hidden');
    const statusMsg = document.getElementById('statusMessage');
    statusMsg.classList.remove('hidden', 'error-message', 'success-message');
    statusMsg.classList.add('error-message');
    statusMsg.textContent = `✗ ${message}`;
}

function clearOutput() {
    document.getElementById('workflowOutput').classList.add('hidden');
    document.getElementById('statusMessage').classList.add('hidden');
    document.getElementById('outputContent').textContent = '';
}

function addToHistory(workflow, status, result) {
    const timestamp = new Date().toLocaleTimeString();
    const statusClass = status === 'completed' ? 'status-success' : status === 'failed' ? 'status-error' : 'status-pending';
    const statusText = status.charAt(0).toUpperCase() + status.slice(1);
    
    const historyItem = document.createElement('div');
    historyItem.style.padding = 'var(--space-12)';
    historyItem.style.borderBottom = '1px solid rgba(94, 82, 64, 0.15)';
    historyItem.style.fontSize = '13px';
    historyItem.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-4);">
            <strong>${workflow}</strong>
            <span class="status-badge ${statusClass}">${statusText}</span>
        </div>
        <div style="color: var(--color-text-secondary);">${timestamp}</div>
    `;
    
    const history = document.getElementById('executionHistory');
    if (history.textContent.includes('No workflows')) {
        history.innerHTML = '';
    }
    history.insertBefore(historyItem, history.firstChild);
    
    if (history.children.length > 10) {
        history.removeChild(history.lastChild);
    }
}
