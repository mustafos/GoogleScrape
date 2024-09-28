document.getElementById('searchForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value;
    
    try {
        const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
        const results = await response.json();
        
        // Check for errors
        if (results.error) {
            document.getElementById('results').textContent = 'Error fetching results.';
            return;
        }
        
        document.getElementById('results').textContent = JSON.stringify(results, null, 2);
        
        // Enable save button
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
        document.getElementById('results').textContent = 'Error fetching results.';
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
    document.getElementById('results').textContent = ''; // Clear search results
    document.getElementById('saveResults').style.display = 'none'; // Hide the save button
});
