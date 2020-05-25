jQuery(function($) {
    $(document).ready(function() {
	const interval = 3000;
	const ajax_call = function() {
	  $.ajax({
		type: "GET",
		url: "/http_requests/",
		contentType: "application/json",
		dataType: "text",
		cache: false,
		success: function(data){
			const total = JSON.parse(data)["total"];
			const tableValue = parseInt($(".http-requests td:first").text());
			const newEntries = total - tableValue
			$('#new-entries').html(newEntries)
			if (window.location.pathname == '/http_requests/'){
				document.title = `(${newEntries}) - 42 CC Ticket#3`;
			};
		}
	  })
	};
	setInterval(ajax_call, interval);
});
});




