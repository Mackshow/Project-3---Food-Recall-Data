
function brands_chart() {
  const selectedBrandValue = selectBrandElement.value;
  // Make an AJAX request to fetch data from the API endpoint
  fetch(`/select_brands_by_year?year=${selectedYear}&limit=${selectedBrandValue}`)  // Change the year as needed
    .then(response => response.json())
    .then(data => {
      console.log('brands_chart', data)
      // Extracting data for plotting
      var pieData = data.map(entry => ({
        name: entry.slice(1, 3).join(' - '), // Sector name: Industry - Brand
        y: entry[0] // Value: Count
      }));

      // Create Highcharts pie chart
      Highcharts.chart('topBrandsChart', {
        chart: {
          type: 'pie'
        },
        title: {
          text: 'Top '+selectedBrandValue+' Food Brands'
        },
        series: [{
          name: 'Count',
          data: pieData,
          colorByPoint: true
        }],
        colors: ['#FCE700', '#F8C4B4', '#f6e1ea', '#B8E8FC', '#BCE29E']
      });
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    })

};
