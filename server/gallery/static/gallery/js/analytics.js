$(function(){
    $("#tabs").tabs();
    buildLineChart("#traffic_chart", window.timeByDay);
    buildTrendChart("#day_trend_chart", window.trendTimes.day, window.exhibitImages);   
    buildTrendChart("#week_trend_chart", window.trendTimes.week, window.exhibitImages);   
    buildTrendChart("#all_time_trend_chart", window.trendTimes.all_time, window.exhibitImages);   
    buildHeatmap("#viewpoint_chart", window.detectionWidths, window.exhibitImages);

    /* Use the following to switch tabs before inserting graphics. */ /*
    var index = $('#tabs a[href="#vantage-tab"]').parent().index();
    $("#tabs").tabs("option", "active", index);
    */ 
});
