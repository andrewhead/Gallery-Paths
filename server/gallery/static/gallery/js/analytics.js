$(function(){

    function toTabRef(ref) {
        var index = $('#tabs a[href="' + ref + '"]').parent().index();
        $("#tabs").tabs("option", "active", index);
    }

    $("#tabs").tabs();

    /* Change to tab before building SVGs to get proper chart dimensions. */
    toTabRef("#summary_tab");
    buildLineChart("#traffic_chart", window.timeByDay);

    toTabRef("#trend_tab");
    var dayTrendTime = [
        {'exhibit_id': 7, 'totalTime': 1100},
        {'exhibit_id': 4, 'totalTime': 900},
        {'exhibit_id': 6, 'totalTime': 400},
        {'exhibit_id': 5, 'totalTime': 300},
        {'exhibit_id': 8, 'totalTime': 200},
        {'exhibit_id': 9, 'totalTime': 100},
    ];
    console.log(window.trendTimes.week);
    buildTrendChart("#day_trend_chart", dayTrendTime, window.exhibitImages);   
    buildTrendChart("#week_trend_chart", window.trendTimes.week, window.exhibitImages);   
    buildTrendChart("#all_time_trend_chart", window.trendTimes.all_time, window.exhibitImages);   

    toTabRef("#vantage_tab");
    buildHeatmap("#viewpoint_chart", window.detectionWidths, window.exhibitImages);

    /* Return to original tab */
    toTabRef("#summary_tab");
});
