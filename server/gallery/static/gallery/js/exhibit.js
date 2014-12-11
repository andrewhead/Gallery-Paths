$(function(){
    buildLineChart("#exhibit_line_chart", window.timesPerDate);
    buildHeatmap("#exhibit_vantage_chart", window.detectionWidths, window.exhibitImages);
});
