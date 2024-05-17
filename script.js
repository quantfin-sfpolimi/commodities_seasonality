async function display_chart(url) {

  const data_seasonality = await fetch(url).then(response => response.json());
  const data_single_year = await fetch(url+"/history").then(response => response.json());

  var chart_series = []

  chart_series.push({
    name: "Seasonality",
    data: data_seasonality
  })

  for (obj in data_single_year) {
  	var data = [];
    data_single_year[obj].forEach(function(el) {
    	data.push(eval(el));
    });
    chart_series.push({
    	name: obj,
    	data: data
    });



  // Create the chart
  Highcharts.stockChart('container-chart', {
    rangeSelector: {
        selected: 1
    },

    title: {
        text: 'Seasonality'
    },

    series: chart_series
  });
}
}

let inputForm = document.getElementById('inputForm')


inputForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let start = document.getElementById("startYear").value
  let end = document.getElementById("endYear").value
  let ticker = document.getElementById("ticker").value
      
  let input = {
    "start": parseInt(start),
    "end": parseInt(end),
  }

  console.log(input)

  url = 'http://127.0.0.1:8000/' + 'get-seasonality/' + ticker + '/' + start + end
  console.log(url)
  //window.location.href = url

  display_chart(url)
})