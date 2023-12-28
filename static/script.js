function submitPlaylist() {
    const playlistLink = document.getElementById('playlistLink').value;
    
    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ playlistLink }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerHTML = `<p>${data.message}</p>`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = '<p>An error occurred. Please try again.</p>';
    });
}
