const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");

function addMessage(message, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, "user");
    userInput.value = "";

    try {
        const response = await fetch("http://localhost:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (data.reply) {
            addMessage(data.reply, "bot");
        } else {
            addMessage("Error: Unable to get response", "bot");
        }

    } catch (error) {
        addMessage("Server error. Make sure backend is running.", "bot");
        console.error(error);
    }
}
