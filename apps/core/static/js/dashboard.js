// Real‑time dashboard updates via WebSocket (dummy example)
const dashSocket = new WebSocket('ws://' + window.location.host + '/ws/live/');
dashSocket.onmessage = function(e) {
    const update = JSON.parse(e.data);
    console.log('Live update:', update);
    // Update UI elements based on update.type
};