$(document).ready(function() {

    $('#id_date_of_birth').datepicker({
        uiLibrary: 'bootstrap4',
        iconsLibrary: 'fontawesome',
        locale: 'en-en',
        format: 'yyyy-mm-dd',
    });

    $('#id_username, #id_password').addClass('form-controll');
    $('.spinner-border').hide();

    let options = {
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
            window.location.href = '/';
        } else {
            if($('div.invalid-feedback').length > 0){
                $('div.invalid-feedback').remove();
                $('input.is-invalid').removeClass("is-invalid");
            }
            for (let [key, value] of Object.entries(responseText.error)) {
                const error_field = `id_${key}`;
                const errField = document.getElementById(error_field).classList.add("is-invalid");
                const el = document.createElement("div");
                el.classList.add("invalid-feedback");
                el.innerHTML = `${value}`;
                const div = document.getElementById(error_field);
                // const  = $(div).closest('div').find('div.invalid-feedback');
                if ($(div).closest('div').find('div.invalid-feedback').length == 0) {
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
});