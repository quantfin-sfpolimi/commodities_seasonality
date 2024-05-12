async function display_chart(url) {

  const data = await fetch(url).then(response => response.json());

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
}

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

  display_chart(url)
})