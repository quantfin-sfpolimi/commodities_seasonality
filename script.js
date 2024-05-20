async function display_seasonality_chart(url) {

  const data_seasonality = await fetch(url).then(response => response.json());

  // Create the chart
  Highcharts.stockChart('container-chart1', {
    rangeSelector: {
        selected: 1
    },

    title: {
        text: 'Seasonality'
    },

    series: [{
        name: 'Seasonality',
        data: data_seasonality,
        tooltip: {
            valueDecimals: 3
        }
    }]
  });
}

async function display_single_years(url) {

  const data_single_year = await fetch(url+"/history").then(response => response.json());
  console.log(data_single_year)

  let chart_series = []

  for (obj in data_single_year) {
    chart_series.push({
    	name: obj,
    	data: data_single_year[obj]
    });
  }

  Highcharts.stockChart('container-chart2', {
    rangeSelector: {
        selected: 1
    },

    title: {
        text: 'Seasonality'
    },

    series: chart_series
    
  });

  



   
};

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

  display_seasonality_chart(url)
  display_single_years(url)
})