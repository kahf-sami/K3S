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