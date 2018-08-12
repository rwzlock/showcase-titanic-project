var plots_url = "/plot";

Plotly.d3.json(plots_url, function(error, response) {
    if (error) return console.warn(error);
    var data = [response];
    console.log(response)
    var layout = { margin: { t: 30, b:50 },
                   title: "Results by Gender",
                   xaxis: { title: "Gender"},
                   yaxis: { title: "Number of Survival"}            
    }
    Plotly.plot("bar1", data, layout)
})