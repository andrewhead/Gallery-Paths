$(function() {
    console.log("Hello paths!");
    $("#time_range").slider();
    $("#time_range").on("slide", function() {
        console.log("Range changed");
    });
});
