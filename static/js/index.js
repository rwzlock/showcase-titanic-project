var embarked_url = "/embarked";
var gender_url = "/gender";
var plots_url = "/plots";

Plotly.d3.json(embarked_url, function(error, response) {
    if (error) return console.warn(error);
    var data = [response];
    console.log(response)
    var layout = { margin: { t: 30, b:50 },
                   title: "Number of New User by Ports",
                   xaxis: { title: "User Embarked from the Ports "},
                   yaxis: { title: "Number of New User"}            
    }
    Plotly.plot("bar1", data, layout)
})



Plotly.d3.json(gender_url, function(error, response) {
    if (error) return console.warn(error);
    var data = [response];
    console.log(response)
    var layout = { margin: { t: 30, b:50 },
                   title: "Number of New User by Gender",
                   xaxis: { title: "User by Gender "},
                   yaxis: { title: "Number of New User"}            
    }
    Plotly.plot("bar2", data, layout)
})

Plotly.d3.json(plots_url, function(error, response) {
    if (error) return console.warn(error);
    var data = [response];
    console.log(response)
    var layout = { margin: { t: 30, b:50 },
                   title: "Number of Passengers by Gender",
                   xaxis: { title: "Passenger by Gender "},
                   yaxis: { title: "Number of Passenger"}            
    }
    Plotly.plot("bar3", data, layout)
})