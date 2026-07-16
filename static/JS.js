function fetchLogs() {
    fetch('/stats')
        .then(response => response.json())
        .then(data => {
            let logHTML = "<h2>Blocked IPs</h2>";
            data.forEach(entry => {
                logHTML += `<p>${entry[2]}: Blocked ${entry[0]} for ${entry[1]}</p>`;
            });
            document.getElementById('logs').innerHTML = logHTML;
        });
}

setInterval(fetchLogs, 5000);
fetchLogs();