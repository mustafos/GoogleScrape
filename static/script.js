document.getElementById('searchForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value;
    
    try {
        const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
        const results = await response.json();
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
