// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const languageSelect = document.getElementById('language');
const audioFileInput = document.getElementById('audioFile');
const fileNameDisplay = document.getElementById('fileName');
const apiKeyInput = document.getElementById('apiKey');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultSection = document.getElementById('resultSection');
const errorSection = document.getElementById('errorSection');

// State
let selectedFile = null;
let audioBase64 = null;

// Event Listeners
audioFileInput.addEventListener('change', handleFileSelect);
languageSelect.addEventListener('change', validateForm);
apiKeyInput.addEventListener('input', validateForm);
analyzeBtn.addEventListener('click', analyzeVoice);

/**
 * Handle file selection
 */
function handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (!file) {
        selectedFile = null;
        audioBase64 = null;
        fileNameDisplay.textContent = 'Choose MP3 file...';
        validateForm();
        return;
    }
    
    // Validate file type
    if (!file.type.includes('mp3') && !file.name.endsWith('.mp3')) {
        showError('Please select a valid MP3 file');
        audioFileInput.value = '';
        return;
    }
    
    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('File size must be less than 10MB');
        audioFileInput.value = '';
        return;
    }
    
    selectedFile = file;
    fileNameDisplay.textContent = file.name;
    
    // Convert to base64
    convertToBase64(file);
}

/**
 * Convert file to base64
 */
function convertToBase64(file) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        // Remove data URL prefix
        const base64String = e.target.result.split(',')[1];
        audioBase64 = base64String;
        validateForm();
    };
    
    reader.onerror = function() {
        showError('Failed to read file');
        audioBase64 = null;
        validateForm();
    };
    
    reader.readAsDataURL(file);
}

/**
 * Validate form and enable/disable submit button
 */
function validateForm() {
    const isValid = 
        languageSelect.value !== '' &&
        audioBase64 !== null &&
        apiKeyInput.value.trim() !== '';
    
    analyzeBtn.disabled = !isValid;
}

/**
 * Analyze voice
 */
async function analyzeVoice() {
    // Hide previous results/errors
    hideResults();
    hideError();
    
    // Show loading state
    setLoading(true);
    
    try {
        const requestBody = {
            language: languageSelect.value,
            audioFormat: 'mp3',
            audioBase64: audioBase64
        };
        
        const response = await fetch(`${API_BASE_URL}/voice-detection`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': apiKeyInput.value.trim()
            },
            body: JSON.stringify(requestBody)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || data.detail || 'Request failed');
        }
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        showError(error.message || 'An error occurred while analyzing the voice');
    } finally {
        setLoading(false);
    }
}

/**
 * Display analysis results
 */
function displayResults(data) {
    // Update result values
    document.getElementById('resultLanguage').textContent = data.language;
    
    const classificationBadge = document.getElementById('resultClassification');
    classificationBadge.textContent = data.classification.replace('_', ' ');
    classificationBadge.className = 'result-value classification-badge ' + 
        (data.classification === 'AI_GENERATED' ? 'ai' : 'human');
    
    const confidencePercent = Math.round(data.confidenceScore * 100);
    document.getElementById('confidenceScore').textContent = `${confidencePercent}%`;
    document.getElementById('confidenceBar').style.width = `${confidencePercent}%`;
    
    document.getElementById('resultExplanation').textContent = data.explanation;
    
    // Show result section with animation
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Show error message
 */
function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Hide error message
 */
function hideError() {
    errorSection.style.display = 'none';
}

/**
 * Hide results
 */
function hideResults() {
    resultSection.style.display = 'none';
}

/**
 * Set loading state
 */
function setLoading(isLoading) {
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = analyzeBtn.querySelector('.btn-loader');
    
    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        analyzeBtn.disabled = true;
    } else {
        btnText.style.display = 'inline-block';
        btnLoader.style.display = 'none';
        validateForm();
    }
}

// Initialize
validateForm();
