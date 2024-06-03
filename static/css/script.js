async function display_seasonality_chart(default_url, query_parameters) {
    /**
     * Fetches seasonality data from the provided URL and displays it in a Highcharts chart.
     *
     * @param {string} url - The URL to fetch the seasonality data from.
     * @returns {Promise<void>} - A promise that resolves when the chart has been successfully created and rendered.
     *
     * The function performs the following steps:
     * 1. Fetches JSON data from the specified URL.
     * 2. Uses Highcharts to create a stock chart with the fetched data.
     * 3. Displays the chart in an HTML container with the ID 'container-chart1'.
     */

    url = default_url + query_parameters;
    const data_seasonality = await fetch(url).then((response) =>
        response.json()
    );

    // Create the chart
    Highcharts.stockChart("container-chart1", {
        xAxis: {
            type: "datetime",
            dateTimeLabelFormats: {
                month: "%b",
            },
        },
        scrollbar: {
            enabled: true,
            barBackgroundColor: "gray",
            barBorderRadius: 7,
            barBorderWidth: 0,
            buttonBackgroundColor: "gray",
            buttonBorderWidth: 0,
            buttonBorderRadius: 7,
            trackBackgroundColor: "none",
            trackBorderWidth: 1,
            trackBorderRadius: 8,
            trackBorderColor: "#CCC",
            dateTimeLabelFormats: {
                month: "%b",
            },
        },

        title: {
            text: "Seasonality",
        },

        series: [
            {
                name: "Seasonality",
                data: data_seasonality,
                tooltip: {
                    valueDecimals: 3,
                },
            },
        ],
    });
}

async function display_single_years(default_url, query_parameters) {
    url = default_url + "/history" + query_parameters;
    const data_single_year = await fetch(url).then((response) =>
        response.json()
    );
    dict = JSON.parse(data_single_year);

    let chart_series = [];

    for (obj in dict) {
        array_list = [];
        sub_dict = dict[obj];

        keys = Object.keys(sub_dict);
        for (key in keys) {
            array_list.push(sub_dict[key]);
        }

        chart_series.push({
            name: obj,
            data: array_list,
        });
    }

    /**
     * Create the chart when all data is loaded
     * @return {undefined}
     */
    function createChart(series) {
        Highcharts.stockChart("container-chart2", {
            rangeSelector: {
                selected: 4,
            },
            yAxis: {
                labels: {
                    format: "{#if (gt value 0)}+{/if}{value}%",
                },
                plotLines: [
                    {
                        value: 0,
                        width: 2,
                        color: "silver",
                    },
                ],
            },
            plotOptions: {
                series: {
                    compare: "percent",
                    showInNavigator: true,
                },
            },
            xAxis: {
                type: "datetime",
                dateTimeLabelFormats: {
                    month: "%b",
                },
            },
            tooltip: {
                pointFormat:
                    '<span style="color:{series.color}">' +
                    "{series.name}</span>: <b>{point.y}</b> " +
                    "({point.change}%)<br/>",
                valueDecimals: 2,
                split: true,
            },
            series,
        });
    }
    createChart(chart_series);
}

async function display_monthly_returns(default_url, query_parameters) {
    url = default_url + "/monthly" + query_parameters;
    const data_monthly = await fetch(url).then((response) => response.json());

    // Create the chart
    Highcharts.stockChart("container-chart3", {
        rangeSelector: {
            selected: 1,
        },
        xAxis: {
            type: "datetime",
            dateTimeLabelFormats: {
                month: "%b",
            },
        },

        title: {
            text: "Monthly Average Returns",
        },

        series: [
            {
                name: "Monthly Average Returns",
                data: data_monthly,
                type: "histogram",
                tooltip: {
                    valueDecimals: 3,
                },
            },
        ],
    });
}

async function display_monthly_stdev(default_url, query_parameters) {
    url = default_url + "/stdev" + query_parameters;
    const data_monthly_stdev = await fetch(url).then((response) =>
        response.json()
    );

    // Create the chart
    Highcharts.stockChart("container-chart4", {
        rangeSelector: {
            selected: 1,
        },
        title: {
            text: "Monthly Standard Deviation of Seasonality",
        },
        xAxis: {
            type: "datetime",
            dateTimeLabelFormats: {
                month: "%b",
            },
        },
        series: [
            {
                name: "Monthly Average Returns",
                data: data_monthly_stdev,
                type: "histogram",
                tooltip: {
                    valueDecimals: 3,
                },
            },
        ],
    });
}

let inputForm = document.getElementById("inputForm");

// The following code is executed when "Submit" button is clicked by the user.
window.onload = function load_graphs() {
    path_parameters = "get-seasonality/" + ticker;
    default_url = "http://127.0.0.1:8000/" + path_parameters;
    query_parameters =
        "?start=" + start_year.toString() + "&end=" + end_year.toString();

    display_seasonality_chart(default_url, query_parameters);
    display_single_years(default_url, query_parameters);
    display_monthly_returns(default_url, query_parameters);
    display_monthly_stdev(default_url, query_parameters);
};
