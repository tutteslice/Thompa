document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chat-container');
    const inputField = document.getElementById('input-field');
    const sendButton = document.getElementById('send-button');
    const newChatButton = document.getElementById('new-chat-button');

    function addMessage(role, content) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message');
        messageElement.innerHTML = `<span class="role">${role}:</span> <span class="content">${content}</span>`;
        chatContainer.appendChild(messageElement);
    }

    sendButton.addEventListener('click', function() {
        const message = inputField.value;
        inputField.value = '';
        addMessage('User', message);

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessage('Thompa GPT: ', data.response);
        });
    });

    function initChat() {
        fetch('/init_chat')
            .then(response => response.json())
            .then(data => {
                addMessage('Thompa GPT:', data.response);
            });
    }

    initChat();  // Initialize the chat when the page is loaded.

    newChatButton.addEventListener('click', function() {
        location.reload();
    });

    inputField.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });

    document.getElementById('messageInput').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault(); // Prevents the default action of the enter key
            document.getElementById('sendButton').click();
        }
    });
    

    function addMessage(role, content) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message');
        if (content.startsWith("`")) {
            messageElement.classList.add('code');
            content = content.slice(1);  // Remove the first character
        }
        messageElement.innerHTML = `<span class="role">${role}:</span> <span class="content">${content}</span>`;
        chatContainer.appendChild(messageElement);
    }
    
    
});
