document.addEventListener('DOMContentLoaded', () => {
    // State management
    const state = {
        isGenerating: false,
        isProtein: false,
        isSortProtein: false,
        sequence: {
            sequence_strand: '',
            sequence_type: '',
            sequence_length: 0,
            sequence_label: ''
        },
        sequence_option: '',
        sequence_output: ''
    };

    // Cache DOM elements
    const elements = {
        sequenceInput: document.getElementById('sequence--input'),
        sequenceType: document.getElementById('sequence_type'),
        sequenceLength: document.getElementById('sequence_length'),
        sequenceLabel: document.getElementById('sequence_label'),
        sequenceOption: document.getElementById('sequence_option'),
        sequenceOutput: document.getElementById('sequence--output'),
        randomBasesCheckbox: document.getElementById('random_bases'),
        generateBtn: document.getElementById('generate-btn'),
        submitBtn: document.getElementById('submit-btn'),
        selectFileBtn: document.getElementById('select-file-btn'),
        fileInput: document.getElementById('file'),
        sortProteinContainer: document.getElementById('sort-protein-container'),
        sortProteinCheckbox: document.getElementById('sort_protein'),
        lengthContainer: document.getElementById('length-container'),
        labelContainer: document.getElementById('label-container'),
        currentYear: document.getElementById('current-year')
    };

    // Validate that all elements exist
    const validateElements = () => {
        for (const [key, element] of Object.entries(elements)) {
            if (!element) {
                console.error(`Element '${key}' not found in the DOM`);
                return false;
            }
        }
        return true;
    };

    // State management functions
    const updateState = (key, value) => {
        if (key.includes('.')) {
            const [object, property] = key.split('.');
            if (state[object] && property in state[object]) {
                state[object][property] = value;
            }
        } else if (key in state) {
            state[key] = value;
        } else {
            console.warn(`Invalid state key: ${key}`);
        }
    };

    // UI update functions
    const updateUI = () => {
        // Update input/output fields
        elements.sequenceInput.value = state.sequence.sequence_strand;
        elements.sequenceType.value = state.sequence.sequence_type;
        elements.sequenceLength.value = state.sequence.sequence_length;
        elements.sequenceLabel.value = state.sequence.sequence_label;
        elements.sequenceOption.value = state.sequence_option;
        elements.sequenceOutput.value = state.sequence_output;

        // Update visibility states
        elements.sortProteinContainer.style.display = state.isProtein ? 'inline-block' : 'none';
        elements.generateBtn.style.display = state.isGenerating ? 'inline-block' : 'none';
        elements.submitBtn.style.display = state.isGenerating ? 'none' : 'inline-block';
        elements.lengthContainer.style.display = state.isGenerating ? 'block' : 'none';
        elements.labelContainer.style.display = state.isGenerating ? 'none' : 'block';
    };

    // Event handlers
    const handleRandomBasesToggle = (event) => {
        updateState('isGenerating', event.target.checked);
        updateUI();
    };

    const handleSequenceActionChange = (event) => {
        const selectedOption = event.target.value;
        updateState('sequence_option', selectedOption);
        updateState('isProtein', selectedOption === 'proteins');
        updateUI();
    };

    const handleFileSelect = () => {
        elements.fileInput.click();
    };

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const lines = e.target.result.split(/\r?\n/);
                let sequenceStrand = '';
                
                lines.forEach(line => {
                    if (line.startsWith('>')) {
                        updateState('sequence.sequence_label', line);
                    } else {
                        sequenceStrand += line.trim();
                    }
                });

                updateState('sequence.sequence_strand', sequenceStrand);
                updateState('sequence.sequence_type', sequenceStrand.includes('T') ? 'DNA' : 'RNA');
                updateUI();
            } catch (error) {
                console.error('Error processing file:', error);
                alert('Error processing the file. Please check the file format.');
            }
        };

        reader.onerror = () => {
            console.error('Error reading file');
            alert('Error reading the file. Please try again.');
        };

        reader.readAsText(file);
    };

    const handleSortProtein = (event) => {
        updateState('isSortProtein', event.target.checked);
        if (state.sequence_output) {
            const proteins = state.sequence_output.split('\n');
            const sortedProteins = proteins.sort((a, b) => 
                event.target.checked ? b.length - a.length : a.length - b.length
            );
            updateState('sequence_output', sortedProteins.join('\n'));
            elements.sequenceOutput.value = state.sequence_output;
        }
    };

    // Initialize
    const initialize = () => {
        if (!validateElements()) {
            console.error('Failed to initialize: Missing DOM elements');
            return;
        }

        // Set current year
        elements.currentYear.textContent = new Date().getFullYear();

        // Add event listeners
        elements.randomBasesCheckbox.addEventListener('change', handleRandomBasesToggle);
        elements.sequenceOption.addEventListener('change', handleSequenceActionChange);
        elements.selectFileBtn.addEventListener('click', handleFileSelect);
        elements.fileInput.addEventListener('change', handleFileUpload);
        elements.sortProteinCheckbox.addEventListener('change', handleSortProtein);

        // Initial UI update
        updateUI();
    };

    // Start the application
    initialize();
});