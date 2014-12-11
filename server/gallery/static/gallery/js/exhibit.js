$(function(){
    buildLineChart("#exhibit_line_chart", window.timeByDay);
    buildHeatmap("#exhibit_vantage_chart", window.detectionWidths, window.exhibitImages);
});
