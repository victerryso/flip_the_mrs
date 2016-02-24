// Get urls
var currentURL = window.location.href;
var sslURL     = /^https:/;

// Check for match
if (sslURL.test(currentURL)) {

  // Server method to redirect if not logged into AAF
  $.getJSON('/data2u/logged', function(data) {
    if (data.redirect) {
      window.location = data.redirect
    }
  });

} else {

  console.log(currentURL + ': Not in production');

}
