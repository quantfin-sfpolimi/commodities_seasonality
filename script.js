let inputForm = document.getElementById('inputForm')

inputForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let start = document.getElementById("startYear").value
  let end = document.getElementById("endYear").value
      
  let input = {
    "start": parseInt(start),
    "end": parseInt(end),
  }

  console.log(input)

  url = 'http://127.0.0.1:8000/' + 'get-seasonality/' + start + end
  console.log(url)
  //window.location.href = url

  data = fetch(url).then(res => res.json())
  console.log("Tipo: " + typeof(data))
  console.log("Data: " + data)



  // Create the chart
  Highcharts.stockChart('container-chart', {
    rangeSelector: {
        selected: 1
    },

    title: {
        text: 'Seasonality'
    },

    series: [{
        name: 'Seasonality',
        data: data,
        tooltip: {
            valueDecimals: 3
        }
    }]
  });

})