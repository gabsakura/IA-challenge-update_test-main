function scrollToBottom() {
    var messageBody = document.getElementById("messageFormeight");
    messageBody.scrollTop = messageBody.scrollHeight;
}

$(document).ready(function () {
    $("#messageArea").on("submit", function (event) {
        const date = new Date();
        const hour = date.getHours();
        const minute = date.getMinutes();
        const str_time = hour + ":" + (minute < 10 ? '0' + minute : minute);
        var rawText = $("#text").val();

        var userHtml =
            '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' +
            rawText +
            '<span class="msg_time_send">' +
            str_time +
            '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';

        $("#text").val("");
        $("#messageFormeight").append(userHtml); // Mensagem do usuário no final
        scrollToBottom(); // Rola para baixo para ver a nova mensagem

        $("#loading").show();  // Mostra o carregando

        $.ajax({
            data: {
                msg: rawText,
            },
            type: "POST",
            url: "/get",
        }).done(function (data) {
            $("#loading").hide();  // Esconde o carregando
            var botHtml =
                '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' +
                data +
                '<span class="msg_time">' +
                str_time +
                "</span></div></div>";
            $("#messageFormeight").append($.parseHTML(botHtml)); // Mensagem do bot no final
            scrollToBottom(); // Rola para baixo para ver a nova mensagem
        });
        event.preventDefault();
    });
});