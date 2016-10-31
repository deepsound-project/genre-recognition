'use strict';

(function() {

function drawPieChart(canvasID, distribution, timeFn) {
    var startValue = 0;
    var data = GENRES.map(function(genre) {
        var color = GENRE_TO_COLOR[genre];
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
        for(var j = 0; j < 10; j++) {
            chart.segments[j].value =
                parseFloat(distribution[i][1][GENRES[j]]);
        }
        chart.update();
        setTimeout(updateChart, 100);
    }
    updateChart();
}

$(function() {
    var id = window.location.hash.substr(1);
    var songPath = 'uploads/' + id + '.mp3';
    var jsonPath = 'uploads/' + id + '.json';
    $.ajax({
        url: jsonPath,
        success: function(result) {
            $('.logo-big').removeClass('logo-big').addClass('logo-small');
            pills(songPath, result);
            drawPieChart('#piechart', result, function() {
                return $('audio').get(0).currentTime;
            });
            $('#piechart-container').show();
        }
    });
});

})();
