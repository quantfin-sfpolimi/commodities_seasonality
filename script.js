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
  let names = []

  /*
  for (obj in data_single_year) {
  	var data = [];
    data_single_year[obj].forEach(function(el) {
    	data.push(eval(el));
    });
    chart_series.push({
    	name: obj,
    	data: data
    });
    names.append(str(obj))
  }
  */

  for (obj in data_single_year) {
    chart_series.push({
    	name: obj,
    	data: data_single_year[obj]
    });
  }





    /**
     * Create the chart when all data is loaded
     * @return {undefined}
     */
    function createChart(series) {

        Highcharts.stockChart('container-chart2', {

            rangeSelector: {
                selected: 4
            },

            yAxis: {
                labels: {
                    format: '{#if (gt value 0)}+{/if}{value}%'
                },
                plotLines: [{
                    value: 0,
                    width: 2,
                    color: 'silver'
                }]
            },

            plotOptions: {
                series: {
                    compare: 'percent',
                    showInNavigator: true
                }
            },

            tooltip: {
                pointFormat: '<span style="color:{series.color}">' +
                    '{series.name}</span>: <b>{point.y}</b> ' +
                    '({point.change}%)<br/>',
                valueDecimals: 2,
                split: true
            },

            series
        });

    }

    createChart(chart_series);

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