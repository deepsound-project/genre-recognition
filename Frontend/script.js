

let draw = false;
let songToAnalyze = 3;
const genres = ["Rap", "Rock", "Jazz", "Classical", "Punk"]

var rap = [0];
var rock = [0];
var jazz = [0];
var classical = [0];
var punk = [0];
var time = [0];
let now = [.2,.2,.2,.2,.2];
let sum = [.2,.2,.2,.2,.2];

var dataDisplay = document.getElementById("dataDisplay");
var guessDisplay = document.getElementById("guessDisplay");
var guessFont = document.getElementById("guessFont");


function indexOfMax(arr) {
      if (arr.length === 0) {
          return -1;
      }

      var max = arr[0];
      var maxIndex = 0;

      for (var i = 1; i < arr.length; i++) {
          if (arr[i] > max) {
              maxIndex = i;
              max = arr[i];
          }
      }

      return maxIndex;
  }

function generateSumTo1Array(){
    tot = 0
    toRet = Array.from({length: 5}, () => (Math.random()));

    for(i = 0; i < toRet.length; i ++){
      tot = tot + toRet[i]
    }
    for(i = 0; i < toRet.length; i ++){
      toRet[i] = toRet[i]/tot
    }

    guessFont.innerHTML = "I think the genre of this song is " + genres[indexOfMax(toRet)];
    /*
    tot = 0
    for(i = 0; i < toRet.length; i ++){
      tot = tot + toRet[i]
    }
    console.log(tot);
  */

    return toRet

  }

/*
Button click handling below

*/

var startButton = document.getElementById("startButton");

startButton.onclick = function(){
  if(songToAnalyze!= null){
    draw = true;
    document.getElementById("dropZoneMessage").innerHTML = "Song Analysis Below";
    dataDisplay.style.display = "inline";
    guessDisplay.style.display = "inline";
  }

};
/*
Chart display stuff below
*/
var canvas1 = document.getElementById("chart1");
var canvas2 = document.getElementById("chart2");
var canvas3 = document.getElementById("chart3");
    ctx1 = canvas1.getContext('2d'),
    ctx2 = canvas2.getContext('2d'),
    ctx3 = canvas3.getContext('2d'),
    data1 = {
      labels: genres,
      datasets: [
          {
              fillColor: "rgba(220,220,220,0.2)",
              strokeColor: "rgba(220,220,220,1)",
              pointColor: "rgba(220,220,220,1)",
              pointStrokeColor: "#fff",
              backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
              data:  [.2,.2,.2,.2,.2]
          },
      ]
    };

    data2 = {
      labels: time,
      datasets: [
        {
          data: rap,
          label: "Rap",
          borderColor: "#3e95cd",
          fill: false
        },
        {
          data: rock,
          label: "Rock",
          borderColor: "#8e5ea2",
          fill: false
        },
        {
          data: jazz,
          label: "Jazz",
          borderColor: "#3cba9f",
          fill: false
        },
        {
          data: classical,
          label: "Classical",
          borderColor: "#e8c3b9",
          fill: false
        },
        {
          data: punk,
          label: "Punk",
          borderColor: "#c45850",
          fill: false
        }
        ]
      },

      data3= {
        labels: ["Rap", "Rock", "Jazz", "Classical", "Punk"],
        datasets: [{
          label: "Current Probability",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
          data: now

        }]
      },


setInterval(function(){
      if(draw){
        const x = generateSumTo1Array()
        now = x.slice()

        chart3.data.datasets.data = now

        sum = []

        for (i = 0; i < x.length; i++) {
          chart1.data.datasets[0].data[i] = chart1.data.datasets[0].data[i] + x[i];
          chart3.data.datasets[0].data[i] = x[i];
        }

        rap.push(x[0])
        rock.push(x[1])
        jazz.push(x[2])
        classical.push(x[3])
        punk.push(x[4])

        if (rap.length > 7){
          rap.shift();
          rock.shift();
          jazz.shift();
          classical.shift();
          punk.shift();
        }

        time.push(time[time.length-1] +1);

        if(time.length > 7){
          time.shift();
        }

        chart1.update();
        chart2.update();
        chart3.update()
      }
}, 1000);

// Reduce the animation steps for demo clarity.
var chart1 = new Chart(ctx1, {
  type : 'bar',
  data : data1,
  animationSteps: 60,


  options: {
    title : {
      display:true,
      fontSize : 18,
      text: "Cummulative Probability",

    },
      scales: {
              yAxes: [{
                    display: true,
                    stacked: false,
                    ticks: {
                          min: 0,
                          max: 10,
                          stepSize: 2
                      }
                   }]
                 },
        legend: {
           display: false
        },
        tooltips: {
           enabled: true
        }
   }
}
)

var chart2 = new Chart(ctx2, {
  type : 'line',
  data : data2,
  animationSteps: 60,
  options: {

      title : {
        display:true,
        fontSize : 18,
        text: "Probability over past 6 seconds",
      },

      scales: {
              yAxes: [{
                    display: true,
                    stacked: false,
                    ticks: {
                          min: 0,
                          max: 1,
                      }
                   }],
                 },
        legend: {
           display: false
        },
        tooltips: {
           enabled: true
        }

 }
 }
)

var chart3 = new Chart(ctx3, {
    type: 'pie',
    data : data3,
    animationSteps: 60,
    options: {
      title: {
        display: true,
        fontSize : 18,
        text: 'Current Probability'
      }
    }
});



/**

Drop Zone handling below

*/

window.onload = function(){

  Dropzone.options.myDropzone = {

    paramName: "file", // The name that will be used to transfer the file
    maxFilesize: 1, // MB
    acceptedFiles: "text/plain",
    accept: function(file, done) {
      if (file.name == "justinbieber.jpg") {
        done("Naha, you don't.");
      }
      else { done(); }
    }
  }



}
