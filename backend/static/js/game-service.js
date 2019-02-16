function get_hostname(url) {
    var m = url.match(/^http:\/\/[^/]+/);
    return m ? m[0] : null;
}

function send_error_msg(gameFrame, err) {
    var errorMessage = {
        messageType: "ERROR",
        info: err
    };
    $('#result').text("")
    gameFrame.contentWindow.postMessage(errorMessage, '*');
    return;
}

function send_load_msg(gameFrame, data) {
    var loadMessage = JSON.parse(data);
    loadMessage.messageType = "LOAD";
    gameFrame.contentWindow.postMessage(loadMessage, '*');
    $('#result').text("Game loaded successfully!");
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
        case "SAVE":
            if (msg.gameState == null) {
                send_error_msg(gameFrame, "No game state specified");
                return;
            }
            save_game(gameFrame, msg.gameState);
            break;
        case "LOAD_REQUEST":
            load_game(gameFrame);
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

function load_game(gameFrame) {
    $.ajax({
        url: 'load_game/',
        type: 'POST',
        success: function (data) {
            send_load_msg(gameFrame, data);
        },
        error: function() {
            send_error_msg(gameFrame, "Error: game not loaded.");
        }
      });
}

function save_game(gameFrame, gameState) {
    $.ajax({
        url: 'save_game/',
        data: JSON.stringify({'gameState': gameState}),
        dataType: 'json',
        type: 'POST',
        success: function (data) {
            $('#result').text(data['status']);
        },
        error: function() {
            send_error_msg(gameFrame, "Error: game not saved.");
        }
      });
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
            $('#result').text(data["status"]);
        },
        error: function() {
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