var margin = { top: 100, right: 10, bottom: 10, left: 10 },
    outerWidth = 1050,
    outerHeight = 600,
    width = outerWidth - margin.left - margin.right,
    height = outerHeight - margin.top - margin.bottom;

var x = d3.scale.linear()
    .range([0, width]).nice();

var y = d3.scale.linear()
    .range([height, 0]).nice();


var xCat = "local_avg",
    yCat = "global_docs",
    rCat = "global_tf_idf",
    colorCat = "global_cluster";


var svgContainer = d3.select("body").append("svg").attr("width", outerWidth).attr("height", outerHeight);
 9
10var circles = svgContainer.selectAll("circle")
11                          .data(jsonCircles)
12                          .enter()
13                          .append("circle");
14
15var circleAttributes = circles
16                       .attr("cx", function (d) { return d.x_axis; })
17                       .attr("cy", function (d) { return d.y_axis; })
18                       .attr("r", function (d) { return d.radius; })
19                       .style("fill", function(d) { return d.color; });