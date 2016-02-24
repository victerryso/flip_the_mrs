$(function() {
    var player = $('iframe');
    var playerOrigin = '*';

    // Listen for messages from the player
    if (window.addEventListener) {
        window.addEventListener('message', onMessageReceived, false);
    }
    else {
        window.attachEvent('onmessage', onMessageReceived, false);
    }

    // Handle messages received from the player
    function onMessageReceived(event) {
        // Handle messages from the vimeo player only
        if (!(/^https?:\/\/player.vimeo.com/).test(event.origin)) {
            return false;
        }

        if (playerOrigin === '*') {
            playerOrigin = event.origin;
        }

        var data = JSON.parse(event.data);
        var vimeoId = player.attr('src').replace(/\D/g, '')

        data['id'] = vimeoId

        switch (data.event) {
            case 'ready':
                onReady();
                break;

            // case 'playProgress':
            //     onPlayProgress(data.data);
            //     break;

            case 'play':
                // onPlay();
                dynsite_send_data(given_uid, "embedded-video", data);
                break;

            // case 'pause':
            //     onPause();
            //     break;

            case 'finish':
                // onFinish();
                dynsite_send_data(given_uid, "embedded-video", data);
                break;
        }
    }

    // Helper function for sending a message to the player
    function post(action, value) {
        var data = {
          method: action
        };

        if (value) {
            data.value = value;
        }

        var message = JSON.stringify(data);
        player[0].contentWindow.postMessage(message, playerOrigin);
    }

    function onReady() {
        // status.text('ready');

        post('addEventListener', 'play');
        // post('addEventListener', 'pause');
        post('addEventListener', 'finish');
        // post('addEventListener', 'playProgress');
    }

    // function onPlay(event) {
    //     status.text('play');
    // }

    // function onPause() {
    //     status.text('paused');
    // }

    // function onFinish(event) {
    //     status.text('finished');
    // }

    // function onPlayProgress(data) {
    //     status.text(data.seconds + 's played');
    // }
});
