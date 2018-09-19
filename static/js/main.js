'use strict';

(function() {

var worker = new Worker('static/js/worker.js');

const modelPromise = tf.loadModel('static/model/model.json');

function getRandColor(brightness) {
    var rgb = [Math.random() * 256, Math.random() * 256, Math.random() * 256];
    var mix = [brightness * 51, brightness * 51, brightness * 51];
    var mixedrgb = [0, 1, 2].map(function(i) {
        return Math.round((rgb[i] + mix[i]) / 2.0);
    });
    return mixedrgb.join(',');
}

function specToInputTensor(spec) {
    const width = spec.length;
    const height = spec[0].length;
    var flatSpec = new Float32Array(width * height);
    for(var i = 0; i < width; ++i) {
        flatSpec.set(spec[i], i * height);
    }
    return tf.tensor3d(flatSpec, [1, width, height]);
}

function preprocess(file) {
    return new Promise(function(resolve, reject) {
        worker.onmessage = async function(event) {
            resolve(event.data);
        };
        worker.postMessage(file);
    });
}

async function process(file) {
    const spec = await preprocess(file);
    const input = specToInputTensor(event.data);
    const model = await modelPromise;
    const predictionTensor = tf.tidy(function() {
        return model.predict(input);
    });
    const predictionArray = await predictionTensor.data();
    predictionTensor.dispose();
    return predictionArray;
}

function drawPieChart(canvasID, distribution, timeFn) {
    var startValue = 0;
    var data = GENRES.map(function(genre) {
        var color = GENRE_TO_COLOR.get(genre);
        return {
            value: startValue,
            color: color,
            highlight: color,
            label: genre
        };
    });

    var shown = false;
    var context = $(canvasID).get(0).getContext('2d');
    var options = {
        animationEasing: 'linear',
        animationSteps: 10
    };
    var chart = new Chart(context).Pie(data, options);

    function updateChart() {
        var i = lowerBound(distribution, timeFn(), function(x) {
            return x[0];
        });
        GENRES.forEach(function(genre, index) {
            chart.segments[index].value = parseFloat(
                distribution[i][1][genre]
            );
        });
        chart.update();
        setTimeout(updateChart, 100);
    }
    updateChart();
}

function createAudioElement(file) {
    const fileSrc = URL.createObjectURL(file);
    const audio = new Audio(fileSrc);
    audio.crossOrigin = "anonymous";
    audio.controls = true;
    return audio;
}

function genreDistributionOverTime(prediction, duration) {
    const dt = (duration + 0.001) / prediction.length * GENRES.length;
    var distribution = [];
    for(var i = 0; i < prediction.length / GENRES.length; ++i) {
        const from = i * GENRES.length;
        const to = from + GENRES.length;
        distribution.push(
            [(i + 1) * dt, prediction.slice(from, to).reduce(function(acc, cur, j) {
                acc[GENRES[j]] = cur;
                return acc;
            }, {})]
        );
    }
    return distribution;
}

async function sendForm() {
    // SAMPLE RATE!!!
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

    $('#upload').fadeOut(300, function() {
        wave.start();
        $('body').addClass('loading');

        const file = $('#upload input')[0].files[0];
        process(file).then(function(prediction) {
            wave.stop();
            $('body').removeClass('loading');
            $('.logo-big').removeClass('logo-big').addClass('logo-small');

            const audio = createAudioElement(file);
            $(audio).on("loadedmetadata", function() {
                const distribution = genreDistributionOverTime(
                    prediction, audio.duration
                );
                pills(audio, distribution);
                drawPieChart('#piechart', distribution, function() {
                    return $('audio').get(0).currentTime;
                });
                $('#piechart-container').show();
            });
        });
    });

    // window.location.href = window.location.href.replace(/[^\/]*$/,
            // 'play.html#' + JSON.parse(data));
}

$(function() {
    $('#upload input').change(sendForm);
});

})();
