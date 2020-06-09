const interval = 3000;
const ajax_call = function() {
    $.ajax({
        type: "GET",
        url: "/ajax_request/",
        contentType: "application/json",
        dataType: "text",
        cache: false,
        success: function(data) {
            const total = JSON.parse(data)["total"];
            if (total != 0) {
                let [, ...second] = document.title.split(" - ");
                document.title = `(${total}) - ${second.join(' - ')}`;
                $('span#new-entries').html(total);
            }
        }
    })
};

setInterval(ajax_call, interval);