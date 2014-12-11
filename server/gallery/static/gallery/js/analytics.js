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
    buildTrendChart("#day_trend_chart", window.trendTimes.day, window.exhibitImages);   
    buildTrendChart("#week_trend_chart", window.trendTimes.week, window.exhibitImages);   
    buildTrendChart("#all_time_trend_chart", window.trendTimes.all_time, window.exhibitImages);   

    toTabRef("#vantage_tab");
    buildHeatmap("#viewpoint_chart", window.detectionWidths, window.exhibitImages);

    /* Return to original tab */
    toTabRef("#summary_tab");
});
