let socket;

function initWebSocket() {
    socket = new WebSocket("ws://localhost:8000/ws");

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);

        if (data.type === "status_update") {
            document.getElementById("state").innerText =
                "Oven Status: " + data.state;
            document.getElementById("mode").innerText =
                "Mode: " + (data.mode || "None");
            document.getElementById("time").innerText =
                "Time Remaining: " + data.time_remaining + " seconds";
        }

        if (data.state === "ON") {
            document.getElementById("time").innerText =
                "Time Remaining: " + data.time_remaining + " seconds";
        }
    };

    socket.onclose = function () {
        setTimeout(initWebSocket, 1000);
    };
}

window.onload = function () {
    initWebSocket();
};
