// Make an AJAX request to fetch data from the API endpoint
fetch('/select_top5_brands_by_year')
  .then(response => response.json())
  .then(data => {
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
        text: 'Top 5 Industry - Brand Combinations'
      },
      series: [{
        name: 'Count',
        data: pieData,
        colorByPoint: true
      }]
    });
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });
