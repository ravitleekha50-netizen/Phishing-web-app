document.addEventListener('DOMContentLoaded', () => {
    const urlForm = document.getElementById('urlForm');
    const urlInput = document.getElementById('urlInput');
    const resultSection = document.getElementById('resultSection');
    const resultStatus = document.getElementById('resultStatus');
    const resultMessage = document.getElementById('resultMessage');
    const reasonsList = document.getElementById('reasonsList');
    const historyList = document.getElementById('historyList');
    const loading = document.getElementById('loading');
    const checkBtn = document.getElementById('checkBtn');

    // Load history from local storage
    let history = JSON.parse(localStorage.getItem('urlHistory')) || [];
    renderHistory();

    urlForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const url = urlInput.value.trim();
        if (!url) return;

        // Simple frontend validation
        if (!isValidURL(url)) {
            alert("Please enter a valid URL format.");
            return;
        }

        // Show loading state
        resultSection.classList.add('hidden');
        loading.classList.remove('hidden');
        checkBtn.disabled = true;

        try {
            const response = await fetch('/api/check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Hide loading
            loading.classList.add('hidden');
            checkBtn.disabled = false;

            // Display results
            displayResult(url, data);
            
            // Add to history
            addToHistory(url, data.status);

        } catch (error) {
            console.error('Error:', error);
            loading.classList.add('hidden');
            checkBtn.disabled = false;
            alert("An error occurred while checking the URL. Please try again.");
        }
    });

    function displayResult(url, data) {
        resultSection.classList.remove('hidden', 'safe', 'suspicious');
        reasonsList.innerHTML = '';
        reasonsList.style.display = 'none';

        if (data.status === 'Safe') {
            resultSection.classList.add('safe');
            resultStatus.innerHTML = '<i class="fa-solid fa-circle-check"></i> SAFE';
            resultMessage.textContent = 'This URL appears to be safe.';
        } else {
            resultSection.classList.add('suspicious');
            resultStatus.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> SUSPICIOUS';
            resultMessage.textContent = 'This URL exhibits potentially unsafe characteristics.';
            
            if (data.reasons && data.reasons.length > 0) {
                reasonsList.style.display = 'block';
                data.reasons.forEach(reason => {
                    const li = document.createElement('li');
                    li.textContent = reason;
                    reasonsList.appendChild(li);
                });
            }
        }
    }

    function addToHistory(url, status) {
        // Add to beginning of array
        history.unshift({ url, status, date: new Date().toISOString() });
        
        // Keep only last 5 items
        if (history.length > 5) {
            history.pop();
        }
        
        // Save to local storage
        localStorage.setItem('urlHistory', JSON.stringify(history));
        
        // Update UI
        renderHistory();
    }

    function renderHistory() {
        historyList.innerHTML = '';
        
        if (history.length === 0) {
            historyList.innerHTML = '<li style="color: var(--text-secondary); font-size: 0.9rem;">No recent checks.</li>';
            return;
        }

        history.forEach(item => {
            const li = document.createElement('li');
            li.className = 'history-item';
            
            const urlSpan = document.createElement('span');
            urlSpan.className = 'history-url';
            urlSpan.textContent = item.url;
            urlSpan.title = item.url; // Tooltip for full URL
            
            const badgeSpan = document.createElement('span');
            badgeSpan.className = `badge ${item.status.toLowerCase()}`;
            badgeSpan.textContent = item.status;
            
            li.appendChild(urlSpan);
            li.appendChild(badgeSpan);
            
            // Allow clicking history to check again
            li.style.cursor = 'pointer';
            li.addEventListener('click', () => {
                urlInput.value = item.url;
                urlForm.dispatchEvent(new Event('submit'));
            });
            
            historyList.appendChild(li);
        });
    }

    function isValidURL(string) {
        try {
            // A simple validation to check if it can be parsed as a URL, or at least looks like one
            if (!string.startsWith('http://') && !string.startsWith('https://')) {
                new URL('http://' + string);
                return true;
            }
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }
});
