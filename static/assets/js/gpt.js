async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    const chatBox = document.getElementById('chat-messages');
    chatBox.innerHTML += `<div class="user-message">${message}</div>`;
    input.value = '';

    const response = await fetch('/gpt-response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    if (data.reply) {
        chatBox.innerHTML += `<div class="gpt-message">${data.reply}</div>`;
    } else {
        chatBox.innerHTML += `<div class="gpt-message error">Ошибка: ${data.error}</div>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}
