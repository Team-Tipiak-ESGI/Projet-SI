// Create and open WebSocket
const socket = new WebSocket(`ws://${window.location.host}/websocket`);
const output = document.getElementById('output');

// Send form
function sendForm(form) {
    const formData = new FormData(form);
    const data = {
        string: formData.get('hashed-string'),
        method: formData.get('hash-method'),
    }

    output.innerText = '';

    socket.send(JSON.stringify(data)) // Send data through websocket

    // Show spinner
    document.getElementById('spinner').classList.remove('d-none');

    // Clear previous results
    document.getElementById('results').innerHTML = '';

    return false;
}

// On socket opened
/*socket.onopen = function (event) {
    socket.send('dir');
}*/

// On message received
socket.onmessage = function (event) {
    event.data.text().then((text) => {
        // Add text on page
        output.innerText += text;
        console.log(text);

        // Add result to page result
        if (text.startsWith('?:')) {
            const result = text.slice(2);
            const span = document.createElement('span');
            span.classList.add('badge', 'bg-success');
            span.innerText = result;
            document.getElementById('results').append(span);
        }

        // Hide spinner
        if (text.includes('0 left') || text.includes('Session completed')) {
            document.getElementById('spinner').classList.add('d-none');
        }
    });
}