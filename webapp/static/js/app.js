// AI Calculator Web App - JavaScript

// Translations cache
let currentTranslations = {};
let currentLanguage = 'en';

// DOM Elements
const elements = {
    languageSelect: document.getElementById('language-select'),
    difficultySelect: document.getElementById('difficulty-select'),
    countInput: document.getElementById('count-input'),
    operationCheckboxes: document.querySelectorAll('.operation-checkbox'),
    generateBtn: document.getElementById('generate-btn'),
    clearBtn: document.getElementById('clear-btn'),
    exportJsonBtn: document.getElementById('export-json-btn'),
    exportCsvBtn: document.getElementById('export-csv-btn'),
    statusMessage: document.getElementById('status-message'),
    problemsList: document.getElementById('problems-list'),
    statTotal: document.getElementById('stat-total'),
    statAverage: document.getElementById('stat-average'),
    statMin: document.getElementById('stat-min'),
    statMax: document.getElementById('stat-max'),
    statDistribution: document.getElementById('stat-distribution'),
    appTitle: document.getElementById('app-title'),
    appSubtitle: document.getElementById('app-subtitle')
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadTranslations(currentLanguage);
});

// Initialize event listeners
function initializeEventListeners() {
    elements.languageSelect.addEventListener('change', handleLanguageChange);
    elements.generateBtn.addEventListener('click', handleGenerate);
    elements.clearBtn.addEventListener('click', handleClear);
    elements.exportJsonBtn.addEventListener('click', handleExportJson);
    elements.exportCsvBtn.addEventListener('click', handleExportCsv);
}

// Handle language change
async function handleLanguageChange(event) {
    const newLanguage = event.target.value;
    await loadTranslations(newLanguage);
}

// Load translations for a specific language
async function loadTranslations(language) {
    try {
        const response = await fetch(`/api/translations/${language}`);
        const data = await response.json();
        
        if (data.success) {
            currentTranslations = data.translations;
            currentLanguage = language;
            updateUIText();
        }
    } catch (error) {
        console.error('Error loading translations:', error);
    }
}

// Update UI text with current translations
function updateUIText() {
    elements.appTitle.textContent = currentTranslations.title;
    elements.appSubtitle.textContent = currentTranslations.subtitle;
    elements.generateBtn.textContent = currentTranslations.generate_btn;
    elements.clearBtn.textContent = currentTranslations.clear_btn;
    elements.exportJsonBtn.textContent = currentTranslations.export_json;
    elements.exportCsvBtn.textContent = currentTranslations.export_csv;
    
    // Update operation labels
    const checkboxes = document.querySelectorAll('.operation-checkbox');
    const operationsMap = {
        '+': currentTranslations.addition,
        '-': currentTranslations.subtraction,
        '×': currentTranslations.multiplication,
        '÷': currentTranslations.division
    };
    
    checkboxes.forEach(cb => {
        const label = cb.parentElement;
        if (operationsMap[cb.value]) {
            label.childNodes[2].textContent = ` ${operationsMap[cb.value]}`;
        }
    });
    
    // Update placeholder if no problems
    if (elements.problemsList.querySelector('.placeholder')) {
        elements.problemsList.querySelector('.placeholder').textContent = currentTranslations.no_problems;
    }
}

// Handle generate button click
async function handleGenerate() {
    const count = parseInt(elements.countInput.value) || 100;
    const difficulty = elements.difficultySelect.value;
    const operations = Array.from(elements.operationCheckboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);
    
    if (operations.length === 0) {
        showStatus('Please select at least one operation', 'error');
        return;
    }
    
    // Show loading state
    elements.generateBtn.disabled = true;
    elements.generateBtn.innerHTML = '<span class="loading"></span> Generating...';
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                count,
                difficulty,
                operations,
                language: currentLanguage
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayResults(data.problems, data.summary);
            showStatus(data.message, 'success');
        } else {
            showStatus(data.error || currentTranslations.error.replace('{message}', 'Unknown error'), 'error');
        }
    } catch (error) {
        console.error('Generation error:', error);
        showStatus(currentTranslations.error.replace('{message}', error.message), 'error');
    } finally {
        elements.generateBtn.disabled = false;
        elements.generateBtn.textContent = currentTranslations.generate_btn;
    }
}

// Handle clear button click
async function handleClear() {
    try {
        const response = await fetch('/api/clear', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            clearDisplay();
            showStatus('Results cleared', 'success');
        }
    } catch (error) {
        console.error('Clear error:', error);
        clearDisplay();
    }
}

// Handle JSON export
async function handleExportJson() {
    try {
        window.open('/api/export/json', '_blank');
        showStatus('JSON export started', 'success');
    } catch (error) {
        console.error('Export error:', error);
        showStatus('Export failed: ' + error.message, 'error');
    }
}

// Handle CSV export
async function handleExportCsv() {
    try {
        window.open('/api/export/csv', '_blank');
        showStatus('CSV export started', 'success');
    } catch (error) {
        console.error('Export error:', error);
        showStatus('Export failed: ' + error.message, 'error');
    }
}

// Display results in the UI
function displayResults(problems, summary) {
    // Display problems list
    if (problems.length > 0) {
        elements.problemsList.innerHTML = problems.map((problem, index) => `
            <div class="problem-item">
                <span>${index + 1}. ${problem.expression}</span>
                <strong>= ${problem.formatted_result}</strong>
            </div>
        `).join('');
    } else {
        elements.problemsList.innerHTML = `<p class="placeholder">${currentTranslations.no_problems}</p>`;
    }
    
    // Display statistics
    elements.statTotal.textContent = summary.total_problems;
    elements.statAverage.textContent = summary.average_result.toFixed(2);
    elements.statMin.textContent = summary.min_result.toFixed(2);
    elements.statMax.textContent = summary.max_result.toFixed(2);
    
    // Display distribution
    if (summary.operator_distribution && Object.keys(summary.operator_distribution).length > 0) {
        elements.statDistribution.innerHTML = Object.entries(summary.operator_distribution)
            .map(([op, count]) => `<span class="distribution-badge">${op}×${count}</span>`)
            .join('');
    } else {
        elements.statDistribution.innerHTML = '<span>-</span>';
    }
}

// Clear display
function clearDisplay() {
    elements.problemsList.innerHTML = `<p class="placeholder">${currentTranslations.no_problems}</p>`;
    elements.statTotal.textContent = '0';
    elements.statAverage.textContent = '0';
    elements.statMin.textContent = '0';
    elements.statMax.textContent = '0';
    elements.statDistribution.innerHTML = '';
}

// Show status message
function showStatus(message, type) {
    elements.statusMessage.textContent = message;
    elements.statusMessage.className = `status-message ${type}`;
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        elements.statusMessage.className = 'status-message';
    }, 5000);
}

// Keyboard shortcuts
document.addEventListener('keydown', (event) => {
    // Ctrl+G or Cmd+G - Generate
    if ((event.ctrlKey || event.metaKey) && event.key === 'g') {
        event.preventDefault();
        handleGenerate();
    }
    
    // Ctrl+C or Cmd+C - Clear (when not in input field)
    if ((event.ctrlKey || event.metaKey) && event.key === 'c') {
        if (document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            event.preventDefault();
            handleClear();
        }
    }
    
    // Ctrl+E or Cmd+E - Export JSON
    if ((event.ctrlKey || event.metaKey) && event.key === 'e') {
        event.preventDefault();
        handleExportJson();
    }
});
