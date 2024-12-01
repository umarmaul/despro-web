async function capture() {
    const response = await fetch("/capture", {
        method: "POST",
    });
    const data = await response.json();
    if (data.error) {
        alert(data.error);
        return;
    }

    document.getElementById("label").innerText = data.prediction;
    document.getElementById("captured-image").src = data.img_path;
}

document.querySelector("form").addEventListener("submit", function (e) {
    e.preventDefault();
    capture();
});
