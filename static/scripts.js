$(document).ready(function () {
    const messageForm = $("#message-form");
    const messageInput = $("#message-input");
    const chatBox = $("#chat-box");

    function appendMessage(message, className) {
        const messageElement = $("<div>")
            .addClass("message")
            .append($("<div>").addClass(className).text(message));
        chatBox.append(messageElement);
        chatBox.scrollTop(chatBox.prop("scrollHeight"));
    }

    messageForm.submit(function (event) {
        event.preventDefault();
        const userMessage = messageInput.val();
        appendMessage(userMessage, "user-message");
        messageInput.val("");
        $.ajax({
            type: "POST",
            url: "/get_response",
            data: { message: userMessage },
            success: function (response) {
                const aiMessage = response.response;
                appendMessage(aiMessage, "ai-message");
            },
            error: function (xhr) {
                appendMessage("Error: " + xhr.statusText, "system-message");
            },
        });
    });
});