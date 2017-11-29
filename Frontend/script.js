
var rap = [0];
var rock = [0];
var jazz = [0];
var classical = [0];
var punk = [0];
var time = [0];
let now = [.2,.2,.2,.2,.2];
let sum = [.2,.2,.2,.2,.2];

var canvas1 = document.getElementById("chart1");
var canvas2 = document.getElementById("chart2");
var canvas3 = document.getElementById("chart3");
    ctx1 = canvas1.getContext('2d'),
    ctx2 = canvas2.getContext('2d'),
    ctx3 = canvas3.getContext('2d'),
    data1 = {
      labels: ["Rap", "Rock", "Jazz", "Classical", "Punk"],
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
          borderColor: "#ffa500",
          fill: false
        },
        {
          data: jazz,
          label: "Jazz",
          borderColor: "#800080",
          fill: false
        },
        {
          data: classical,
          label: "Classical",
          borderColor: "#0000ff",
          fill: false
        },
        {
          data: punk,
          label: "Punk",
          borderColor: "#800000",
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
}, 1000);

// Reduce the animation steps for demo clarity.
var chart1 = new Chart(ctx1, {
  type : 'bar',
  data : data1,
  animationSteps: 60
  }
)

var chart2 = new Chart(ctx2, {
  type : 'line',
  data : data2,
  animationSteps: 60
  }
)

var chart3 = new Chart(ctx3, {
    type: 'pie',
    data : data3,
    animationSteps: 60,
    options: {
      title: {
        display: true,
        text: 'Current Probability'
      }
    }
});

function generateSumTo1Array(){
  tot = 0
  toRet = Array.from({length: 5}, () => (Math.random()));

  console.log(toRet);
  for(i = 0; i < toRet.length; i ++){
    tot = tot + toRet[i]
  }
  for(i = 0; i < toRet.length; i ++){
    toRet[i] = toRet[i]/tot
  }
  console.log(toRet);


  return toRet

}
