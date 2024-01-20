// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Make an API request to "/select_by_outcomes_by_year" and get the data
    fetch('/select_by_outcomes_by_year?year=2023')  // Change the year as needed
        .then(response => response.json())
        .then(data => {
            // Process the data and create the chart
            createChart(data);
        })
        .catch(error => console.error('Error fetching data:', error));

    function createChart(data) {
        // Extract data for Highcharts series
        var seriesData = data.map(item => ({
            name: item[1],
            y: item[0]
        }));

        // Create the Highcharts chart
        Highcharts.chart('outcomesChart', {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Outcomes from Food Reactions'
            },
            xAxis: {
                type: 'category',
                title: {
                    text: 'Outcome Type'
                }
            },
            yAxis: {
                title: {
                    text: 'Count'
                }
            },
            series: [{
                name: 'Count',
                data: seriesData
            }]
        });
    }
});
