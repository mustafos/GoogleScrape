document.getElementById('searchForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value.trim();
    
    if (!query) {
        // If the input is empty, return and do not proceed with the search
        document.getElementById('results-container').innerHTML = '';
        document.getElementById('saveResults').style.display = 'none';
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
        
        // Show results and save button
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
