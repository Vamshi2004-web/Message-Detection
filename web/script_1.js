document.addEventListener("DOMContentLoaded", function () {
  const chatbotContainer = document.getElementById("chatbot-container");
  const closeBtn = document.getElementById("close-btn");
  const sendBtn = document.getElementById("send-btn");
  const chatBotInput = document.getElementById("chatbot-input");
  const chatbotMessages = document.getElementById("chatbot-messages");
  const chatbotIcon = document.getElementById("chatbot-icon");

  // Show chatbot window
  chatbotIcon.addEventListener("click", () => {
    chatbotContainer.classList.remove("hidden");
    chatbotIcon.style.display = "none";
  });

  // Close chatbot window
  closeBtn.addEventListener("click", () => {
    chatbotContainer.classList.add("hidden");
    chatbotIcon.style.display = "flex";
  });

  // Send message on button click
  sendBtn.addEventListener("click", sendMessage);

  // Send message on Enter key
  chatBotInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});

function sendMessage() {
  const inputElement = document.getElementById("chatbot-input");
  const userMessage = inputElement.value.trim();
  if (userMessage) {
    appendMessage("user", userMessage);
    inputElement.value = ""; // Clear the input after sending
    getBotResponse(userMessage);
  }
}

function appendMessage(sender, message) {
  const messageContainer = document.getElementById("chatbot-messages");
  const messageElement = document.createElement("div");
  messageElement.classList.add("message", sender);

  // Format text: convert \n to <br> for new lines
  messageElement.innerHTML = message.replace(/\n/g, "<br>");

  messageContainer.appendChild(messageElement);
  messageContainer.scrollTop = messageContainer.scrollHeight;
}

async function getBotResponse(userMessage) {
  const API_KEY = "AIzaSyBqnQXWfOFgu5zjJE8K8IzIWRoCSy1G3eE";
  const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}`;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [
          {
            role: "user",
            parts: [
              {
                text: `You are a helpful chatbot. Answer the user's question clearly and politely.\n\nUser: ${userMessage}\nBot:`
              }
            ]
          }
        ]
      }),
    });

    const data = await response.json();

    if (!data.candidates || !data.candidates.length) {
      throw new Error("No response from Gemini API");
    }

    const botMessage = data.candidates[0].content.parts[0].text;
    appendMessage("bot", botMessage);
  } catch (error) {
    console.error("Error:", error);
    appendMessage("bot", "Sorry, I'm having trouble responding. Please try again.");
  }
}
