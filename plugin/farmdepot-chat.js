jQuery(document).ready(function ($) {

    $("#sendBtn").on("click", function () {

        let userMsg = $("#chatInput").val();
        let lang = $("#langSelect").val();

        $("#chatBox").append(`<div class="user-msg"><b>You:</b> ${userMsg}</div>`);

        $.post({
            url: farmdepot_ajax.ajax_url,
            data: {
                action: "farmdepot_ai_chat",
                message: userMsg,
                language: lang
            },
            success: function (response) {
                if (response.success) {
                    $("#chatBox").append(`<div class="ai-msg"><b>AI:</b> ${response.data.response}</div>`);
                } else {
                    $("#chatBox").append(`<div class="ai-msg"><b>Error:</b> Failed to get response</div>`);
                }
            }
        });
    });

});