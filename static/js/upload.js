'use strict';

(function() {

function getRandColor(brightness) {
    var rgb = [Math.random() * 256, Math.random() * 256, Math.random() * 256];
    var mix = [brightness * 51, brightness * 51, brightness * 51];
    var mixedrgb = [0, 1, 2].map(function(i) {
        return Math.round((rgb[i] + mix[i]) / 2.0);
    });
    return mixedrgb.join(',');
}

function sendForm() {
    var wave = new SiriWave({
        width: window.innerWidth,
        height: window.innerHeight / 2,
        speed: 0.06,
        noise: 0.9,
        container: $('#wave').get(0),
        color1: getRandColor(3),
        color2: getRandColor(3),
        color3: getRandColor(3),
        color4: getRandColor(3),
        color5: getRandColor(3)
    });

    var formData = new FormData($('#upload form')[0]);
    $.ajax({
        url: '/upload',
        type: 'POST',

        // Ajax events
        beforeSend: function(data, testStatus, jqXHR) {
            // hide upload button
            $('#upload').fadeOut(300, function() {
                wave.start();
                $('body').addClass('loading');
            });
        },
        success: function(data, testStatus, jqXHR) {
            // stop loading animation
            wave.stop()
            $('body').removeClass('loading')

            // redirect to play.html
            window.location.href = window.location.href.replace(/[^\/]*$/,
                    'play.html#' + JSON.parse(data));
        },
        error: function(data, texstStatus, jqXHR) {
            wave.stop()
            $('body').removeClass('loading')
        },

        data: formData,

        // Options to tell jQuery not to process data or worry about content-type.
        cache: false,
        contentType: false,
        processData: false
    });
}

$(function() {
    $('#upload input').change(sendForm);
});

})();
