let socket;

function initWebSocket() {
    socket = new WebSocket("ws://smartoven.local/ws");

    // Update the oven status when a message is received
    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        document.getElementById("status").innerText =
            "Oven Status: " + data.oven_status;
    };

    // Reconnect WebSocket if the connection is closed
    socket.onclose = function () {
        console.log("WebSocket closed, reconnecting...");
        setTimeout(initWebSocket, 1000);
    };
}

window.onload = function () {
    initWebSocket();
};
