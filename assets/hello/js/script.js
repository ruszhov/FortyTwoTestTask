const interval = 3000;
const ajax_call = function() {
  if(window.location.pathname == '/http_requests/'){
      $.ajax({
        type: "GET",
        url: "/ajax_request/",
        contentType: "application/json",
        dataType: "text",
        cache: false,
        success: function(data){
            const total = JSON.parse(data)["total"];
            if(total != 0){
                document.title = `(${total}) - 42 CC Ticket#5 - Requests`;
                $('span#new-entries').html(total);
            }
         }
      })
  }
};
setInterval(ajax_call, interval);