$(function(){

    $("#tabs").tabs();

    function px_to_num(str) { return Number(str.replace("px", "")); };
    var parseDate = d3.time.format("%Y-%m-%d").parse;
 
    /* Recent Traffic Chart */
    var data = window.timeByDay;
    data.forEach(function(d) {
        d.date = parseDate(d.date);
    });

    var chartDiv = d3.select("#traffic_chart");
    var divW = px_to_num(chartDiv.style("width"));
    var divH = px_to_num(chartDiv.style("height"));

    var margin = {top: 10, bottom: 30, right: 10, left: 60};
    var w = divW - margin.right - margin.left;
    var h = divH - margin.top - margin.bottom;

    var x = d3.time.scale()
        .domain(d3.extent(data, function(d) { return d.date; }))
        .range([0, w]);

    var y = d3.scale.linear()
        .domain(d3.extent(data, function(d) { return d.sighting_count; }))
        .range([h, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var line = d3.svg.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.sighting_count); });

    var svg = chartDiv.append("svg")
        .attr("width", divW)
        .attr("height", divH)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + h + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Events");

    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);


    function buildTrendChart(divSelector, data) {

        var margin = {top: 10, bottom: 10, right: 10, left: 40};
        var chartDiv = d3.select(divSelector);
        var divW = px_to_num(chartDiv.style("width"));
        var divH = px_to_num(chartDiv.style("height"));

        if (data.length === 0) {
            chartDiv.append("svg")
                .style("width", divW)
                .style("height", divH)
              .append("text")
                .attr("text-anchor", "middle")
                .text("No data")
                .attr("class", "chart_label")
                .attr("x", divW / 2)
                .attr("y", divH / 2);
            return;
        }

        var w = divW - margin.right - margin.left;
        var h = divH - margin.top - margin.bottom;

        var wScale = d3.scale.linear()
            .domain([0, d3.max(data, function(d) { return d.totalTime; })])
            .range([0, w]);
        var yScale = d3.scale.ordinal()
            .domain(data.map(function(d) { return d.location_id; }))
            .rangeRoundBands([0, h], .1);
        var colorScale = d3.scale.linear()
            .domain([0, d3.max(data, function(d) { return d.totalTime; })])
            .range(["#000000", "#008800"]);

        var svg = chartDiv.append("svg")
            .style("width", divW)
            .style("height", divH)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var bars = svg.selectAll("g") 
            .data(data)
            .enter()
            .append("g")
            .attr("transform", function(d) { return "translate(0," + yScale(d.location_id) + ")" ; });

        var rects = bars
            .append("rect")
            .attr("class", "time_bar")
            .style("fill", function(d) { return colorScale(d.totalTime); })
            .attr("x", margin.left)
            .attr("width", function(d) { return wScale(d.totalTime); })
            .attr("height", yScale.rangeBand());

        var thumbnails = bars
            .append("image")
            .attr("xlink:href", function(d) { return window.exhibitImages[d.location_id]; })
            .attr("width", 20)
            .attr("height", yScale.rangeBand());
    }

    buildTrendChart("#day_trend_chart", window.trendTimes.day);   
    buildTrendChart("#week_trend_chart", window.trendTimes.week);   
    buildTrendChart("#all_time_trend_chart", window.trendTimes.all_time);   

    /* Heatmap */
    function buildHeatmap(divSelector, data) {

        var data = d3.entries(data).sort(function(a, b) {
            function sum(arr) {
                return arr.reduce(function(a, b) { return a + b; });
            }
            return sum(a.value) - (b.value);
        });
        console.log(data);
        if (data.length === 0) {
            return;
        }

        var margin = {top: 10, bottom: 10, right: 10, left: 30};
        var chartDiv = d3.select(divSelector);
        var divW = px_to_num(chartDiv.style("width"));
        var divH = px_to_num(chartDiv.style("height"));
        var w = divW - margin.right - margin.left;
        var h = divH - margin.top - margin.bottom;
        var legend = {
            w: 480,
            h: 10,
            m: {top: 20, right: 10, bottom: 0}
        }
        var thumbnailWidth = 40;

        var svg = chartDiv.append("svg")
            .style("width", divW)
            .style("height", divH)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var xScale = d3.scale.linear()
            .domain([data[0].value.length + 1, 0])
            .range([thumbnailWidth, w]);
        var xUnitRange = Math.abs(xScale(1) - xScale(0));
        var yScale = d3.scale.ordinal()
            .domain(data.map(function(d) { return d.key; }))
            .rangeRoundBands([legend.h + legend.m.top + legend.m.bottom, h], .15);
        var colorScale = d3.scale.log()
            .base(2)
            .domain([
                Math.max(d3.min(data, function(d) { return d3.min(d.value); }), 1),
                d3.max(data, function(d) { return d3.max(d.value); })
            ])
            .range(["#eeeeee", "#3f6c8d"])
            .clamp(true);

        var maxTime = d3.max(data, function(d) { return d3.max(d.value); });
        var legendTime = 1;
        legendTimes = [];
        while (legendTime <= maxTime) {
            legendTimes.push(legendTime);
            legendTime *= 10;
        }
        var legXScale = d3.scale.ordinal()
            .domain(legendTimes)
            .rangeRoundBands([0, legend.w], 0.01);
        var legend_g = svg.append("g")
            .attr("transform", "translate(" + 
                (divW - margin.right - legend.m.right - legend.w) + "," + 
                legend.m.top + ")");
        
        legend_g.selectAll("rect")
            .data(legendTimes)
            .enter()
            .append("rect")
            .attr("x", function(d) { return legXScale(d); })
            .attr("y", 0)
            .attr("width", legXScale.rangeBand())
            .attr("height", legend.h)
            .attr("fill", function(d) { return colorScale(d); })

        legend_g.selectAll("text")
            .data(legendTimes)
            .enter()
            .append("text")
            .attr("x", function(d) { return legXScale(d) + legXScale.rangeBand() / 2; })
            .attr("y", legend.h + 15)
            .attr("class", "chart_label")
            .attr("text-anchor", "middle")
            .text(function(d) { return d; });

        legend_g.append("text")
            .text("Seconds per work")
            .attr("x", legend.w / 2)
            .attr("y", -10)
            .attr("text-anchor", "middle")
            .attr("class", "chart_label");

        var lines = svg.selectAll("g")
            .data(data)
            .enter()
            .append("g")
            .attr("transform", function(d, i) {
                return "translate(0," + yScale(d.key) + ")";
            });

        lines.selectAll("rect")
            .data(function(d) { return d.value; })
            .enter()
            .append("rect")
            .attr("x", function(d, i) { return xScale(i); })
            .attr("y", 0)
            .attr("width", xUnitRange * .9)
            .attr("height", yScale.rangeBand())
            .attr("fill", function(d) { return colorScale(d); });
         
        var thumbnails = lines
            .append("image")
            .attr("xlink:href", function(d) { return window.exhibitImages[d.key]; })
            .attr("width", thumbnailWidth)
            .attr("height", yScale.rangeBand());
    }

    /* Use the following to switch tabs before inserting graphics. */
    /*
    var index = $('#tabs a[href="#vantage-tab"]').parent().index();
    $("#tabs").tabs("option", "active", index);
    */ 
    buildHeatmap("#viewpoint_chart", window.detectionWidths);
});
