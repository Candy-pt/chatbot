    function sendMessage() {
        const input = document.getElementById('message-input');
        const message = input.value;
        if (message.trim() === '') return;

        // Hiển thị tin nhắn người dùng
        addMessage('user', message);
        input.value = '';

        // Thêm hiệu ứng loading
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading';
        loadingDiv.id = 'loading-message';
        loadingDiv.innerHTML = '<span class="loading-dots">.</span>';
        document.getElementById('chat-messages').appendChild(loadingDiv);
    

        // Gửi tin nhắn đến server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Xóa hiệu ứng loading
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                loadingMessage.remove();
            }
            // Hiển thị phản hồi từ bot
            addMessage('bot', data.response);
        })
        .catch(error => {
            // Xóa hiệu ứng loading nếu có lỗi
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                loadingMessage.remove();
            }
            addMessage('bot', 'Xin lỗi, đã có lỗi xảy ra.');
        });
    }

    function addMessage(sender, message) {
        const chatMessages = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
        
        if (sender === 'user') {
            messageDiv.innerHTML = message;
            chatMessages.appendChild(messageDiv);
        } else {
            // Hiệu ứng đánh máy cho tin nhắn bot
            messageDiv.innerHTML = '';
            chatMessages.appendChild(messageDiv);
            
            let i = 0;
            const speed = 20; // Tốc độ đánh máy (ms)
            
            function typeWriter() {
                if (i < message.length) {
                    messageDiv.innerHTML += message.charAt(i);
                    i++;
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                    setTimeout(typeWriter, speed);
                }
            }
            
            typeWriter();
        }
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Cho phép gửi tin nhắn bằng phím Enter
    document.getElementById('message-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
