const interval = 3000;
const ajax_call = function() {
  $.ajax({
	type: "GET",
	url: "/ajax_request/",
	contentType: "application/json",
	dataType: "text",
	cache: false,
	success: function(data){
		const total = JSON.parse(data)["total"];
		const tableValue = parseInt($("table#http-requests td:first").text());
		const newEntries = total - tableValue;
		$('#new-entries').html(newEntries);
		if(newEntries != 0){
		    if (window.location.pathname == '/http_requests/'){
		    document.title = `(${newEntries}) - 42 CC Ticket#3`;
        }
      }
	}
  })
};
setInterval(ajax_call, interval);