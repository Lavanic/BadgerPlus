document.addEventListener("DOMContentLoaded", function () {
  const messageInput = document.getElementById("messageInput");
  const sendButton = document.getElementById("sendButton");
  const messageContainer = document.querySelector(".message-container");

  function sendMessage() {
    const messageText = messageInput.value;
    if (messageText.trim() === "") {
      return; // Don't send empty messages
    }

    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.textContent = messageText;
    messageContainer.appendChild(messageElement);

    // Clear the input field after sending the message
    messageInput.value = "";
  }

  sendButton.addEventListener("click", sendMessage);
  messageInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
});
