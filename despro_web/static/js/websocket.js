let socket;

function initWebSocket() {
    socket = new WebSocket("ws://localhost:8000/ws");
    const statusImg = document.getElementById("status-img");
    const state = document.getElementById("state");

    // Function to update oven status
    function updateOvenStatus(isOn) {
        if (isOn) {
            statusImg.src = "/static/images/oven-on.png";
            state.firstChild.textContent = "Oven Status: ON";
        } else {
            statusImg.src = "/static/images/oven-off.png";
            state.firstChild.textContent = "Oven Status: OFF";
        }
    }

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
            updateOvenStatus(true);
        } else {
            updateOvenStatus(false);
        }
    };

    socket.onclose = function () {
        setTimeout(initWebSocket, 1000);
    };
}

window.onload = function () {
    initWebSocket();
};
