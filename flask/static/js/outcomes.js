// script.js
function outcomesChart() {
    console.log('outcomes chart') //debugging

    // Make an API request to "/select_by_outcomes_by_year" and get the data
    fetch(`/select_by_outcomes_by_year?year=${selectedYear}`)  
        .then(response => response.json())
        .then(data => {
            console.log('outcomer chart', data)
            // Extract data for Highcharts series
            var seriesData = data.map(item => ({
                name: item[1],
                y: item[0]
            }));
            var femaleCounts = data.map(item => item[1]);
            // Create the Highcharts chart
            Highcharts.chart('outcomesChart', {
                chart: {
                    type: 'column'
                },

                title: {
                    text: 'Outcomes of Food Reactions (Top 5)'
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
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0,
                        colorByPoint: true,
                    },
                },
                colors: ['#FCE700', '#F8C4B4', '#f6e1ea', '#B8E8FC', '#BCE29E'],
                series: [{
                    name: 'Count',
                    data: seriesData
                }]
            });
        })
        .catch(error => console.error('Error fetching data:', error));
};

