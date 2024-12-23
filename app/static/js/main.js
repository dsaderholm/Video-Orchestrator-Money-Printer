document.addEventListener('DOMContentLoaded', function() {
    // API Configuration Handling
    const apiForm = document.getElementById('api-config-form');
    if (apiForm) {
        apiForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(apiForm);
            try {
                const response = await fetch('/api/config/save', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                showNotification(result.success ? 'success' : 'error', result.message);
            } catch (error) {
                showNotification('error', 'Failed to save API configuration');
            }
        });
    }

    // Schedule Management
    const scheduleForm = document.getElementById('schedule-form');
    if (scheduleForm) {
        scheduleForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(scheduleForm);
            try {
                const response = await fetch('/api/schedule/save', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                showNotification(result.success ? 'success' : 'error', result.message);
            } catch (error) {
                showNotification('error', 'Failed to save schedule');
            }
        });
    }

    // Test API Connection
    const testButtons = document.querySelectorAll('.test-api-button');
    testButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const apiId = button.dataset.apiId;
            try {
                const response = await fetch(`/api/test/${apiId}`);
                const result = await response.json();
                showNotification(result.success ? 'success' : 'error', result.message);
            } catch (error) {
                showNotification('error', 'Failed to test API connection');
            }
        });
    });
});

// Utility Functions
function showNotification(type, message) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Dynamic Form Field Generation
function addApiField() {
    const container = document.getElementById('api-fields');
    const fieldIndex = container.children.length;
    const fieldHTML = `
        <div class="form-group api-field">
            <input type="text" name="fields[${fieldIndex}][name]" class="input" placeholder="Field Name" required>
            <input type="text" name="fields[${fieldIndex}][value]" class="input" placeholder="Field Value" required>
            <button type="button" class="button remove-field" onclick="removeApiField(this)">Remove</button>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', fieldHTML);
}

function removeApiField(button) {
    button.parentElement.remove();
}

// Schedule Management
function updateScheduleStatus(scheduleId, status) {
    const indicator = document.querySelector(`#schedule-${scheduleId} .status-indicator`);
    indicator.className = `status-indicator status-${status}`;
}