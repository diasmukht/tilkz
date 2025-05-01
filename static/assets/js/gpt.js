document.getElementById("gpt-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const input = document.getElementById("gpt-input");
    const messagesDiv = document.getElementById("gpt-messages");
    const userMessage = input.value.trim();
    if (!userMessage) return;

    messagesDiv.innerHTML += `<div class="gpt-message user">${userMessage}</div>`;
    input.value = "";

    const response = await fetch("/gpt-response/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    });

    const data = await response.json();
    messagesDiv.innerHTML += `<div class="gpt-message bot">${data.response}</div>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});
