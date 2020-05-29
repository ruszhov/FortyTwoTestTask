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
		console.log(total)
		if(total != 0){
			if (window.location.pathname != '/http_requests/'){
		    document.title = `(${total}) - 42 CC Ticket#3`;
        	}
			else{
			document.title = `42 CC Ticket#3`;
			}
		}
		else{
			document.title = `42 CC Ticket#3`;
		}
	 }
  })
};
setInterval(ajax_call, interval);