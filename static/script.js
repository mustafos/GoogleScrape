document.getElementById('searchForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value.trim();
    
    if (!query) {
        // If the input is empty, return and do not proceed with the search
        document.getElementById('results-container').innerHTML = '';
        document.getElementById('saveResults').style.display = 'none';
        document.getElementById('results-header').style.display = 'none'; // Hide the header
        return;
    }
    
    try {
        const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
        const results = await response.json();
        
        // Check for errors
        if (results.error) {
            document.getElementById('results-container').textContent = 'Error fetching results.';
            return;
        }
        
        // Clear previous results
        const resultsContainer = document.getElementById('results-container');
        resultsContainer.innerHTML = '';
        
        // Display the results
        results.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.classList.add('result-item');
            resultItem.innerHTML = `<strong>${result.title}</strong><br><a href="${result.link}" target="_blank">${result.link}</a>`;
            resultsContainer.appendChild(resultItem);
        });
        
        // Show results header and save button
        document.getElementById('results-header').style.display = 'block';
        resultsContainer.style.display = 'block';
        const saveButton = document.getElementById('saveResults');
        saveButton.style.display = 'block';
        
        saveButton.onclick = () => {
            const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'search_results.json';
            a.click();
            URL.revokeObjectURL(url);
        };
    } catch (error) {
        document.getElementById('results-container').textContent = 'Error fetching results.';
    }
});

// Handle input changes to show or hide the clear button
const queryInput = document.getElementById('query');
const clearButton = document.getElementById('clearButton');

queryInput.addEventListener('input', function() {
    clearButton.style.display = queryInput.value ? 'block' : 'none';
});

// Handle clear button click
clearButton.addEventListener('click', function() {
    queryInput.value = '';
    clearButton.style.display = 'none';
    document.getElementById('results-container').innerHTML = ''; // Clear search results
    document.getElementById('saveResults').style.display = 'none'; // Hide the save button
    document.getElementById('results-header').style.display = 'none'; // Hide the header
    queryInput.focus(); // Set focus back to the input field
});
