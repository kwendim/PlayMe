function get_hostname(url) {
    var m = url.match(/^http:\/\/[^/]+/);
    return m ? m[0] : null;
}

function send_error_msg(gameFrame, err) {
    var errorMessage = {
        messageType: "ERROR",
        info: err
    };
    gameFrame.contentWindow.postMessage(errorMessage, '*');
    return;
}

function handle_message(msg, gameFrame, gameDiv) {
    var msgType = msg.messageType;
    switch(msgType) {
        case "SETTING":
            if (msg.options == null) {
                send_error_msg(gameFrame, "No options specified");
                return;
            }
            set_dimensions(gameDiv, gameFrame, msg.options.width, msg.options.height);
            break;
        case "SCORE":
            if (msg.score == null) {
                send_error_msg(gameFrame, "No score specified");
                return;
            }
            submit_score(gameFrame, msg.score);
            break;
        default:
            send_error_msg(gameFrame, "Unknown message");
            break;
    }
}

function set_dimensions(gameDiv, gameFrame, width, height) {
    gameDiv.height = height;
    gameDiv.width = width;
    gameFrame.height = height;
    gameFrame.width = width;
}

function submit_score(gameFrame, score) {
    $.ajax({
        url: 'submit_score/',
        data: {
            'score': score
        },
        dataType: 'json',
        type: 'POST',
        success: function (data) {
            $('#result').text(data['status']);
        },
        failure: function() {
            send_error_msg(gameFrame, "Error: score not saved.");
        }
      });
}

$(window).on('message', function(event) {
    var gameFrame = document.getElementById('game_frame')
    var gameDiv = document.getElementById('game_div')
    var origin = get_hostname(gameFrame.src);
    if (origin == null || event.originalEvent.origin !== origin) {
        send_error_msg(gameFrame, "Unknown origin");
        return;
    }
    var msg = event.originalEvent.data;
    handle_message(msg, gameFrame, gameDiv);
});