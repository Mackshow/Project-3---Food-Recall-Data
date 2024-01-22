function createDiarrheaGenderChart() {
    // Fetch data from the /select_count_dia_brand_year endpoint
    fetch(`/select_count_dia_brand_year?year=${selectedYear}`)
        .then(response => response.json())
        .then(data => {
            console.log(`/select_count_dia_brand_year?year=${selectedYear}`,data) //debugging
            // Extracting industry names, male counts, and female counts
            var industryNames = data.map(item => item[2]);
            var maleCounts = data.map(item => item[0]);
            var femaleCounts = data.map(item => item[1]);

            // Create a Highcharts horizontal bar chart
            Highcharts.chart('diarrheaBars', {
                chart: {
                    type: 'column',
                    inverted: true
                },
                colors: [ '#B8E8FC', '#F8C4B4'],
                
                title: {
                    text: 'Diarrhea Reaction by Industry and Gender'
                },
                xAxis: {
                    categories: industryNames,
                    title: {
                        text: 'Industry'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Count'
                    }
                },
                legend: {
                    reversed: true
                },
                plotOptions: {
                    series: {
                        stacking: 'normal'
                    }
                },
                series: [{
                    name: 'Male',
                    data: maleCounts,
                    stack: 'gender'
                }, {
                    name: 'Female',
                    data: femaleCounts,
                    stack: 'gender'
                }]
            });
        })
        .catch(error => console.error('Error fetching data:', error));
};