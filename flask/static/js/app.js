var selectedYear = '';

const selectBrandElement = document.getElementById('topBrandsChartSelector'); //get dropdown menu for brands chart from html page
console.log("selectBrandElement:", selectBrandElement)
// Populate brand menu with options starting from count 5
for (var i = 5; i <= 24; i++) {
    var option = document.createElement('option');
    option.value = i;
    option.text = i;
    selectBrandElement.appendChild(option);
}

function handleBrandSelection() {
    console.log("handleBrandSelection >> called") //debugging
    brands_chart()
}

//--------------------------------------------------------------

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Your input handler, wrapped in the debounce function
const debouncedInputHandler = debounce(function (event) {
    console.log(event.target.value);
    update(event.target.value)
}, 500); // 500 ms wait time

// Event listener

//----------------------------------------------------------
//----------------------------------------------------------
var container_ages_by_year_chart;
const startAge = 1,  //assign start age for bar range selector
    endAge = 80,    //assign end age
    input = document.getElementById('play-range'),  //get bar selector element from html page
    nbr = 6;

input.addEventListener('input', debouncedInputHandler);

function update(xval) {
    console.log('xval', xval, input.value);
    increment = input.value
    get_container_ages_by_year_chart_data(input.value)
}

//----------------------------------------------------------- 
//----------------------------------------------------------- 
//-----------------------------------------------------------  


function get_container_ages_by_year_chart_data(age) {
    // fetch data from endpoint
    fetch(`/select_ages_by_year?year=${selectedYear}&age=${age}`)
        .then(response => response.json())
        .then(data => {
            console.log(`/select_ages_by_year?year=${selectedYear}&age=${age}`, data); //debugging
            //Extracting industry names and reaction count
            var categories = data.map(item => item[1]);
            var counts = data.map(item => item[0]);
            console.log('>>> categories',categories, 'counts',counts)  //debugging

            console.log('container_ages_by_year_chart.series[0]', container_ages_by_year_chart.series[0]) //debugging
            container_ages_by_year_chart.series[0].setData(counts, true); 
            container_ages_by_year_chart.xAxis[0].update({categories: categories}, true); 
            container_ages_by_year_chart.setTitle({ text: 'Reactions per Industry for Age:'+age });
            container_ages_by_year_chart.redraw();

        })
        .catch(error => {
            console.error('Error fetching years:', error)

        });
}
// Reactions per industry and age chart
function reactionsPerIndustryChart() {
    // fetch data from endpoint
    fetch(`/select_ages_by_year?year=${selectedYear}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            var categories = data.map(item => item[1]);
            var counts = data.map(item => item[0]);

            container_ages_by_year_chart = Highcharts.chart('container_ages_by_year', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Reactions per Industry'
                },
                xAxis: {
                    categories: categories,
                    crosshair: true
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Count of Reactions per Industry'
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                        '<td style="padding:0"><b>{point.y:.1f} counts</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0,
                        colorByPoint: true,
                    }
                },
                colors: ['#FCE700', '#F8C4B4', '#f6e1ea', '#B8E8FC', '#BCE29E'],
                series: [{
                    name: 'Industries',
                    data: counts
                }]

            });

        })
        .catch(error => console.error('Error fetching years:', error));
}

function refresh_charts() {
    selectedYear = document.getElementById('yearDropdown').value;
    console.log("--selectedYear -->", selectedYear);
    //updateChart();
    reactionsPerIndustryChart()
    createDiarrheaGenderChart()
    outcomesChart()
    brands_chart();

}
//----------------------------------------------------------------------

// Fetch data from the select_years endpoint to populate the dropdown
function load_years() {
    fetch('/select_years')
        .then(response => response.json())
        .then(data => {
            var yearDropdown = document.getElementById('yearDropdown');

            // Populate the dropdown with options
            data.forEach(year => {
                let option = document.createElement('option');
                option.value = year;
                option.text = year;
                yearDropdown.appendChild(option);
            });

            // Add event listener to the dropdown to update the chart
            yearDropdown.addEventListener('change', refresh_charts());

        })
        .catch(error => console.error('Error fetching years:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("Document is ready!");
    load_years();
});
