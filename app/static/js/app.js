/**
 * Knowledge Base - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Initialize Bootstrap popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Search autocomplete (if search input exists)
    const searchInput = document.querySelector('input[type="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();

            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    // Implement search suggestions
                    fetchSearchSuggestions(query);
                }, 300);
            }
        });
    }

    // File upload drag and drop
    const uploadArea = document.querySelector('.upload-area');
    if (uploadArea) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('dragover');
            }, false);
        });

        uploadArea.addEventListener('drop', handleDrop, false);
        uploadArea.addEventListener('click', () => {
            const fileInput = document.querySelector('#file-input');
            if (fileInput) fileInput.click();
        });
    }

    // Markdown preview (if editor exists)
    const markdownEditor = document.querySelector('#markdown-editor');
    const markdownPreview = document.querySelector('#markdown-preview');
    if (markdownEditor && markdownPreview) {
        let previewTimeout;
        markdownEditor.addEventListener('input', function() {
            clearTimeout(previewTimeout);
            previewTimeout = setTimeout(() => {
                updateMarkdownPreview(this.value, markdownPreview);
            }, 500);
        });
    }

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-delete') || 'Are you sure you want to delete this item?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-copy');
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                copyToClipboard(targetElement.textContent || targetElement.value);
                showToast('Copied to clipboard!');
            }
        });
    });

    // Theme toggle
    const themeToggle = document.querySelector('#theme-toggle');
    if (themeToggle) {
        const currentTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-bs-theme', currentTheme);

        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
});

// Helper Functions

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

function handleFiles(files) {
    [...files].forEach(uploadFile);
}

function uploadFile(file) {
    // Implement file upload
    console.log('Uploading file:', file.name);
    // This would typically make an API call to upload the file
}

function fetchSearchSuggestions(query) {
    // Implement search suggestions API call
    fetch(`/api/v1/search/suggestions?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            // Display suggestions
            console.log('Search suggestions:', data);
        })
        .catch(error => console.error('Error fetching suggestions:', error));
}

function updateMarkdownPreview(markdown, previewElement) {
    // Simple markdown preview (in production, use server-side rendering)
    // This is a placeholder - actual implementation would use a markdown parser
    fetch('/api/v1/markdown/preview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ markdown: markdown })
    })
    .then(response => response.json())
    .then(data => {
        previewElement.innerHTML = data.html || markdown;
    })
    .catch(error => {
        console.error('Error updating preview:', error);
        // Fallback to showing raw markdown
        previewElement.textContent = markdown;
    });
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text);
    } else {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }
}

function showToast(message, type = 'success') {
    // Create and show a Bootstrap toast notification
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    const toastElement = document.createElement('div');
    toastElement.innerHTML = toastHTML;
    const toast = toastElement.firstElementChild;
    toastContainer.appendChild(toast);

    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Export functions for use in other scripts
window.KnowledgeBase = {
    showToast,
    copyToClipboard,
    fetchSearchSuggestions,
    updateMarkdownPreview
};