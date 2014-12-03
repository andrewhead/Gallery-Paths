$(function(){

    function px_to_num(str) {
        return Number(str.replace("px", ""));
    };

    var margin = {top: 10, bottom: 10, right: 10, left: 60};
    var chart = d3.select("#dwell_chart");
    var w = px_to_num(chart.style("width"));
    var h = px_to_num(chart.style("height"));

    var w_scale = d3.scale.linear()
        .domain([0, d3.max(d3.values(dwellTimeData))])
        .range([margin.left, w - margin.right]);
    var y_scale = d3.scale.ordinal()
        .domain(d3.keys(dwellTimeData))
        .rangeRoundBands([0, h - margin.bottom], .1);
    var color_scale = d3.scale.linear()
        .domain([0, d3.max(d3.values(dwellTimeData))])
        .range(["#000000", "#008800"]);

    var svg = chart.append("svg")
        .style("width", w)
        .style("height", h);

    var bars = svg.selectAll("g") 
        .data(d3.entries(dwellTimeData))
        .enter()
        .append("g")
        .attr("transform", function(d) { return "translate(" + margin.left + "," + y_scale(d.key) + ")" ; });

    var rects = bars
        .append("rect")
        .attr("class", "time_bar")
        .style("fill", function(d) { return color_scale(d.value); })
        .attr("x", margin.left)
        .attr("width", function(d) { return w_scale(d.value); })
        .attr("height", y_scale.rangeBand());

    var labels = bars
        .append("text")
        .attr("text-anchor", "end")
        .style("font-size", 14)
        .text(function(d) { return "Painting " + d.key; })
        .attr("transform", "translate(" + (margin.left - 20) + "," + y_scale.rangeBand() / 1 + ")");

    /*  Chord chart */
    /* Nest data by user and trip index. */
    var paths = d3.nest()
        .key(function(d) { return d.user; })
        .key(function(d) { return d.tripIndex; })
        .entries(window.sightings);
    
    /* Get nodes as list of all locations recorded. */
    var parentNode = {
        name: "",
        children: []
    };
    var nodeMap = {"": parentNode};
    var nodes = [parentNode];
    for (var i = 0; i < window.sightings.length; i++) {
        var loc = window.sightings[i].location;
        if (!nodeMap.hasOwnProperty(loc)) {
            var name = "Painting" + loc;
            var node = {
              name: name,
              parent: "",
              children: [],
              key: name
            };
            parentNode.children.push(node);
            nodeMap[loc] = node;
        }
    }

    /* Create links from each step in a user trip. */
    var links = [];
    for (var i = 0; i < paths.length; i++) {
        var userPaths = paths[i].values;
        for (var j = 0; j < userPaths.length; j++) {
            var userTripPaths = userPaths[j].values;
            userTripPaths.sort(function(a, b) {
                return a.time - b.time;
            });
            for (var k = 0; k < userTripPaths.length - 1; k++) {
                links.push({
                    source: nodeMap[userTripPaths[k].location], 
                    target: nodeMap[userTripPaths[k + 1].location],
                    startDate: userTripPaths[k].time,
                    endDate: userTripPaths[k + 1].time,
                    user: i,
                    trip: j
                });
            }
        }
    }

    var diameter = 720,
        radius = diameter / 2,
        innerRadius = radius - 120;

    var cluster = d3.layout.cluster()
        .size([360, innerRadius])
        .sort(null)
        .value(function(d) { return d.size; });

    var bundle = d3.layout.bundle();

    var tension_scale = d3.scale.linear()
        .domain([0, links.length])
        .range([0, 1]);

    var line = d3.svg.line.radial()
        .interpolate("bundle")
        .radius(function(d) { return d.y; })
        .angle(function(d) { return d.x / 180 * Math.PI; });

    var svg = d3.select("#bundle_chart").append("svg")
        .attr("width", diameter)
        .attr("height", diameter)
      .append("g")
        .attr("transform", "translate(" + radius + "," + radius + ")");

    var nodes = cluster.nodes(parentNode)

      svg.selectAll(".link")
          .data(bundle(links))
        .enter().append("path")
          .attr("class", "link")
          .attr("d", function(d, i) { return line.tension(tension_scale(i))(d); });

      svg.selectAll(".node")
          .data(nodes.filter(function(n) { return !n.children; }))
        .enter().append("g")
          .attr("class", "node")
          .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })
        .append("text")
          .attr("dx", function(d) { return d.x < 180 ? 8 : -8; })
          .attr("dy", ".31em")
          .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
          .attr("transform", function(d) { return d.x < 180 ? null : "rotate(180)"; })
          .text(function(d) { return d.key; });

    d3.select(self.frameElement).style("height", diameter + "px");
});
