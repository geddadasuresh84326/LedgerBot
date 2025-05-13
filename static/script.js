// function sendMessage() {
//     const userInput = document.getElementById("user-input");
//     const chatBox = document.getElementById("chat-box");
//     const message = userInput.value.trim();
//     if (!message) return;

//     // User message element
//     const userMsg = document.createElement("div");
//     userMsg.className = "message user ms-auto me-2 d-flex justify-content-end";
//     userMsg.textContent = message;
//     chatBox.appendChild(userMsg);

//     userInput.value = "";
//     chatBox.scrollTop = chatBox.scrollHeight;

//     // Typing indicator
//     const typingMsg = document.createElement("div");
//     typingMsg.className = "message bot me-auto ms-2";
//     typingMsg.id = "typing-indicator";
//     typingMsg.textContent = "Bot is typing...";
//     chatBox.appendChild(typingMsg);
//     chatBox.scrollTop = chatBox.scrollHeight;

//     // Send to backend
//     fetch('/chat', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ message })
//     })
//     .then(response => response.json())
//     .then(data => {
//         // Remove typing
//         const typingIndicator = document.getElementById("typing-indicator");
//         if (typingIndicator) chatBox.removeChild(typingIndicator);

//         // Bot response
//         const botMsg = document.createElement("div");
//         botMsg.className = "message bot me-auto ms-2";
//         botMsg.textContent = data.response;
//         chatBox.appendChild(botMsg);
//         chatBox.scrollTop = chatBox.scrollHeight;
//     });
// }

function sendMessage() {
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const message = userInput.value.trim();
    if (!message) return;

    const userIconUrl = "static/icons/person_38dp_000000_FILL0_wght400_GRAD0_opsz40.png";
    const botIconUrl = "static/icons/support_agent_38dp_000000_FILL0_wght400_GRAD0_opsz40.png";

    // User message container
    const userMsgWrapper = document.createElement("div");
    userMsgWrapper.className = "d-flex justify-content-end align-items-start mb-2";

    const userMsg = document.createElement("div");
    userMsg.className = "message user me-2";
    userMsg.textContent = message;

    const userIcon = document.createElement("img");
    userIcon.src = userIconUrl;
    userIcon.alt = "User Icon";
    userIcon.style.width = "30px";
    userIcon.style.height = "30px";
    userIcon.className = "rounded-circle";

    userMsgWrapper.appendChild(userMsg);
    userMsgWrapper.appendChild(userIcon);
    chatBox.appendChild(userMsgWrapper);

    userInput.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Typing indicator
    const typingWrapper = document.createElement("div");
    typingWrapper.className = "d-flex justify-content-start align-items-start mb-2";
    typingWrapper.id = "typing-indicator";

    const botIconTyping = document.createElement("img");
    botIconTyping.src = botIconUrl;
    botIconTyping.alt = "Bot Icon";
    botIconTyping.style.width = "30px";
    botIconTyping.style.height = "30px";
    botIconTyping.className = "rounded-circle me-2";

    const typingMsg = document.createElement("div");
    typingMsg.className = "message bot";
    typingMsg.textContent = "Waiting for the agent's response...";

    typingWrapper.appendChild(botIconTyping);
    typingWrapper.appendChild(typingMsg);
    chatBox.appendChild(typingWrapper);

    chatBox.scrollTop = chatBox.scrollHeight;

    // Send message to backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    })
    .then(response => response.json())
    .then(data => {
        const typingIndicator = document.getElementById("typing-indicator");
        if (typingIndicator) chatBox.removeChild(typingIndicator);
    
        const botMsgWrapper = document.createElement("div");
        botMsgWrapper.className = "d-flex justify-content-start align-items-start mb-2";
    
        const botIcon = document.createElement("img");
        botIcon.src = botIconUrl;
        botIcon.alt = "Bot Icon";
        botIcon.style.width = "30px";
        botIcon.style.height = "30px";
        botIcon.className = "rounded-circle me-2";
    
        const botMsg = document.createElement("div");
        botMsg.className = "message bot";
        botMsg.textContent = data.response;
    
        botMsgWrapper.appendChild(botIcon);
        botMsgWrapper.appendChild(botMsg);
        chatBox.appendChild(botMsgWrapper);
    
        chatBox.scrollTop = chatBox.scrollHeight;
    
       // 🔊 Play the audio from server
        if (data.audio_url) {
            const audioUrl = data.audio_url + '?t=' + new Date().getTime(); // prevent caching
            const audio = new Audio(audioUrl);
            audio.play();
        }
        });
}

