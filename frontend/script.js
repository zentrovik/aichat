const chat = document.getElementById("chat");
const input = document.getElementById("msg");
const voiceBtn = document.getElementById("voice-btn");

function add(text, cls) {
  const div = document.createElement("div");
  div.className = `msg ${cls}`;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function send() {
  const text = input.value.trim();
  if (!text) return;

  add(text, "user");
  input.value = "";

  add("Typing...", "bot");

  const res = await fetch("http://localhost:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  });

  const data = await res.json();
  chat.lastChild.remove();
  add(data.reply || "Error", "bot");
}

// Voice recognition setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.onstart = () => {
  console.log("Voice recognition started...");
};

recognition.onresult = (event) => {
  const transcript = event.results[0][0].transcript;
  input.value = transcript;
};

recognition.onerror = (event) => {
  console.error("Voice recognition error:", event.error);
};

voiceBtn.addEventListener("click", () => {
  recognition.start();
});
