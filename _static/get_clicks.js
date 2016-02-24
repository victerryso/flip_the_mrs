// Function to send a click to the destination for data collection
function send_click(l) {
    data = {};
    data['url'] = l;
    dynsite_send_data(given_uid, "clicked-link", data);
    console.log("You're trying to go to " + href);

}

// Detect left click
$(document).on("click", "a", function() {
    send_click($(this).attr("href"));
    return false;
});

// Detect right click
$(document).on("contextmenu", "a", function(e){
    send_click($(this).attr("href"));
    return false;
});
