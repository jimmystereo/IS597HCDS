document.getElementById('fetchGPT').addEventListener('click', async () => {
    try {
        // Get the current tab
        chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
            const currentTab = tabs[0];
            const url = currentTab.url; // Get the URL of the current tab

            // Send the URL to the Flask backend
            const response = await fetch('http://127.0.0.1:5000/api/scrape', {
                method: 'POST', // Change to POST request
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url , model: 'gpt'}) // Send the URL as JSON
            });

            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            const data = await response.json();
//            document.getElementById('score').innerText = `Paragraphs: ${data.score}`;
            document.getElementById('model').innerText = `Model: GPT`;

            document.getElementById('result').innerText = `Paragraphs: ${data.result}`;
        });
    } catch (error) {
        console.error('Error fetching data:', error);

        document.getElementById('data').innerText = 'Failed to fetch data: ' + error.message;
    }
});
document.getElementById('fetchClaude').addEventListener('click', async () => {
    try {
        // Get the current tab
        chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
            const currentTab = tabs[0];
            const url = currentTab.url; // Get the URL of the current tab

            // Send the URL to the Flask backend
            const response = await fetch('http://127.0.0.1:5000/api/scrape', {
                method: 'POST', // Change to POST request
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url , model: 'claude'}) // Send the URL as JSON
            });

            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            const data = await response.json();
//            document.getElementById('score').innerText = `Paragraphs: ${data.score}`;
            document.getElementById('model').innerText = `Model: Claude`;

            document.getElementById('result').innerText = `Paragraphs: ${data.result}`;
        });
    } catch (error) {
        console.error('Error fetching data:', error);

        document.getElementById('data').innerText = 'Failed to fetch data: ' + error.message;
    }
});
