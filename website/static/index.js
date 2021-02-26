function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

/*jshint esversion: 6 */

/**
 * ---------------------------------------
 * This demo was created using amCharts 4.
 *
 * For more information visit:
 * https://www.amcharts.com/
 *
 * Documentation is available at:
 * https://www.amcharts.com/docs/v4/
 * ---------------------------------------
 */

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

//link up the html button to a js const
const btnRefresh = document.getElementById("refresh-button");

//Event listener to spawn a new graph everytime the button is clicked
btnRefresh.addEventListener("click", function (e) {
  spawnGraph();
});

//function to spawn a new graph.
async function spawnGraph() {
  //get ticker value from DOM
  var ticker = document.getElementById("ticker").value;
  console.log(ticker);

  var query =
    "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" +
    ticker +
    "&outputsize=full&apikey=VAVLYDHGHUGUJORQ";
  console.log(query);

  //currently fetches MSFT stock data. TO-DO: make fetch symbol dynamic for user-selected ticker
  // const resp = await fetch("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&outputsize=full&apikey=VAVLYDHGHUGUJORQ");
  const resp = await fetch(query);
  const data = await resp.json();
  //console.log(data);
  // .then((resp) => resp.json())
  // .then(function(data) {
  console.log(data["Time Series (Daily)"]);

  //just grab the time-series data
  series = data["Time Series (Daily)"];
  console.log(series);
  //

  //array to be populated with graph x,y data (x=date, y=adj closing price)
  let data2 = [];

  // loop through json entries, extract relevant key-value data and push to data array
  Object.entries(series).forEach((entry) => {
    const [date, value] = entry;

    console.log(date, value["5. adjusted close"]);
    data2.push({ date: date, value: value["5. adjusted close"] });
  });

  // data.forEach(obj => {
  //     console.log('date:');
  //     console.log(obj.key);
  //     // console.log("closing value:")
  //     // console.log
  // });

  console.log("arrived here!");
  console.log(data2);

  //boilerplate code below to create AMChart4. Just need to specify data source (=data2 array)

  var chart = am4core.create("chartdiv", am4charts.XYChart);

  chart.data = data2;

  // Create axes
  var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
  dateAxis.renderer.grid.template.location = 0;
  dateAxis.renderer.minGridDistance = 50;

  var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

  // Create series
  var series = chart.series.push(new am4charts.LineSeries());
  series.dataFields.valueY = "value";
  series.dataFields.dateX = "date";
  series.strokeWidth = 3;
  series.fillOpacity = 0.5;

  // Add vertical scrollbar
  chart.scrollbarX = new am4core.Scrollbar();
  chart.scrollbarX.marginLeft = 0;

  // Add cursor
  chart.cursor = new am4charts.XYCursor();
  chart.cursor.behavior = "zoomY";
  chart.cursor.lineX.disabled = true;
}
