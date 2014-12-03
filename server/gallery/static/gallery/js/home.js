$(function(){

    /* Top bar chart */
    var dataset = [];
    for (var i=0; i < 50; i++){
        var newNumber = Math.round(Math.random() * 30);
        dataset.push(newNumber);
    }
    var barSvg0 = d3.select(".barContainer")
        .append("svg")
        .style("width", "100%")
        .selectAll("rect")
        .data(dataset)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .style("fill", "pink")
        .attr("width", 20)
        .attr("height", function(d) {
            return d * 6 + "px";
        })
        .attr("x",function(d,i){ 
            return (20 + 1) * i;
         })
        .attr("y",0);

    var w = "100%";
    var h = 400;
    var r = h/2;
    var color = d3.scale.category20c();

    var data = [{"label":"Olympia", "value":30}, 
                  {"label":"Nana", "value":20}, 
                  {"label":"La Grande Jatte", "value":50}];

    /* Pie chart */
    var vis = d3.select('#chart')
        .append("svg:svg")
        .data([data])
        .attr("width", w)
        .attr("height", h)
        .append("svg:g")
        .attr("transform", "translate(" + r + "," + r + ")");
    var pie = d3.layout.pie().value(function(d){return d.value;});

    // declare an arc generator function
    var arc = d3.svg.arc().outerRadius(r);

    // select paths, use arc generator to draw
    var arcs = vis.selectAll("g.slice").data(pie).enter().append("svg:g").attr("class", "slice");
    arcs.append("svg:path")
        .attr("fill", function(d, i){
            return color(i);
        })
        .attr("d", function (d) {
            // log the result of the arc generator to show how cool it is :)
            return arc(d);
        });

    // add the text
    arcs.append("svg:text")
        .attr("transform", function(d){
            d.innerRadius = 0;
            d.outerRadius = r;
            return "translate(" + arc.centroid(d) + ")";
         })
        .attr("text-anchor", "middle")
        .text( function(d, i) {return data[i].label;} );

    /*  Chord chart */
    var diameter = 960,
        radius = diameter / 2,
        innerRadius = radius - 120;

    var cluster = d3.layout.cluster()
        .size([360, innerRadius])
        .sort(null)
        .value(function(d) { return d.size; });

    var bundle = d3.layout.bundle();

    var line = d3.svg.line.radial()
        .interpolate("bundle")
        .tension(.85)
        .radius(function(d) { return d.y; })
        .angle(function(d) { return d.x / 180 * Math.PI; });

    var svg = d3.select("body").append("svg")
        .attr("width", diameter)
        .attr("height", diameter)
      .append("g")
        .attr("transform", "translate(" + radius + "," + radius + ")");

    d3.json("static/gallery/data/readme-flare-imports.json", function(error, classes) {
      var nodes = cluster.nodes(packageHierarchy(classes)),
          links = packageImports(nodes);

        svg.selectAll(".link")
            .data(bundle(links))
          .enter().append("path")
            .attr("class", "link")
            .attr("d", line);

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
    });

    d3.select(self.frameElement).style("height", diameter + "px");

    // Lazily construct the package hierarchy from class names.
    function packageHierarchy(classes) {
      var map = {};

      function find(name, data) {
        var node = map[name], i;
        if (!node) {
          node = map[name] = data || {name: name, children: []};
          if (name.length) {
            node.parent = find(name.substring(0, i = name.lastIndexOf(".")));
            node.parent.children.push(node);
            node.key = name.substring(i + 1);
          }
        }
        return node;
      }

      classes.forEach(function(d) {
        find(d.name, d);
      });

      return map[""];
    }

    // Return a list of imports for the given array of nodes.
    function packageImports(nodes) {
      var map = {},
          imports = [];

      // Compute a map from name to node.
      nodes.forEach(function(d) {
        map[d.name] = d;
      });

      // For each import, construct a link from the source to target node.
      nodes.forEach(function(d) {
        if (d.imports) d.imports.forEach(function(i) {
          imports.push({source: map[d.name], target: map[i]});
        });
      });

      return imports;
    }


    /* Bottom bar chart */
    var dataset = [];
    for (var i=0; i < 50; i++){
        var newNumber = Math.round(Math.random() * 30);
        dataset.push(newNumber);
    }
    var barSvg1 = d3.select(".barContainer2").append("svg");
    barSvg1.selectAll("rect") 
    .data(dataset)
    .enter()
    .append("rect")
    .attr("class", "bar")
    .style("fill", "green")
    .attr("width", 15)
    .attr("height", function(d) {
        return d * 6 + "px";
    })
    .attr("x",function(d,i){return 6*i;})
    .attr("y",0);
});
