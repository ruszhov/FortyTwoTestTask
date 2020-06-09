
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

$('#id_username, #id_password').addClass('form-controll');
$('.spinner-border').hide();

$(document).ready(function() {
    var options = {
        // target:        '#output2',   // target element(s) to be updated with server response
        beforeSubmit: showRequest, // pre-submit callback
        success: showResponse, // post-submit callback

        // other available options:
        url: '/ajax_submit/', // override for form's 'action' attribute
        type: 'post', // 'get' or 'post', override for form's 'method' attribute
        dataType: 'json', // 'xml', 'script', or 'json' (expected server response type)
        clearForm: false, // clear all form fields after successful submit
        resetForm: false, // reset the form after successful submit

        // $.ajax options can be used here too, for example:
        timeout: 3000,
    };

    // bind to the form's submit event
    $('#main-form').submit(function() {
        $(this).ajaxSubmit(options);
        return false;
    });
});

// pre-submit callback
function showRequest(formData, jqForm, options) {

    // alert('About to submit: \n\n' + queryString);

    // here we could return false to prevent the form from being submitted;
    // returning anything other than false will allow the form submit to continue

    // alert('request')

    $('.spinner-border').show();
    //!?notice: ":file" selector will brake next filter, as well as more generic ":input"
    $('form#main-form').find(':submit, :text, :checkbox, input, textarea').prop('disabled', true);

    return true;
}


// post-submit callback
function showResponse(responseText, statusText, xhr, $form) {
    function insertAfter(referenceNode, newNode) {
        referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
    }

    if (responseText.success) {
        // alert('New data has been saved')
        window.location.href = '/';
    } else {
        for (let [key, value] of Object.entries(responseText.error)) {
            const error_field = `id_${key}`;
            const errField = document.getElementById(error_field).classList.add("is-invalid");
            const el = document.createElement("div");
            el.classList.add("invalid-feedback");
            el.innerHTML = `${value}`;
            const div = document.getElementById(error_field);
            // const  = $(div).closest('div').find('div.invalid-feedback');
            if($(div).closest('div').find('div.invalid-feedback').length == 0) {
                insertAfter(div, el);
            }
        }
        $('.spinner-border').hide();
        $('form#main-form').find(':submit, :text, :checkbox, input, textarea').prop('disabled', false);
    }
}

//JS photo preview
$('#id_photo').change(function() {
    upload_img(this);
    // console.log('changed')
});

function upload_img(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {

            $('#img_id').attr('src', e.target.result);
            $('#img_id').attr('width', 200);
            $('#img_id').attr('height', 200);
        }
        reader.readAsDataURL(input.files[0]);
    }
}